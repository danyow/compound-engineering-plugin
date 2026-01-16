<overview>
自修改是Agent原生工程的高级阶段：Agent可以演变自己的代码、prompt和行为。不是每个应用都需要，但是未来的重要部分。

这是"开发人员能做什么，Agent能做什么"的逻辑扩展。
</overview>

<why_self_modification>
## 为什么选择自修改？

传统软件是静态的——它做你写的东西，仅此而已。自修改Agent可以：

- **修复自己的bug** - 看到错误，修复代码，重启
- **添加新功能** - 用户要求新东西，Agent实现它
- **演变行为** - 从反馈中学习并调整prompt
- **自我部署** - 推送代码、触发构建、重启

Agent成为一个不断改进的活系统，而不是冻结的代码。
</why_self_modification>

<capabilities>
## 自修改启用什么

**代码修改：**
- 读取并理解源文件
- 编写修复和新功能
- 提交并推送到版本控制
- 触发构建并验证它们通过

**Prompt演变：**
- 根据反馈编辑系统prompt
- 添加新功能作为prompt部分
- 改进不起作用的判断标准

**基础设施控制：**
- 从上游拉取最新代码
- 从其他分支/实例合并
- 更改后重启
- 如果某些内容损坏则回滚

**网站/输出生成：**
- 生成并维护网站
- 创建文档
- 从数据构建仪表板
</capabilities>

<guardrails>
## 所需护栏

自修改很强大。它需要安全机制。

**代码更改的审批门：**
```typescript
tool("write_file", async ({ path, content }) => {
  if (isCodeFile(path)) {
    // 存储以供审批，不要立即应用
    pendingChanges.set(path, content);
    const diff = generateDiff(path, content);
    return { text: `需要审批:\n\n${diff}\n\n回复"yes"以应用。` };
  }
  // 非代码文件立即应用
  writeFileSync(path, content);
  return { text: `Wrote ${path}` };
});
```

**变更前自动提交：**
```typescript
tool("self_deploy", async () => {
  // 首先保存当前状态
  runGit("stash");  // 或提交未提交的更改

  // 然后拉取/合并
  runGit("fetch origin");
  runGit("merge origin/main --no-edit");

  // 构建和验证
  runCommand("npm run build");

  // 只有这样才能重启
  scheduleRestart();
});
```

**构建验证：**
```typescript
// 除非构建通过，否则不要重启
try {
  runCommand("npm run build", { timeout: 120000 });
} catch (error) {
  // 回滚合并
  runGit("merge --abort");
  return { text: "构建失败，中止部署", isError: true };
}
```

**重启后的健康检查：**
```typescript
tool("health_check", async () => {
  const uptime = process.uptime();
  const buildValid = existsSync("dist/index.js");
  const gitClean = !runGit("status --porcelain");

  return {
    text: JSON.stringify({
      status: "healthy",
      uptime: `${Math.floor(uptime / 60)}m`,
      build: buildValid ? "valid" : "missing",
      git: gitClean ? "clean" : "uncommitted changes",
    }, null, 2),
  };
});
```
</guardrails>

<git_architecture>
## Git-Based Self-Modification

Use git as the foundation for self-modification. It provides:
- Version history (rollback capability)
- Branching (experiment safely)
- Merge (sync with other instances)
- Push/pull (deploy and collaborate)

**Essential git tools:**
```typescript
tool("status", "Show git status", {}, ...);
tool("diff", "Show file changes", { path: z.string().optional() }, ...);
tool("log", "Show commit history", { count: z.number() }, ...);
tool("commit_code", "Commit code changes", { message: z.string() }, ...);
tool("git_push", "Push to GitHub", { branch: z.string().optional() }, ...);
tool("pull", "Pull from GitHub", { source: z.enum(["main", "instance"]) }, ...);
tool("rollback", "Revert recent commits", { commits: z.number() }, ...);
```

**Multi-instance architecture:**
```
main                      # Shared code
├── instance/bot-a       # Instance A's branch
├── instance/bot-b       # Instance B's branch
└── instance/bot-c       # Instance C's branch
```

Each instance can:
- Pull updates from main
- Push improvements back to main (via PR)
- Sync features from other instances
- Maintain instance-specific config
</git_architecture>

<prompt_evolution>
## Self-Modifying Prompts

The system prompt is a file the agent can read and write.

```typescript
// Agent can read its own prompt
tool("read_file", ...);  // Can read src/prompts/system.md

// Agent can propose changes
tool("write_file", ...);  // Can write to src/prompts/system.md (with approval)
```

**System prompt as living document:**
```markdown
## Feedback Processing

When someone shares feedback:
1. Acknowledge warmly
2. Rate importance 1-5
3. Store using feedback tools

<!-- Note to self: Video walkthroughs should always be 4-5,
     learned this from Dan's feedback on 2024-12-07 -->
```

The agent can:
- Add notes to itself
- Refine judgment criteria
- Add new feature sections
- Document edge cases it learned
</prompt_evolution>

<when_to_use>
## When to Implement Self-Modification

**Good candidates:**
- Long-running autonomous agents
- Agents that need to adapt to feedback
- Systems where behavior evolution is valuable
- Internal tools where rapid iteration matters

**Not necessary for:**
- Simple single-task agents
- Highly regulated environments
- Systems where behavior must be auditable
- One-off or short-lived agents

Start with a non-self-modifying prompt-native agent. Add self-modification when you need it.
</when_to_use>

<example_tools>
## Complete Self-Modification Toolset

```typescript
const selfMcpServer = createSdkMcpServer({
  name: "self",
  version: "1.0.0",
  tools: [
    // FILE OPERATIONS
    tool("read_file", "Read any project file", { path: z.string() }, ...),
    tool("write_file", "Write a file (code requires approval)", { path, content }, ...),
    tool("list_files", "List directory contents", { path: z.string() }, ...),
    tool("search_code", "Search for patterns", { pattern: z.string() }, ...),

    // APPROVAL WORKFLOW
    tool("apply_pending", "Apply approved changes", {}, ...),
    tool("get_pending", "Show pending changes", {}, ...),
    tool("clear_pending", "Discard pending changes", {}, ...),

    // RESTART
    tool("restart", "Rebuild and restart", {}, ...),
    tool("health_check", "Check if bot is healthy", {}, ...),
  ],
});

const gitMcpServer = createSdkMcpServer({
  name: "git",
  version: "1.0.0",
  tools: [
    // STATUS
    tool("status", "Show git status", {}, ...),
    tool("diff", "Show changes", { path: z.string().optional() }, ...),
    tool("log", "Show history", { count: z.number() }, ...),

    // COMMIT & PUSH
    tool("commit_code", "Commit code changes", { message: z.string() }, ...),
    tool("git_push", "Push to GitHub", { branch: z.string().optional() }, ...),

    // SYNC
    tool("pull", "Pull from upstream", { source: z.enum(["main", "instance"]) }, ...),
    tool("self_deploy", "Pull, build, restart", { source: z.enum(["main", "instance"]) }, ...),

    // SAFETY
    tool("rollback", "Revert commits", { commits: z.number() }, ...),
    tool("health_check", "Detailed health report", {}, ...),
  ],
});
```
</example_tools>

<checklist>
## Self-Modification Checklist

Before enabling self-modification:
- [ ] Git-based version control set up
- [ ] 代码更改的审批门
- [ ] 重启前的构建验证
- [ ] 可用的回滚机制
- [ ] Health check endpoint
- [ ] Instance identity configured

When implementing:
- [ ] Agent can read all project files
- [ ] Agent can write files (with appropriate approval)
- [ ] Agent can commit and push
- [ ] Agent can pull updates
- [ ] Agent can restart itself
- [ ] Agent can roll back if needed
</checklist>
