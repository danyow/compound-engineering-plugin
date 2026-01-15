# DSPy.rb 测试、优化与可观测性

## 测试

DSPy.rb 为 LLM 逻辑启用标准的 RSpec 测试模式，使您的 AI 应用可测试和可维护。

### 基本测试设置

```ruby
require 'rspec'
require 'dspy'

RSpec.describe EmailClassifier do
  before do
    DSPy.configure do |c|
      c.lm = DSPy::LM.new('openai/gpt-4o-mini', api_key: ENV['OPENAI_API_KEY'])
    end
  end

  describe '#classify' do
    it 'classifies technical support emails correctly' do
      classifier = EmailClassifier.new
      result = classifier.forward(
        email_subject: "Can't log in",
        email_body: "I'm unable to access my account"
      )

      expect(result[:category]).to eq('Technical')
      expect(result[:priority]).to be_in(['High', 'Medium', 'Low'])
    end
  end
end
```

### 模拟 LLM 响应

无需进行实际 API 调用即可测试您的模块:

```ruby
RSpec.describe MyModule do
  it 'handles mock responses correctly' do
    # 创建一个返回预定结果的模拟预测器
    mock_predictor = instance_double(DSPy::Predict)
    allow(mock_predictor).to receive(:forward).and_return({
      category: 'Technical',
      priority: 'High',
      confidence: 0.95
    })

    # 将模拟注入到您的模块中
    module_instance = MyModule.new
    module_instance.instance_variable_set(:@predictor, mock_predictor)

    result = module_instance.forward(input: 'test data')
    expect(result[:category]).to eq('Technical')
  end
end
```

### 测试类型安全

验证签名强制执行类型约束:

```ruby
RSpec.describe EmailClassificationSignature do
  it 'validates output types' do
    predictor = DSPy::Predict.new(EmailClassificationSignature)

    # 这应该可以工作
    result = predictor.forward(
      email_subject: 'Test',
      email_body: 'Test body'
    )
    expect(result[:category]).to be_a(String)

    # 测试无效类型被捕获
    expect {
      # 模拟 LLM 返回无效类型
      predictor.send(:validate_output, { category: 123 })
    }.to raise_error(DSPy::ValidationError)
  end
end
```

### 测试边缘情况

始终测试边界条件和错误场景:

```ruby
RSpec.describe EmailClassifier do
  it 'handles empty emails' do
    classifier = EmailClassifier.new
    result = classifier.forward(
      email_subject: '',
      email_body: ''
    )
    # 定义边缘情况的预期行为
    expect(result[:category]).to eq('General')
  end

  it 'handles very long emails' do
    long_body = 'word ' * 10000
    classifier = EmailClassifier.new

    expect {
      classifier.forward(
        email_subject: 'Test',
        email_body: long_body
      )
    }.not_to raise_error
  end

  it 'handles special characters' do
    classifier = EmailClassifier.new
    result = classifier.forward(
      email_subject: 'Test <script>alert("xss")</script>',
      email_body: 'Body with émojis 🎉 and spëcial çharacters'
    )

    expect(result[:category]).to be_in(['Technical', 'Billing', 'General'])
  end
end
```

### 集成测试

端到端测试完整工作流:

```ruby
RSpec.describe EmailProcessingPipeline do
  it 'processes email through complete pipeline' do
    pipeline = EmailProcessingPipeline.new

    result = pipeline.forward(
      email_subject: 'Billing question',
      email_body: 'How do I update my payment method?'
    )

    # 验证完整的管道输出
    expect(result[:classification]).to eq('Billing')
    expect(result[:priority]).to eq('Medium')
    expect(result[:suggested_response]).to include('payment')
    expect(result[:assigned_team]).to eq('billing_support')
  end
end
```

### 使用 VCR 进行确定性测试

使用 VCR 记录和重放 API 响应:

```ruby
require 'vcr'

VCR.configure do |config|
  config.cassette_library_dir = 'spec/vcr_cassettes'
  config.hook_into :webmock
  config.filter_sensitive_data('<OPENAI_API_KEY>') { ENV['OPENAI_API_KEY'] }
end

RSpec.describe EmailClassifier do
  it 'classifies emails consistently', :vcr do
    VCR.use_cassette('email_classification') do
      classifier = EmailClassifier.new
      result = classifier.forward(
        email_subject: 'Test subject',
        email_body: 'Test body'
      )

      expect(result[:category]).to eq('Technical')
    end
  end
end
```

## 优化

DSPy.rb 提供强大的优化功能来自动改进您的提示词和模块。

### MIPROv2 优化

MIPROv2 是一种高级多提示优化技术，使用 bootstrap 采样、指令生成和贝叶斯优化。

```ruby
require 'dspy/mipro'

# 定义要优化的模块
class EmailClassifier < DSPy::Module
  def initialize
    super
    @predictor = DSPy::ChainOfThought.new(EmailClassificationSignature)
  end

  def forward(input)
    @predictor.forward(input)
  end
end

# 准备训练数据
training_examples = [
  {
    input: { email_subject: "Can't log in", email_body: "Password reset not working" },
    expected_output: { category: 'Technical', priority: 'High' }
  },
  {
    input: { email_subject: "Billing question", email_body: "How much does premium cost?" },
    expected_output: { category: 'Billing', priority: 'Medium' }
  },
  # 添加更多示例...
]

# 定义评估指标
def accuracy_metric(example, prediction)
  (example[:expected_output][:category] == prediction[:category]) ? 1.0 : 0.0
end

# 运行优化
optimizer = DSPy::MIPROv2.new(
  metric: method(:accuracy_metric),
  num_candidates: 10,
  num_threads: 4
)

optimized_module = optimizer.compile(
  EmailClassifier.new,
  trainset: training_examples
)

# 使用优化后的模块
result = optimized_module.forward(
  email_subject: "New email",
  email_body: "New email content"
)
```

### Bootstrap Few-Shot 学习

从您的训练数据自动生成 few-shot 示例:

```ruby
require 'dspy/teleprompt'

# 创建用于 few-shot 优化的 teleprompter
teleprompter = DSPy::BootstrapFewShot.new(
  metric: method(:accuracy_metric),
  max_bootstrapped_demos: 5,
  max_labeled_demos: 3
)

# 编译优化后的模块
optimized = teleprompter.compile(
  MyModule.new,
  trainset: training_examples
)
```

### 自定义优化指标

为您的特定用例定义自定义指标:

```ruby
def custom_metric(example, prediction)
  score = 0.0

  # 类别准确性 (60% 权重)
  score += 0.6 if example[:expected_output][:category] == prediction[:category]

  # 优先级准确性 (40% 权重)
  score += 0.4 if example[:expected_output][:priority] == prediction[:priority]

  score
end

# 在优化中使用
optimizer = DSPy::MIPROv2.new(
  metric: method(:custom_metric),
  num_candidates: 10
)
```

### A/B 测试不同方法

比较不同的模块实现:

```ruby
# 方法 A: ChainOfThought
class ApproachA < DSPy::Module
  def initialize
    super
    @predictor = DSPy::ChainOfThought.new(EmailClassificationSignature)
  end

  def forward(input)
    @predictor.forward(input)
  end
end

# 方法 B: 带工具的 ReAct
class ApproachB < DSPy::Module
  def initialize
    super
    @predictor = DSPy::ReAct.new(
      EmailClassificationSignature,
      tools: [KnowledgeBaseTool.new]
    )
  end

  def forward(input)
    @predictor.forward(input)
  end
end

# 评估两种方法
def evaluate_approach(approach_class, test_set)
  approach = approach_class.new
  scores = test_set.map do |example|
    prediction = approach.forward(example[:input])
    accuracy_metric(example, prediction)
  end
  scores.sum / scores.size
end

approach_a_score = evaluate_approach(ApproachA, test_examples)
approach_b_score = evaluate_approach(ApproachB, test_examples)

puts "Approach A accuracy: #{approach_a_score}"
puts "Approach B accuracy: #{approach_b_score}"
```

## 可观测性

跟踪 LLM 应用在生产中的性能、token 使用和行为。

### OpenTelemetry 集成

配置后，DSPy.rb 会自动与 OpenTelemetry 集成:

```ruby
require 'opentelemetry/sdk'
require 'dspy'

# 配置 OpenTelemetry
OpenTelemetry::SDK.configure do |c|
  c.service_name = 'my-dspy-app'
  c.use_all # 使用所有可用的监测工具
end

# DSPy 自动为预测创建追踪
predictor = DSPy::Predict.new(MySignature)
result = predictor.forward(input: 'data')
# 追踪自动发送到您的 OpenTelemetry 收集器
```

### Langfuse 集成

使用 Langfuse 跟踪详细的 LLM 执行追踪:

```ruby
require 'dspy/langfuse'

# 配置 Langfuse
DSPy.configure do |c|
  c.lm = DSPy::LM.new('openai/gpt-4o-mini', api_key: ENV['OPENAI_API_KEY'])
  c.langfuse = {
    public_key: ENV['LANGFUSE_PUBLIC_KEY'],
    secret_key: ENV['LANGFUSE_SECRET_KEY'],
    host: ENV['LANGFUSE_HOST'] || 'https://cloud.langfuse.com'
  }
end

# 所有预测都会自动追踪
predictor = DSPy::Predict.new(MySignature)
result = predictor.forward(input: 'data')
# 在 Langfuse 仪表板中查看详细追踪
```

### 手动 Token 跟踪

无需外部服务即可跟踪 token 使用:

```ruby
class TokenTracker
  def initialize
    @total_tokens = 0
    @request_count = 0
  end

  def track_prediction(predictor, input)
    start_time = Time.now
    result = predictor.forward(input)
    duration = Time.now - start_time

    # 从响应元数据获取 token 使用
    tokens = result.metadata[:usage][:total_tokens] rescue 0
    @total_tokens += tokens
    @request_count += 1

    puts "Request ##{@request_count}: #{tokens} tokens in #{duration}s"
    puts "Total tokens used: #{@total_tokens}"

    result
  end
end

# 使用
tracker = TokenTracker.new
predictor = DSPy::Predict.new(MySignature)

result = tracker.track_prediction(predictor, { input: 'data' })
```

### 自定义日志

向您的模块添加详细日志:

```ruby
class EmailClassifier < DSPy::Module
  def initialize
    super
    @predictor = DSPy::ChainOfThought.new(EmailClassificationSignature)
    @logger = Logger.new(STDOUT)
  end

  def forward(input)
    @logger.info "Classifying email: #{input[:email_subject]}"

    start_time = Time.now
    result = @predictor.forward(input)
    duration = Time.now - start_time

    @logger.info "Classification: #{result[:category]} (#{duration}s)"

    if result[:reasoning]
      @logger.debug "Reasoning: #{result[:reasoning]}"
    end

    result
  rescue => e
    @logger.error "Classification failed: #{e.message}"
    raise
  end
end
```

### 性能监控

监控延迟和性能指标:

```ruby
class PerformanceMonitor
  def initialize
    @metrics = {
      total_requests: 0,
      total_duration: 0.0,
      errors: 0,
      success_count: 0
    }
  end

  def monitor_request
    start_time = Time.now
    @metrics[:total_requests] += 1

    begin
      result = yield
      @metrics[:success_count] += 1
      result
    rescue => e
      @metrics[:errors] += 1
      raise
    ensure
      duration = Time.now - start_time
      @metrics[:total_duration] += duration

      if @metrics[:total_requests] % 10 == 0
        print_stats
      end
    end
  end

  def print_stats
    avg_duration = @metrics[:total_duration] / @metrics[:total_requests]
    success_rate = @metrics[:success_count].to_f / @metrics[:total_requests]

    puts "\n=== Performance Stats ==="
    puts "Total requests: #{@metrics[:total_requests]}"
    puts "Average duration: #{avg_duration.round(3)}s"
    puts "Success rate: #{(success_rate * 100).round(2)}%"
    puts "Errors: #{@metrics[:errors]}"
    puts "========================\n"
  end
end

# 使用
monitor = PerformanceMonitor.new
predictor = DSPy::Predict.new(MySignature)

result = monitor.monitor_request do
  predictor.forward(input: 'data')
end
```

### 错误率跟踪

监控错误率并发出警报:

```ruby
class ErrorRateMonitor
  def initialize(alert_threshold: 0.1)
    @alert_threshold = alert_threshold
    @recent_results = []
    @window_size = 100
  end

  def track_result(success:)
    @recent_results << success
    @recent_results.shift if @recent_results.size > @window_size

    error_rate = calculate_error_rate
    alert_if_needed(error_rate)

    error_rate
  end

  private

  def calculate_error_rate
    failures = @recent_results.count(false)
    failures.to_f / @recent_results.size
  end

  def alert_if_needed(error_rate)
    if error_rate > @alert_threshold
      puts "⚠️  ALERT: Error rate #{(error_rate * 100).round(2)}% exceeds threshold!"
      # 发送通知、呼叫待命人员等
    end
  end
end
```

## 最佳实践

### 1. 从测试开始

在优化之前编写测试:

```ruby
# 首先定义测试用例
test_cases = [
  { input: {...}, expected: {...} },
  # 更多测试用例...
]

# 确保基线功能
test_cases.each do |tc|
  result = module.forward(tc[:input])
  assert result[:category] == tc[:expected][:category]
end

# 然后优化
optimized = optimizer.compile(module, trainset: test_cases)
```

### 2. 使用有意义的指标

定义与业务目标一致的指标:

```ruby
def business_aligned_metric(example, prediction)
  # 高优先级错误成本更高
  if example[:expected_output][:priority] == 'High'
    return prediction[:priority] == 'High' ? 1.0 : 0.0
  else
    return prediction[:category] == example[:expected_output][:category] ? 0.8 : 0.0
  end
end
```

### 3. 在生产中监控

始终跟踪生产性能:

```ruby
class ProductionModule < DSPy::Module
  def initialize
    super
    @predictor = DSPy::ChainOfThought.new(MySignature)
    @monitor = PerformanceMonitor.new
    @error_tracker = ErrorRateMonitor.new
  end

  def forward(input)
    @monitor.monitor_request do
      result = @predictor.forward(input)
      @error_tracker.track_result(success: true)
      result
    rescue => e
      @error_tracker.track_result(success: false)
      raise
    end
  end
end
```

### 4. 版本化您的模块

跟踪部署的模块版本:

```ruby
class EmailClassifierV2 < DSPy::Module
  VERSION = '2.1.0'

  def initialize
    super
    @predictor = DSPy::ChainOfThought.new(EmailClassificationSignature)
  end

  def forward(input)
    result = @predictor.forward(input)
    result.merge(model_version: VERSION)
  end
end
```
