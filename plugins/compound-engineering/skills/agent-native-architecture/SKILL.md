---
name: agent-native-architecture
description: 构建将 Agent 视为一等公民的应用程序。当设计自主 Agent、创建 MCP 工具、实现自我修改系统，或构建功能由 Agent 在循环中实现的应用时使用此 Skill。
---

<why_now>
## 为什么是现在

软件 Agent 现在可以可靠地工作了。Claude Code 证明了一个具有 bash 和文件工具访问权限的 LLM，在循环中运行直到达成目标，可以自主完成复杂的多步骤任务。

令人惊讶的发现：**一个真正优秀的编码 Agent 实际上就是一个真正优秀的通用 Agent。**让 Claude Code 重构代码库的同一架构，也可以让 Agent 组织你的文件、管理你的阅读列表或自动化你的工作流程。

Claude Code SDK 使这一切变得可及。你可以构建这样的应用程序：功能不是你编写的代码——而是你描述的结果，由一个拥有工具的 Agent 在循环中运行直到达成结果。

这开启了一个新领域：以 Claude Code 工作方式运行的软件，应用于远超编码的各种类别。
</why_now>

<core_principles>
## 核心原则

### 1. 对等性（Parity）

**用户通过 UI 能做的任何事情，Agent 都应该能够通过工具实现。**

这是基础原则。没有它，其他一切都无关紧要。

想象你构建了一个笔记应用，有一个漂亮的界面用于创建、组织和标记笔记。用户向 Agent 询问："创建一条总结我的会议的笔记，并标记为紧急。"

如果你构建了创建笔记的 UI 但没有相应的 Agent 能力，Agent 就卡住了。它可能会道歉或询问澄清问题，但无法提供帮助——即使对于使用界面的人来说这个操作很简单。

**解决方案：**确保 Agent 拥有工具（或工具组合）可以完成 UI 能做的任何事情。

这不是要创建 UI 按钮到工具的 1:1 映射。而是要确保 Agent 能够**实现相同的结果**。有时是单个工具（`create_note`）。有时是组合原语（用适当的格式 `write_file` 到笔记目录）。

**规范：**在添加任何 UI 功能时，问：Agent 能实现这个结果吗？如果不能，添加必要的工具或原语。

能力映射表很有帮助：

| 用户操作 | Agent 如何实现 |
|-------------|----------------------|
| 创建笔记 | `write_file` 到笔记目录，或 `create_note` 工具 |
| 将笔记标记为紧急 | `update_file` 元数据，或 `tag_note` 工具 |
| 搜索笔记 | `search_files` 或 `search_notes` 工具 |
| 删除笔记 | `delete_file` 或 `delete_note` 工具 |

**测试：**选择用户可以在 UI 中执行的任何操作。向 Agent 描述它。它能完成这个结果吗？

---

### 2. 粒度（Granularity）

**优先使用原子原语。功能是 Agent 在循环中实现的结果。**

工具是原始能力：读取文件、写入文件、运行 bash 命令、存储记录、发送通知。

**功能**不是你编写的函数。它是你在 prompt 中描述的结果，由拥有工具的 Agent 在循环中运行直到达成结果。

**粒度较粗（限制 Agent）：**
```
Tool: classify_and_organize_files(files)
→ 你编写了决策逻辑
→ Agent 执行你的代码
→ 要改变行为，你需要重构
```

**粒度较细（赋能 Agent）：**
```
Tools: read_file, write_file, move_file, list_directory, bash
Prompt: "整理用户的下载文件夹。分析每个文件，
        根据内容和最近使用情况确定适当的位置，
        然后移动它们。"
Agent: 在循环中运行——读取文件、做出判断、移动文件、
       检查结果——直到文件夹被整理好。
→ Agent 做出决策
→ 要改变行为，你编辑 prompt
```

**关键转变：**Agent 正在凭借判断力追求结果，而不是执行编排好的序列。它可能遇到意外的文件类型、调整方法或询问澄清问题。循环继续直到达成结果。

你的工具越原子化，Agent 使用它们就越灵活。如果你将决策逻辑捆绑到工具中，你就把判断力移回了代码。

**测试：**要改变功能的行为，你是编辑文本还是重构代码？

---

### 3. 可组合性（Composability）

**有了原子工具和对等性，你可以仅通过编写新 prompt 来创建新功能。**

这是前两个原则的回报。当你的工具是原子化的，并且 Agent 可以做用户能做的任何事情时，新功能就只是新 prompt。

想要一个"每周回顾"功能来总结活动并建议优先事项？那就是一个 prompt：

```
"回顾本周修改的文件。总结关键变化。基于
未完成的项目和即将到来的截止日期，建议下周的三个优先事项。"
```

Agent 使用 `list_files`、`read_file` 及其判断力来完成这个任务。你没有编写每周回顾代码。你描述了一个结果，Agent 在循环中运行直到实现它。

**这对开发者和用户都有效。**你可以通过添加 prompt 来发布新功能。用户可以通过修改 prompt 或创建自己的 prompt 来自定义行为。"当我说'归档这个'时，总是将它移动到我的行动文件夹并标记为紧急"成为了扩展应用程序的用户级 prompt。

**约束：**这仅在工具足够原子化以便以你未预料的方式组合，并且 Agent 与用户具有对等性时才有效。如果工具编码了过多逻辑，或者 Agent 无法访问关键能力，组合就会崩溃。

**测试：**你能通过编写新的 prompt 部分来添加新功能，而无需添加新代码吗？

---

### 4. Emergent Capability

**The agent can accomplish things you didn't explicitly design for.**

When tools are atomic, parity is maintained, and prompts are composable, users will ask the agent for things you never anticipated. And often, the agent can figure it out.

*"Cross-reference my meeting notes with my task list and tell me what I've committed to but haven't scheduled."*

You didn't build a "commitment tracker" feature. But if the agent can read notes, read tasks, and reason about them—operating in a loop until it has an answer—it can accomplish this.

**This reveals latent demand.** Instead of guessing what features users want, you observe what they're asking the agent to do. When patterns emerge, you can optimize them with domain-specific tools or dedicated prompts. But you didn't have to anticipate them—you discovered them.

**The flywheel:**
1. Build with atomic tools and parity
2. Users ask for things you didn't anticipate
3. Agent composes tools to accomplish them (or fails, revealing a gap)
4. You observe patterns in what's being requested
5. Add domain tools or prompts to make common patterns efficient
6. Repeat

This changes how you build products. You're not trying to imagine every feature upfront. You're creating a capable foundation and learning from what emerges.

**The test:** Give the agent an open-ended request relevant to your domain. Can it figure out a reasonable approach, operating in a loop until it succeeds? If it just says "I don't have a feature for that," your architecture is too constrained.

---

### 5. Improvement Over Time

**Agent-native applications get better through accumulated context and prompt refinement.**

Unlike traditional software, agent-native applications can improve without shipping code:

**Accumulated context:** The agent can maintain state across sessions—what exists, what the user has done, what worked, what didn't. A `context.md` file the agent reads and updates is layer one. More sophisticated approaches involve structured memory and learned preferences.

**Prompt refinement at multiple levels:**
- **Developer level:** You ship updated prompts that change agent behavior for all users
- **User level:** Users customize prompts for their workflow
- **Agent level:** The agent modifies its own prompts based on feedback (advanced)

**Self-modification (advanced):** Agents that can edit their own prompts or even their own code. For production use cases, consider adding safety rails—approval gates, automatic checkpoints for rollback, health checks. This is where things are heading.

The improvement mechanisms are still being discovered. Context and prompt refinement are proven. Self-modification is emerging. What's clear: the architecture supports getting better in ways traditional software doesn't.

**The test:** Does the application work better after a month of use than on day one, even without code changes?
</core_principles>

<intake>
## What aspect of agent-native architecture do you need help with?

1. **Design architecture** - Plan a new agent-native system from scratch
2. **Files & workspace** - Use files as the universal interface, shared workspace patterns
3. **Tool design** - Build primitive tools, dynamic capability discovery, CRUD completeness
4. **Domain tools** - Know when to add domain tools vs stay with primitives
5. **Execution patterns** - Completion signals, partial completion, context limits
6. **System prompts** - Define agent behavior in prompts, judgment criteria
7. **Context injection** - Inject runtime app state into agent prompts
8. **Action parity** - Ensure agents can do everything users can do
9. **Self-modification** - Enable agents to safely evolve themselves
10. **Product design** - Progressive disclosure, latent demand, approval patterns
11. **Mobile patterns** - iOS storage, background execution, checkpoint/resume
12. **Testing** - Test agent-native apps for capability and parity
13. **Refactoring** - Make existing code more agent-native

**Wait for response before proceeding.**
</intake>

<routing>
| Response | Action |
|----------|--------|
| 1, "design", "architecture", "plan" | Read [architecture-patterns.md](./references/architecture-patterns.md), then apply Architecture Checklist below |
| 2, "files", "workspace", "filesystem" | Read [files-universal-interface.md](./references/files-universal-interface.md) and [shared-workspace-architecture.md](./references/shared-workspace-architecture.md) |
| 3, "tool", "mcp", "primitive", "crud" | Read [mcp-tool-design.md](./references/mcp-tool-design.md) |
| 4, "domain tool", "when to add" | Read [from-primitives-to-domain-tools.md](./references/from-primitives-to-domain-tools.md) |
| 5, "execution", "completion", "loop" | Read [agent-execution-patterns.md](./references/agent-execution-patterns.md) |
| 6, "prompt", "system prompt", "behavior" | Read [system-prompt-design.md](./references/system-prompt-design.md) |
| 7, "context", "inject", "runtime", "dynamic" | Read [dynamic-context-injection.md](./references/dynamic-context-injection.md) |
| 8, "parity", "ui action", "capability map" | Read [action-parity-discipline.md](./references/action-parity-discipline.md) |
| 9, "self-modify", "evolve", "git" | Read [self-modification.md](./references/self-modification.md) |
| 10, "product", "progressive", "approval", "latent demand" | Read [product-implications.md](./references/product-implications.md) |
| 11, "mobile", "ios", "android", "background", "checkpoint" | Read [mobile-patterns.md](./references/mobile-patterns.md) |
| 12, "test", "testing", "verify", "validate" | Read [agent-native-testing.md](./references/agent-native-testing.md) |
| 13, "review", "refactor", "existing" | Read [refactoring-to-prompt-native.md](./references/refactoring-to-prompt-native.md) |

**After reading the reference, apply those patterns to the user's specific context.**
</routing>

<architecture_checklist>
## Architecture Review Checklist

When designing an agent-native system, verify these **before implementation**:

### Core Principles
- [ ] **Parity:** Every UI action has a corresponding agent capability
- [ ] **Granularity:** Tools are primitives; features are prompt-defined outcomes
- [ ] **Composability:** New features can be added via prompts alone
- [ ] **Emergent Capability:** Agent can handle open-ended requests in your domain

### Tool Design
- [ ] **Dynamic vs Static:** For external APIs where agent should have full access, use Dynamic Capability Discovery
- [ ] **CRUD Completeness:** Every entity has create, read, update, AND delete
- [ ] **Primitives not Workflows:** Tools enable capability, don't encode business logic
- [ ] **API as Validator:** Use `z.string()` inputs when the API validates, not `z.enum()`

### Files & Workspace
- [ ] **Shared Workspace:** Agent and user work in same data space
- [ ] **context.md Pattern:** Agent reads/updates context file for accumulated knowledge
- [ ] **File Organization:** Entity-scoped directories with consistent naming

### Agent Execution
- [ ] **Completion Signals:** Agent has explicit `complete_task` tool (not heuristic detection)
- [ ] **Partial Completion:** Multi-step tasks track progress for resume
- [ ] **Context Limits:** Designed for bounded context from the start

### Context Injection
- [ ] **Available Resources:** System prompt includes what exists (files, data, types)
- [ ] **Available Capabilities:** System prompt documents tools with user vocabulary
- [ ] **Dynamic Context:** Context refreshes for long sessions (or provide `refresh_context` tool)

### UI Integration
- [ ] **Agent → UI:** Agent changes reflect in UI (shared service, file watching, or event bus)
- [ ] **No Silent Actions:** Agent writes trigger UI updates immediately
- [ ] **Capability Discovery:** Users can learn what agent can do

### Mobile (if applicable)
- [ ] **Checkpoint/Resume:** Handle iOS app suspension gracefully
- [ ] **iCloud Storage:** iCloud-first with local fallback for multi-device sync
- [ ] **Cost Awareness:** Model tier selection (Haiku/Sonnet/Opus)

**When designing architecture, explicitly address each checkbox in your plan.**
</architecture_checklist>

<quick_start>
## Quick Start: Build an Agent-Native Feature

**Step 1: Define atomic tools**
```typescript
const tools = [
  tool("read_file", "Read any file", { path: z.string() }, ...),
  tool("write_file", "Write any file", { path: z.string(), content: z.string() }, ...),
  tool("list_files", "List directory", { path: z.string() }, ...),
  tool("complete_task", "Signal task completion", { summary: z.string() }, ...),
];
```

**Step 2: Write behavior in the system prompt**
```markdown
## Your Responsibilities
When asked to organize content, you should:
1. Read existing files to understand the structure
2. Analyze what organization makes sense
3. Create/move files using your tools
4. Use your judgment about layout and formatting
5. Call complete_task when you're done

You decide the structure. Make it good.
```

**Step 3: Let the agent work in a loop**
```typescript
const result = await agent.run({
  prompt: userMessage,
  tools: tools,
  systemPrompt: systemPrompt,
  // Agent loops until it calls complete_task
});
```
</quick_start>

<reference_index>
## Reference Files

All references in `references/`:

**Core Patterns:**
- [architecture-patterns.md](./references/architecture-patterns.md) - Event-driven, unified orchestrator, agent-to-UI
- [files-universal-interface.md](./references/files-universal-interface.md) - Why files, organization patterns, context.md
- [mcp-tool-design.md](./references/mcp-tool-design.md) - Tool design, dynamic capability discovery, CRUD
- [from-primitives-to-domain-tools.md](./references/from-primitives-to-domain-tools.md) - When to add domain tools, graduating to code
- [agent-execution-patterns.md](./references/agent-execution-patterns.md) - Completion signals, partial completion, context limits
- [system-prompt-design.md](./references/system-prompt-design.md) - Features as prompts, judgment criteria

**Agent-Native Disciplines:**
- [dynamic-context-injection.md](./references/dynamic-context-injection.md) - Runtime context, what to inject
- [action-parity-discipline.md](./references/action-parity-discipline.md) - Capability mapping, parity workflow
- [shared-workspace-architecture.md](./references/shared-workspace-architecture.md) - Shared data space, UI integration
- [product-implications.md](./references/product-implications.md) - Progressive disclosure, latent demand, approval
- [agent-native-testing.md](./references/agent-native-testing.md) - Testing outcomes, parity tests

**Platform-Specific:**
- [mobile-patterns.md](./references/mobile-patterns.md) - iOS storage, checkpoint/resume, cost awareness
- [self-modification.md](./references/self-modification.md) - Git-based evolution, guardrails
- [refactoring-to-prompt-native.md](./references/refactoring-to-prompt-native.md) - Migrating existing code
</reference_index>

<anti_patterns>
## Anti-Patterns

### Common Approaches That Aren't Fully Agent-Native

These aren't necessarily wrong—they may be appropriate for your use case. But they're worth recognizing as different from the architecture this document describes.

**Agent as router** — The agent figures out what the user wants, then calls the right function. The agent's intelligence is used to route, not to act. This can work, but you're using a fraction of what agents can do.

**Build the app, then add agent** — You build features the traditional way (as code), then expose them to an agent. The agent can only do what your features already do. You won't get emergent capability.

**Request/response thinking** — Agent gets input, does one thing, returns output. This misses the loop: agent gets an outcome to achieve, operates until it's done, handles unexpected situations along the way.

**Defensive tool design** — You over-constrain tool inputs because you're used to defensive programming. Strict enums, validation at every layer. This is safe, but it prevents the agent from doing things you didn't anticipate.

**Happy path in code, agent just executes** — Traditional software handles edge cases in code—you write the logic for what happens when X goes wrong. Agent-native lets the agent handle edge cases with judgment. If your code handles all the edge cases, the agent is just a caller.

---

### Specific Anti-Patterns

**THE CARDINAL SIN: Agent executes your code instead of figuring things out**

```typescript
// WRONG - You wrote the workflow, agent just executes it
tool("process_feedback", async ({ message }) => {
  const category = categorize(message);      // Your code decides
  const priority = calculatePriority(message); // Your code decides
  await store(message, category, priority);   // Your code orchestrates
  if (priority > 3) await notify();           // Your code decides
});

// RIGHT - Agent figures out how to process feedback
tools: store_item, send_message  // Primitives
prompt: "Rate importance 1-5 based on actionability, store feedback, notify if >= 4"
```

**Workflow-shaped tools** — `analyze_and_organize` bundles judgment into the tool. Break it into primitives and let the agent compose them.

**Context starvation** — Agent doesn't know what resources exist in the app.
```
User: "Write something about Catherine the Great in my feed"
Agent: "What feed? I don't understand what system you're referring to."
```
Fix: Inject available resources, capabilities, and vocabulary into system prompt.

**Orphan UI actions** — User can do something through the UI that the agent can't achieve. Fix: maintain parity.

**Silent actions** — Agent changes state but UI doesn't update. Fix: Use shared data stores with reactive binding, or file system observation.

**Heuristic completion detection** — Detecting agent completion through heuristics (consecutive iterations without tool calls, checking for expected output files). This is fragile. Fix: Require agents to explicitly signal completion through a `complete_task` tool.

**Static tool mapping for dynamic APIs** — Building 50 tools for 50 API endpoints when a `discover` + `access` pattern would give more flexibility.
```typescript
// WRONG - Every API type needs a hardcoded tool
tool("read_steps", ...)
tool("read_heart_rate", ...)
tool("read_sleep", ...)
// When glucose tracking is added... code change required

// RIGHT - Dynamic capability discovery
tool("list_available_types", ...)  // Discover what's available
tool("read_health_data", { dataType: z.string() }, ...)  // Access any type
```

**Incomplete CRUD** — Agent can create but not update or delete.
```typescript
// User: "Delete that journal entry"
// Agent: "I don't have a tool for that"
tool("create_journal_entry", ...)  // Missing: update, delete
```
Fix: Every entity needs full CRUD.

**Sandbox isolation** — Agent works in separate data space from user.
```
Documents/
├── user_files/        ← User's space
└── agent_output/      ← Agent's space (isolated)
```
Fix: Use shared workspace where both operate on same files.

**Gates without reason** — Domain tool is the only way to do something, and you didn't intend to restrict access. The default is open. Keep primitives available unless there's a specific reason to gate.

**Artificial capability limits** — Restricting what the agent can do out of vague safety concerns rather than specific risks. Be thoughtful about restricting capabilities. The agent should generally be able to do what users can do.
</anti_patterns>

<success_criteria>
## Success Criteria

You've built an agent-native application when:

### Architecture
- [ ] The agent can achieve anything users can achieve through the UI (parity)
- [ ] Tools are atomic primitives; domain tools are shortcuts, not gates (granularity)
- [ ] New features can be added by writing new prompts (composability)
- [ ] The agent can accomplish tasks you didn't explicitly design for (emergent capability)
- [ ] Changing behavior means editing prompts, not refactoring code

### Implementation
- [ ] System prompt includes dynamic context about app state
- [ ] Every UI action has a corresponding agent tool (action parity)
- [ ] Agent tools are documented in system prompt with user vocabulary
- [ ] Agent and user work in the same data space (shared workspace)
- [ ] Agent actions are immediately reflected in the UI
- [ ] Every entity has full CRUD (Create, Read, Update, Delete)
- [ ] Agents explicitly signal completion (no heuristic detection)
- [ ] context.md or equivalent for accumulated knowledge

### Product
- [ ] Simple requests work immediately with no learning curve
- [ ] Power users can push the system in unexpected directions
- [ ] You're learning what users want by observing what they ask the agent to do
- [ ] Approval requirements match stakes and reversibility

### Mobile (if applicable)
- [ ] Checkpoint/resume handles app interruption
- [ ] iCloud-first storage with local fallback
- [ ] Background execution uses available time wisely
- [ ] Model tier matched to task complexity

---

### The Ultimate Test

**Describe an outcome to the agent that's within your application's domain but that you didn't build a specific feature for.**

Can it figure out how to accomplish it, operating in a loop until it succeeds?

If yes, you've built something agent-native.

If it says "I don't have a feature for that"—your architecture is still too constrained.
</success_criteria>
