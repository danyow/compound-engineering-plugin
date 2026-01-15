<golden_rule>
将你的 skill 展示给没有上下文的人，让他们按照说明操作。如果他们感到困惑，Claude 也很可能会困惑。
</golden_rule>

<overview>
清晰和直接是有效编写 skill 的基础。清晰的指令可以减少错误、提高执行质量并最小化 token 浪费。
</overview>

<guidelines>
<contextual_information>
为 Claude 提供界定任务范围的上下文信息：

- 任务结果将用于什么用途
- 输出面向什么受众
- 任务是哪个工作流程的一部分
- 最终目标或成功完成的标准

上下文帮助 Claude 做出更好的决策并产生更合适的输出。

<example>
```xml
<context>
This analysis will be presented to investors who value transparency and actionable insights. Focus on financial metrics and clear recommendations.
</context>
```
</example>
</contextual_information>

<specificity>
明确说明你希望 Claude 做什么。如果你只想要代码，没有其他内容，就明确说出来。

**模糊**: "帮助处理报告"
**具体**: "生成一个包含三个部分的 markdown 报告：执行摘要、关键发现、建议"

**模糊**: "处理数据"
**具体**: "从 CSV 文件中提取客户姓名和电子邮件地址，删除重复项，并保存为 JSON 格式"

具体性消除了歧义并减少了迭代周期。
</specificity>

<sequential_steps>
以连续步骤的形式提供指令。使用编号列表或项目符号。

```xml
<workflow>
1. Extract data from source file
2. Transform to target format
3. Validate transformation
4. Save to output file
5. Verify output correctness
</workflow>
```

连续步骤创建清晰的期望，减少 Claude 跳过重要操作的可能性。
</sequential_steps>
</guidelines>

<example_comparison>
<unclear_example>
```xml
<quick_start>
Please remove all personally identifiable information from these customer feedback messages: {{FEEDBACK_DATA}}
</quick_start>
```

**问题**:
- 什么算作 PII？
- 应该用什么替换 PII？
- 输出应该是什么格式？
- 如果没有找到 PII 怎么办？
- 产品名称是否应该删除？
</unclear_example>

<clear_example>
```xml
<objective>
Anonymize customer feedback for quarterly review presentation.
</objective>

<quick_start>
<instructions>
1. Replace all customer names with "CUSTOMER_[ID]" (e.g., "Jane Doe" → "CUSTOMER_001")
2. Replace email addresses with "EMAIL_[ID]@example.com"
3. Redact phone numbers as "PHONE_[ID]"
4. If a message mentions a specific product (e.g., "AcmeCloud"), leave it intact
5. If no PII is found, copy the message verbatim
6. Output only the processed messages, separated by "---"
</instructions>

Data to process: {{FEEDBACK_DATA}}
</quick_start>

<success_criteria>
- All customer names replaced with IDs
- All emails and phones redacted
- Product names preserved
- Output format matches specification
</success_criteria>
```

**为什么这样更好**:
- 说明了目的（季度审查）
- 提供明确的逐步规则
- 清晰地定义输出格式
- 指定边界情况（产品名称、未找到 PII）
- 定义成功标准
</clear_example>
</example_comparison>

<key_differences>
清晰版本：
- 说明了目的（季度审查）
- 提供明确的逐步规则
- 定义输出格式
- 指定边界情况（产品名称、未找到 PII）
- 包含成功标准

不清晰的版本将所有这些决策留给 Claude，增加了与期望不一致的可能性。
</key_differences>

<show_dont_just_tell>
<principle>
当格式很重要时，展示示例而不是仅仅描述。
</principle>

<telling_example>
```xml
<commit_messages>
Generate commit messages in conventional format with type, scope, and description.
</commit_messages>
```
</telling_example>

<showing_example>
```xml
<commit_message_format>
Generate commit messages following these examples:

<example number="1">
<input>Added user authentication with JWT tokens</input>
<output>
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```
</output>
</example>

<example number="2">
<input>Fixed bug where dates displayed incorrectly in reports</input>
<output>
```
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation
```
</output>
</example>

Follow this style: type(scope): brief description, then detailed explanation.
</commit_message_format>
```
</showing_example>

<why_showing_works>
示例传达了文本描述无法传达的细微差别：
- 精确格式（间距、大小写、标点）
- 语气和风格
- 详细程度
- 跨多个案例的模式

Claude 从示例中学习模式比从描述中学习更可靠。
</why_showing_works>
</show_dont_just_tell>

<avoid_ambiguity>
<principle>
消除造成歧义或留下开放决策的词语和短语。
</principle>

<ambiguous_phrases>
❌ **"尝试..."** - 暗示可选
✅ **"始终..."** 或 **"从不..."** - 明确要求

❌ **"可能应该..."** - 义务不明确
✅ **"必须..."** 或 **"可以选择性地..."** - 明确义务级别

❌ **"通常..."** - 何时允许例外？
✅ **"始终... 除非..."** - 具有明确例外的清晰规则

❌ **"考虑..."** - Claude 应该总是这样做还是只是有时候？
✅ **"如果 X，则 Y"** 或 **"始终..."** - 明确条件
</ambiguous_phrases>

<example>
❌ **模糊**:
```xml
<validation>
You should probably validate the output and try to fix any errors.
</validation>
```

✅ **清晰**:
```xml
<validation>
Always validate output before proceeding:

```bash
python scripts/validate.py output_dir/
```

If validation fails, fix errors and re-validate. Only proceed when validation passes with zero errors.
</validation>
```
</example>
</avoid_ambiguity>

<define_edge_cases>
<principle>
预测边界情况并定义如何处理它们。不要让 Claude 猜测。
</principle>

<without_edge_cases>
```xml
<quick_start>
Extract email addresses from the text file and save to a JSON array.
</quick_start>
```

**未回答的问题**:
- 如果没有找到电子邮件怎么办？
- 如果同一个电子邮件出现多次怎么办？
- 如果电子邮件格式错误怎么办？
- 确切的 JSON 格式是什么？
</without_edge_cases>

<with_edge_cases>
```xml
<quick_start>
Extract email addresses from the text file and save to a JSON array.

<edge_cases>
- **No emails found**: Save empty array `[]`
- **Duplicate emails**: Keep only unique emails
- **Malformed emails**: Skip invalid formats, log to stderr
- **Output format**: Array of strings, one email per element
</edge_cases>

<example_output>
```json
[
  "user1@example.com",
  "user2@example.com"
]
```
</example_output>
</quick_start>
```
</with_edge_cases>
</define_edge_cases>

<output_format_specification>
<principle>
当输出格式很重要时，精确地指定它。展示示例。
</principle>

<vague_format>
```xml
<output>
Generate a report with the analysis results.
</output>
```
</vague_format>

<specific_format>
```xml
<output_format>
Generate a markdown report with this exact structure:

```markdown
# Analysis Report: [Title]

## Executive Summary
[1-2 paragraphs summarizing key findings]

## Key Findings
- Finding 1 with supporting data
- Finding 2 with supporting data
- Finding 3 with supporting data

## Recommendations
1. Specific actionable recommendation
2. Specific actionable recommendation

## Appendix
[Raw data and detailed calculations]
```

**Requirements**:
- Use exactly these section headings
- Executive summary must be 1-2 paragraphs
- List 3-5 key findings
- Provide 2-4 recommendations
- Include appendix with source data
</output_format>
```
</specific_format>
</output_format_specification>

<decision_criteria>
<principle>
当 Claude 必须做出决策时，提供明确的标准。
</principle>

<no_criteria>
```xml
<workflow>
Analyze the data and decide which visualization to use.
</workflow>
```

**问题**: 应该由哪些因素指导这个决策？
</no_criteria>

<with_criteria>
```xml
<workflow>
Analyze the data and select appropriate visualization:

<decision_criteria>
**Use bar chart when**:
- Comparing quantities across categories
- Fewer than 10 categories
- Exact values matter

**Use line chart when**:
- Showing trends over time
- Continuous data
- Pattern recognition matters more than exact values

**Use scatter plot when**:
- Showing relationship between two variables
- Looking for correlations
- Individual data points matter
</decision_criteria>
</workflow>
```

**优势**: Claude 有客观标准来做决策，而不是猜测。
</with_criteria>
</decision_criteria>

<constraints_and_requirements>
<principle>
清楚地区分"必须做"、"最好有"和"不能做"。
</principle>

<unclear_requirements>
```xml
<requirements>
The report should include financial data, customer metrics, and market analysis. It would be good to have visualizations. Don't make it too long.
</requirements>
```

**问题**:
- 这三种内容类型都是必需的吗？
- 可视化是可选的还是必需的？
- "太长"是多长？
</unclear_requirements>

<clear_requirements>
```xml
<requirements>
<must_have>
- Financial data (revenue, costs, profit margins)
- Customer metrics (acquisition, retention, lifetime value)
- Market analysis (competition, trends, opportunities)
- Maximum 5 pages
</must_have>

<nice_to_have>
- Charts and visualizations
- Industry benchmarks
- Future projections
</nice_to_have>

<must_not>
- Include confidential customer names
- Exceed 5 pages
- Use technical jargon without definitions
</must_not>
</requirements>
```

**优势**: 清晰的优先级和约束防止不一致。
</clear_requirements>
</constraints_and_requirements>

<success_criteria>
<principle>
定义成功是什么样子。Claude 如何知道它成功了？
</principle>

<without_success_criteria>
```xml
<objective>
Process the CSV file and generate a report.
</objective>
```

**问题**: 这个任务何时完成？什么定义了成功？
</without_success_criteria>

<with_success_criteria>
```xml
<objective>
Process the CSV file and generate a summary report.
</objective>

<success_criteria>
- All rows in CSV successfully parsed
- No data validation errors
- Report generated with all required sections
- Report saved to output/report.md
- Output file is valid markdown
- Process completes without errors
</success_criteria>
```

**优势**: 明确的完成标准消除了关于任务何时完成的歧义。
</with_success_criteria>
</success_criteria>

<testing_clarity>
<principle>
通过问自己来测试你的指令："我能否将这些指令交给初级开发人员并期望得到正确的结果？"
</principle>

<testing_process>
1. 阅读你的 skill 指令
2. 删除只有你才有的上下文（项目知识、未明说的假设）
3. 识别模糊的术语或模糊的要求
4. 在需要的地方添加具体性
5. 与没有你的上下文的人一起测试
6. 根据他们的问题和困惑进行迭代

如果具有最少上下文的人感到困难，Claude 也会如此。
</testing_process>
</testing_clarity>

<practical_examples>
<example domain="data_processing">
❌ **不清晰**:
```xml
<quick_start>
Clean the data and remove bad entries.
</quick_start>
```

✅ **清晰**:
```xml
<quick_start>
<data_cleaning>
1. Remove rows where required fields (name, email, date) are empty
2. Standardize date format to YYYY-MM-DD
3. Remove duplicate entries based on email address
4. Validate email format (must contain @ and domain)
5. Save cleaned data to output/cleaned_data.csv
</data_cleaning>

<success_criteria>
- No empty required fields
- All dates in YYYY-MM-DD format
- No duplicate emails
- All emails valid format
- Output file created successfully
</success_criteria>
</quick_start>
```
</example>

<example domain="code_generation">
❌ **不清晰**:
```xml
<quick_start>
Write a function to process user input.
</quick_start>
```

✅ **清晰**:
```xml
<quick_start>
<function_specification>
Write a Python function with this signature:

```python
def process_user_input(raw_input: str) -> dict:
    """
    Validate and parse user input.

    Args:
        raw_input: Raw string from user (format: "name:email:age")

    Returns:
        dict with keys: name (str), email (str), age (int)

    Raises:
        ValueError: If input format is invalid
    """
```

**Requirements**:
- Split input on colon delimiter
- Validate email contains @ and domain
- Convert age to integer, raise ValueError if not numeric
- Return dictionary with specified keys
- Include docstring and type hints
</function_specification>

<success_criteria>
- Function signature matches specification
- All validation checks implemented
- Proper error handling for invalid input
- Type hints included
- Docstring included
</success_criteria>
</quick_start>
```
</example>
</practical_examples>
