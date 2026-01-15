# 模型 - DHH Rails 风格

<model_concerns>
## 用于水平行为的 Concern

模型大量使用 concern。典型的 Card 模型包含 14+ 个 concern：

```ruby
class Card < ApplicationRecord
  include Assignable
  include Attachments
  include Broadcastable
  include Closeable
  include Colored
  include Eventable
  include Golden
  include Mentions
  include Multistep
  include Pinnable
  include Postponable
  include Readable
  include Searchable
  include Taggable
  include Watchable
end
```

每个 concern 都是独立的，包含关联、作用域和方法。

**命名：**形容词，描述能力（`Closeable`、`Publishable`、`Watchable`）
</model_concerns>

<state_records>
## 状态作为记录，而非布尔值

不使用布尔列，而是创建独立的记录：

```ruby
# 而不是：
closed: boolean
is_golden: boolean
postponed: boolean

# 创建记录：
class Card::Closure < ApplicationRecord
  belongs_to :card
  belongs_to :creator, class_name: "User"
end

class Card::Goldness < ApplicationRecord
  belongs_to :card
  belongs_to :creator, class_name: "User"
end

class Card::NotNow < ApplicationRecord
  belongs_to :card
  belongs_to :creator, class_name: "User"
end
```

**优势：**
- 自动时间戳（何时发生）
- 追踪谁做的更改
- 通过连接和 `where.missing` 轻松过滤
- 允许丰富的 UI 显示时间/操作人

**在模型中：**
```ruby
module Closeable
  extend ActiveSupport::Concern

  included do
    has_one :closure, dependent: :destroy
  end

  def closed?
    closure.present?
  end

  def close(creator: Current.user)
    create_closure!(creator: creator)
  end

  def reopen
    closure&.destroy
  end
end
```

**查询：**
```ruby
Card.joins(:closure)         # 已关闭的卡片
Card.where.missing(:closure) # 未关闭的卡片
```
</state_records>

<callbacks>
## 回调 - 谨慎使用

Fizzy 中 30 个文件只有 38 个回调。指南：

**用于：**
- `after_commit` 用于异步工作
- `before_save` 用于派生数据
- `after_create_commit` 用于副作用

**避免：**
- 复杂的回调链
- 回调中的业务逻辑
- 同步外部调用

```ruby
class Card < ApplicationRecord
  after_create_commit :notify_watchers_later
  before_save :update_search_index, if: :title_changed?

  private
    def notify_watchers_later
      NotifyWatchersJob.perform_later(self)
    end
end
```
</callbacks>

<scopes>
## 作用域命名

标准作用域名称：

```ruby
class Card < ApplicationRecord
  scope :chronologically, -> { order(created_at: :asc) }
  scope :reverse_chronologically, -> { order(created_at: :desc) }
  scope :alphabetically, -> { order(title: :asc) }
  scope :latest, -> { reverse_chronologically.limit(10) }

  # 标准预加载
  scope :preloaded, -> { includes(:creator, :assignees, :tags) }

  # 参数化
  scope :indexed_by, ->(column) { order(column => :asc) }
  scope :sorted_by, ->(column, direction = :asc) { order(column => direction) }
end
```
</scopes>

<poros>
## 纯 Ruby 对象（PORO）

PORO 在父模型下命名空间：

```ruby
# app/models/event/description.rb
class Event::Description
  def initialize(event)
    @event = event
  end

  def to_s
    # 事件描述的展示逻辑
  end
end

# app/models/card/eventable/system_commenter.rb
class Card::Eventable::SystemCommenter
  def initialize(card)
    @card = card
  end

  def comment(message)
    # 业务逻辑
  end
end

# app/models/user/filtering.rb
class User::Filtering
  # 视图上下文打包
end
```

**不用于服务对象。**业务逻辑留在模型中。
</poros>

<verbs_predicates>
## 方法命名

**动词** - 改变状态的操作：
```ruby
card.close
card.reopen
card.gild      # 标记为重要
card.ungild
board.publish
board.archive
```

**谓词** - 从状态派生的查询：
```ruby
card.closed?    # closure.present?
card.golden?    # goldness.present?
board.published?
```

**避免**通用的 setter：
```ruby
# 不好
card.set_closed(true)
card.update_golden_status(false)

# 好的
card.close
card.ungild
```
</verbs_predicates>

<validation_philosophy>
## 验证哲学

模型上的最小验证。在表单/操作对象上使用上下文验证：

```ruby
# 模型 - 最小化
class User < ApplicationRecord
  validates :email, presence: true, format: { with: URI::MailTo::EMAIL_REGEXP }
end

# 表单对象 - 上下文化
class Signup
  include ActiveModel::Model

  attr_accessor :email, :name, :terms_accepted

  validates :email, :name, presence: true
  validates :terms_accepted, acceptance: true

  def save
    return false unless valid?
    User.create!(email: email, name: name)
  end
end
```

**优先使用数据库约束**而非模型验证来保证数据完整性：
```ruby
# migration
add_index :users, :email, unique: true
add_foreign_key :cards, :boards
```
</validation_philosophy>

<error_handling>
## Let It Crash 哲学

使用在失败时抛出异常的 bang 方法：

```ruby
# 首选 - 失败时抛出异常
@card = Card.create!(card_params)
@card.update!(title: new_title)
@comment.destroy!

# 避免 - 静默失败
@card = Card.create(card_params)  # 失败时返回 false
if @card.save
  # ...
end
```

让错误自然传播。Rails 用 422 响应处理 ActiveRecord::RecordInvalid。
</error_handling>

<default_values>
## Lambda 默认值

对包含 Current 的关联使用 lambda 默认值：

```ruby
class Card < ApplicationRecord
  belongs_to :creator, class_name: "User", default: -> { Current.user }
  belongs_to :account, default: -> { Current.account }
end

class Comment < ApplicationRecord
  belongs_to :commenter, class_name: "User", default: -> { Current.user }
end
```

Lambda 确保在创建时动态解析。
</default_values>

<rails_71_patterns>
## Rails 7.1+ 模型模式

**Normalizes** - 验证前清理数据：
```ruby
class User < ApplicationRecord
  normalizes :email, with: ->(email) { email.strip.downcase }
  normalizes :phone, with: ->(phone) { phone.gsub(/\D/, "") }
end
```

**Delegated Types** - 替代多态关联：
```ruby
class Message < ApplicationRecord
  delegated_type :messageable, types: %w[Comment Reply Announcement]
end

# 现在你可以使用：
message.comment?        # 如果是 Comment 则返回 true
message.comment         # 返回 Comment 对象
Message.comments        # Comment 消息的作用域
```

**Store Accessor** - 结构化 JSON 存储：
```ruby
class User < ApplicationRecord
  store :settings, accessors: [:theme, :notifications_enabled], coder: JSON
end

user.theme = "dark"
user.notifications_enabled = true
```
</rails_71_patterns>

<concern_guidelines>
## Concern 指南

- **50-150 行**每个 concern（大多数约 100 行）
- **内聚** - 只包含相关功能
- **以能力命名** - `Closeable`、`Watchable`，而非 `CardHelpers`
- **独立** - 关联、作用域、方法放在一起
- **不仅仅是为了组织** - 当确实需要重用时才创建

**触碰链**用于缓存失效：
```ruby
class Comment < ApplicationRecord
  belongs_to :card, touch: true
end

class Card < ApplicationRecord
  belongs_to :board, touch: true
end
```

当评论更新时，卡片的 `updated_at` 会改变，然后级联到看板。

**事务包装**用于相关更新：
```ruby
class Card < ApplicationRecord
  def close(creator: Current.user)
    transaction do
      create_closure!(creator: creator)
      record_event(:closed)
      notify_watchers_later
    end
  end
end
```
</concern_guidelines>
