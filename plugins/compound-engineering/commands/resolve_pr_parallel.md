---
name: resolve_pr_parallel
description: 使用并行处理解决所有 PR 评论
argument-hint: "[可选：PR 编号或当前 PR]"
---

使用并行处理解决所有 PR 评论。

Claude Code 自动检测并理解您的 git 上下文：

- 当前分支检测
- 关联的 PR 上下文
- 所有 PR 评论和审查线程
- 可以通过指定 PR 编号处理任何 PR，或询问它

## 工作流

### 1. 分析

获取 PR 的所有未解决评论

```bash
gh pr status
bin/get-pr-comments PR_NUMBER
```

### 2. 计划

创建所有未解决项目的 TodoWrite 列表，按类型分组。

### 3. 实施（并行）

为每个未解决的项目并行生成一个 pr-comment-resolver Agent。

因此，如果有 3 条评论，它将并行生成 3 个 pr-comment-resolver Agent，像这样

1. Task pr-comment-resolver(comment1)
2. Task pr-comment-resolver(comment2)
3. Task pr-comment-resolver(comment3)

始终为每个 Todo 项目并行运行所有子 Agent/Task。

### 4. 提交和解决

- 提交更改
- 运行 bin/resolve-pr-thread THREAD_ID_1
- 推送到远程

最后，再次检查 bin/get-pr-comments PR_NUMBER 以查看是否所有评论都已解决。它们应该是，如果没有，从 1 开始重复该过程。
