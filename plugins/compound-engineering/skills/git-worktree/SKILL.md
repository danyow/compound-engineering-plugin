---
name: git-worktree
description: 此技能管理用于隔离并行开发的 Git worktrees。它通过简单的交互式界面处理 worktrees 的创建、列出、切换和清理，遵循 KISS 原则。
---

# Git Worktree Manager

此技能为跨开发工作流程管理 Git worktrees 提供统一接口。无论你是隔离审查 PR 还是并行处理功能，此技能都能处理所有复杂性。

## 此技能的功能

- **创建 worktrees** 从主分支创建具有清晰分支名称的 worktrees
- **列出 worktrees** 显示当前状态
- **在 worktrees 之间切换** 进行并行工作
- **自动清理已完成的 worktrees**
- **每步交互式确认**
- **自动 .gitignore 管理** worktree 目录
- **自动复制 .env 文件** 从主仓库到新 worktrees

## 关键：始终使用 Manager 脚本

**永远不要直接调用 `git worktree add`。** 始终使用 `worktree-manager.sh` 脚本。

该脚本处理原始 git 命令无法处理的关键设置：
1. 从主仓库复制 `.env`、`.env.local`、`.env.test` 等
2. 确保 `.worktrees` 在 `.gitignore` 中
3. 创建一致的目录结构

```bash
# ✅ 正确 - 始终使用脚本
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh create feature-name

# ❌ 错误 - 永远不要直接这样做
git worktree add .worktrees/feature-name -b feature-name main
```

## 何时使用此技能

在以下场景中使用此技能：

1. **代码审查（`/workflows:review`）**：如果尚未在 PR 分支上，提供 worktree 以进行隔离审查
2. **功能工作（`/workflows:work`）**：始终询问用户是想要并行 worktree 还是实时分支工作
3. **并行开发**：同时处理多个功能时
4. **清理**：在 worktree 中完成工作后

## 如何使用

### 在 Claude Code 工作流程中

该技能自动从 `/workflows:review` 和 `/workflows:work` 命令调用：

```
# 对于审查：如果不在 PR 分支上，提供 worktree
# 对于工作：始终询问 - 新分支还是 worktree？
```

### 手动使用

你也可以直接从 bash 调用技能：

```bash
# 创建一个新的 worktree（自动复制 .env 文件）
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh create feature-login

# 列出所有 worktrees
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh list

# 切换到一个 worktree
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh switch feature-login

# 将 .env 文件复制到现有 worktree（如果它们未被复制）
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh copy-env feature-login

# 清理已完成的 worktrees
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh cleanup
```

## 命令

### `create <branch-name> [from-branch]`

使用给定的分支名称创建一个新的 worktree。

**选项：**
- `branch-name`（必需）：新分支和 worktree 的名称
- `from-branch`（可选）：要创建的基础分支（默认为 `main`）

**示例：**
```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh create feature-login
```

**发生的情况：**
1. 检查 worktree 是否已存在
2. 从远程更新基础分支
3. 创建新的 worktree 和分支
4. **从主仓库复制所有 .env 文件**（.env、.env.local、.env.test 等）
5. 显示 cd 到 worktree 的路径

### `list` 或 `ls`

列出所有可用的 worktrees 及其分支和当前状态。

**示例：**
```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh list
```

**输出显示：**
- Worktree 名称
- 分支名称
- 哪个是当前的（用 ✓ 标记）
- 主仓库状态

### `switch <name>` 或 `go <name>`

切换到现有的 worktree 并 cd 到其中。

**示例：**
```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh switch feature-login
```

**可选：**
- 如果未提供名称，列出可用的 worktrees 并提示选择

### `cleanup` 或 `clean`

交互式清理非活动 worktrees，需要确认。

**示例：**
```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh cleanup
```

**发生的情况：**
1. 列出所有非活动 worktrees
2. 请求确认
3. 删除选定的 worktrees
4. 清理空目录

## 工作流程示例

### 使用 Worktree 进行代码审查

```bash
# Claude Code 识别你不在 PR 分支上
# 提供："Use worktree for isolated review? (y/n)"

# 你回答：yes
# 脚本运行（自动复制 .env 文件）：
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh create pr-123-feature-name

# 你现在在隔离的 worktree 中进行审查，包含所有环境变量
cd .worktrees/pr-123-feature-name

# 审查后，返回主仓库：
cd ../..
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh cleanup
```

### 并行功能开发

```bash
# 对于第一个功能（复制 .env 文件）：
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh create feature-login

# 稍后，开始第二个功能（也复制 .env 文件）：
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh create feature-notifications

# 列出你有什么：
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh list

# 根据需要在它们之间切换：
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh switch feature-login

# 完成后返回主仓库并清理：
cd .
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh cleanup
```

## 关键设计原则

### KISS（保持简单，愚蠢）

- **一个 manager 脚本** 处理所有 worktree 操作
- **简单的命令** 具有合理的默认值
- **交互式提示** 防止意外操作
- **清晰的命名** 直接使用分支名称

### 固执己见的默认值

- Worktrees 始终从 **main** 创建（除非指定）
- Worktrees 存储在 **.worktrees/** 目录中
- 分支名称成为 worktree 名称
- **.gitignore** 自动管理

### 安全第一

- **创建前确认** worktrees
- **清理前确认** 以防止意外删除
- **不会删除当前 worktree**
- **清晰的错误消息** 用于问题

## 与工作流程的集成

### `/workflows:review`

而不是总是创建 worktree：

```
1. 检查当前分支
2. 如果已经在 PR 分支上 → 留在那里，不需要 worktree
3. 如果是不同的分支 → 提供 worktree：
   "Use worktree for isolated review? (y/n)"
   - yes → 调用 git-worktree skill
   - no → 在当前分支上继续使用 PR diff
```

### `/workflows:work`

始终提供选择：

```
1. 询问："How do you want to work?
   1. New branch on current worktree (live work)
   2. Worktree (parallel work)"

2. 如果选择 1 → 正常创建新分支
3. 如果选择 2 → 调用 git-worktree skill 从 main 创建
```

## 故障排除

### "Worktree already exists"

如果你看到这个，脚本会询问你是否想切换到它。

### "Cannot remove worktree: it is the current worktree"

首先切换出 worktree（到主仓库），然后清理：

```bash
cd $(git rev-parse --show-toplevel)
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh cleanup
```

### 在 worktree 中迷路了？

查看你在哪里：

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh list
```

### worktree 中缺少 .env 文件？

如果一个 worktree 是在没有 .env 文件的情况下创建的（例如，通过原始 `git worktree add`），复制它们：

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh copy-env feature-name
```

导航回主仓库：

```bash
cd $(git rev-parse --show-toplevel)
```

## 技术细节

### 目录结构

```
.worktrees/
├── feature-login/          # Worktree 1
│   ├── .git
│   ├── app/
│   └── ...
├── feature-notifications/  # Worktree 2
│   ├── .git
│   ├── app/
│   └── ...
└── ...

.gitignore（更新以包含 .worktrees）
```

### 工作原理

- 使用 `git worktree add` 创建隔离环境
- 每个 worktree 有自己的分支
- 一个 worktree 中的更改不会影响其他 worktree
- 与主仓库共享 git 历史
- 可以从任何 worktree push

### 性能

- Worktrees 是轻量级的（只是文件系统链接）
- 无仓库重复
- 共享 git 对象以提高效率
- 比克隆或 stashing/switching 快得多
