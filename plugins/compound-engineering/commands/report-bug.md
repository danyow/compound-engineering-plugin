---
name: report-bug
description: 报告 compound-engineering Plugin 中的 bug
argument-hint: "[可选：bug 的简要描述]"
---

# 报告 Compounding Engineering Plugin Bug

报告使用 compound-engineering Plugin 时遇到的 bug。此 Command 收集结构化信息并为维护者创建 GitHub Issue。

## 步骤 1：收集 Bug 信息

使用 AskUserQuestion 工具收集以下信息：

**问题 1：Bug 类别**
- 您遇到了什么类型的问题？
- 选项：Agent 不工作、Command 不工作、Skill 不工作、MCP Server 问题、安装问题、其他

**问题 2：具体组件**
- 哪个具体组件受到影响？
- 询问 Agent、Command、Skill 或 MCP Server 的名称

**问题 3：发生了什么（实际行为）**
- 询问："当您使用此组件时发生了什么？"
- 获取实际行为的清晰描述

**问题 4：应该发生什么（预期行为）**
- 询问："您期望发生什么？"
- 获取预期行为的清晰描述

**问题 5：重现步骤**
- 询问："在 bug 发生之前您采取了哪些步骤？"
- 获取重现步骤

**问题 6：错误消息**
- 询问："您看到任何错误消息了吗？如果是，请分享它们。"
- 捕获任何错误输出

## 步骤 2：收集环境信息

自动收集：
```bash
# 获取 Plugin 版本
cat ~/.claude/plugins/installed_plugins.json 2>/dev/null | grep -A5 "compound-engineering" | head -10 || echo "Plugin info not found"

# 获取 Claude Code 版本
claude --version 2>/dev/null || echo "Claude CLI version unknown"

# 获取操作系统信息
uname -a
```

## 步骤 3：格式化 Bug 报告

创建结构良好的 bug 报告：

```markdown
## Bug 描述

**Component:** [Type] - [Name]
**Summary:** [从参数或收集的信息中简要描述]

## 环境

- **Plugin Version:** [来自 installed_plugins.json]
- **Claude Code Version:** [来自 claude --version]
- **OS:** [来自 uname]

## 发生了什么

[实际行为描述]

## 预期行为

[预期行为描述]

## 重现步骤

1. [步骤 1]
2. [步骤 2]
3. [步骤 3]

## 错误消息

```
[任何错误输出]
```

## 其他背景

[任何其他相关信息]

---
*通过 `/report-bug` Command 报告*
```

## 步骤 4：创建 GitHub Issue

使用 GitHub CLI 创建 Issue：

```bash
gh issue create \
  --repo EveryInc/every-marketplace \
  --title "[compound-engineering] Bug: [简要描述]" \
  --body "[步骤 3 中格式化的 bug 报告]" \
  --label "bug,compound-engineering"
```

**注意：** 如果标签不存在，不带标签创建：
```bash
gh issue create \
  --repo EveryInc/every-marketplace \
  --title "[compound-engineering] Bug: [简要描述]" \
  --body "[格式化的 bug 报告]"
```

## 步骤 5：确认提交

Issue 创建后：
1. 向用户显示 Issue URL
2. 感谢他们报告 bug
3. 让他们知道维护者（Kieran Klaassen）将收到通知

## 输出格式

```
✅ Bug 报告提交成功！

Issue: https://github.com/EveryInc/every-marketplace/issues/[NUMBER]
Title: [compound-engineering] Bug: [描述]

感谢您帮助改进 compound-engineering Plugin！
维护者将审查您的报告并尽快回复。
```

## 错误处理

- 如果 `gh` CLI 未认证：提示用户先运行 `gh auth login`
- 如果 Issue 创建失败：显示格式化的报告，以便用户可以手动创建 Issue
- 如果缺少必需信息：重新提示该特定字段

## 隐私声明

此 Command 不收集：
- 个人信息
- API 密钥或凭据
- 您项目中的私有代码
- 除基本操作系统信息之外的文件路径

报告中仅包含有关 bug 的技术信息。
