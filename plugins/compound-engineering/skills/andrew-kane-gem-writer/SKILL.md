---
name: andrew-kane-gem-writer
description: 在编写遵循 Andrew Kane 经过验证的模式和哲学的 Ruby gem 时应使用此 skill。适用于创建新的 Ruby gem、重构现有 gem、设计 gem API，或需要简洁、最小化、生产就绪的 Ruby 库代码时。触发词："创建 gem"、"编写 Ruby 库"、"设计 gem API"，或提及 Andrew Kane 的风格。
---

# Andrew Kane Gem Writer

遵循 Andrew Kane 经过实战检验的模式编写 Ruby gem，这些模式来自 100+ 个 gem，总下载量达 374M+（Searchkick、PgHero、Chartkick、Strong Migrations、Lockbox、Ahoy、Blazer、Groupdate、Neighbor、Blind Index）。

## 核心哲学

**简单胜于聪明。** 零依赖或最小依赖。显式代码胜于元编程。Rails 集成但不耦合 Rails。每个模式都服务于生产用例。

## 入口点结构

每个 gem 在 `lib/gemname.rb` 中都遵循这个确切模式：

```ruby
# 1. 依赖（优先使用标准库）
require "forwardable"

# 2. 内部模块
require_relative "gemname/model"
require_relative "gemname/version"

# 3. 条件加载 Rails（关键 - 永远不要直接 require Rails）
require_relative "gemname/railtie" if defined?(Rails)

# 4. 包含配置和错误的模块
module GemName
  class Error < StandardError; end
  class InvalidConfigError < Error; end

  class << self
    attr_accessor :timeout, :logger
    attr_writer :client
  end

  self.timeout = 10  # 立即设置默认值
end
```

## 类宏 DSL 模式

Kane 的标志性模式——单个方法调用配置一切：

```ruby
# 使用方式
class Product < ApplicationRecord
  searchkick word_start: [:name]
end

# 实现方式
module GemName
  module Model
    def gemname(**options)
      unknown = options.keys - KNOWN_KEYWORDS
      raise ArgumentError, "unknown keywords: #{unknown.join(", ")}" if unknown.any?

      mod = Module.new
      mod.module_eval do
        define_method :some_method do
          # implementation
        end unless method_defined?(:some_method)
      end
      include mod

      class_eval do
        cattr_reader :gemname_options, instance_reader: false
        class_variable_set :@@gemname_options, options.dup
      end
    end
  end
end
```

## Rails 集成

**始终使用 `ActiveSupport.on_load`——永远不要直接 require Rails gem：**

```ruby
# 错误方式
require "active_record"
ActiveRecord::Base.include(MyGem::Model)

# 正确方式
ActiveSupport.on_load(:active_record) do
  extend GemName::Model
end

# 使用 prepend 来修改行为
ActiveSupport.on_load(:active_record) do
  ActiveRecord::Migration.prepend(GemName::Migration)
end
```

## 配置模式

使用 `class << self` 和 `attr_accessor`，而非配置对象：

```ruby
module GemName
  class << self
    attr_accessor :timeout, :logger
    attr_writer :master_key
  end

  def self.master_key
    @master_key ||= ENV["GEMNAME_MASTER_KEY"]
  end

  self.timeout = 10
  self.logger = nil
end
```

## 错误处理

简单的层次结构和信息丰富的消息：

```ruby
module GemName
  class Error < StandardError; end
  class ConfigError < Error; end
  class ValidationError < Error; end
end

# 使用 ArgumentError 尽早验证
def initialize(key:)
  raise ArgumentError, "Key must be 32 bytes" unless key&.bytesize == 32
end
```

## 测试（仅使用 Minitest）

```ruby
# test/test_helper.rb
require "bundler/setup"
Bundler.require(:default)
require "minitest/autorun"
require "minitest/pride"

# test/model_test.rb
class ModelTest < Minitest::Test
  def test_basic_functionality
    assert_equal expected, actual
  end
end
```

## Gemspec 模式

尽可能零运行时依赖：

```ruby
Gem::Specification.new do |spec|
  spec.name = "gemname"
  spec.version = GemName::VERSION
  spec.required_ruby_version = ">= 3.1"
  spec.files = Dir["*.{md,txt}", "{lib}/**/*"]
  spec.require_path = "lib"
  # 不添加 add_dependency 行 - 开发依赖放在 Gemfile 中
end
```

## 要避免的反模式

- `method_missing`（使用 `define_method` 代替）
- 配置对象（使用类访问器）
- `@@class_variables`（使用 `class << self`）
- 直接 require Rails gem
- 过多的运行时依赖
- 在 gem 中提交 Gemfile.lock
- RSpec（使用 Minitest）
- 重量级 DSL（优先使用显式 Ruby）

## 参考文件

深入了解模式，请参阅：
- **[references/module-organization.md](references/module-organization.md)** - 目录布局、方法分解
- **[references/rails-integration.md](references/rails-integration.md)** - Railtie、Engine、on_load 模式
- **[references/database-adapters.md](references/database-adapters.md)** - 多数据库支持模式
- **[references/testing-patterns.md](references/testing-patterns.md)** - 多版本测试、CI 设置
- **[references/resources.md](references/resources.md)** - Kane 的代码库和文章链接
