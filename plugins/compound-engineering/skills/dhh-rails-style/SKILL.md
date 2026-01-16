---
name: dhh-rails-style
description: 在以 DHH 独特的 37signals 风格编写 Ruby 和 Rails 代码时应使用此 skill。适用于编写 Ruby 代码、Rails 应用、创建 model、controller 或任何 Ruby 文件。触发词：Ruby/Rails 代码生成、重构请求、代码审查，或用户提及 DHH、37signals、Basecamp、HEY 或 Campfire 风格。体现 REST 纯粹性、fat model、thin controller、Current 属性、Hotwire 模式和"清晰胜于聪明"的哲学。
---

<objective>
将 37signals/DHH Rails 约定应用于 Ruby 和 Rails 代码。此 skill 提供从分析生产环境 37signals 代码库（Fizzy/Campfire）和 DHH 的代码审查模式中提取的全面领域专业知识。
</objective>

<essential_principles>
## 核心哲学

"最好的代码是你不写的代码。第二好的是显而易见正确的代码。"

**原生 Rails 就足够：**
- 丰富的领域模型而非 service 对象
- CRUD controller 而非自定义 action
- 使用 concern 进行横向代码共享
- 用记录表示状态而非布尔列
- 一切基于数据库（不用 Redis）
- 在求助 gem 之前先构建解决方案

**他们刻意避免的：**
- devise（自定义约 150 行的认证代替）
- pundit/cancancan（model 中简单的角色检查）
- sidekiq（Solid Queue 使用数据库）
- redis（一切用数据库）
- view_component（partial 就够用）
- GraphQL（REST + Turbo 足够）
- factory_bot（fixture 更简单）
- rspec（Minitest 随 Rails 自带）
- Tailwind（原生 CSS + layers）

**开发哲学：**
- 发布、验证、改进 - 将原型质量的代码投入生产以学习
- 修复根本原因，而非症状
- 写时操作优于读时计算
- 数据库约束优于 ActiveRecord 验证
</essential_principles>

<intake>
你在做什么？

1. **Controller** - REST 映射、concern、Turbo 响应、API 模式
2. **Model** - Concern、状态记录、回调、scope、PORO
3. **视图与前端** - Turbo、Stimulus、CSS、partial
4. **架构** - 路由、多租户、认证、job、缓存
5. **测试** - Minitest、fixture、集成测试
6. **Gem 与依赖** - 使用什么 vs 避免什么
7. **代码审查** - 根据 DHH 风格审查代码
8. **一般指导** - 哲学和约定

**指定一个数字或描述你的任务。**
</intake>

<routing>
| 响应 | 要阅读的参考 |
|----------|-------------------|
| 1, "controller" | [controllers.md](./references/controllers.md) |
| 2, "model" | [models.md](./references/models.md) |
| 3, "view", "frontend", "turbo", "stimulus", "css" | [frontend.md](./references/frontend.md) |
| 4, "architecture", "routing", "auth", "job", "cache" | [architecture.md](./references/architecture.md) |
| 5, "test", "testing", "minitest", "fixture" | [testing.md](./references/testing.md) |
| 6, "gem", "dependency", "library" | [gems.md](./references/gems.md) |
| 7, "review" | 阅读所有参考，然后审查代码 |
| 8, general task | 根据上下文阅读相关参考 |

**阅读相关参考后，将模式应用到用户的代码中。**
</routing>

<quick_reference>
## 命名约定

**动词：** `card.close`、`card.gild`、`board.publish`（不是 `set_style` 方法）

**谓词：** `card.closed?`、`card.golden?`（从相关记录的存在派生）

**Concern：** 描述能力的形容词（`Closeable`、`Publishable`、`Watchable`）

**Controller：** 匹配资源的名词（`Cards::ClosuresController`）

**Scope：**
- `chronologically`、`reverse_chronologically`、`alphabetically`、`latest`
- `preloaded`（标准预加载名称）
- `indexed_by`、`sorted_by`（参数化）
- `active`、`unassigned`（业务术语，而非 SQL 式）

## REST 映射

不要使用自定义 action，而是创建新资源：

```
POST /cards/:id/close    → POST /cards/:id/closure
DELETE /cards/:id/close  → DELETE /cards/:id/closure
POST /cards/:id/archive  → POST /cards/:id/archival
```

## Ruby 语法偏好

```ruby
# Symbol 数组括号内有空格
before_action :set_message, only: %i[ show edit update destroy ]

# Private 方法缩进
  private
    def set_message
      @message = Message.find(params[:id])
    end

# 无表达式的 case 用于条件判断
case
when params[:before].present?
  messages.page_before(params[:before])
else
  messages.last_page
end

# Bang 方法实现快速失败
@message = Message.create!(params)

# 三元运算符用于简单条件
@room.direct? ? @room.users : @message.mentionees
```

## 关键模式

**状态作为记录：**
```ruby
Card.joins(:closure)         # 已关闭的卡片
Card.where.missing(:closure) # 未关闭的卡片
```

**Current 属性：**
```ruby
belongs_to :creator, default: -> { Current.user }
```

**Model 上的授权：**
```ruby
class User < ApplicationRecord
  def can_administer?(message)
    message.creator == self || admin?
  end
end
```
</quick_reference>

<reference_index>
## 领域知识

所有详细模式在 `references/` 中：

| 文件 | 主题 |
|------|--------|
| [controllers.md](./references/controllers.md) | REST 映射、concern、Turbo 响应、API 模式、HTTP 缓存 |
| [models.md](./references/models.md) | Concern、状态记录、回调、scope、PORO、授权、广播 |
| [frontend.md](./references/frontend.md) | Turbo Stream、Stimulus controller、CSS layer、OKLCH 颜色、partial |
| [architecture.md](./references/architecture.md) | 路由、认证、job、Current 属性、缓存、数据库模式 |
| [testing.md](./references/testing.md) | Minitest、fixture、单元/集成/系统测试、测试模式 |
| [gems.md](./references/gems.md) | 使用什么 vs 避免什么、决策框架、Gemfile 示例 |
</reference_index>

<success_criteria>
符合 DHH 风格的代码：
- Controller 映射到资源上的 CRUD 动词
- Model 使用 concern 实现横向行为
- 通过记录而非布尔值追踪状态
- 没有不必要的 service 对象或抽象
- 优先使用基于数据库的解决方案而非外部服务
- 测试使用 Minitest + fixture
- 使用 Turbo/Stimulus 实现交互（不用重型 JS 框架）
- 使用现代特性的原生 CSS（layer、OKLCH、嵌套）
- 授权逻辑位于 User model 中
- Job 是调用 model 方法的浅层包装
</success_criteria>

<credits>
基于 [Marc Köhlbrugge](https://x.com/marckohlbrugge) 的 [The Unofficial 37signals/DHH Rails Style Guide](https://github.com/marckohlbrugge/unofficial-37signals-coding-style-guide)，通过深度分析 Fizzy 代码库的 265 个 pull request 生成。

**重要免责声明：**
- LLM 生成的指南 - 可能包含不准确之处
- Fizzy 的代码示例依据 O'Saasy License 授权
- 未经 37signals 认可或附属
</credits>
