# 模块组织模式

## 简单 Gem 布局

```
lib/
├── gemname.rb          # 入口点，配置，错误
└── gemname/
    ├── helper.rb       # 核心功能
    ├── engine.rb       # Rails engine（如需要）
    └── version.rb      # 仅包含 VERSION 常量
```

## 复杂 Gem 布局（PgHero 模式）

```
lib/
├── pghero.rb
└── pghero/
    ├── database.rb     # 主类
    ├── engine.rb       # Rails engine
    └── methods/        # 功能分解
        ├── basic.rb
        ├── connections.rb
        ├── indexes.rb
        ├── queries.rb
        └── replication.rb
```

## 方法分解模式

将大型类按功能拆分为可包含的模块：

```ruby
# lib/pghero/database.rb
module PgHero
  class Database
    include Methods::Basic
    include Methods::Connections
    include Methods::Indexes
    include Methods::Queries
  end
end

# lib/pghero/methods/indexes.rb
module PgHero
  module Methods
    module Indexes
      def index_hit_rate
        # implementation
      end

      def unused_indexes
        # implementation
      end
    end
  end
end
```

## 版本文件模式

保持 version.rb 最小化：

```ruby
# lib/gemname/version.rb
module GemName
  VERSION = "2.0.0"
end
```

## 入口点中的引用顺序

```ruby
# lib/searchkick.rb

# 1. 标准库
require "forwardable"
require "json"

# 2. 外部依赖（最小化）
require "active_support"

# 3. 通过 require_relative 引用内部文件
require_relative "searchkick/index"
require_relative "searchkick/model"
require_relative "searchkick/query"
require_relative "searchkick/version"

# 4. 条件加载 Rails（最后）
require_relative "searchkick/railtie" if defined?(Rails)
```

## Autoload vs Require

Kane 使用显式的 `require_relative`，而不是 autoload：

```ruby
# 正确
require_relative "gemname/model"
require_relative "gemname/query"

# 避免
autoload :Model, "gemname/model"
autoload :Query, "gemname/query"
```

## 注释风格

仅使用最少的章节标题：

```ruby
# dependencies
require "active_support"

# adapters
require_relative "adapters/postgresql_adapter"

# modules
require_relative "migration"
```
