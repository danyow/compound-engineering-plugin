# 推荐的 Skill 结构

复杂 skill 的最佳结构将路由、工作流和知识分开。

<structure>
```
skill-name/
├── SKILL.md              # 路由器 + 基本原则（不可避免）
├── workflows/            # 分步程序（如何）
│   ├── workflow-a.md
│   ├── workflow-b.md
│   └── ...
└── references/           # 领域知识（是什么）
    ├── reference-a.md
    ├── reference-b.md
    └── ...
```
</structure>

<why_this_works>
## 解决的问题

**问题 1：上下文被跳过**
当重要原则在单独的文件中时，Claude 可能不会读取它们。
**解决方案：** 将基本原则直接放在 SKILL.md 中。它们会自动加载。

**问题 2：加载了错误的上下文**
"构建"任务加载调试参考。"调试"任务加载构建参考。
**解决方案：** 引导问题确定意图 → 路由到特定工作流 → 工作流指定要读取的参考。

**问题 3：单体 skill 令人不知所措**
500+ 行混合内容使查找相关部分变得困难。
**解决方案：** 小路由器（SKILL.md）+ 专注的工作流 + 参考库。

**问题 4：程序与知识混合**
"如何做 X"与"X 是什么意思"混合会造成混淆。
**解决方案：** 工作流是程序（步骤）。参考是知识（模式、示例）。
</why_this_works>

<skill_md_template>
## SKILL.md 模板

```markdown
---
name: skill-name
description: What it does and when to use it.
---

<essential_principles>
## How This Skill Works

[适用于所有工作流的内联原则。不能跳过。]

### Principle 1: [Name]
[简要解释]

### Principle 2: [Name]
[简要解释]
</essential_principles>

<intake>
**询问用户：**

你想做什么？
1. [Option A]
2. [Option B]
3. [Option C]
4. Something else

**等待响应后再继续。**
</intake>

<routing>
| 响应 | 工作流 |
|----------|----------|
| 1, "keyword", "keyword" | `workflows/option-a.md` |
| 2, "keyword", "keyword" | `workflows/option-b.md` |
| 3, "keyword", "keyword" | `workflows/option-c.md` |
| 4, other | 澄清，然后选择 |

**读取工作流后，精确遵循它。**
</routing>

<reference_index>
`references/` 中的所有领域知识：

**Category A:** file-a.md, file-b.md
**Category B:** file-c.md, file-d.md
</reference_index>

<workflows_index>
| 工作流 | 目的 |
|----------|---------|
| option-a.md | [它的作用] |
| option-b.md | [它的作用] |
| option-c.md | [它的作用] |
</workflows_index>
```
</skill_md_template>

<workflow_template>
## 工作流模板

```markdown
# Workflow: [Name]

<required_reading>
**现在读取这些参考文件：**
1. references/relevant-file.md
2. references/another-file.md
</required_reading>

<process>
## Step 1: [Name]
[要做什么]

## Step 2: [Name]
[要做什么]

## Step 3: [Name]
[要做什么]
</process>

<success_criteria>
此工作流在以下情况下完成：
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3
</success_criteria>
```
</workflow_template>

<when_to_use_this_pattern>
## 何时使用此模式

**何时使用路由器 + 工作流 + 参考：**
- 多个不同的工作流（构建 vs 调试 vs 发布）
- 不同的工作流需要不同的参考
- 基本原则不能被跳过
- Skill 已超过 200 行

**何时使用简单的单文件 skill：**
- 一个工作流
- 小型参考集
- 总共少于 200 行
- 没有要强制执行的基本原则
</when_to_use_this_pattern>

<key_insight>
## 关键见解

**SKILL.md 始终加载。使用此保证。**

将不可避免的内容放在 SKILL.md 中：
- 基本原则
- 引导问题
- 路由逻辑

将特定于工作流的内容放在 workflows/ 中：
- 分步程序
- 该工作流所需的参考
- 该工作流的成功标准

将可重用的知识放在 references/ 中：
- 模式和示例
- 技术细节
- 领域专业知识
</key_insight>
