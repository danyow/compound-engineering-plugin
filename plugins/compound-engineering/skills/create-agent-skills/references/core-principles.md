<overview>
核心原则指导 skill 编写决策。这些原则确保 skills 在不同模型和用例中高效、有效且可维护。
</overview>

<xml_structure_principle>
<description>
Skills 使用纯 XML 结构以实现一致的解析、高效的 token 使用和改进的 Claude 性能。
</description>

<why_xml>
<consistency>
XML 在所有 skills 中强制执行一致的结构。所有 skills 使用相同的标签名称用于相同的目的：
- `<objective>` 始终定义 skill 做什么
- `<quick_start>` 始终提供即时指导
- `<success_criteria>` 始终定义完成标准

这种一致性使 skills 可预测且更易于维护。
</consistency>

<parseability>
XML 提供明确的边界和语义含义。Claude 可以可靠地：
- 识别节边界（内容开始和结束的位置）
- 理解内容目的（每个部分扮演的角色）
- 跳过不相关的部分（渐进式披露）
- 程序化解析（验证工具可以检查结构）

Markdown 标题只是视觉格式。Claude 必须从标题文本推断含义，这不太可靠。
</parseability>

<token_efficiency>
XML 标签比 markdown 标题更高效：

**Markdown 标题**:
```markdown
## Quick start
## Workflow
## Advanced features
## Success criteria
```
总计：~20 tokens，对 Claude 没有语义含义

**XML 标签**:
```xml
<quick_start>
<workflow>
<advanced_features>
<success_criteria>
```
总计：~15 tokens，内置语义含义

节省在生态系统中的所有 skills 中累积。
</token_efficiency>

<claude_performance>
Claude 在使用纯 XML 时表现更好，因为：
- 明确的节边界减少解析错误
- 语义标签直接传达意图（无需推断）
- 嵌套标签创建清晰的层次结构
- 跨 skills 的一致结构减少认知负担
- 渐进式披露工作更可靠

纯 XML 结构不仅仅是风格偏好——它是性能优化。
</claude_performance>
</why_xml>

<critical_rule>
**从 skill 主体内容中删除所有 markdown 标题（#、##、###）。** 用语义 XML 标签替换。保留内容中的 markdown 格式（粗体、斜体、列表、代码块、链接）。
</critical_rule>

<required_tags>
每个 skill 必须具有：
- `<objective>` - Skill 做什么以及为什么重要
- `<quick_start>` - 即时、可操作的指导
- `<success_criteria>` 或 `<when_successful>` - 如何知道它工作了

查看 [use-xml-tags.md](use-xml-tags.md) 了解条件标签和智能规则。
</required_tags>
</xml_structure_principle>

<conciseness_principle>
<description>
上下文窗口是共享的。你的 skill 与系统 prompt、对话历史、其他 skills 的元数据和实际请求共享它。
</description>

<guidance>
只添加 Claude 还没有的上下文。质疑每条信息：
- "Claude 真的需要这个解释吗？"
- "我可以假设 Claude 知道这个吗？"
- "这段话值得它的 token 成本吗？"

假设 Claude 很聪明。不要解释显而易见的概念。
</guidance>

<concise_example>
**简洁** (~50 tokens):
```xml
<quick_start>
Extract PDF text with pdfplumber:

```python
import pdfplumber

with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
</quick_start>
```

**冗长** (~150 tokens):
```xml
<quick_start>
PDF files are a common file format used for documents. To extract text from them, we'll use a Python library called pdfplumber. First, you'll need to import the library, then open the PDF file using the open method, and finally extract the text from each page. Here's how to do it:

```python
import pdfplumber

with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

This code opens the PDF and extracts text from the first page.
</quick_start>
```

简洁版本假设 Claude 知道什么是 PDF，理解 Python imports，并且可以阅读代码。所有这些假设都是正确的。
</concise_example>

<when_to_elaborate>
在以下情况下添加解释：
- 概念是特定领域的（不是通用编程知识）
- 模式不明显或违反直觉
- 上下文以微妙的方式影响行为
- 权衡需要判断

不要为以下内容添加解释：
- 常见的编程概念（循环、函数、imports）
- 标准库使用（读取文件、发出 HTTP 请求）
- 众所周知的工具（git、npm、pip）
- 显而易见的下一步
</when_to_elaborate>
</conciseness_principle>

<degrees_of_freedom_principle>
<description>
将具体程度与任务的脆弱性和可变性相匹配。对于创造性任务给予 Claude 更多自由，对于脆弱的操作给予更少自由。
</description>

<high_freedom>
<when>
- 多种方法都有效
- 决策取决于上下文
- 启发式方法指导方法
- 欢迎创造性解决方案
</when>

<example>
```xml
<objective>
Review code for quality, bugs, and maintainability.
</objective>

<workflow>
1. Analyze the code structure and organization
2. Check for potential bugs or edge cases
3. Suggest improvements for readability and maintainability
4. Verify adherence to project conventions
</workflow>

<success_criteria>
- All major issues identified
- Suggestions are actionable and specific
- Review balances praise and criticism
</success_criteria>
```

Claude 可以根据代码需要自由调整审查。
</example>
</high_freedom>

<medium_freedom>
<when>
- 存在首选模式
- 可以接受一些变化
- 配置影响行为
- 模板可以调整
</when>

<example>
```xml
<objective>
Generate reports with customizable format and sections.
</objective>

<report_template>
Use this template and customize as needed:

```python
def generate_report(data, format="markdown", include_charts=True):
    # Process data
    # Generate output in specified format
    # Optionally include visualizations
```
</report_template>

<success_criteria>
- Report includes all required sections
- Format matches user preference
- Data accurately represented
</success_criteria>
```

Claude 可以根据要求自定义模板。
</example>
</medium_freedom>

<low_freedom>
<when>
- 操作脆弱且容易出错
- 一致性至关重要
- 必须遵循特定顺序
- 偏差导致失败
</when>

<example>
```xml
<objective>
Run database migration with exact sequence to prevent data loss.
</objective>

<workflow>
Run exactly this script:

```bash
python scripts/migrate.py --verify --backup
```

**Do not modify the command or add additional flags.**
</workflow>

<success_criteria>
- Migration completes without errors
- Backup created before migration
- Verification confirms data integrity
</success_criteria>
```

Claude 必须完全按照命令执行，不能有任何变化。
</example>
</low_freedom>

<matching_specificity>
关键是将具体性与脆弱性相匹配：

- **脆弱操作**（数据库迁移、支付处理、安全）：低自由度，精确指令
- **标准操作**（API 调用、文件处理、数据转换）：中等自由度，具有灵活性的首选模式
- **创造性操作**（代码审查、内容生成、分析）：高自由度，启发式和原则

不匹配的具体性会导致问题：
- 脆弱任务上的太多自由 → 错误和失败
- 创造性任务上的太少自由 → 僵化、次优输出
</matching_specificity>
</degrees_of_freedom_principle>

<model_testing_principle>
<description>
Skills 作为模型的补充，因此有效性取决于底层模型。适用于 Opus 的可能需要为 Haiku 提供更多细节。
</description>

<testing_across_models>
使用你计划使用的所有模型测试你的 skill：

<haiku_testing>
**Claude Haiku**（快速、经济）

要问的问题：
- Skill 是否提供足够的指导？
- 示例是否清晰完整？
- 隐含假设是否变得明确？
- Haiku 是否需要更多结构？

Haiku 受益于：
- 更明确的指令
- 完整的示例（没有部分代码）
- 明确的成功标准
- 逐步工作流程
</haiku_testing>

<sonnet_testing>
**Claude Sonnet**（平衡）

要问的问题：
- Skill 是否清晰高效？
- 是否避免过度解释？
- 工作流程是否结构良好？
- 渐进式披露是否有效？

Sonnet 受益于：
- 平衡的细节级别
- 用于清晰度的 XML 结构
- 渐进式披露
- 简洁但完整的指导
</sonnet_testing>

<opus_testing>
**Claude Opus**（强大推理）

要问的问题：
- Skill 是否避免过度解释？
- Opus 能否推断明显的步骤？
- 约束是否明确？
- 上下文是否最少但足够？

Opus 受益于：
- 简洁的指令
- 原则优于程序
- 高度自由
- 信任推理能力
</opus_testing>
</testing_across_models>

<balancing_across_models>
目标是跨所有目标模型都能良好工作的指令：

**良好的平衡**:
```xml
<quick_start>
Use pdfplumber for text extraction:

```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

For scanned PDFs requiring OCR, use pdf2image with pytesseract instead.
</quick_start>
```

这适用于所有模型：
- Haiku 获得完整的工作示例
- Sonnet 获得带有备选方案的清晰默认值
- Opus 获得足够的上下文而不过度解释

**对 Haiku 来说太简单**:
```xml
<quick_start>
Use pdfplumber for text extraction.
</quick_start>
```

**对 Opus 来说太冗长**:
```xml
<quick_start>
PDF files are documents that contain text. To extract that text, we use a library called pdfplumber. First, import the library at the top of your Python file. Then, open the PDF file using the pdfplumber.open() method. This returns a PDF object. Access the pages attribute to get a list of pages. Each page has an extract_text() method that returns the text content...
</quick_start>
```
</balancing_across_models>

<iterative_improvement>
1. 从中等细节级别开始
2. 使用目标模型测试
3. 观察模型在哪里挣扎或成功
4. 根据实际性能调整
5. 重新测试并迭代

不要为一个模型优化。找到适用于目标模型的平衡。
</iterative_improvement>
</model_testing_principle>

<progressive_disclosure_principle>
<description>
SKILL.md 作为概述。参考文件包含详细信息。Claude 仅在需要时加载参考文件。
</description>

<token_efficiency>
渐进式披露使 token 使用与任务复杂性成比例：

- 简单任务：仅加载 SKILL.md（~500 tokens）
- 中等任务：加载 SKILL.md + 一个参考（~1000 tokens）
- 复杂任务：加载 SKILL.md + 多个参考（~2000 tokens）

没有渐进式披露，每个任务都会加载所有内容，无论是否需要。
</token_efficiency>

<implementation>
- 保持 SKILL.md 在 500 行以下
- 将详细内容拆分为参考文件
- 保持参考文件从 SKILL.md 深度为一级
- 从相关部分链接到参考
- 使用描述性的参考文件名

查看 [skill-structure.md](skill-structure.md) 了解渐进式披露模式。
</implementation>
</progressive_disclosure_principle>

<validation_principle>
<description>
验证脚本是力量倍增器。它们捕获 Claude 可能遗漏的错误并提供可操作的反馈。
</description>

<characteristics>
好的验证脚本：
- 提供详细、具体的错误消息
- 当某些内容无效时显示可用的有效选项
- 精确定位问题的确切位置
- 建议可操作的修复
- 是确定性和可靠的

查看 [workflows-and-validation.md](workflows-and-validation.md) 了解验证模式。
</characteristics>
</validation_principle>

<principle_summary>
<xml_structure>
使用纯 XML 结构以实现一致性、可解析性和 Claude 性能。必需标签：objective、quick_start、success_criteria。
</xml_structure>

<conciseness>
只添加 Claude 没有的上下文。假设 Claude 很聪明。质疑每条内容。
</conciseness>

<degrees_of_freedom>
将具体性与脆弱性相匹配。创造性任务高自由度，脆弱操作低自由度，标准工作中等。
</degrees_of_freedom>

<model_testing>
使用所有目标模型测试。平衡细节级别以跨 Haiku、Sonnet 和 Opus 工作。
</model_testing>

<progressive_disclosure>
保持 SKILL.md 简洁。将详细信息拆分为参考文件。仅在需要时加载参考文件。
</progressive_disclosure>

<validation>
使验证脚本详细且具体。通过可操作的反馈尽早捕获错误。
</validation>
</principle_summary>
