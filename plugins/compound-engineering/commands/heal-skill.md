---
name: heal-skill
description: 当 Skill 有错误的说明或过时的 API 引用时修复不正确的 SKILL.md 文件
argument-hint: [可选：要修复的具体问题]
allowed-tools: [Read, Edit, Bash(ls:*), Bash(git:*)]
---

<objective>
根据执行过程中发现的更正更新 Skill 的 SKILL.md 和相关文件。

分析对话以检测正在运行哪个 Skill，反思出了什么问题，提出具体修复，获得用户批准，然后应用更改并可选择提交。
</objective>

<context>
Skill 检测：!`ls -1 ./skills/*/SKILL.md | head -5`
</context>

<quick_start>
<workflow>
1. **检测 Skill** 从对话上下文（调用消息、最近的 SKILL.md 引用）
2. **反思** 出了什么问题以及您如何发现修复
3. **呈现** 带有前后对比的建议更改
4. **获得批准** 在进行任何编辑之前
5. **应用** 更改并可选择提交
</workflow>
</quick_start>

<process>
<step_1 name="detect_skill">
从对话上下文中识别 Skill：

- 查找 Skill 调用消息
- 检查最近引用了哪个 SKILL.md
- 检查当前任务上下文

设置：`SKILL_NAME=[skill-name]` 和 `SKILL_DIR=./skills/$SKILL_NAME`

如果不清楚，询问用户。
</step_1>

<step_2 name="reflection_and_analysis">
如果提供了 $ARGUMENTS，则关注它，否则分析更广泛的上下文。

确定：
- **什么是错误的**：引用 SKILL.md 中不正确的具体部分
- **发现方法**：Context7、错误消息、反复试验、文档查找
- **根本原因**：过时的 API、不正确的参数、错误的端点、缺少上下文
- **影响范围**：单个部分还是多个？相关文件受影响？
- **建议的修复**：哪些文件，哪些部分，每个的前后对比
</step_2>

<step_3 name="scan_affected_files">
```bash
ls -la $SKILL_DIR/
ls -la $SKILL_DIR/references/ 2>/dev/null
ls -la $SKILL_DIR/scripts/ 2>/dev/null
```
</step_3>

<step_4 name="present_proposed_changes">
以此格式呈现更改：

```
**正在修复的 Skill：** [skill-name]
**发现的问题：** [1-2 句摘要]
**根本原因：** [简要说明]

**要修改的文件：**
- [ ] SKILL.md
- [ ] references/[file].md
- [ ] scripts/[file].py

**建议的更改：**

### 更改 1：SKILL.md - [部分名称]
**位置：** SKILL.md 第 [X] 行

**当前（不正确）：**
```
[当前文件的确切文本]
```

**更正后：**
```
[新文本]
```

**原因：** [为什么这修复了问题]

[对所有文件的每个更改重复]

**影响评估：**
- 影响：[身份验证/API 端点/参数/示例/等]

**验证：**
这些更改将防止：[提示这个的具体错误]
```
</step_4>

<step_5 name="request_approval">
```
我应该应用这些更改吗？

1. 是，应用并提交所有更改
2. 应用但不提交（让我先审查）
3. 修订更改（我将提供反馈）
4. 取消（不做更改）

选择 (1-4)：
```

**等待用户响应。未经批准不要继续。**
</step_5>

<step_6 name="apply_changes">
仅在批准后（选项 1 或 2）：

1. 对所有文件的每个更正使用 Edit 工具
2. 读回修改的部分以验证
3. 如果选项 1，使用显示修复内容的结构化消息提交
4. 使用文件列表确认完成
</step_6>
</process>

<success_criteria>
- Skill 从对话上下文中正确检测
- 所有不正确的部分都用前后对比识别
- 用户在应用之前批准更改
- 所有编辑应用于 SKILL.md 和相关文件
- 通过读回验证更改
- 如果用户选择选项 1，则创建提交
- 使用文件列表确认完成
</success_criteria>

<verification>
完成前：

- 读回每个修改的部分以确认应用的更改
- 确保跨文件一致性（SKILL.md 示例与 references/ 匹配）
- 如果选择了选项 1，验证创建了 git 提交
- 检查没有修改意外文件
</verification>
