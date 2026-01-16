# 种植你自己的花园：自适应 Agent 生态系统

> **Issue:** https://github.com/EveryInc/compound-engineering-plugin/issues/20

## 核心理念

每个人都种植自己的花园，但我们都使用相同的流程。

从一个**种子**开始（最小核心：`/plan`、`/work`、`/review`、`/compound`）。每次 `/compound` 循环都可以根据你正在处理的内容建议添加 Agent——就像构建测试套件来防止回归，但这是针对代码审查专业知识的。

## 当前问题

- 单体 Plugin：24 个 Agent，用户仅使用约 30%
- 缺乏个性化（Rails 开发者和 Python 开发者使用相同的 Agent）
- 静态集合，不会自适应

## 解决方案

### 种子（核心 Plugin）

4 个 Command + 最小 Agent 集合：

| Component | What's Included |
|-----------|-----------------|
| Commands | `/plan`、`/work`、`/review`、`/compound` |
| Review Agents | security、performance、simplicity、architecture、patterns |
| Research Agents | best-practices、framework-docs、git-history、repo-analyst |
| Skills | compound-docs、file-todos、git-worktree |
| MCP Servers | playwright、context7 |

### 成长循环

每次 `/compound` 之后：

```
✅ 学习内容已记录

💡 看起来你正在使用 Rails。
   是否要添加 "DHH Rails Reviewer"？

   [y] 是  [n] 否  [x] 不再询问
```

三个新 Agent 来源：
1. **预定义** - "你正在使用 Rails，添加 DHH 审查器？"
2. **动态** - "你正在使用 actor 模型，创建一个专家？"
3. **自定义** - "想为这个模式创建一个 Agent 吗？"

### Agent 存储

```
.claude/agents/       → 项目特定（最高优先级）
~/.claude/agents/     → 用户的花园
plugin/agents/        → 来自已安装的 Plugin
```

## 实施阶段

### 阶段 1：拆分 Plugin
- 创建 `agent-library/`，包含框架特定的 Agent（Rails、Python、TypeScript、Frontend）
- 保持 `compound-engineering` 作为核心，包含通用 Agent
- 无破坏性变更——现有用户不受影响

### 阶段 2：Agent 发现
- `/review` 从所有三个位置发现 Agent
- 项目 Agent 覆盖用户 Agent 覆盖 Plugin Agent

### 阶段 3：通过 /compound 成长
- 检测技术栈（Gemfile、package.json 等）
- 在记录学习内容后建议相关 Agent
- 将接受的 Agent 安装到 `~/.claude/agents/`

### 阶段 4：管理
- `/agents list` - 查看你的花园
- `/agents add <name>` - 从库中添加
- `/agents disable <name>` - 临时禁用

## 什么放在哪里

**核心（种子）：** 11 个框架无关的 Agent
- security-sentinel、performance-oracle、code-simplicity-reviewer
- architecture-strategist、pattern-recognition-specialist
- 4 个 research Agent、2 个 workflow Agent

**Agent 库：** 10 个专业 Agent
- Rails: kieran-rails、dhh-rails、data-integrity (3)
- Python: kieran-python (1)
- TypeScript: kieran-typescript (1)
- Frontend: julik-races、design-iterator、design-reviewer、figma-sync (4)
- Editorial: every-style-editor (1)

## 关键约束

Claude Code 不支持 Plugin 依赖。每个 Plugin 必须是独立的。用户手动安装他们需要的内容，或者我们通过 `/compound` 建议添加。

## 验收标准

- [ ] 核心 Plugin 可以独立工作，带有通用 Agent
- [ ] `/compound` 根据检测到的技术栈建议 Agent
- [ ] 用户可以接受/拒绝建议
- [ ] `/agents` Command 用于花园管理
- [ ] 对现有用户无破坏性变更
