---
name: creating-agent-skills
description: 创建、编写和优化 Claude Code Skills 的专家指导。在处理 SKILL.md 文件、编写新技能、改进现有技能或理解技能结构和最佳实践时使用。
---

# 创建 Agent Skills

此技能教你如何按照 Anthropic 官方规范创建有效的 Claude Code Skills。

## 核心原则

### 1. Skills 就是提示词

所有提示词最佳实践都适用。要清晰、直接。假设 Claude 很聪明 - 只添加 Claude 没有的上下文。

### 2. 标准 Markdown 格式

使用 YAML frontmatter + markdown 正文。**不使用 XML 标签** - 使用标准 markdown 标题。

```markdown
---
name: my-skill-name
description: 它做什么以及何时使用
---

# My Skill Name

## Quick Start
立即可行的指导...

## Instructions
分步骤过程...

## Examples
具体的使用示例...
```

### 3. 渐进式披露

保持 SKILL.md 在 500 行以内。将详细内容拆分到参考文件中。仅加载需要的内容。

```
my-skill/
├── SKILL.md              # 入口点（必需）
├── reference.md          # 详细文档（需要时加载）
├── examples.md           # 使用示例
└── scripts/              # 实用脚本（执行，不加载）
```

### 4. 有效的描述

描述字段能够启用技能发现。包括技能做什么以及何时使用。使用第三人称。

**好的示例：**
```yaml
description: 从 PDF 文件中提取文本和表格，填写表单，合并文档。在处理 PDF 文件或用户提到 PDF、表单或文档提取时使用。
```

**不好的示例：**
```yaml
description: 帮助处理文档
```

## 技能结构

### 必需的 Frontmatter

| 字段 | 必需 | 最大长度 | 描述 |
|-------|----------|------------|-------------|
| `name` | 是 | 64 字符 | 仅小写字母、数字、连字符 |
| `description` | 是 | 1024 字符 | 它做什么以及何时使用 |
| `allowed-tools` | 否 | - | Claude 可以无需询问使用的工具 |
| `model` | 否 | - | 要使用的特定模型 |

### 命名约定

使用**动名词形式**（动词 + -ing）作为技能名称：

- `processing-pdfs`
- `analyzing-spreadsheets`
- `generating-commit-messages`
- `reviewing-code`

避免：`helper`、`utils`、`tools`、`anthropic-*`、`claude-*`

### 正文结构

使用标准 markdown 标题：

```markdown
# Skill Name

## Quick Start
最快速的价值路径...

## Instructions
Claude 遵循的核心指导...

## Examples
显示预期行为的输入/输出对...

## Advanced Features
其他功能（链接到参考文件）...

## Guidelines
规则和约束...
```

## 你想做什么？

1. **创建新技能** - 从头开始构建
2. **审核现有技能** - 对照最佳实践检查
3. **添加组件** - 添加工作流程/参考/示例
4. **获取指导** - 了解技能设计

## 创建新技能

### 步骤 1：选择类型

**简单技能（单文件）：**
- 少于 500 行
- 独立的指导
- 无复杂工作流程

**渐进式披露技能（多文件）：**
- SKILL.md 作为概述
- 详细文档的参考文件
- 实用程序的脚本

### 步骤 2：创建 SKILL.md

```markdown
---
name: your-skill-name
description: [它做什么]。在 [触发条件] 时使用。
---

# Your Skill Name

## Quick Start

[立即可行的示例]

```[language]
[代码示例]
```

## Instructions

[核心指导]

## Examples

**示例 1：**
输入：[描述]
输出：
```
[结果]
```

## Guidelines

- [约束 1]
- [约束 2]
```

### 步骤 3：添加参考文件（如需要）

从 SKILL.md 链接到详细内容：

```markdown
有关 API 参考，请参阅 [REFERENCE.md](REFERENCE.md)。
有关表单填写指南，请参阅 [FORMS.md](FORMS.md)。
```

保持参考文件与 SKILL.md **一级深度**。

### 步骤 4：添加脚本（如需要）

脚本执行而不加载到上下文中：

```markdown
## Utility Scripts

提取字段：
```bash
python scripts/analyze.py input.pdf > fields.json
```
```

### 步骤 5：用实际使用进行测试

1. 使用实际任务测试，而不是测试场景
2. 观察 Claude 在哪里遇到困难
3. 根据实际行为进行优化
4. 使用 Haiku、Sonnet 和 Opus 进行测试

## 审核现有技能

根据此评分表检查：

- [ ] 有效的 YAML frontmatter（name + description）
- [ ] 描述包含触发关键字
- [ ] 使用标准 markdown 标题（而不是 XML 标签）
- [ ] SKILL.md 少于 500 行
- [ ] 参考文件一级深度
- [ ] 示例具体，而不是抽象
- [ ] 术语一致
- [ ] 无时效性信息
- [ ] 脚本明确处理错误

## 常见模式

### 模板模式

提供输出模板以获得一致的结果：

```markdown
## Report Template

```markdown
# [分析标题]

## Executive Summary
[一段概述]

## Key Findings
- 发现 1
- 发现 2

## Recommendations
1. [行动项目]
2. [行动项目]
```
```

### 工作流程模式

对于复杂的多步骤任务：

```markdown
## Migration Workflow

复制此检查清单：

```
- [ ] 步骤 1：备份数据库
- [ ] 步骤 2：运行迁移脚本
- [ ] 步骤 3：验证输出
- [ ] 步骤 4：更新配置
```

**步骤 1：备份数据库**
运行：`./scripts/backup.sh`
...
```

### 条件模式

引导通过决策点：

```markdown
## Choose Your Approach

**创建新内容？** 遵循下面的"Creation workflow"。
**编辑现有内容？** 遵循下面的"Editing workflow"。
```

## 要避免的反模式

- **正文中的 XML 标签** - 改用 markdown 标题
- **模糊的描述** - 使用触发关键字具体说明
- **深层嵌套** - 保持参考文件与 SKILL.md 一级深度
- **太多选项** - 提供带逃生舱的默认值
- **Windows 路径** - 始终使用正斜杠
- **踢皮球给 Claude** - 脚本应处理错误
- **时效性信息** - 改用"旧模式"部分

## 参考文件

有关详细指导，请参阅：

- [official-spec.md](references/official-spec.md) - Anthropic 的官方技能规范
- [best-practices.md](references/best-practices.md) - 技能编写最佳实践

## 成功标准

结构良好的技能：
- 具有带描述性 name 和 description 的有效 YAML frontmatter
- 使用标准 markdown 标题（而不是 XML 标签）
- 保持 SKILL.md 少于 500 行
- 链接到详细内容的参考文件
- 包含带有输入/输出对的具体示例
- 已通过实际使用测试

来源：
- [Agent Skills - Claude Code Docs](https://code.claude.com/docs/en/skills)
- [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [GitHub - anthropics/skills](https://github.com/anthropics/skills)
