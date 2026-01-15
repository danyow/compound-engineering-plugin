---
name: file-todos
description: 管理 todos/ 目录中基于文件的待办事项跟踪系统时应使用此技能。它提供了创建待办事项、管理状态和依赖关系、进行分类审查以及与斜杠命令和代码审查流程集成的工作流程。
---

# 基于文件的待办事项跟踪技能

## 概述

`todos/` 目录包含一个基于文件的跟踪系统，用于管理代码审查反馈、技术债务、功能请求和工作项。每个待办事项都是一个带有 YAML frontmatter 和结构化章节的 markdown 文件。

此技能应在以下情况使用：
- 从发现或反馈创建新的待办事项
- 管理待办事项生命周期（pending → ready → complete）
- 对待审核项目进行分类审批
- 检查或管理依赖关系
- 将 PR 评论或代码发现转换为跟踪的工作
- 在待办事项执行期间更新工作日志

## 文件命名约定

待办事项文件遵循以下命名模式：

```
{issue_id}-{status}-{priority}-{description}.md
```

**组成部分：**
- **issue_id**：顺序编号（001、002、003...）- 永不重用
- **status**：`pending`（需要审查）、`ready`（已批准）、`complete`（已完成）
- **priority**：`p1`（关键）、`p2`（重要）、`p3`（可选）
- **description**：kebab-case，简要描述

**示例：**
```
001-pending-p1-mailer-test.md
002-ready-p1-fix-n-plus-1.md
005-complete-p2-refactor-csv.md
```

## 文件结构

每个待办事项都是一个带有 YAML frontmatter 和结构化章节的 markdown 文件。创建新待办事项时使用 [todo-template.md](./assets/todo-template.md) 模板作为起点。

**必需的章节：**
- **Problem Statement（问题陈述）** - 什么出了问题、缺失或需要改进？
- **Findings（发现）** - 调查结果、根本原因、关键发现
- **Proposed Solutions（建议的解决方案）** - 多个选项及其优缺点、工作量、风险
- **Recommended Action（推荐的行动）** - 清晰的计划（在审查期间填写）
- **Acceptance Criteria（验收标准）** - 可测试的检查清单项目
- **Work Log（工作日志）** - 按时间顺序记录日期、行动、学习

**可选的章节：**
- **Technical Details（技术细节）** - 受影响的文件、相关组件、DB 更改
- **Resources（资源）** - 错误链接、测试、PR、文档
- **Notes（备注）** - 额外的上下文或决策

**YAML frontmatter 字段：**
```yaml
---
status: ready              # pending | ready | complete
priority: p1              # p1 | p2 | p3
issue_id: "002"
tags: [rails, performance, database]
dependencies: ["001"]     # 此项被阻塞的 Issue ID
---
```

## 常见工作流程

### 创建新的待办事项

**从发现或反馈创建新待办事项：**

1. 确定下一个 issue ID：`ls todos/ | grep -o '^[0-9]\+' | sort -n | tail -1`
2. 复制模板：`cp assets/todo-template.md todos/{NEXT_ID}-pending-{priority}-{description}.md`
3. 编辑并填写必需的章节：
   - Problem Statement（问题陈述）
   - Findings（发现）（如果来自调查）
   - Proposed Solutions（建议的解决方案）（多个选项）
   - Acceptance Criteria（验收标准）
   - 添加初始 Work Log 条目
4. 确定状态：`pending`（需要审查）或 `ready`（预先批准）
5. 添加相关标签以便过滤

**何时创建待办事项：**
- 需要超过 15-20 分钟的工作
- 需要研究、计划或考虑多种方法
- 对其他工作有依赖关系
- 需要经理批准或确定优先级
- 更大功能或重构的一部分
- 需要记录的技术债务

**何时立即行动：**
- 问题很简单（< 15 分钟）
- 现在有完整的上下文
- 不需要计划
- 用户明确要求立即行动
- 有明显解决方案的简单 bug 修复

### 对待审核项目进行分类

**对待审核的待办事项进行分类：**

1. 列出待审核项目：`ls todos/*-pending-*.md`
2. 对于每个待办事项：
   - 阅读 Problem Statement 和 Findings
   - 审查 Proposed Solutions
   - 做出决定：批准、推迟或修改优先级
3. 更新已批准的待办事项：
   - 重命名文件：`mv {file}-pending-{pri}-{desc}.md {file}-ready-{pri}-{desc}.md`
   - 更新 frontmatter：`status: pending` → `status: ready`
   - 填写"Recommended Action"章节，提供清晰的计划
   - 如果与初始评估不同，调整优先级
4. 推迟的待办事项保持 `pending` 状态

**使用斜杠命令：** `/triage` 进行交互式批准工作流程

### 管理依赖关系

**跟踪依赖关系：**

```yaml
dependencies: ["002", "005"]  # 此待办事项被 issue 002 和 005 阻塞
dependencies: []               # 无阻塞者 - 可以立即开始工作
```

**检查什么阻塞了待办事项：**
```bash
grep "^dependencies:" todos/003-*.md
```

**查找待办事项阻塞了什么：**
```bash
grep -l 'dependencies:.*"002"' todos/*.md
```

**在开始之前验证阻塞者是否已完成：**
```bash
for dep in 001 002 003; do
  [ -f "todos/${dep}-complete-*.md" ] || echo "Issue $dep not complete"
done
```

### 更新工作日志

**在处理待办事项时，始终添加工作日志条目：**

```markdown
### YYYY-MM-DD - Session Title

**By:** Claude Code / Developer Name

**Actions:**
- 具体做出的更改（包括 file:line 引用）
- 执行的命令
- 运行的测试
- 调查结果

**Learnings:**
- 什么有效 / 什么无效
- 发现的模式
- 未来工作的关键见解
```

工作日志用于：
- 调查的历史记录
- 尝试方法的文档
- 团队知识共享
- 未来类似工作的上下文

### 完成待办事项

**将待办事项标记为完成：**

1. 验证所有验收标准已完成勾选
2. 使用最终会话和结果更新 Work Log
3. 重命名文件：`mv {file}-ready-{pri}-{desc}.md {file}-complete-{pri}-{desc}.md`
4. 更新 frontmatter：`status: ready` → `status: complete`
5. 检查未被阻塞的工作：`grep -l 'dependencies:.*"002"' todos/*-ready-*.md`
6. 使用 issue 引用提交：`feat: resolve issue 002`

## 与开发工作流程的集成

| 触发器 | 流程 | 工具 |
|---------|------|------|
| 代码审查 | `/workflows:review` → Findings → `/triage` → Todos | Review agent + skill |
| PR 评论 | `/resolve_pr_parallel` → 个别修复 → Todos | gh CLI + skill |
| 代码 TODOs | `/resolve_todo_parallel` → 修复 + 复杂 todos | Agent + skill |
| 计划 | 头脑风暴 → 创建 todo → 工作 → 完成 | Skill |
| 反馈 | 讨论 → 创建 todo → 审查 → 工作 | Skill + slash |

## 快速参考命令

**查找工作：**
```bash
# 列出最高优先级无阻塞的工作
grep -l 'dependencies: \[\]' todos/*-ready-p1-*.md

# 列出所有需要审查的待审核项目
ls todos/*-pending-*.md

# 查找下一个 issue ID
ls todos/ | grep -o '^[0-9]\+' | sort -n | tail -1 | awk '{printf "%03d", $1+1}'

# 按状态统计
for status in pending ready complete; do
  echo "$status: $(ls -1 todos/*-$status-*.md 2>/dev/null | wc -l)"
done
```

**依赖管理：**
```bash
# 什么阻塞了这个待办事项？
grep "^dependencies:" todos/003-*.md

# 这个待办事项阻塞了什么？
grep -l 'dependencies:.*"002"' todos/*.md
```

**搜索：**
```bash
# 按标签搜索
grep -l "tags:.*rails" todos/*.md

# 按优先级搜索
ls todos/*-p1-*.md

# 全文搜索
grep -r "payment" todos/
```

## 关键区别

**File-todos 系统（此技能）：**
- `todos/` 目录中的 Markdown 文件
- 开发/项目跟踪
- 带有 YAML frontmatter 的独立 markdown 文件
- 由人类和 agent 使用

**Rails Todo 模型：**
- `app/models/todo.rb` 中的数据库模型
- 应用程序中面向用户的功能
- Active Record CRUD 操作
- 与此基于文件的系统不同

**TodoWrite 工具：**
- agent 会话期间的内存任务跟踪
- 单次对话的临时跟踪
- 不持久化到磁盘
- 与上述两个系统都不同
