---
name: dspy-ruby
description: 当使用 DSPy.rb（一个用于构建类型安全、可组合 LLM 应用的 Ruby 框架）时，应使用此 Skill。在实现可预测的 AI 功能、创建 LLM signature 和模块、配置语言模型提供商（OpenAI、Anthropic、Gemini、Ollama）、构建带工具的 Agent 系统、优化 prompt 或在 Ruby 应用中测试 LLM 驱动的功能时使用此 Skill。
---

# DSPy.rb 专家

## 概述

DSPy.rb 是一个 Ruby 框架，使开发者能够**编程 LLM，而不是提示它们**。不是手动制作 prompt，而是通过类型安全、可组合的模块定义应用程序需求，这些模块可以像常规代码一样进行测试、优化和版本控制。

此 skill 提供全面的指导：
- 为 LLM 操作创建类型安全的 signature
- 构建可组合的模块和工作流
- 配置多个 LLM 提供商
- 使用工具实现 Agent
- 测试和优化 LLM 应用
- 生产部署模式

## 核心能力

### 1. 类型安全的 Signature

为 LLM 操作创建输入/输出契约，具有运行时类型检查。

**何时使用**：定义任何 LLM 任务，从简单分类到复杂分析。

**快速参考**：
```ruby
class EmailClassificationSignature < DSPy::Signature
  description "Classify customer support emails"

  input do
    const :email_subject, String
    const :email_body, String
  end

  output do
    const :category, T.enum(["Technical", "Billing", "General"])
    const :priority, T.enum(["Low", "Medium", "High"])
  end
end
```

**模板**：参见 `assets/signature-template.rb` 获取全面示例，包括：
- 带多种字段类型的基本 signature
- 用于多模态任务的视觉 signature
- 情感分析 signature
- 代码生成 signature

**最佳实践**：
- 始终提供清晰、具体的描述
- 对受约束的输出使用枚举
- 使用 `desc:` 参数包含字段描述
- 在可能时优先使用具体类型而非通用 String

**完整文档**：参见 `references/core-concepts.md` 中关于 Signature 和类型安全的部分。

### 2. 可组合模块

构建可重用、可链接的模块，封装 LLM 操作。

**何时使用**：实现任何 LLM 驱动的功能，特别是复杂的多步骤工作流。

**快速参考**：
```ruby
class EmailProcessor < DSPy::Module
  def initialize
    super
    @classifier = DSPy::Predict.new(EmailClassificationSignature)
  end

  def forward(email_subject:, email_body:)
    @classifier.forward(
      email_subject: email_subject,
      email_body: email_body
    )
  end
end
```

**模板**：参见 `assets/module-template.rb` 获取全面示例，包括：
- 带单个预测器的基本模块
- 链接模块的多步骤管道
- 带条件逻辑的模块
- 错误处理和重试模式
- 带历史的有状态模块
- 缓存实现

**模块组合**：将模块链接在一起创建复杂工作流：
```ruby
class Pipeline < DSPy::Module
  def initialize
    super
    @step1 = Classifier.new
    @step2 = Analyzer.new
    @step3 = Responder.new
  end

  def forward(input)
    result1 = @step1.forward(input)
    result2 = @step2.forward(result1)
    @step3.forward(result2)
  end
end
```

**完整文档**：参见 `references/core-concepts.md` 中关于模块和模块组合的部分。

### 3. 多种预测器类型

为你的任务选择正确的预测器：

**Predict**：基本 LLM 推理，具有类型安全的输入/输出
```ruby
predictor = DSPy::Predict.new(TaskSignature)
result = predictor.forward(input: "data")
```

**ChainOfThought**：添加自动推理以提高准确性
```ruby
predictor = DSPy::ChainOfThought.new(TaskSignature)
result = predictor.forward(input: "data")
# 返回：{ reasoning: "...", output: "..." }
```

**ReAct**：带迭代推理的工具使用 Agent
```ruby
predictor = DSPy::ReAct.new(
  TaskSignature,
  tools: [SearchTool.new, CalculatorTool.new],
  max_iterations: 5
)
```

**CodeAct**：动态代码生成（需要 `dspy-code_act` gem）
```ruby
predictor = DSPy::CodeAct.new(TaskSignature)
result = predictor.forward(task: "Calculate factorial of 5")
```

**何时使用每种**：
- **Predict**：简单任务、分类、提取
- **ChainOfThought**：复杂推理、分析、多步骤思考
- **ReAct**：需要外部工具的任务（搜索、计算、API 调用）
- **CodeAct**：最好用生成的代码解决的任务

**完整文档**：参见 `references/core-concepts.md` 中关于预测器的部分。

### 4. LLM 提供商配置

支持 OpenAI、Anthropic Claude、Google Gemini、Ollama 和 OpenRouter。

**快速配置示例**：
```ruby
# OpenAI
DSPy.configure do |c|
  c.lm = DSPy::LM.new('openai/gpt-4o-mini',
    api_key: ENV['OPENAI_API_KEY'])
end

# Anthropic Claude
DSPy.configure do |c|
  c.lm = DSPy::LM.new('anthropic/claude-3-5-sonnet-20241022',
    api_key: ENV['ANTHROPIC_API_KEY'])
end

# Google Gemini
DSPy.configure do |c|
  c.lm = DSPy::LM.new('gemini/gemini-1.5-pro',
    api_key: ENV['GOOGLE_API_KEY'])
end

# 本地 Ollama（免费、私密）
DSPy.configure do |c|
  c.lm = DSPy::LM.new('ollama/llama3.1')
end
```

**模板**：参见 `assets/config-template.rb` 获取全面示例，包括：
- 基于环境的配置
- 针对不同任务的多模型设置
- 带可观测性的配置（OpenTelemetry、Langfuse）
- 重试逻辑和回退策略
- 预算跟踪
- Rails 初始化器模式

**提供商兼容性矩阵**：

| 功能 | OpenAI | Anthropic | Gemini | Ollama |
|---------|--------|-----------|--------|--------|
| 结构化输出 | ✅ | ✅ | ✅ | ✅ |
| 视觉（图像） | ✅ | ✅ | ✅ | ⚠️ 有限 |
| 图像 URL | ✅ | ❌ | ❌ | ❌ |
| 工具调用 | ✅ | ✅ | ✅ | 因模型而异 |

**成本优化策略**：
- 开发：Ollama（免费）或 gpt-4o-mini（便宜）
- 测试：gpt-4o-mini，temperature=0.0
- 生产简单任务：gpt-4o-mini、claude-3-haiku、gemini-1.5-flash
- 生产复杂任务：gpt-4o、claude-3-5-sonnet、gemini-1.5-pro

**完整文档**：参见 `references/providers.md` 获取所有配置选项、提供商特定功能和故障排除。

### 5. 多模态和视觉支持

使用统一的 `DSPy::Image` 接口处理图像和文本。

**快速参考**：
```ruby
class VisionSignature < DSPy::Signature
  description "Analyze image and answer questions"

  input do
    const :image, DSPy::Image
    const :question, String
  end

  output do
    const :answer, String
  end
end

predictor = DSPy::Predict.new(VisionSignature)
result = predictor.forward(
  image: DSPy::Image.from_file("path/to/image.jpg"),
  question: "What objects are visible?"
)
```

**图像加载方法**：
```ruby
# 从文件
DSPy::Image.from_file("path/to/image.jpg")

# 从 URL（仅 OpenAI）
DSPy::Image.from_url("https://example.com/image.jpg")

# 从 base64
DSPy::Image.from_base64(base64_data, mime_type: "image/jpeg")
```

**提供商支持**：
- OpenAI：完全支持包括 URL
- Anthropic、Gemini：仅 Base64 或文件加载
- Ollama：有限的多模态，取决于模型

**完整文档**：参见 `references/core-concepts.md` 中关于多模态支持的部分。

### 6. 测试 LLM 应用

为 LLM 逻辑编写标准 RSpec 测试。

**快速参考**：
```ruby
RSpec.describe EmailClassifier do
  before do
    DSPy.configure do |c|
      c.lm = DSPy::LM.new('openai/gpt-4o-mini',
        api_key: ENV['OPENAI_API_KEY'])
    end
  end

  it 'classifies technical emails correctly' do
    classifier = EmailClassifier.new
    result = classifier.forward(
      email_subject: "Can't log in",
      email_body: "Unable to access account"
    )

    expect(result[:category]).to eq('Technical')
    expect(result[:priority]).to be_in(['High', 'Medium', 'Low'])
  end
end
```

**测试模式**：
- 为单元测试模拟 LLM 响应
- 使用 VCR 进行确定性 API 测试
- 测试类型安全和验证
- 测试边缘情况（空输入、特殊字符、长文本）
- 集成测试完整工作流

**完整文档**：参见 `references/optimization.md` 中关于测试的部分。

### 7. 优化与改进

使用优化技术自动改进 prompt 和模块。

**MIPROv2 优化**：
```ruby
require 'dspy/mipro'

# 定义评估指标
def accuracy_metric(example, prediction)
  example[:expected_output][:category] == prediction[:category] ? 1.0 : 0.0
end

# 准备训练数据
training_examples = [
  {
    input: { email_subject: "...", email_body: "..." },
    expected_output: { category: 'Technical' }
  },
  # 更多示例...
]

# 运行优化
optimizer = DSPy::MIPROv2.new(
  metric: method(:accuracy_metric),
  num_candidates: 10
)

optimized_module = optimizer.compile(
  EmailClassifier.new,
  trainset: training_examples
)
```

**A/B 测试不同方法**：
```ruby
# 测试 ChainOfThought vs ReAct
approach_a_score = evaluate_approach(ChainOfThoughtModule, test_set)
approach_b_score = evaluate_approach(ReActModule, test_set)
```

**完整文档**：参见 `references/optimization.md` 中关于优化的部分。

### 8. 可观测性与监控

跟踪生产中的性能、token 使用情况和行为。

**OpenTelemetry 集成**：
```ruby
require 'opentelemetry/sdk'

OpenTelemetry::SDK.configure do |c|
  c.service_name = 'my-dspy-app'
  c.use_all
end

# DSPy 自动创建追踪
```

**Langfuse 追踪**：
```ruby
DSPy.configure do |c|
  c.lm = DSPy::LM.new('openai/gpt-4o-mini',
    api_key: ENV['OPENAI_API_KEY'])

  c.langfuse = {
    public_key: ENV['LANGFUSE_PUBLIC_KEY'],
    secret_key: ENV['LANGFUSE_SECRET_KEY']
  }
end
```

**自定义监控**：
- Token 跟踪
- 性能监控
- 错误率跟踪
- 自定义日志

**完整文档**：参见 `references/optimization.md` 中关于可观测性的部分。

## 快速开始工作流

### 对于新项目

1. **安装 DSPy.rb 和提供商 gem**：
```bash
gem install dspy dspy-openai  # 或 dspy-anthropic、dspy-gemini
```

2. **配置 LLM 提供商**（参见 `assets/config-template.rb`）：
```ruby
require 'dspy'

DSPy.configure do |c|
  c.lm = DSPy::LM.new('openai/gpt-4o-mini',
    api_key: ENV['OPENAI_API_KEY'])
end
```

3. **创建 signature**（参见 `assets/signature-template.rb`）：
```ruby
class MySignature < DSPy::Signature
  description "Clear description of task"

  input do
    const :input_field, String, desc: "Description"
  end

  output do
    const :output_field, String, desc: "Description"
  end
end
```

4. **创建模块**（参见 `assets/module-template.rb`）：
```ruby
class MyModule < DSPy::Module
  def initialize
    super
    @predictor = DSPy::Predict.new(MySignature)
  end

  def forward(input_field:)
    @predictor.forward(input_field: input_field)
  end
end
```

5. **使用模块**：
```ruby
module_instance = MyModule.new
result = module_instance.forward(input_field: "test")
puts result[:output_field]
```

6. **添加测试**（参见 `references/optimization.md`）：
```ruby
RSpec.describe MyModule do
  it 'produces expected output' do
    result = MyModule.new.forward(input_field: "test")
    expect(result[:output_field]).to be_a(String)
  end
end
```

### 对于 Rails 应用

1. **添加到 Gemfile**：
```ruby
gem 'dspy'
gem 'dspy-openai'  # 或其他提供商
```

2. **创建初始化器**，位于 `config/initializers/dspy.rb`（完整示例参见 `assets/config-template.rb`）：
```ruby
require 'dspy'

DSPy.configure do |c|
  c.lm = DSPy::LM.new('openai/gpt-4o-mini',
    api_key: ENV['OPENAI_API_KEY'])
end
```

3. **在 `app/llm/` 目录中创建模块**：
```ruby
# app/llm/email_classifier.rb
class EmailClassifier < DSPy::Module
  # 实现在这里
end
```

4. **在控制器/服务中使用**：
```ruby
class EmailsController < ApplicationController
  def classify
    classifier = EmailClassifier.new
    result = classifier.forward(
      email_subject: params[:subject],
      email_body: params[:body]
    )
    render json: result
  end
end
```

## 常见模式

### 模式：多步骤分析管道

```ruby
class AnalysisPipeline < DSPy::Module
  def initialize
    super
    @extract = DSPy::Predict.new(ExtractSignature)
    @analyze = DSPy::ChainOfThought.new(AnalyzeSignature)
    @summarize = DSPy::Predict.new(SummarizeSignature)
  end

  def forward(text:)
    extracted = @extract.forward(text: text)
    analyzed = @analyze.forward(data: extracted[:data])
    @summarize.forward(analysis: analyzed[:result])
  end
end
```

### 模式：带工具的 Agent

```ruby
class ResearchAgent < DSPy::Module
  def initialize
    super
    @agent = DSPy::ReAct.new(
      ResearchSignature,
      tools: [
        WebSearchTool.new,
        DatabaseQueryTool.new,
        SummarizerTool.new
      ],
      max_iterations: 10
    )
  end

  def forward(question:)
    @agent.forward(question: question)
  end
end

class WebSearchTool < DSPy::Tool
  def call(query:)
    results = perform_search(query)
    { results: results }
  end
end
```

### 模式：条件路由

```ruby
class SmartRouter < DSPy::Module
  def initialize
    super
    @classifier = DSPy::Predict.new(ClassifySignature)
    @simple_handler = SimpleModule.new
    @complex_handler = ComplexModule.new
  end

  def forward(input:)
    classification = @classifier.forward(text: input)

    if classification[:complexity] == 'Simple'
      @simple_handler.forward(input: input)
    else
      @complex_handler.forward(input: input)
    end
  end
end
```

### 模式：带回退的重试

```ruby
class RobustModule < DSPy::Module
  MAX_RETRIES = 3

  def forward(input, retry_count: 0)
    begin
      @predictor.forward(input)
    rescue DSPy::ValidationError => e
      if retry_count < MAX_RETRIES
        sleep(2 ** retry_count)
        forward(input, retry_count: retry_count + 1)
      else
        # 回退到默认值或抛出
        raise
      end
    end
  end
end
```

## 资源

此 skill 包含全面的参考材料和模板：

### 参考资料（根据需要加载以获取详细信息）

- [core-concepts.md](./references/core-concepts.md)：signature、模块、预测器、多模态支持和最佳实践的完整指南
- [providers.md](./references/providers.md)：所有 LLM 提供商配置、兼容性矩阵、成本优化和故障排除
- [optimization.md](./references/optimization.md)：测试模式、优化技术、可观测性设置和监控

### 资产（快速开始模板）

- [signature-template.rb](./assets/signature-template.rb)：signature 示例，包括基本、视觉、情感分析和代码生成
- [module-template.rb](./assets/module-template.rb)：模块模式，包括管道、Agent、错误处理、缓存和状态管理
- [config-template.rb](./assets/config-template.rb)：所有提供商、环境、可观测性和生产模式的配置示例

## 何时使用此 Skill

在以下情况下触发此 skill：
- 在 Ruby 应用中实现 LLM 驱动的功能
- 为 AI 操作创建类型安全接口
- 构建带工具使用的 Agent 系统
- 设置或排除 LLM 提供商故障
- 优化 prompt 和提高准确性
- 测试 LLM 功能
- 向 AI 应用添加可观测性
- 从手动 prompt 工程转换到程序化方法
- 调试 DSPy.rb 代码或配置问题
