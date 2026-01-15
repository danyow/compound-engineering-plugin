---
name: deepen-plan
description: 使用并行研究 agent 增强计划的每个部分，添加深度、最佳实践和实施细节
argument-hint: "[计划文件路径]"
---

# 深化计划 - 强力增强模式

## 简介

**注意：当前年份是 2025。** 在搜索最新文档和最佳实践时使用此信息。

此命令获取现有计划（来自 `/workflows:plan`）并使用并行研究 agent 增强每个部分。 每个主要元素都有自己专用的研究子 agent 来查找：
- 最佳实践和行业模式
- 性能优化
- UI/UX 改进（如适用）
- 质量增强和边界情况
- 实际实施示例

结果是一个有深厚基础、可投入生产的计划，包含具体实施细节。

## 计划文件

<plan_path> #$ARGUMENTS </plan_path>

**如果上面的计划路径为空：**
1. 检查最近的计划： `ls -la plans/`
2. 询问用户："您想深化哪个计划？请提供路径 (e.g., `plans/my-feature.md`)."

在获得有效的计划文件路径之前不要继续。

## 主要任务

### 1. 解析和分析计划结构

<thinking>
首先，读取并解析计划以识别可以通过研究增强的每个主要部分。
</thinking>

**读取计划文件并提取：**
- [ ] 概述/问题陈述
- [ ] 建议解决方案部分
- [ ] 技术方法/架构
- [ ] 实施阶段/步骤
- [ ] 代码示例和文件引用
- [ ] 验收标准
- [ ] 提到的任何 UI/UX 组件
- [ ] 提到的技术/框架 (Rails, React, Python, TypeScript, etc.)
- [ ] 领域区域（数据模型、API、UI、安全、性能等）

**创建部分清单：**
```
部分 1： [Title] - [要研究内容的简要描述]
Section 2: [Title] - [要研究内容的简要描述]
...
```

### 2. 发现并应用可用 Skill

<thinking>
动态发现所有可用 skill 并将它们匹配到计划部分。 不要假设存在哪些 skill - 在运行时发现它们。
</thinking>

**步骤 1：从所有来源发现所有可用 skill**

```bash
# 1. 项目本地 skill（最高优先级 - 项目特定）
ls .claude/skills/

# 2. 用户的全局 skill (~/.claude/)
ls ~/.claude/skills/

# 3. compound-engineering 插件 skill
ls ~/.claude/plugins/cache/*/compound-engineering/*/skills/

# 4. 所有其他已安装插件 - 检查每个插件的 skill
find ~/.claude/plugins/cache -type d -name "skills" 2>/dev/null

# 5. 还要检查 installed_plugins.json 以获取所有插件位置
cat ~/.claude/plugins/installed_plugins.json
```

**Important:** Check EVERY source. 不要假设 compound-engineering 是唯一的插件。 使用任何已安装插件的 skill's relevant.

**步骤 2：对于每个发现的 skill，读取其 SKILL.md 以了解它的功能**

```bash
# 对于找到的每个 skill 目录，读取其文档
cat [skill-path]/SKILL.md
```

**步骤 3：将 skill 匹配到计划内容**

对于发现的每个 skill：
- 读取其 SKILL.md 描述
- 检查是否有任何计划部分匹配该 skill's domain
- 如果匹配，生成子 agent 以应用该 skill 的知识

**步骤 4：为每个匹配的 skill 生成子 agent**

**关键：对于每个匹配的 skill，生成单独的子 agent 并指示它使用该 skill。**

对于每个匹配的 skill：
```
Task general-purpose: "You have the [skill-name] skill available at [skill-path].

你的工作：在计划上使用此 skill。

1. 读取 skill： cat [skill-path]/SKILL.md
2. 遵循 skill's instructions exactly
3. 将 skill 应用到此内容：

[相关计划部分或完整计划]

4. 返回 skill's full output

skill 告诉你该做什么 - 遵循它。完整执行 skill。"
```

**并行生成所有 skill 子 agent：**
- 每个匹配的 skill 1 个子 agent
- 每个子 agent 读取并使用其分配的 skill
- 全部同时运行
- 10、20、30 个 skill 子 agent 都可以

**每个子 agent：**
1. 读取其 skill's SKILL.md
2. 遵循 skill's workflow/instructions
3. 将 skill 应用到计划
4. 返回 skill 生成的任何内容 (代码、建议、模式、审查等)

**示例生成：**
```
Task general-purpose: "使用 dhh-rails-style skill at ~/.claude/plugins/.../dhh-rails-style. 读取 SKILL.md 并将其应用于： [计划的 Rails 部分]"

Task general-purpose: "使用 frontend-design skill at ~/.claude/plugins/.../frontend-design. 读取 SKILL.md 并将其应用于： [计划的 UI 部分]"

Task general-purpose: "使用 agent-native-architecture skill at ~/.claude/plugins/.../agent-native-architecture. 读取 SKILL.md 并将其应用于： [计划的 agent/tool 部分]"

Task general-purpose: "使用 security-patterns skill at ~/.claude/skills/security-patterns. 读取 SKILL.md 并将其应用于： [完整计划]"
```

**对 skill 子 agent 没有限制。为每个可能相关的 skill 生成一个。**

### 3. 发现并应用经验教训/解决方案

<thinking>
检查来自 /workflows:compound 的记录的经验教训。 这些是存储为 markdown 文件的已解决问题。 为每个经验教训生成子 agent 以检查是否 it's relevant.
</thinking>

**经验教训位置 - 检查这些确切的文件夹：**

```
docs/solutions/           <-- 主要：项目级经验教训（由 /workflows:compound 创建）
├── performance-issues/
│   └── *.md
├── debugging-patterns/
│   └── *.md
├── configuration-fixes/
│   └── *.md
├── integration-issues/
│   └── *.md
├── deployment-issues/
│   └── *.md
└── [other-categories]/
    └── *.md
```

**步骤 1：查找所有经验教训 markdown 文件**

运行这些命令以获取每个经验教训文件：

```bash
# 主要位置 - 项目经验教训
find docs/solutions -name "*.md" -type f 2>/dev/null

# 如果 docs/solutions 不't exist, 检查备用位置：
find .claude/docs -name "*.md" -type f 2>/dev/null
find ~/.claude/docs -name "*.md" -type f 2>/dev/null
```

**步骤 2：读取每个经验教训的 frontmatter 以过滤**

每个经验教训文件都有带元数据的 YAML frontmatter。 读取每个文件的前约 20 行以获取：

```yaml
---
title: "N+1 Query Fix for Briefs"
category: performance-issues
标签： [activerecord, n-plus-one, includes, eager-loading]
module: Briefs
symptom: "Slow page load, multiple queries in logs"
root_cause: "Missing includes on association"
---
```

**For each .md file, quickly scan its frontmatter:**

```bash
# 读取每个经验教训的前 20 行（frontmatter + 摘要）
head -20 docs/solutions/**/*.md
```

**步骤 3：过滤 - 仅为可能相关的经验教训生成子 agent**

比较每个经验教训's frontmatter 与计划：
- `标签：` - 是否有任何标签与计划中的技术/模式匹配？
- `category:` - 这个类别是否相关？ (e.g., 如果计划仅是 UI，则跳过 deployment-issues)
- `module:` - 计划是否涉及此模块？
- `symptom:` / `root_cause:` - 此问题是否可能出现在计划中？

**跳过明显不适用的经验教训：**
- 计划仅是前端 → 跳过 `database-migrations/` 经验教训
- 计划是 Python → 跳过 `rails-specific/` 经验教训
- 计划没有 auth → 跳过 `authentication-issues/` 经验教训

**SPAWN sub-agents for 经验教训 that MIGHT apply:**
- 与计划技术有任何标签重叠
- 与计划领域相同的类别
- 相似的模式或关注点

**Step 4: Spawn sub-agents for filtered 经验教训**

对于通过过滤器的每个经验教训：

```
Task general-purpose: "
经验教训文件： [.md 文件的完整路径]

1. 完整阅读此经验教训文件
2. 此经验教训记录了先前解决的问题

检查此经验教训是否适用于此计划：

---
[完整计划 content]
---

如果相关：
- 具体解释如何适用
- 引用关键见解或解决方案
- 建议在何处/如何纳入

如果经过更深入分析后不相关：
- Say '不适用：[原因]'
"
```

**示例过滤：**
```
# 找到 15 个经验教训文件，计划是关于 "Rails API caching"

# 生成（可能相关）：
docs/solutions/performance-issues/n-plus-one-queries.md      # 标签： [activerecord] ✓
docs/solutions/performance-issues/redis-cache-stampede.md    # 标签： [caching, redis] ✓
docs/solutions/configuration-fixes/redis-connection-pool.md  # 标签： [redis] ✓

# 跳过（明显不适用）：
docs/solutions/deployment-issues/heroku-memory-quota.md      # 不是关于缓存
docs/solutions/frontend-issues/stimulus-race-condition.md    # 计划是 API，不是前端
docs/solutions/authentication-issues/jwt-expiry.md           # 计划没有 auth
```

**Spawn sub-agents in PARALLEL for all filtered 经验教训.**

**These 经验教训 are institutional knowledge - 应用它们可以防止重复过去的错误。**

### 4. 为每个部分启动研究 Agent

<thinking>
对于计划中的每个主要部分，生成专用的子 agent 以研究改进。 使用 Explore agent 类型进行开放式研究。
</thinking>

**对于每个已识别的部分，启动并行研究：**

```
Task Explore: "研究以下方面的最佳实践、模式和实际示例： [部分主题].
Find:
- 行业标准和约定
- 性能考虑
- 常见陷阱以及如何避免它们
- 文档和教程
返回具体的、可操作的建议。"
```

**还使用 Context7 MCP 获取框架文档：**

对于计划中提到的任何技术/框架，查询 Context7：
```
mcp__plugin_compound-engineering_context7__resolve-library-id: 查找 [framework] 的库 ID
mcp__plugin_compound-engineering_context7__query-docs: 查询特定模式的文档
```

**使用 WebSearch 获取当前最佳实践：**

搜索计划中主题的最新（2024-2025）文章、博客文章和文档。

### 5. 发现并运行所有审查 Agent

<thinking>
动态发现每个可用的 agent 并对计划运行它们全部。 Don't filter, don't 跳过, don't assume relevance. 40+ parallel agents is fine. 使用所有可用的。
</thinking>

**步骤 1：从所有来源发现所有可用 agent**

```bash
# 1. 项目本地 agent（最高优先级 - 项目特定）
find .claude/agents -name "*.md" 2>/dev/null

# 2. User's global agents (~/.claude/)
find ~/.claude/agents -name "*.md" 2>/dev/null

# 3. compound-engineering 插件 agent（所有子目录）
find ~/.claude/plugins/cache/*/compound-engineering/*/agents -name "*.md" 2>/dev/null

# 4. 所有其他已安装插件 - 检查每个插件的 agent
find ~/.claude/plugins/cache -path "*/agents/*.md" 2>/dev/null

# 5. 检查 installed_plugins.json 以查找所有插件位置
cat ~/.claude/plugins/installed_plugins.json

# 6. 对于本地插件（isLocal: true），检查它们的源目录
# 解析 installed_plugins.json 并查找本地插件路径
```

**Important:** 检查每个来源。包括来自以下的 agent：
- Project `.claude/agents/`
- User's `~/.claude/agents/`
- compound-engineering plugin (but SKIP workflow/ agents - only use review/, research/, design/, docs/)
- ALL other installed plugins (agent-sdk-dev, frontend-design, etc.)
- Any local plugins

**特别针对 compound-engineering 插件：**
- 使用： `agents/review/*` (所有审查者)
- 使用： `agents/research/*` (所有研究人员)
- 使用： `agents/design/*` (设计 agent)
- 使用： `agents/docs/*` (文档 agent)
- 跳过： `agents/workflow/*` (这些是工作流编排器，不是审查者)

**步骤 2：对于每个发现的 agent，读取其描述**

读取每个 agent 文件的前几行以了解它审查/分析什么。

**步骤 3：并行启动所有 agent**

对于发现的每个 agent，并行启动一个任务：

```
Task [agent-name]: "使用您的专业知识审查此计划。应用您所有的检查和模式。计划内容： [完整计划 content]"
```

**关键规则：**
- 不要根据 "relevance" 运行它们全部
- Do NOT 跳过 agents because they "可能不适用" 让它们决定
- 在单个消息中使用多个任务工具调用启动所有 agent
- 20、30、40 个并行 agent 很好 - 使用所有
- 每个 agent 可能会捕获其他人遗漏的东西
- 目标是最大覆盖率，而不是效率

**步骤 4：还要发现并运行研究 agent**

研究 agent（如 `best-practices-researcher`, `framework-docs-researcher`, `git-history-analyzer`, `repo-research-analyst`) 也应该为相关计划部分运行。

### 6. Wait for ALL Agents and Synthesize Everything

<thinking>
Wait for ALL parallel agents to complete - skills, research agents, review agents, everything. Then synthesize all findings into a comprehensive enhancement.
</thinking>

**Collect outputs from ALL sources:**

1. **Skill-based sub-agents** - Each skill's full output (code examples, patterns, recommendations)
2. **Learnings/Solutions sub-agents** - Relevant documented 经验教训 from /workflows:compound
3. **Research agents** - Best practices, documentation, real-world examples
4. **Review agents** - All feedback from every reviewer (architecture, security, performance, simplicity, etc.)
5. **Context7 queries** - Framework documentation and patterns
6. **Web searches** - Current best practices and articles

**For each agent's findings, extract:**
- [ ] Concrete recommendations (actionable items)
- [ ] Code patterns and examples (copy-paste ready)
- [ ] Anti-patterns to avoid (warnings)
- [ ] 性能考虑 (metrics, benchmarks)
- [ ] Security considerations (vulnerabilities, mitigations)
- [ ] Edge cases discovered (handling strategies)
- [ ] Documentation links (references)
- [ ] Skill-specific patterns (from matched skills)
- [ ] Relevant 经验教训 (past solutions that apply - prevent repeating mistakes)

**Deduplicate and prioritize:**
- Merge similar recommendations from multiple agents
- Prioritize by impact (high-value improvements first)
- Flag conflicting advice for human review
- Group by plan section

### 7. Enhance Plan Sections

<thinking>
Merge research findings back into the plan, adding depth without changing the original structure.
</thinking>

**Enhancement format for each section:**

```markdown
## [Original Section Title]

[Original content preserved]

### Research Insights

**Best Practices:**
- [Concrete recommendation 1]
- [Concrete recommendation 2]

**Performance Considerations:**
- [Optimization opportunity]
- [Benchmark or metric to target]

**Implementation Details:**
```[language]
// Concrete code example from research
```

**Edge Cases:**
- [Edge case 1 and how to handle]
- [Edge case 2 and how to handle]

**References:**
- [Documentation URL 1]
- [Documentation URL 2]
```

### 8. Add Enhancement Summary

At the top of the plan, add a summary section:

```markdown
## Enhancement Summary

**Deepened on:** [Date]
**Sections enhanced:** [Count]
**Research agents used:** [List]

### Key Improvements
1. [Major improvement 1]
2. [Major improvement 2]
3. [Major improvement 3]

### New Considerations Discovered
- [Important finding 1]
- [Important finding 2]
```

### 9. Update Plan File

**Write the enhanced plan:**
- Preserve original filename
- Add `-deepened` suffix if user prefers a new file
- Update any timestamps or metadata

## Output Format

Update the plan file in place (or create `plans/<original-name>-deepened.md` if requested).

## Quality Checks

Before finalizing:
- [ ] All original content preserved
- [ ] Research insights clearly marked and attributed
- [ ] Code examples are syntactically correct
- [ ] Links are valid and relevant
- [ ] No contradictions between sections
- [ ] Enhancement summary accurately reflects changes

## Post-Enhancement Options

After writing the enhanced plan, use the **AskUserQuestion tool** to present these options:

**Question:** "Plan deepened at `[plan_path]`. What would you like to do next?"

**Options:**
1. **View diff** - Show what was added/changed
2. **Run `/plan_review`** - Get feedback from reviewers on enhanced plan
3. **Start `/workflows:work`** - Begin implementing this enhanced plan
4. **Deepen further** - Run another round of research on specific sections
5. **Revert** - Restore original plan (if backup exists)

Based on selection:
- **View diff** → Run `git diff [plan_path]` or show before/after
- **`/plan_review`** → Call the /plan_review command with the plan file path
- **`/workflows:work`** → Call the /workflows:work command with the plan file path
- **Deepen further** → Ask which sections need more research, then re-run those agents
- **Revert** → Restore from git or backup

## Example Enhancement

**Before (from /workflows:plan):**
```markdown
## Technical Approach

Use React Query for data fetching with optimistic updates.
```

**After (from /workflows:deepen-plan):**
```markdown
## Technical Approach

Use React Query for data fetching with optimistic updates.

### Research Insights

**Best Practices:**
- Configure `staleTime` and `cacheTime` based on data freshness requirements
- Use `queryKey` factories for consistent cache invalidation
- Implement error boundaries around query-dependent components

**Performance Considerations:**
- Enable `refetchOnWindowFocus: false` for stable data to reduce unnecessary requests
- Use `select` option to transform and memoize data at query level
- Consider `placeholderData` for instant perceived loading

**Implementation Details:**
```typescript
// Recommended query configuration
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      retry: 2,
      refetchOnWindowFocus: false,
    },
  },
});
```

**Edge Cases:**
- Handle race conditions with `cancelQueries` on component unmount
- Implement retry logic for transient network failures
- Consider offline support with `persistQueryClient`

**References:**
- https://tanstack.com/query/latest/docs/react/guides/optimistic-updates
- https://tkdodo.eu/blog/practical-react-query
```

NEVER CODE! Just research and enhance the plan.
