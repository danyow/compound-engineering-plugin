# Skill 编写最佳实践

来源：[platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

## 核心原则

### 简洁是关键

上下文窗口是公共资源。你的 Skill 与 Claude 需要知道的其他所有内容共享上下文窗口。

**默认假设**：Claude 已经非常聪明。只添加 Claude 还没有的上下文。

质疑每条信息：
- "Claude 真的需要这个解释吗？"
- "我能假设 Claude 知道这个吗？"
- "这段文字值得它的 token 成本吗？"

**好的示例（简洁，约 50 tokens）：**
```markdown
## 提取 PDF 文本

使用 pdfplumber 进行文本提取：

```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
```

**错误示例（过于冗长，约 150 tokens）：**
```markdown
## 提取 PDF 文本

PDF（便携式文档格式）文件是一种常见的文件格式，包含
文本、图像和其他内容。要从 PDF 中提取文本，你需要
使用一个库。有很多库可用...
```

### 设置适当的自由度

将具体程度与任务脆弱性和可变性相匹配。

**高自由度**（多种有效方法）：
```markdown
## 代码审查流程

1. 分析代码结构和组织
2. 检查潜在的 bug 或边缘情况
3. 建议提高可读性的改进
4. 验证是否遵守项目约定
```

**中等自由度**（首选模式，有变化空间）：
```markdown
## 生成报告

使用此模板并根据需要自定义：

```python
def generate_report(data, format="markdown"):
    # 处理数据
    # 以指定格式生成输出
```
```

**低自由度**（脆弱，需要精确顺序）：
```markdown
## 数据库迁移

精确运行此脚本：

```bash
python scripts/migrate.py --verify --backup
```

不要修改命令或添加标志。
```

### 使用所有模型测试

Skill 作为模型的补充。使用 Haiku、Sonnet 和 Opus 测试。

- **Haiku**：Skill 是否提供了足够的指导？
- **Sonnet**：Skill 是否清晰且高效？
- **Opus**：Skill 是否避免了过度解释？

## 命名约定

使用**动名词形式**（动词 + -ing）命名 Skill：

**好的：**
- `processing-pdfs`
- `analyzing-spreadsheets`
- `managing-databases`
- `testing-code`
- `writing-documentation`

**可接受的替代：**
- 名词短语：`pdf-processing`、`spreadsheet-analysis`
- 面向操作：`process-pdfs`、`analyze-spreadsheets`

**避免：**
- 模糊的：`helper`、`utils`、`tools`
- 通用的：`documents`、`data`、`files`
- 保留的：`anthropic-*`、`claude-*`

## 编写有效的描述

**始终使用第三人称。** 描述会被注入到系统提示中。

**要具体并包含关键术语：**

```yaml
# PDF Processing skill
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.

# Excel Analysis skill
description: Analyze Excel spreadsheets, create pivot tables, generate charts. Use when analyzing Excel files, spreadsheets, tabular data, or .xlsx files.

# Git Commit Helper skill
description: Generate descriptive commit messages by analyzing git diffs. Use when the user asks for help writing commit messages or reviewing staged changes.
```

**避免模糊的描述：**
```yaml
description: Helps with documents  # 太模糊！
description: Processes data       # 太通用！
description: Does stuff with files # 无用！
```

## 渐进式披露模式

### 模式 1：高层指南与参考

```markdown
---
name: pdf-processing
description: Extracts text and tables from PDF files, fills forms, merges documents.
---

# PDF Processing

## 快速开始

```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

## 高级功能

**表单填充**：参见 [FORMS.md](FORMS.md)
**API 参考**：参见 [REFERENCE.md](REFERENCE.md)
**示例**：参见 [EXAMPLES.md](EXAMPLES.md)
```

### 模式 2：特定领域组织

```
bigquery-skill/
├── SKILL.md（概述和导航）
└── reference/
    ├── finance.md（收入、账单）
    ├── sales.md（机会、渠道）
    ├── product.md（API 使用、功能）
    └── marketing.md（活动、归因）
```

### 模式 3：条件详细信息

```markdown
# DOCX 处理

## 创建文档

使用 docx-js 创建新文档。参见 [DOCX-JS.md](DOCX-JS.md)。

## 编辑文档

对于简单的编辑，直接修改 XML。

**对于跟踪更改**：参见 [REDLINING.md](REDLINING.md)
**对于 OOXML 详情**：参见 [OOXML.md](OOXML.md)
```

## 保持参考深度为一级

Claude 可能只会部分读取从其他参考文件引用的文件。

**错误（过深）：**
```markdown
# SKILL.md
参见 [advanced.md](advanced.md)...

# advanced.md
参见 [details.md](details.md)...

# details.md
这是实际信息...
```

**正确（一级深度）：**
```markdown
# SKILL.md

**基本用法**：[在 SKILL.md 中]
**高级功能**：参见 [advanced.md](advanced.md)
**API 参考**：参见 [reference.md](reference.md)
**示例**：参见 [examples.md](examples.md)
```

## 工作流和反馈循环

### 带清单的工作流

```markdown
## 研究综合工作流

复制此清单：

```
- [ ] 步骤 1：阅读所有源文档
- [ ] 步骤 2：识别关键主题
- [ ] 步骤 3：交叉引用声明
- [ ] 步骤 4：创建结构化摘要
- [ ] 步骤 5：验证引用
```

**步骤 1：阅读所有源文档**

查看 `sources/` 中的每个文档。注意主要论点。
...
```

### 反馈循环模式

```markdown
## 文档编辑流程

1. 对 `word/document.xml` 进行编辑
2. **立即验证**：`python scripts/validate.py unpacked_dir/`
3. 如果验证失败：
   - 查看错误消息
   - 修复问题
   - 再次运行验证
4. **仅在验证通过后继续**
5. 重新构建：`python scripts/pack.py unpacked_dir/ output.docx`
```

## 常见模式

### 模板模式

```markdown
## 报告结构

使用此模板：

```markdown
# [分析标题]

## 执行摘要
[一段式概述]

## 关键发现
- 发现 1 及支持数据
- 发现 2 及支持数据

## 建议
1. 具体可操作的建议
2. 具体可操作的建议
```
```

### 示例模式

```markdown
## 提交消息格式

**示例 1：**
输入：Added user authentication with JWT tokens
输出：
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```

**示例 2：**
输入：Fixed bug where dates displayed incorrectly
输出：
```
fix(reports): correct date formatting in timezone conversion
```
```

### 条件工作流模式

```markdown
## 文档修改

1. 确定修改类型：

   **创建新内容？** → 遵循"创建工作流"
   **编辑现有内容？** → 遵循"编辑工作流"

2. 创建工作流：
   - 使用 docx-js 库
   - 从头构建文档

3. 编辑工作流：
   - 解包现有文档
   - 直接修改 XML
   - 每次更改后验证
```

## 内容指南

### 避免时间敏感信息

**错误：**
```markdown
如果你在 2025 年 8 月之前执行此操作，请使用旧 API。
```

**正确：**
```markdown
## 当前方法

使用 v2 API 端点：`api.example.com/v2/messages`

## 旧模式

<details>
<summary>旧版 v1 API（2025-08 已弃用）</summary>
v1 API 使用：`api.example.com/v1/messages`
</details>
```

### 使用一致的术语

**正确 - 一致：**
- 始终"API endpoint"
- 始终"field"
- 始终"extract"

**错误 - 不一致：**
- 混用"API endpoint"、"URL"、"API route"、"path"
- 混用"field"、"box"、"element"、"control"

## 应避免的反模式

### Windows 风格路径

- **正确**：`scripts/helper.py`、`reference/guide.md`
- **避免**：`scripts\helper.py`、`reference\guide.md`

### 太多选项

**错误：**
```markdown
你可以使用 pypdf、pdfplumber、PyMuPDF、pdf2image 或...
```

**正确：**
```markdown
使用 pdfplumber 进行文本提取：
```python
import pdfplumber
```

对于需要 OCR 的扫描 PDF，改用 pdf2image 和 pytesseract。
```

## 有效 Skill 的检查清单

### 核心质量
- [ ] 描述具体且包含关键术语
- [ ] 描述包含是什么和何时使用
- [ ] SKILL.md 主体少于 500 行
- [ ] 额外详细信息在单独的文件中
- [ ] 无时间敏感信息
- [ ] 术语一致
- [ ] 示例具体
- [ ] 参考深度为一级
- [ ] 适当使用渐进式披露
- [ ] 工作流有清晰的步骤

### 代码和脚本
- [ ] 脚本明确处理错误
- [ ] 无"魔法常数"（所有值都有理由）
- [ ] 列出所需的包
- [ ] 脚本有清晰的文档
- [ ] 无 Windows 风格路径
- [ ] 关键操作有验证步骤
- [ ] 质量关键任务有反馈循环

### 测试
- [ ] 至少三个测试场景
- [ ] 使用 Haiku、Sonnet 和 Opus 测试
- [ ] 使用真实使用场景测试
- [ ] 团队反馈已整合
