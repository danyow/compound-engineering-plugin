<overview>
此参考文档记录了 skill 编写的常见模式，包括模板、示例、术语一致性和反模式。所有模式使用纯 XML 结构。
</overview>

<template_pattern>
<description>
为输出格式提供模板。根据需求匹配严格程度。
</description>

<strict_requirements>
当输出格式必须精确且一致时使用：

```xml
<report_structure>
始终使用这个精确的模板结构：

```markdown
# [分析标题]

## 执行摘要
[关键发现的一段式概述]

## 关键发现
- 发现 1 及支持数据
- 发现 2 及支持数据
- 发现 3 及支持数据

## 建议
1. 具体可操作的建议
2. 具体可操作的建议
```
</report_structure>
```

**何时使用**：合规报告、标准化格式、自动化处理
</strict_requirements>

<flexible_guidance>
当 Claude 应根据上下文调整格式时使用：

```xml
<report_structure>
这是一个合理的默认格式，但请使用你的最佳判断：

```markdown
# [分析标题]

## 执行摘要
[概述]

## 关键发现
[根据你的发现调整章节]

## 建议
[针对特定上下文定制]
```

根据具体分析类型的需要调整章节。
</report_structure>
```

**何时使用**：探索性分析、依赖上下文的格式、创意任务
</flexible_guidance>
</template_pattern>

<examples_pattern>
<description>
对于输出质量取决于查看示例的 skill，提供输入/输出对。
</description>

<commit_messages_example>
```xml
<objective>
生成遵循约定式提交格式的提交消息。
</objective>

<commit_message_format>
按照以下示例生成提交消息：

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

遵循此风格：type(scope): 简短描述，然后详细解释。
</commit_message_format>
```
</commit_messages_example>

<when_to_use>
- 输出格式有文本解释无法捕捉的细微差别
- 模式识别比规则遵循更容易
- 示例展示边缘情况
- 多样本学习提高质量
</when_to_use>
</examples_pattern>

<consistent_terminology>
<principle>
选择一个术语并在整个 skill 中使用。不一致的术语会让 Claude 困惑并降低执行质量。
</principle>

<good_example>
一致的用法：
- 始终"API endpoint"（不与"URL"、"API route"、"path"混用）
- 始终"field"（不与"box"、"element"、"control"混用）
- 始终"extract"（不与"pull"、"get"、"retrieve"混用）

```xml
<objective>
使用字段映射从 API endpoint 提取数据。
</objective>

<quick_start>
1. 识别 API endpoint
2. 将响应字段映射到你的模式
3. 提取字段值
</quick_start>
```
</good_example>

<bad_example>
不一致的用法会造成混淆：

```xml
<objective>
从 API route 拉取数据使用元素映射。
</objective>

<quick_start>
1. 识别 URL
2. 将响应框映射到你的模式
3. 检索控件值
</quick_start>
```

Claude 现在必须解释："API route"和"URL"是否相同？"field"、"box"、"element"和"control"是否相同？
</bad_example>

<implementation>
1. 在 skill 开发早期选择术语
2. 在 `<objective>` 或 `<context>` 中记录关键术语
3. 使用查找/替换强制一致性
4. 检查参考文件的一致使用
</implementation>
</consistent_terminology>

<provide_default_with_escape_hatch>
<principle>
提供带有特殊情况逃生通道的默认方法，而不是备选方案列表。太多选项会导致决策瘫痪。
</principle>

<good_example>
清晰的默认和逃生通道：

```xml
<quick_start>
使用 pdfplumber 进行文本提取：

```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

对于需要 OCR 的扫描 PDF，改用 pdf2image 和 pytesseract。
</quick_start>
```
</good_example>

<bad_example>
太多选项导致决策瘫痪：

```xml
<quick_start>
你可以使用以下任何库：

- **pypdf**：适合基本提取
- **pdfplumber**：更适合表格
- **PyMuPDF**：更快但更复杂
- **pdf2image**：用于扫描文档
- **pdfminer**：低级控制
- **tabula-py**：专注表格

根据你的需求选择。
</quick_start>
```

Claude 现在必须在开始之前研究和比较所有选项。这浪费了 token 和时间。
</bad_example>

<implementation>
1. 推荐一个默认方法
2. 解释何时使用默认方法（暗示：大多数时候）
3. 为边缘情况添加一个逃生通道
4. 如果确实需要多个备选方案，链接到高级参考
</implementation>
</provide_default_with_escape_hatch>

<anti_patterns>
<description>
编写 skill 时要避免的常见错误。
</description>

<pitfall name="markdown_headings_in_body">
❌ **错误**：在 skill 主体中使用 markdown 标题：

```markdown
# PDF Processing

## Quick start
Extract text with pdfplumber...

## Advanced features
Form filling requires additional setup...
```

✅ **正确**：使用纯 XML 结构：

```xml
<objective>
PDF processing with text extraction, form filling, and merging capabilities.
</objective>

<quick_start>
Extract text with pdfplumber...
</quick_start>

<advanced_features>
Form filling requires additional setup...
</advanced_features>
```

**为什么重要**：XML 提供语义含义、可靠解析和 token 效率。
</pitfall>

<pitfall name="vague_descriptions">
❌ **错误**：
```yaml
description: Helps with documents
```

✅ **正确**：
```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

**为什么重要**：模糊的描述会阻止 Claude 正确发现和使用 skill。
</pitfall>

<pitfall name="inconsistent_pov">
❌ **错误**：
```yaml
description: I can help you process Excel files
```

✅ **正确**：
```yaml
description: Processes Excel files and generates reports. Use when analyzing spreadsheets or .xlsx files.
```

**为什么重要**：Skill 必须使用第三人称。第一/第二人称会破坏 skill 元数据模式。
</pitfall>

<pitfall name="wrong_naming_convention">
❌ **错误**：目录名与 skill 名不匹配或不符合动词-名词约定：
- 目录：`facebook-ads`，名称：`facebook-ads-manager`
- 目录：`stripe-integration`，名称：`stripe`
- 目录：`helper-scripts`，名称：`helper`

✅ **正确**：一致的动词-名词约定：
- 目录：`manage-facebook-ads`，名称：`manage-facebook-ads`
- 目录：`setup-stripe-payments`，名称：`setup-stripe-payments`
- 目录：`process-pdfs`，名称：`process-pdfs`

**为什么重要**：命名的一致性使 skill 可发现且可预测。
</pitfall>

<pitfall name="too_many_options">
❌ **错误**：
```xml
<quick_start>
你可以使用 pypdf、pdfplumber、PyMuPDF、pdf2image、pdfminer 或 tabula-py...
</quick_start>
```

✅ **正确**：
```xml
<quick_start>
使用 pdfplumber 进行文本提取：

```python
import pdfplumber
```

对于需要 OCR 的扫描 PDF，改用 pdf2image 和 pytesseract。
</quick_start>
```

**为什么重要**：决策瘫痪。提供一个默认方法和特殊情况的逃生通道。
</pitfall>

<pitfall name="deeply_nested_references">
❌ **错误**：嵌套多层的参考：
```
SKILL.md → advanced.md → details.md → examples.md
```

✅ **正确**：从 SKILL.md 一级深度的参考：
```
SKILL.md → advanced.md
SKILL.md → details.md
SKILL.md → examples.md
```

**为什么重要**：Claude 可能只会部分读取深度嵌套的文件。保持从 SKILL.md 一级深度的参考。
</pitfall>

<pitfall name="windows_paths">
❌ **错误**：
```xml
<reference_guides>
参见 scripts\validate.py 进行验证
</reference_guides>
```

✅ **正确**：
```xml
<reference_guides>
参见 scripts/validate.py 进行验证
</reference_guides>
```

**为什么重要**：始终使用正斜杠以实现跨平台兼容性。
</pitfall>

<pitfall name="dynamic_context_and_file_reference_execution">
**问题**：当显示动态上下文语法（感叹号 + 反引号）或文件引用（@ 前缀）的示例时，skill 加载器会在 skill 加载期间执行这些。

❌ **错误** - 这些会在 skill 加载时执行：
```xml
<examples>
使用以下方式加载当前状态：!`git status`
在以下位置查看依赖项：@package.json
</examples>
```

✅ **正确** - 添加空格以防止执行：
```xml
<examples>
使用以下方式加载当前状态：! `git status`（实际使用时删除反引号前的空格）
在以下位置查看依赖项：@ package.json（实际使用时删除 @ 后的空格）
</examples>
```

**何时适用**：
- 教用户动态上下文的 skill（slash command、提示）
- 显示感叹号前缀语法或 @ 文件引用的任何文档
- 具有示例命令或不应在加载期间执行的文件路径的 skill

**为什么重要**：没有空格，这些会在 skill 加载期间执行，导致错误或不需要的文件读取。
</pitfall>

<pitfall name="missing_required_tags">
❌ **错误**：缺少必需标签：
```xml
<quick_start>
使用此工具进行处理...
</quick_start>
```

✅ **正确**：所有必需标签都存在：
```xml
<objective>
使用验证和转换处理数据文件。
</objective>

<quick_start>
使用此工具进行处理...
</quick_start>

<success_criteria>
- 输入文件成功处理
- 输出文件无错误验证
- 转换正确应用
</success_criteria>
```

**为什么重要**：每个 skill 必须有 `<objective>`、`<quick_start>` 和 `<success_criteria>`（或 `<when_successful>`）。
</pitfall>

<pitfall name="hybrid_xml_markdown">
❌ **错误**：混合 XML 标签和 markdown 标题：
```markdown
<objective>
PDF processing capabilities
</objective>

## Quick start

Extract text with pdfplumber...

## Advanced features

Form filling...
```

✅ **正确**：全程使用纯 XML：
```xml
<objective>
PDF processing capabilities
</objective>

<quick_start>
Extract text with pdfplumber...
</quick_start>

<advanced_features>
Form filling...
</advanced_features>
```

**为什么重要**：结构的一致性。要么使用纯 XML，要么使用纯 markdown（首选 XML）。
</pitfall>

<pitfall name="unclosed_xml_tags">
❌ **错误**：忘记关闭 XML 标签：
```xml
<objective>
Process PDF files

<quick_start>
Use pdfplumber...
</quick_start>
```

✅ **正确**：正确关闭标签：
```xml
<objective>
Process PDF files
</objective>

<quick_start>
Use pdfplumber...
</quick_start>
```

**为什么重要**：未关闭的标签会破坏 XML 解析并创建模糊的边界。
</pitfall>
</anti_patterns>

<progressive_disclosure_pattern>
<description>
通过链接到详细的参考文件来保持 SKILL.md 简洁。Claude 只在需要时加载参考文件。
</description>

<implementation>
```xml
<objective>
通过 Marketing API 管理 Facebook Ads 活动、广告集和广告。
</objective>

<quick_start>
<basic_operations>
参见 [basic-operations.md](basic-operations.md) 了解活动创建和管理。
</basic_operations>
</quick_start>

<advanced_features>
**自定义受众**：参见 [audiences.md](audiences.md)
**转化跟踪**：参见 [conversions.md](conversions.md)
**预算优化**：参见 [budgets.md](budgets.md)
**API 参考**：参见 [api-reference.md](api-reference.md)
</advanced_features>
```

**优势**：
- SKILL.md 保持在 500 行以下
- Claude 只读取相关的参考文件
- Token 使用与任务复杂度成比例
- 更易于维护和更新
</implementation>
</progressive_disclosure_pattern>

<validation_pattern>
<description>
对于具有验证步骤的 skill，使验证脚本详细且具体。
</description>

<implementation>
```xml
<validation>
进行更改后，立即验证：

```bash
python scripts/validate.py output_dir/
```

如果验证失败，请在继续之前修复错误。验证错误包括：

- **未找到字段**："未找到字段 'signature_date'。可用字段：customer_name、order_total、signature_date_signed"
- **类型不匹配**："字段 'order_total' 期望数字，获得字符串"
- **缺少必需字段**："缺少必需字段 'customer_name'"

仅在验证通过且无错误时继续。
</validation>
```

**为什么详细的错误有帮助**：
- Claude 可以修复问题而无需猜测
- 具体的错误消息减少迭代周期
- 错误消息中显示可用选项
</implementation>
</validation_pattern>

<checklist_pattern>
<description>
对于复杂的多步骤工作流，提供 Claude 可以复制和跟踪进度的清单。
</description>

<implementation>
```xml
<workflow>
复制此清单并在完成项目时勾选：

```
任务进度：
- [ ] 步骤 1：分析表单（运行 analyze_form.py）
- [ ] 步骤 2：创建字段映射（编辑 fields.json）
- [ ] 步骤 3：验证映射（运行 validate_fields.py）
- [ ] 步骤 4：填充表单（运行 fill_form.py）
- [ ] 步骤 5：验证输出（运行 verify_output.py）
```

<step_1>
**分析表单**

运行：`python scripts/analyze_form.py input.pdf`

这会提取表单字段及其位置，保存到 `fields.json`。
</step_1>

<step_2>
**创建字段映射**

编辑 `fields.json` 为每个字段添加值。
</step_2>

<step_3>
**验证映射**

运行：`python scripts/validate_fields.py fields.json`

在继续之前修复任何验证错误。
</step_3>

<step_4>
**填充表单**

运行：`python scripts/fill_form.py input.pdf fields.json output.pdf`
</step_4>

<step_5>
**验证输出**

运行：`python scripts/verify_output.py output.pdf`

如果验证失败，返回步骤 2。
</step_5>
</workflow>
```

**优势**：
- 清晰的进度跟踪
- 防止跳过步骤
- 中断后易于恢复
</implementation>
</checklist_pattern>
