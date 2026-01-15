# Gem - DHH Rails 风格

<what_they_use>
## 37signals 使用的 Gem

**核心 Rails 技术栈：**
- turbo-rails, stimulus-rails, importmap-rails
- propshaft（资源管道）

**基于数据库的服务（Solid 套件）：**
- solid_queue - 后台任务
- solid_cache - 缓存
- solid_cable - WebSocket/Action Cable

**认证与安全：**
- bcrypt（用于任何需要的密码哈希）

**自家的 gem：**
- geared_pagination（基于游标的分页）
- lexxy（富文本编辑器）
- mittens（邮件工具）

**工具：**
- rqrcode（二维码生成）
- redcarpet + rouge（Markdown 渲染）
- web-push（推送通知）

**部署与运维：**
- kamal（Docker 部署）
- thruster（HTTP/2 代理）
- mission_control-jobs（任务监控）
- autotuner（GC 调优）
</what_they_use>

<what_they_avoid>
## 刻意避免的内容

**认证：**
```
devise → 自定义约150行认证
```
原因：完全控制，使用魔法链接无密码责任，更简单。

**授权：**
```
pundit/cancancan → 模型中的简单角色检查
```
原因：大多数应用不需要策略对象。模型上的方法就足够了：
```ruby
class Board < ApplicationRecord
  def editable_by?(user)
    user.admin? || user == creator
  end
end
```

**后台任务：**
```
sidekiq → Solid Queue
```
原因：基于数据库意味着无需 Redis，相同的事务保证。

**缓存：**
```
redis → Solid Cache
```
原因：数据库已经存在，更简单的基础设施。

**搜索：**
```
elasticsearch → 自定义分片搜索
```
原因：精确构建所需功能，无外部服务依赖。

**视图层：**
```
view_component → 标准局部视图
```
原因：局部视图就很好用。ViewComponents 在他们的用例中增加复杂性而无明显好处。

**API：**
```
GraphQL → REST 配合 Turbo
```
原因：当你控制两端时，REST 就足够了。GraphQL 的复杂性无法证明其合理性。

**工厂：**
```
factory_bot → Fixture
```
原因：Fixture 更简单、更快，并鼓励提前思考数据关系。

**服务对象：**
```
Interactor、Trailblazer → 胖模型
```
原因：业务逻辑留在模型中。使用 `card.close` 这样的方法而非 `CardCloser.call(card)`。

**表单对象：**
```
Reform、dry-validation → params.expect + 模型验证
```
原因：Rails 7.1 的 `params.expect` 足够清晰。模型上的上下文验证。

**装饰器：**
```
Draper → 视图辅助方法 + 局部视图
```
原因：辅助方法和局部视图更简单。无需装饰器间接层。

**CSS：**
```
Tailwind、Sass → 原生 CSS
```
原因：现代 CSS 有嵌套、变量、层。无需构建步骤。

**前端：**
```
React、Vue、SPA → Turbo + Stimulus
```
原因：服务器渲染的 HTML 加少量 JS。SPA 的复杂性无法证明其合理性。

**测试：**
```
RSpec → Minitest
```
原因：更简单、启动更快、更少的 DSL 魔法、随 Rails 一起发布。
</what_they_avoid>

<testing_philosophy>
## 测试哲学

**Minitest** - 更简单、更快：
```ruby
class CardTest < ActiveSupport::TestCase
  test "closing creates closure" do
    card = cards(:one)
    assert_difference -> { Card::Closure.count } do
      card.close
    end
    assert card.closed?
  end
end
```

**Fixture** - 加载一次，确定性：
```yaml
# test/fixtures/cards.yml
open_card:
  title: Open Card
  board: main
  creator: alice

closed_card:
  title: Closed Card
  board: main
  creator: bob
```

**动态时间戳**使用 ERB：
```yaml
recent:
  title: Recent
  created_at: <%= 1.hour.ago %>

old:
  title: Old
  created_at: <%= 1.month.ago %>
```

**时间旅行**用于依赖时间的测试：
```ruby
test "expires after 15 minutes" do
  magic_link = MagicLink.create!(user: users(:alice))

  travel 16.minutes

  assert magic_link.expired?
end
```

**VCR** 用于外部 API：
```ruby
VCR.use_cassette("stripe/charge") do
  charge = Stripe::Charge.create(amount: 1000)
  assert charge.paid
end
```

**测试与功能一起交付** - 同一提交，不是之前或之后。
</testing_philosophy>

<decision_framework>
## 决策框架

在添加 gem 之前，问以下问题：

1. **原生 Rails 能做到吗？**
   - ActiveRecord 能做 Sequel 能做的大多数事情
   - ActionMailer 处理邮件很好
   - ActiveJob 适用于大多数任务需求

2. **复杂性值得吗？**
   - 150 行自定义代码 vs 10,000 行的 gem
   - 你会更好地理解自己的代码
   - 更少的升级麻烦

3. **它会增加基础设施吗？**
   - Redis？考虑基于数据库的替代方案
   - 外部服务？考虑内部构建
   - 更简单的基础设施 = 更少的故障模式

4. **它来自你信任的人吗？**
   - 37signals 的 gem：在规模上经过实战考验
   - 维护良好、专注的 gem：通常没问题
   - 全家桶 gem：可能过度设计

**哲学：**
> "在使用 gem 之前先构建解决方案。"

不是反对 gem，而是支持理解。当 gem 真正解决你遇到的问题时使用它，而不是你可能遇到的问题。
</decision_framework>

<gem_patterns>
## Gem 使用模式

**分页：**
```ruby
# geared_pagination - cursor-based
class CardsController < ApplicationController
  def index
    @cards = @board.cards.geared(page: params[:page])
  end
end
```

**Markdown：**
```ruby
# redcarpet + rouge
class MarkdownRenderer
  def self.render(text)
    Redcarpet::Markdown.new(
      Redcarpet::Render::HTML.new(filter_html: true),
      autolink: true,
      fenced_code_blocks: true
    ).render(text)
  end
end
```

**后台任务：**
```ruby
# solid_queue - 无需 Redis
class ApplicationJob < ActiveJob::Base
  queue_as :default
  # 直接工作，由数据库支持
end
```

**缓存：**
```ruby
# solid_cache - 无需 Redis
# config/environments/production.rb
config.cache_store = :solid_cache_store
```
</gem_patterns>
