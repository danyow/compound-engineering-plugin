# 测试 - DHH Rails 风格

## 核心哲学

"Minitest 配合 fixture - 简单、快速、确定性。"这种方法优先考虑实用性而非约定。

## 为什么选择 Minitest 而非 RSpec

- **更简单**：更少的 DSL 魔法，纯 Ruby 断言
- **随 Rails 一起发布**：无需额外依赖
- **更快的启动时间**：更少的开销
- **纯 Ruby**：无需学习专门的语法

## Fixture 作为测试数据

相比工厂，fixture 提供预加载的数据：
- 加载一次，在测试中重用
- 无运行时对象创建开销
- 明确的关系可见性
- 确定性的 ID，便于调试

### Fixture 结构
```yaml
# test/fixtures/users.yml
david:
  identity: david
  account: basecamp
  role: admin

jason:
  identity: jason
  account: basecamp
  role: member

# test/fixtures/rooms.yml
watercooler:
  name: Water Cooler
  creator: david
  direct: false

# test/fixtures/messages.yml
greeting:
  body: Hello everyone!
  room: watercooler
  creator: david
```

### 在测试中使用 Fixture
```ruby
test "sending a message" do
  user = users(:david)
  room = rooms(:watercooler)

  # 使用 fixture 数据进行测试
end
```

### 动态 Fixture 值
ERB 支持时间敏感的数据：
```yaml
recent_card:
  title: Recent Card
  created_at: <%= 1.hour.ago %>

old_card:
  title: Old Card
  created_at: <%= 1.month.ago %>
```

## 测试组织

### 单元测试
使用 setup 块和标准断言验证业务逻辑：

```ruby
class CardTest < ActiveSupport::TestCase
  setup do
    @card = cards(:one)
    @user = users(:david)
  end

  test "closing a card creates a closure" do
    assert_difference -> { Card::Closure.count } do
      @card.close(creator: @user)
    end

    assert @card.closed?
    assert_equal @user, @card.closure.creator
  end

  test "reopening a card destroys the closure" do
    @card.close(creator: @user)

    assert_difference -> { Card::Closure.count }, -1 do
      @card.reopen
    end

    refute @card.closed?
  end
end
```

### 集成测试
测试完整的请求/响应周期：

```ruby
class CardsControllerTest < ActionDispatch::IntegrationTest
  setup do
    @user = users(:david)
    sign_in @user
  end

  test "closing a card" do
    card = cards(:one)

    post card_closure_path(card)

    assert_response :success
    assert card.reload.closed?
  end

  test "unauthorized user cannot close card" do
    sign_in users(:guest)
    card = cards(:one)

    post card_closure_path(card)

    assert_response :forbidden
    refute card.reload.closed?
  end
end
```

### 系统测试
使用 Capybara 的基于浏览器的测试：

```ruby
class MessagesTest < ApplicationSystemTestCase
  test "发送消息" do
    sign_in users(:david)
    visit room_path(rooms(:watercooler))

    fill_in "消息", with: "你好，世界！"
    click_button "发送"

    assert_text "你好，世界！"
  end

  test "编辑自己的消息" do
    sign_in users(:david)
    visit room_path(rooms(:watercooler))

    within "#message_#{messages(:greeting).id}" do
      click_on "编辑"
    end

    fill_in "消息", with: "更新后的消息"
    click_button "保存"

    assert_text "更新后的消息"
  end

  test "拖放卡片到新列" do
    sign_in users(:david)
    visit board_path(boards(:main))

    card = find("#card_#{cards(:one).id}")
    target = find("#column_#{columns(:done).id}")

    card.drag_to target

    assert_selector "#column_#{columns(:done).id} #card_#{cards(:one).id}"
  end
end
```

## Advanced Patterns

### Time Testing
Use `travel_to` for deterministic time-dependent assertions:

```ruby
test "card expires after 30 days" do
  card = cards(:one)

  travel_to 31.days.from_now do
    assert card.expired?
  end
end
```

### 使用 VCR 进行外部 API 测试
记录和重放 HTTP 交互：

```ruby
test "fetches user data from API" do
  VCR.use_cassette("user_api") do
    user_data = ExternalApi.fetch_user(123)

    assert_equal "John", user_data[:name]
  end
end
```

### 后台任务测试
断言任务入队和邮件发送：

```ruby
test "closing card enqueues notification job" do
  card = cards(:one)

  assert_enqueued_with(job: NotifyWatchersJob, args: [card]) do
    card.close
  end
end

test "welcome email is sent on signup" do
  assert_emails 1 do
    Identity.create!(email: "new@example.com")
  end
end
```

### 测试 Turbo Stream
```ruby
test "message creation broadcasts to room" do
  room = rooms(:watercooler)

  assert_turbo_stream_broadcasts [room, :messages] do
    room.messages.create!(body: "Test", creator: users(:david))
  end
end
```

## 测试原则

### 1. 测试可观察行为
关注代码做什么，而不是如何做：

```ruby
# ❌ 测试实现
test "对每个观察者调用 notify 方法" do
  card.expects(:notify).times(3)
  card.close
end

# ✅ 测试行为
test "关闭卡片时观察者收到通知" do
  assert_difference -> { Notification.count }, 3 do
    card.close
  end
end
```

### 2. 不要过度 Mock

```ruby
# ❌ 过度 mock 的测试
test "sending message" do
  room = mock("room")
  user = mock("user")
  message = mock("message")

  room.expects(:messages).returns(stub(create!: message))
  message.expects(:broadcast_create)

  MessagesController.new.create
end

# ✅ 测试真实情况
test "发送消息" do
  sign_in users(:david)
  post room_messages_url(rooms(:watercooler)),
    params: { message: { body: "你好" } }

  assert_response :success
  assert Message.exists?(body: "你好")
end
```

### 3. 测试与功能一起交付
同一提交，不是先 TDD 也不是后补测试。

### 4. 安全修复始终包含回归测试
每个安全修复都必须包含一个能捕获该漏洞的测试。

### 5. 集成测试验证完整工作流
不要只测试单个部分 - 测试它们如何协同工作。

## 文件组织

```
test/
├── controllers/         # 控制器的集成测试
├── fixtures/           # 所有模型的 YAML fixture
├── helpers/            # 辅助方法测试
├── integration/        # API 集成测试
├── jobs/               # 后台任务测试
├── mailers/            # 邮件测试
├── models/             # 模型的单元测试
├── system/             # 基于浏览器的系统测试
└── test_helper.rb      # 测试配置
```

## Test Helper 设置

```ruby
# test/test_helper.rb
ENV["RAILS_ENV"] ||= "test"
require_relative "../config/environment"
require "rails/test_help"

class ActiveSupport::TestCase
  fixtures :all

  parallelize(workers: :number_of_processors)
end

class ActionDispatch::IntegrationTest
  include SignInHelper
end

class ApplicationSystemTestCase < ActionDispatch::SystemTestCase
  driven_by :selenium, using: :headless_chrome
end
```

## 登录辅助方法

```ruby
# test/support/sign_in_helper.rb
module SignInHelper
  def sign_in(user)
    session = user.identity.sessions.create!
    cookies.signed[:session_id] = session.id
  end
end
```
