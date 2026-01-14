---
name: resolve_parallel
description: 使用并行处理解决所有 TODO 注释
argument-hint: "[可选：特定 TODO 模式或文件]"
---

使用并行处理解决所有 TODO 注释。

## 工作流

### 1. 分析

从上面收集需要做的事情。

### 2. 计划

创建所有未解决项目的 TodoWrite 列表，按类型分组。确保查看可能发生的依赖关系并优先处理其他人需要的内容。例如，如果您需要更改名称，则必须等待执行其他操作。输出一个 mermaid 流程图，显示我们如何做到这一点。我们可以并行完成所有操作吗？我们是否需要先做一个，然后并行执行其他操作？我将把待办事项按流程方式放在 mermaid 图中，以便 Agent 知道如何按顺序进行。

### 3. 实施（并行）

为每个未解决的项目并行生成一个 pr-comment-resolver Agent。

因此，如果有 3 条评论，它将并行生成 3 个 pr-comment-resolver Agent，像这样

1. Task pr-comment-resolver(comment1)
2. Task pr-comment-resolver(comment2)
3. Task pr-comment-resolver(comment3)

始终为每个 Todo 项目并行运行所有子 Agent/Task。

### 4. 提交和解决

- 提交更改
- 推送到远程
