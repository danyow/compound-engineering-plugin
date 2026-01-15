# Anthropic 官方 Skill 规范

来源：[code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills)

## SKILL.md 文件结构

每个 Skill 都需要一个包含 YAML frontmatter 和 Markdown 指令的 `SKILL.md` 文件。

### 基本格式

```markdown
---
name: your-skill-name
description: Brief description of what this Skill does and when to use it
---

# Your Skill Name

## Instructions
Provide clear, step-by-step guidance for Claude.

## Examples
Show concrete examples of using this Skill.
```

## 必需的 Frontmatter 字段

| 字段 | 必需 | 描述 |
|-------|----------|-------------|
| `name` | 是 | 仅使用小写字母、数字和连字符的 Skill 名称（最多 64 个字符）。应与目录名称匹配。 |
| `description` | 是 | Skill 的作用以及何时使用（最多 1024 个字符）。Claude 使用此来决定何时应用 Skill。 |
| `allowed-tools` | 否 | 当此 Skill 激活时 Claude 可以使用而无需请求许可的工具。示例：`Read, Grep, Glob` |
| `model` | 否 | 此 Skill 激活时要使用的特定模型（例如，`claude-sonnet-4-20250514`）。默认为对话的模型。 |

## Skill 位置和优先级

```
Enterprise（最高优先级）→ Personal → Project → Plugin（最低优先级）
```

| 类型 | 路径 | 适用于 |
|------|------|-----------|
| **Enterprise** | 参见托管设置 | 组织中的所有用户 |
| **Personal** | `~/.claude/skills/` | 你，跨所有项目 |
| **Project** | `.claude/skills/` | 在仓库中工作的任何人 |
| **Plugin** | 与 plugin 捆绑 | 安装了 plugin 的任何人 |

## Skill 如何工作

1. **发现**：Claude 在启动时只加载名称和描述
2. **激活**：当你的请求匹配 Skill 的描述时，Claude 会要求确认
3. **执行**：Claude 遵循 Skill 的指令并加载引用的文件

**关键原则**：Skill 是**模型调用的** —— Claude 根据你的请求自动决定使用哪些 Skill。

## 渐进式披露模式

通过链接到支持文件，保持 `SKILL.md` 少于 500 行：

```
my-skill/
├── SKILL.md（必需 - 概述和导航）
├── reference.md（详细的 API 文档 - 需要时加载）
├── examples.md（用法示例 - 需要时加载）
└── scripts/
    └── helper.py（实用脚本 - 执行，不加载）
```

### 带参考的示例 SKILL.md

```markdown
---
name: pdf-processing
description: Extract text, fill forms, merge PDFs. Use when working with PDF files, forms, or document extraction. Requires pypdf and pdfplumber packages.
allowed-tools: Read, Bash(python:*)
---

# PDF Processing

## 快速开始

提取文本：
```python
import pdfplumber
with pdfplumber.open("doc.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

对于表单填充，参见 [FORMS.md](FORMS.md)。
对于详细的 API 参考，参见 [REFERENCE.md](REFERENCE.md)。

## 要求

必须安装包：
```bash
pip install pypdf pdfplumber
```
```

## 限制工具访问

```yaml
---
name: reading-files-safely
description: Read files without making changes. Use when you need read-only file access.
allowed-tools: Read, Grep, Glob
---
```

优势：
- 不应修改文件的只读 Skill
- 特定任务的有限范围
- 安全敏感的工作流

## 编写有效的描述

`description` 字段启用 Skill 发现，应包括 Skill 的作用和何时使用它。

**始终使用第三人称。** 描述会被注入到系统提示中。

- **正确**："处理 Excel 文件并生成报告"
- **避免**："我可以帮你处理 Excel 文件"
- **避免**："你可以使用它处理 Excel 文件"

**要具体并包含关键术语：**

```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

**避免模糊的描述：**

```yaml
description: Helps with documents  # 太模糊！
```

## 完整示例：提交消息生成器

```markdown
---
name: generating-commit-messages
description: Generates clear commit messages from git diffs. Use when writing commit messages or reviewing staged changes.
---

# Generating Commit Messages

## 指令

1. 运行 `git diff --staged` 查看更改
2. 我会建议一个提交消息，包括：
   - 少于 50 个字符的摘要
   - 详细描述
   - 受影响的组件

## 最佳实践

- 使用现在时
- 解释是什么和为什么，而不是如何
```

## 完整示例：代码解释 Skill

```markdown
---
name: explaining-code
description: Explains code with visual diagrams and analogies. Use when explaining how code works, teaching about a codebase, or when the user asks "how does this work?"
---

# Explaining Code

解释代码时，始终包括：

1. **从类比开始**：将代码与日常生活中的东西进行比较
2. **绘制图表**：使用 ASCII 艺术显示流程、结构或关系
3. **遍历代码**：逐步解释发生了什么
4. **突出一个陷阱**：常见的误解是什么？

保持解释对话化。对于复杂的概念，使用多个类比。
```

## 分发

- **Project Skill**：将 `.claude/skills/` 提交到版本控制
- **Plugin**：将 `skills/` 目录添加到带有 Skill 文件夹的 plugin
- **Enterprise**：通过托管设置部署到整个组织
