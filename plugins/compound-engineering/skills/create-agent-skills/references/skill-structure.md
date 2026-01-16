<overview>
Skill 有三个结构组件：YAML frontmatter（元数据）、纯 XML 主体结构（内容组织）和渐进式披露（文件组织）。此参考定义了每个组件的要求和最佳实践。
</overview>

<xml_structure_requirements>
<critical_rule>
**从 skill 主体内容中删除所有 markdown 标题（#、##、###）。** 替换为语义 XML 标签。保留内容中的 markdown 格式（粗体、斜体、列表、代码块、链接）。
</critical_rule>

<required_tags>
每个 skill 必须有这三个标签：

- **`<objective>`** - Skill 的作用以及为什么重要（1-3 段）
- **`<quick_start>`** - 即时、可操作的指导（最小工作示例）
- **`<success_criteria>`** 或 **`<when_successful>`** - 如何知道它有效
</required_tags>

<conditional_tags>
根据 skill 复杂度和领域要求添加：

- **`<context>`** - 背景/情境信息
- **`<workflow>` 或 `<process>`** - 分步程序
- **`<advanced_features>`** - 深入主题（渐进式披露）
- **`<validation>`** - 如何验证输出
- **`<examples>`** - 多样本学习
- **`<anti_patterns>`** - 要避免的常见错误
- **`<security_checklist>`** - 不可协商的安全模式
- **`<testing>`** - 测试工作流
- **`<common_patterns>`** - 代码示例和配方
- **`<reference_guides>` 或 `<detailed_references>`** - 到参考文件的链接

参见 [use-xml-tags.md](use-xml-tags.md) 了解每个标签的详细指导。
</conditional_tags>

<tag_selection_intelligence>
**简单的 skill**（单一领域，直接了当）：
- 仅必需标签
- 示例：文本提取、文件格式转换

**中等 skill**（多个模式，一些复杂性）：
- 必需标签 + 根据需要添加工作流/示例
- 示例：具有步骤的文档处理、API 集成

**复杂的 skill**（多个领域、安全、API）：
- 必需标签 + 适当的条件标签
- 示例：支付处理、认证系统、多步骤工作流
</tag_selection_intelligence>

<xml_nesting>
为分层内容正确嵌套 XML 标签：

```xml
<examples>
<example number="1">
<input>User input</input>
<output>Expected output</output>
</example>
</examples>
```

始终关闭标签：
```xml
<objective>
Content here
</objective>
```
</xml_nesting>

<tag_naming_conventions>
使用描述性、语义的名称：
- `<workflow>` 而不是 `<steps>`
- `<success_criteria>` 而不是 `<done>`
- `<anti_patterns>` 而不是 `<dont_do>`

在你的 skill 中保持一致。如果你使用 `<workflow>`，不要也为相同目的使用 `<process>`（除非它们服务于不同的角色）。
</tag_naming_conventions>
</xml_structure_requirements>

<yaml_requirements>
<required_fields>
```yaml
---
name: skill-name-here
description: What it does and when to use it (third person, specific triggers)
---
```
</required_fields>

<name_field>
**验证规则**：
- 最多 64 个字符
- 仅小写字母、数字、连字符
- 无 XML 标签
- 无保留词："anthropic"、"claude"
- 必须与目录名称完全匹配

**示例**：
- ✅ `process-pdfs`
- ✅ `manage-facebook-ads`
- ✅ `setup-stripe-payments`
- ❌ `PDF_Processor`（大写）
- ❌ `helper`（模糊）
- ❌ `claude-helper`（保留词）
</name_field>

<description_field>
**验证规则**：
- 非空，最多 1024 个字符
- 无 XML 标签
- 第三人称（永不第一或第二人称）
- 包括它的作用和何时使用

**关键规则**：始终使用第三人称。
- ✅ "处理 Excel 文件并生成报告"
- ❌ "我可以帮你处理 Excel 文件"
- ❌ "你可以使用它处理 Excel 文件"

**结构**：包括能力和触发器。

**有效示例**：
```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

```yaml
description: Analyze Excel spreadsheets, create pivot tables, generate charts. Use when analyzing Excel files, spreadsheets, tabular data, or .xlsx files.
```

```yaml
description: Generate descriptive commit messages by analyzing git diffs. Use when the user asks for help writing commit messages or reviewing staged changes.
```

**避免**：
```yaml
description: Helps with documents
```

```yaml
description: Processes data
```
</description_field>
</yaml_requirements>

<naming_conventions>
使用 **动词-名词约定** 命名 skill：

<pattern name="create">
构建/编写工具

示例：`create-agent-skills`、`create-hooks`、`create-landing-pages`
</pattern>

<pattern name="manage">
管理外部服务或资源

示例：`manage-facebook-ads`、`manage-zoom`、`manage-stripe`、`manage-supabase`
</pattern>

<pattern name="setup">
配置/集成任务

示例：`setup-stripe-payments`、`setup-meta-tracking`
</pattern>

<pattern name="generate">
生成任务

示例：`generate-ai-images`
</pattern>

<avoid_patterns>
- 模糊：`helper`、`utils`、`tools`
- 通用：`documents`、`data`、`files`
- 保留词：`anthropic-helper`、`claude-tools`
- 不一致：目录 `facebook-ads` 但名称 `facebook-ads-manager`
</avoid_patterns>
</naming_conventions>

<progressive_disclosure>
<principle>
SKILL.md 作为概述，根据需要指向详细材料。这使上下文窗口使用效率高。
</principle>

<practical_guidance>
- 保持 SKILL.md 主体少于 500 行
- 接近此限制时将内容拆分为单独的文件
- 从 SKILL.md 保持参考一级深度
- 为超过 100 行的参考文件添加目录
</practical_guidance>

<pattern name="high_level_guide">
SKILL.md 中的快速开始，参考文件中的详细信息：

```markdown
---
name: pdf-processing
description: Extracts text and tables from PDF files, fills forms, and merges documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
---

<objective>
使用 Python 库从 PDF 文件中提取文本和表格、填充表单和合并文档。
</objective>

<quick_start>
使用 pdfplumber 提取文本：

```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
</quick_start>

<advanced_features>
**表单填充**：参见 [forms.md](forms.md)
**API 参考**：参见 [reference.md](reference.md)
</advanced_features>
```

Claude 仅在需要时加载 forms.md 或 reference.md。
</pattern>

<pattern name="domain_organization">
对于具有多个领域的 skill，按领域组织以避免加载不相关的上下文：

```
bigquery-skill/
├── SKILL.md（概述和导航）
└── reference/
    ├── finance.md（收入、账单指标）
    ├── sales.md（机会、渠道）
    ├── product.md（API 使用、功能）
    └── marketing.md（活动、归因）
```

当用户询问收入时，Claude 只读取 finance.md。其他文件保留在文件系统上，消耗零 token。
</pattern>

<pattern name="conditional_details">
在 SKILL.md 中显示基本内容，链接到参考文件中的高级内容：

```xml
<objective>
使用创建和编辑功能处理 DOCX 文件。
</objective>

<quick_start>
<creating_documents>
使用 docx-js 创建新文档。参见 [docx-js.md](docx-js.md)。
</creating_documents>

<editing_documents>
对于简单的编辑，直接修改 XML。

**对于跟踪更改**：参见 [redlining.md](redlining.md)
**对于 OOXML 详情**：参见 [ooxml.md](ooxml.md)
</editing_documents>
</quick_start>
```

Claude 仅在用户需要这些功能时读取 redlining.md 或 ooxml.md。
</pattern>

<critical_rules>
**保持参考一级深度**：所有参考文件应直接从 SKILL.md 链接。避免嵌套参考（SKILL.md → advanced.md → details.md），因为 Claude 可能只会部分读取深度嵌套的文件。

**为长文件添加目录**：对于超过 100 行的参考文件，在顶部包含目录。

**在参考文件中使用纯 XML**：参考文件也应使用纯 XML 结构（主体中没有 markdown 标题）。
</critical_rules>
</progressive_disclosure>

<file_organization>
<filesystem_navigation>
Claude 使用 bash 命令导航你的 skill 目录：

- 使用正斜杠：`reference/guide.md`（不是 `reference\guide.md`）
- 描述性地命名文件：`form_validation_rules.md`（不是 `doc2.md`）
- 按领域组织：`reference/finance.md`、`reference/sales.md`
</filesystem_navigation>

<directory_structure>
典型的 skill 结构：

```
skill-name/
├── SKILL.md（主入口点，纯 XML 结构）
├── references/（可选，用于渐进式披露）
│   ├── guide-1.md（纯 XML 结构）
│   ├── guide-2.md（纯 XML 结构）
│   └── examples.md（纯 XML 结构）
└── scripts/（可选，用于实用脚本）
    ├── validate.py
    └── process.py
```
</directory_structure>
</file_organization>

<anti_patterns>
<pitfall name="markdown_headings_in_body">
❌ 不要在 skill 主体中使用 markdown 标题：

```markdown
# PDF Processing

## Quick start
Extract text...

## Advanced features
Form filling...
```

✅ 使用纯 XML 结构：

```xml
<objective>
PDF processing with text extraction, form filling, and merging.
</objective>

<quick_start>
Extract text...
</quick_start>

<advanced_features>
Form filling...
</advanced_features>
```
</pitfall>

<pitfall name="vague_descriptions">
- ❌ "Helps with documents"
- ✅ "Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction."
</pitfall>

<pitfall name="inconsistent_pov">
- ❌ "I can help you process Excel files"
- ✅ "Processes Excel files and generates reports"
</pitfall>

<pitfall name="wrong_naming_convention">
- ❌ 目录：`facebook-ads`，名称：`facebook-ads-manager`
- ✅ 目录：`manage-facebook-ads`，名称：`manage-facebook-ads`
- ❌ 目录：`stripe-integration`，名称：`stripe`
- ✅ 目录：`setup-stripe-payments`，名称：`setup-stripe-payments`
</pitfall>

<pitfall name="deeply_nested_references">
从 SKILL.md 保持参考一级深度。Claude 可能只会部分读取嵌套文件（SKILL.md → advanced.md → details.md）。
</pitfall>

<pitfall name="windows_paths">
始终使用正斜杠：`scripts/helper.py`（不是 `scripts\helper.py`）
</pitfall>

<pitfall name="missing_required_tags">
每个 skill 必须有：`<objective>`、`<quick_start>` 和 `<success_criteria>`（或 `<when_successful>`）。
</pitfall>
</anti_patterns>

<validation_checklist>
完成 skill 前，验证：

- ✅ YAML frontmatter 有效（名称与目录匹配，描述使用第三人称）
- ✅ 主体中没有 markdown 标题（纯 XML 结构）
- ✅ 必需标签存在：objective、quick_start、success_criteria
- ✅ 条件标签适合复杂度级别
- ✅ 所有 XML 标签正确关闭
- ✅ 应用渐进式披露（SKILL.md < 500 行）
- ✅ 参考文件使用纯 XML 结构
- ✅ 文件路径使用正斜杠
- ✅ 描述性文件名
</validation_checklist>
