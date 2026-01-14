---
name: generate_command
description: 遵循约定和最佳实践创建新的自定义 slash Command
argument-hint: "[Command 目的和要求]"
---

# 创建自定义 Claude Code Command

在 `.claude/commands/` 中为请求的任务创建新的 slash Command。

## 目标

#$ARGUMENTS

## 可利用的关键功能

**文件操作：**
- Read、Edit、Write - 精确修改文件
- Glob、Grep - 搜索代码库
- MultiEdit - 原子多部分更改

**开发：**
- Bash - 运行命令（git、测试、linter）
- Task - 为复杂任务启动专业 Agent
- TodoWrite - 使用 todo 列表跟踪进度

**Web & API：**
- WebFetch、WebSearch - 研究文档
- GitHub (gh cli) - PR、Issue、审查
- Playwright - 浏览器自动化、截图

**集成：**
- AppSignal - 日志和监控
- Context7 - 框架文档
- Stripe、Todoist、Featurebase（如果相关）

## 最佳实践

1. **具体明确** - 详细的说明产生更好的结果
2. **分解复杂任务** - 使用分步计划
3. **使用示例** - 引用现有代码模式
4. **包含成功标准** - 测试通过、linting 清洁等
5. **先思考** - 对复杂问题使用 "think hard" 或 "plan" 关键字
6. **迭代** - 逐步指导流程

## 必需：YAML Frontmatter

**每个 Command 必须以 YAML frontmatter 开头：**

```yaml
---
name: command-name
description: 此 Command 功能的简要描述（最多 100 个字符）
argument-hint: "[Command 接受的参数]"
---
```

**字段：**
- `name`：小写 Command 标识符（内部使用）
- `description`：Command 目的的清晰、简洁摘要
- `argument-hint`：向用户显示预期的参数（例如，`[file path]`、`[PR number]`、`[optional: format]`）

## 构建您的 Command

```markdown
# [Command 名称]

[此 Command 功能的简要描述]

## 步骤

1. [第一步，包含具体细节]
   - 包括文件路径、模式或约束
   - 引用现有代码（如适用）

2. [第二步]
   - 尽可能使用并行工具调用
   - 检查/验证结果

3. [最后步骤]
   - 运行测试
   - Lint 代码
   - 提交更改（如适当）

## 成功标准

- [ ] 测试通过
- [ ] 代码遵循风格指南
- [ ] 文档已更新（如需要）
```

## 有效 Command 的提示

- **使用 $ARGUMENTS** 占位符获取动态输入
- **引用 CLAUDE.md** 模式和约定
- **包含验证步骤** - 测试、linting、视觉检查
- **明确约束** - 不要修改 X，使用模式 Y
- **使用 XML 标签** 进行结构化提示：`<task>`、`<requirements>`、`<constraints>`

## 示例模式

```markdown
按照以下步骤实施 #$ARGUMENTS：

1. 研究现有模式
   - 使用 Grep 搜索类似代码
   - 阅读相关文件以了解方法

2. 规划实施
   - 思考边缘情况和要求
   - 考虑需要的测试用例

3. 实施
   - 遵循现有代码模式（引用特定文件）
   - 如果进行 TDD，先编写测试
   - 确保代码遵循 CLAUDE.md 约定

4. 验证
   - 运行测试：`bin/rails test`
   - 运行 linter：`bundle exec standardrb`
   - 使用 git diff 检查更改

5. 提交（可选）
   - 暂存更改
   - 编写清晰的提交消息
```

## 创建 Command 文件

1. **创建文件** 在 `.claude/commands/[name].md`（支持子目录如 `workflows/`）
2. **以 YAML frontmatter 开头**（见上节）
3. **使用模板构建 Command**
4. **测试 Command** 通过使用适当的参数

## Command 文件模板

```markdown
---
name: command-name
description: 此 Command 的功能
argument-hint: "[预期参数]"
---

# Command 标题

Command 功能和何时使用的简要介绍。

## 工作流

### 步骤 1：[第一个主要步骤]

要做什么的详细信息。

### 步骤 2：[第二个主要步骤]

要做什么的详细信息。

## 成功标准

- [ ] 预期结果 1
- [ ] 预期结果 2
```
