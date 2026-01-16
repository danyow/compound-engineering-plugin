# 控制器 - DHH Rails 风格

<rest_mapping>
## 一切都映射到 CRUD

自定义操作变成新资源。不要在现有资源上使用动词，而是创建名词资源：

```ruby
# 不要这样做：
POST /cards/:id/close
DELETE /cards/:id/close
POST /cards/:id/archive

# 应该这样做：
POST /cards/:id/closure      # 创建关闭记录
DELETE /cards/:id/closure    # 销毁关闭记录
POST /cards/:id/archival     # 创建归档记录
```

**来自 37signals 的真实示例：**
```ruby
resources :cards do
  resource :closure       # 关闭/重新打开
  resource :goldness      # 标记为重要
  resource :not_now       # 推迟
  resources :assignments  # 管理指派
end
```

每个资源都有自己的控制器，包含标准的 CRUD 操作。
</rest_mapping>

<controller_concerns>
## 用于共享行为的 Concern

控制器广泛使用 concern。常见模式：

**CardScoped** - 加载 @card、@board，提供 render_card_replacement
```ruby
module CardScoped
  extend ActiveSupport::Concern

  included do
    before_action :set_card
  end

  private
    def set_card
      @card = Card.find(params[:card_id])
      @board = @card.board
    end

    def render_card_replacement
      render turbo_stream: turbo_stream.replace(@card)
    end
end
```

**BoardScoped** - 加载 @board
**CurrentRequest** - 用请求数据填充 Current
**CurrentTimezone** - 在用户时区内包装请求
**FilterScoped** - 处理复杂过滤
**TurboFlash** - 通过 Turbo Stream 显示闪现消息
**ViewTransitions** - 在页面刷新时禁用
**BlockSearchEngineIndexing** - 设置 X-Robots-Tag 头
**RequestForgeryProtection** - Sec-Fetch-Site CSRF（现代浏览器）
</controller_concerns>

<authorization_patterns>
## 授权模式

控制器通过 before_action 检查权限，模型定义权限的含义：

```ruby
# Controller concern
module Authorization
  extend ActiveSupport::Concern

  private
    def ensure_can_administer
      head :forbidden unless Current.user.admin?
    end

    def ensure_is_staff_member
      head :forbidden unless Current.user.staff?
    end
end

# 使用方式
class BoardsController < ApplicationController
  before_action :ensure_can_administer, only: [:destroy]
end
```

**模型级授权：**
```ruby
class Board < ApplicationRecord
  def editable_by?(user)
    user.admin? || user == creator
  end

  def publishable_by?(user)
    editable_by?(user) && !published?
  end
end
```

保持授权简单、可读，与领域逻辑放在一起。
</authorization_patterns>

<security_concerns>
## 安全关注点

**Sec-Fetch-Site CSRF 防护：**
现代浏览器发送 Sec-Fetch-Site 头。使用它进行纵深防御：

```ruby
module RequestForgeryProtection
  extend ActiveSupport::Concern

  included do
    before_action :verify_request_origin
  end

  private
    def verify_request_origin
      return if request.get? || request.head?
      return if %w[same-origin same-site].include?(
        request.headers["Sec-Fetch-Site"]&.downcase
      )
      # 对于旧浏览器回退到令牌验证
      verify_authenticity_token
    end
end
```

**限流（Rails 8+）：**
```ruby
class MagicLinksController < ApplicationController
  rate_limit to: 10, within: 15.minutes, only: :create
end
```

应用于：认证端点、邮件发送、外部 API 调用、资源创建。
</security_concerns>

<request_context>
## 请求上下文 Concern

**CurrentRequest** - 用 HTTP 元数据填充 Current：
```ruby
module CurrentRequest
  extend ActiveSupport::Concern

  included do
    before_action :set_current_request
  end

  private
    def set_current_request
      Current.request_id = request.request_id
      Current.user_agent = request.user_agent
      Current.ip_address = request.remote_ip
      Current.referrer = request.referrer
    end
end
```

**CurrentTimezone** - 在用户时区内包装请求：
```ruby
module CurrentTimezone
  extend ActiveSupport::Concern

  included do
    around_action :set_timezone
    helper_method :timezone_from_cookie
  end

  private
    def set_timezone
      Time.use_zone(timezone_from_cookie) { yield }
    end

    def timezone_from_cookie
      cookies[:timezone] || "UTC"
    end
end
```

**SetPlatform** - 检测移动端/桌面端：
```ruby
module SetPlatform
  extend ActiveSupport::Concern

  included do
    helper_method :platform
  end

  def platform
    @platform ||= request.user_agent&.match?(/Mobile|Android/) ? :mobile : :desktop
  end
end
```
</request_context>

<turbo_responses>
## Turbo Stream 响应

使用 Turbo Stream 进行部分更新：

```ruby
class Cards::ClosuresController < ApplicationController
  include CardScoped

  def create
    @card.close
    render_card_replacement
  end

  def destroy
    @card.reopen
    render_card_replacement
  end
end
```

对于复杂更新，使用变形（morphing）：
```ruby
render turbo_stream: turbo_stream.morph(@card)
```
</turbo_responses>

<api_patterns>
## API 设计

相同的控制器，不同的格式。响应约定：

```ruby
def create
  @card = Card.create!(card_params)

  respond_to do |format|
    format.html { redirect_to @card }
    format.json { head :created, location: @card }
  end
end

def update
  @card.update!(card_params)

  respond_to do |format|
    format.html { redirect_to @card }
    format.json { head :no_content }
  end
end

def destroy
  @card.destroy

  respond_to do |format|
    format.html { redirect_to cards_path }
    format.json { head :no_content }
  end
end
```

**状态码：**
- 创建：201 Created + Location 头
- 更新：204 No Content
- 删除：204 No Content
- Bearer token 认证
</api_patterns>

<http_caching>
## HTTP 缓存

广泛使用 ETag 和条件 GET：

```ruby
class CardsController < ApplicationController
  def show
    @card = Card.find(params[:id])
    fresh_when etag: [@card, Current.user.timezone]
  end

  def index
    @cards = @board.cards.preloaded
    fresh_when etag: [@cards, @board.updated_at]
  end
end
```

关键洞察：时间在服务器端以用户时区渲染，因此时区必须影响 ETag，以防止向其他时区提供错误的时间。

**ApplicationController 全局 etag：**
```ruby
class ApplicationController < ActionController::Base
  etag { "v1" }  # 增加版本号以失效所有缓存
end
```

在关联上使用 `touch: true` 进行缓存失效。
</http_caching>
