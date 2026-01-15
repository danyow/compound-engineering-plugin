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

### 4. 涌现能力

**Agent 可以完成你没有明确设计的功能。**

当工具是原子化的，保持对等性，并且 prompt 是可组合的时，用户会向 Agent 询问你从未预料到的事情。而通常，Agent 能够解决这些问题。

*"将我的会议笔记与任务列表交叉引用，告诉我承诺了但还没安排的事项。"*

你没有构建"承诺跟踪"功能。但如果 Agent 可以阅读笔记、阅读任务，并对它们进行推理——在循环中运行直到有答案——它就能完成这个任务。

**这揭示了潜在需求。**你不需要猜测用户想要什么功能，而是观察他们要求 Agent 做什么。当模式出现时，你可以用特定领域的工具或专用 prompt 来优化它们。但你不必预先设想它们——你是从实践中发现它们。

**飞轮效应：**
1. 使用原子工具和对等性构建
2. 用户询问你未预料的事情
3. Agent 组合工具来完成它们（或失败，揭示差距）
4. 你观察被请求的模式
5. 添加领域工具或 prompt 使常见模式更高效
6. 重复

这改变了你构建产品的方式。你不是试图预先想象每个功能。你是在创建一个有能力的基础，并从涌现的内容中学习。

**测试：**给 Agent 一个与你的领域相关的开放式请求。它能找出合理的方法，在循环中运行直到成功吗？如果它只是说"我没有这个功能"，你的架构就过于受限了。

---

### 5. 持续改进

**Agent 原生应用通过积累的上下文和 prompt 优化而不断改进。**

与传统软件不同，Agent 原生应用可以在不发布代码的情况下改进：

**积累的上下文：**Agent 可以在会话之间维护状态——存在什么、用户做了什么、什么有效、什么无效。Agent 读取和更新的 `context.md` 文件是第一层。更复杂的方法涉及结构化记忆和学习的偏好。

**多层次的 Prompt 优化：**
- **开发者层面：**你发布更新的 prompt，改变所有用户的 Agent 行为
- **用户层面：**用户为其工作流程自定义 prompt
- **Agent 层面：**Agent 根据反馈修改自己的 prompt（高级）

**自我修改（高级）：**Agent 可以编辑自己的 prompt 甚至自己的代码。对于生产用例，考虑添加安全护栏——审批门槛、自动检查点用于回滚、健康检查。这是未来的方向。

改进机制仍在被发现。上下文和 prompt 优化已被证明有效。自我修改正在出现。可以肯定的是：该架构支持以传统软件无法实现的方式变得更好。

**测试：**使用一个月后，即使没有代码更改，应用程序的工作效果是否比第一天更好？
</core_principles>

<intake>
## 你需要关于 Agent 原生架构哪方面的帮助？

1. **设计架构** - 从头规划新的 Agent 原生系统
2. **文件与工作空间** - 使用文件作为通用接口、共享工作空间模式
3. **工具设计** - 构建原始工具、动态能力发现、CRUD 完整性
4. **领域工具** - 了解何时添加领域工具与保持原语
5. **执行模式** - 完成信号、部分完成、上下文限制
6. **系统 Prompt** - 在 prompt 中定义 Agent 行为、判断标准
7. **上下文注入** - 将运行时应用状态注入 Agent prompt
8. **操作对等性** - 确保 Agent 可以做用户能做的一切
9. **自我修改** - 使 Agent 能够安全地演进自己
10. **产品设计** - 渐进式披露、潜在需求、审批模式
11. **移动端模式** - iOS 存储、后台执行、检查点/恢复
12. **测试** - 测试 Agent 原生应用的能力和对等性
13. **重构** - 使现有代码更 Agent 原生化

**等待响应后再继续。**
</intake>

<routing>
| 响应 | 操作 |
|----------|--------|
| 1, "design", "architecture", "plan" | 阅读 [architecture-patterns.md](./references/architecture-patterns.md)，然后应用下面的架构检查清单 |
| 2, "files", "workspace", "filesystem" | 阅读 [files-universal-interface.md](./references/files-universal-interface.md) 和 [shared-workspace-architecture.md](./references/shared-workspace-architecture.md) |
| 3, "tool", "mcp", "primitive", "crud" | 阅读 [mcp-tool-design.md](./references/mcp-tool-design.md) |
| 4, "domain tool", "when to add" | 阅读 [from-primitives-to-domain-tools.md](./references/from-primitives-to-domain-tools.md) |
| 5, "execution", "completion", "loop" | 阅读 [agent-execution-patterns.md](./references/agent-execution-patterns.md) |
| 6, "prompt", "system prompt", "behavior" | 阅读 [system-prompt-design.md](./references/system-prompt-design.md) |
| 7, "context", "inject", "runtime", "dynamic" | 阅读 [dynamic-context-injection.md](./references/dynamic-context-injection.md) |
| 8, "parity", "ui action", "capability map" | 阅读 [action-parity-discipline.md](./references/action-parity-discipline.md) |
| 9, "self-modify", "evolve", "git" | 阅读 [self-modification.md](./references/self-modification.md) |
| 10, "product", "progressive", "approval", "latent demand" | 阅读 [product-implications.md](./references/product-implications.md) |
| 11, "mobile", "ios", "android", "background", "checkpoint" | 阅读 [mobile-patterns.md](./references/mobile-patterns.md) |
| 12, "test", "testing", "verify", "validate" | 阅读 [agent-native-testing.md](./references/agent-native-testing.md) |
| 13, "review", "refactor", "existing" | 阅读 [refactoring-to-prompt-native.md](./references/refactoring-to-prompt-native.md) |

**阅读参考资料后，将这些模式应用到用户的具体情境中。**
</routing>

<architecture_checklist>
## 架构审查检查清单

在设计 Agent 原生系统时，在**实施前**验证这些项目：

### 核心原则
- [ ] **对等性：**每个 UI 操作都有相应的 Agent 能力
- [ ] **粒度：**工具是原语；功能是 prompt 定义的结果
- [ ] **可组合性：**新功能可以仅通过 prompt 添加
- [ ] **涌现能力：**Agent 可以处理你领域内的开放式请求

### 工具设计
- [ ] **动态 vs 静态：**对于 Agent 应该完全访问的外部 API，使用动态能力发现
- [ ] **CRUD 完整性：**每个实体都有创建、读取、更新和删除
- [ ] **原语而非工作流：**工具启用能力，不编码业务逻辑
- [ ] **API 作为验证器：**当 API 验证时使用 `z.string()` 输入，而非 `z.enum()`

### 文件与工作空间
- [ ] **共享工作空间：**Agent 和用户在相同的数据空间工作
- [ ] **context.md 模式：**Agent 读取/更新上下文文件以积累知识
- [ ] **文件组织：**实体范围的目录，命名一致

### Agent 执行
- [ ] **完成信号：**Agent 有明确的 `complete_task` 工具（不是启发式检测）
- [ ] **部分完成：**多步骤任务跟踪进度以便恢复
- [ ] **上下文限制：**从一开始就设计为有界上下文

### 上下文注入
- [ ] **可用资源：**系统 prompt 包括存在什么（文件、数据、类型）
- [ ] **可用能力：**系统 prompt 用用户词汇记录工具
- [ ] **动态上下文：**长会话的上下文刷新（或提供 `refresh_context` 工具）

### UI 集成
- [ ] **Agent → UI：**Agent 更改反映在 UI 中（共享服务、文件监视或事件总线）
- [ ] **无静默操作：**Agent 写入触发 UI 立即更新
- [ ] **能力发现：**用户可以了解 Agent 能做什么

### 移动端（如适用）
- [ ] **检查点/恢复：**优雅处理 iOS 应用挂起
- [ ] **iCloud 存储：**iCloud 优先，本地回退以实现多设备同步
- [ ] **成本意识：**模型层级选择（Haiku/Sonnet/Opus）

**设计架构时，在你的计划中明确处理每个复选框。**
</architecture_checklist>

<quick_start>
## 快速开始：构建 Agent 原生功能

**步骤 1：定义原子工具**
```typescript
const tools = [
  tool("read_file", "Read any file", { path: z.string() }, ...),
  tool("write_file", "Write any file", { path: z.string(), content: z.string() }, ...),
  tool("list_files", "List directory", { path: z.string() }, ...),
  tool("complete_task", "Signal task completion", { summary: z.string() }, ...),
];
```

**步骤 2：在系统 prompt 中编写行为**
```markdown
## 你的职责
当被要求组织内容时，你应该：
1. 阅读现有文件以了解结构
2. 分析什么样的组织方式合理
3. 使用你的工具创建/移动文件
4. 运用你的判断力决定布局和格式
5. 完成后调用 complete_task

你决定结构。做好它。
```

**步骤 3：让 Agent 在循环中工作**
```typescript
const result = await agent.run({
  prompt: userMessage,
  tools: tools,
  systemPrompt: systemPrompt,
  // Agent 循环直到调用 complete_task
});
```
</quick_start>

<reference_index>
## 参考文件

所有参考资料在 `references/` 目录：

**核心模式：**
- [architecture-patterns.md](./references/architecture-patterns.md) - 事件驱动、统一编排器、Agent 到 UI
- [files-universal-interface.md](./references/files-universal-interface.md) - 为什么使用文件、组织模式、context.md
- [mcp-tool-design.md](./references/mcp-tool-design.md) - 工具设计、动态能力发现、CRUD
- [from-primitives-to-domain-tools.md](./references/from-primitives-to-domain-tools.md) - 何时添加领域工具、升级到代码
- [agent-execution-patterns.md](./references/agent-execution-patterns.md) - 完成信号、部分完成、上下文限制
- [system-prompt-design.md](./references/system-prompt-design.md) - 作为 prompt 的功能、判断标准

**Agent 原生准则：**
- [dynamic-context-injection.md](./references/dynamic-context-injection.md) - 运行时上下文、注入什么
- [action-parity-discipline.md](./references/action-parity-discipline.md) - 能力映射、对等性工作流
- [shared-workspace-architecture.md](./references/shared-workspace-architecture.md) - 共享数据空间、UI 集成
- [product-implications.md](./references/product-implications.md) - 渐进式披露、潜在需求、审批
- [agent-native-testing.md](./references/agent-native-testing.md) - 测试结果、对等性测试

**平台特定：**
- [mobile-patterns.md](./references/mobile-patterns.md) - iOS 存储、检查点/恢复、成本意识
- [self-modification.md](./references/self-modification.md) - 基于 Git 的演进、护栏
- [refactoring-to-prompt-native.md](./references/refactoring-to-prompt-native.md) - 迁移现有代码
</reference_index>

<anti_patterns>
## 反模式

### 不完全 Agent 原生的常见方法

这些方法不一定是错误的——它们可能适合你的用例。但值得认识到它们与本文档描述的架构不同。

**Agent 作为路由器** — Agent 弄清楚用户想要什么，然后调用正确的函数。Agent 的智能用于路由，而不是行动。这可以工作，但你只使用了 Agent 能力的一小部分。

**先构建应用，再添加 Agent** — 你以传统方式（作为代码）构建功能，然后将它们暴露给 Agent。Agent 只能做你的功能已经做的事情。你不会获得涌现能力。

**请求/响应思维** — Agent 获取输入，做一件事，返回输出。这错过了循环：Agent 获得要实现的结果，运行直到完成，沿途处理意外情况。

**防御性工具设计** — 你过度约束工具输入，因为你习惯了防御性编程。严格的枚举，每一层都有验证。这是安全的，但它阻止了 Agent 做你没有预料到的事情。

**快乐路径在代码中，Agent 只是执行** — 传统软件在代码中处理边缘情况——你编写当 X 出错时发生什么的逻辑。Agent 原生让 Agent 用判断力处理边缘情况。如果你的代码处理所有边缘情况，Agent 只是一个调用者。

---

### 具体反模式

**原罪：Agent 执行你的代码而不是自己想办法**

```typescript
// 错误 - 你编写了工作流，Agent 只是执行它
tool("process_feedback", async ({ message }) => {
  const category = categorize(message);      // 你的代码决定
  const priority = calculatePriority(message); // 你的代码决定
  await store(message, category, priority);   // 你的代码编排
  if (priority > 3) await notify();           // 你的代码决定
});

// 正确 - Agent 弄清楚如何处理反馈
tools: store_item, send_message  // 原语
prompt: "根据可操作性评估重要性 1-5，存储反馈，如果 >= 4 则通知"
```

**工作流形状的工具** — `analyze_and_organize` 将判断捆绑到工具中。将其分解为原语，让 Agent 组合它们。

**上下文匮乏** — Agent 不知道应用中存在什么资源。
```
用户："在我的 feed 中写一些关于凯瑟琳大帝的内容"
Agent："什么 feed？我不理解你指的是什么系统。"
```
修复：将可用资源、能力和词汇注入系统 prompt。

**孤立的 UI 操作** — 用户可以通过 UI 做某事，但 Agent 无法实现。修复：保持对等性。

**静默操作** — Agent 改变状态但 UI 不更新。修复：使用带响应式绑定的共享数据存储，或文件系统观察。

**启发式完成检测** — 通过启发式方法检测 Agent 完成（连续迭代无工具调用，检查预期输出文件）。这很脆弱。修复：要求 Agent 通过 `complete_task` 工具明确发出完成信号。

**动态 API 的静态工具映射** — 为 50 个 API 端点构建 50 个工具，而 `discover` + `access` 模式会提供更多灵活性。
```typescript
// 错误 - 每个 API 类型都需要硬编码工具
tool("read_steps", ...)
tool("read_heart_rate", ...)
tool("read_sleep", ...)
// 当添加葡萄糖跟踪时...需要代码更改

// 正确 - 动态能力发现
tool("list_available_types", ...)  // 发现可用内容
tool("read_health_data", { dataType: z.string() }, ...)  // 访问任何类型
```

**不完整的 CRUD** — Agent 可以创建但不能更新或删除。
```typescript
// 用户："删除那条日志条目"
// Agent："我没有这个工具"
tool("create_journal_entry", ...)  // 缺失：update、delete
```
修复：每个实体都需要完整的 CRUD。

**沙箱隔离** — Agent 在与用户分离的数据空间中工作。
```
Documents/
├── user_files/        ← 用户的空间
└── agent_output/      ← Agent 的空间（隔离）
```
修复：使用共享工作空间，双方操作相同的文件。

**无理由的门控** — 领域工具是做某事的唯一方式，而你并不打算限制访问。默认是开放的。保持原语可用，除非有特定原因要门控。

**人为的能力限制** — 出于模糊的安全担忧而不是特定风险来限制 Agent 能做什么。要深思熟虑地限制能力。Agent 通常应该能够做用户能做的事情。
</anti_patterns>

<success_criteria>
## 成功标准

当你构建了一个 Agent 原生应用时：

### 架构
- [ ] Agent 可以实现用户通过 UI 能实现的任何事情（对等性）
- [ ] 工具是原子原语；领域工具是快捷方式，而非门控（粒度）
- [ ] 新功能可以通过编写新 prompt 添加（可组合性）
- [ ] Agent 可以完成你没有明确设计的任务（涌现能力）
- [ ] 改变行为意味着编辑 prompt，而非重构代码

### 实施
- [ ] 系统 prompt 包含关于应用状态的动态上下文
- [ ] 每个 UI 操作都有相应的 Agent 工具（操作对等性）
- [ ] Agent 工具在系统 prompt 中用用户词汇记录
- [ ] Agent 和用户在相同的数据空间工作（共享工作空间）
- [ ] Agent 操作立即反映在 UI 中
- [ ] 每个实体都有完整的 CRUD（创建、读取、更新、删除）
- [ ] Agent 明确发出完成信号（无启发式检测）
- [ ] context.md 或等效方式用于积累知识

### 产品
- [ ] 简单请求立即工作，无学习曲线
- [ ] 高级用户可以将系统推向意外方向
- [ ] 你通过观察用户要求 Agent 做什么来了解用户想要什么
- [ ] 审批要求与风险和可逆性匹配

### 移动端（如适用）
- [ ] 检查点/恢复处理应用中断
- [ ] iCloud 优先存储，本地回退
- [ ] 后台执行明智地使用可用时间
- [ ] 模型层级与任务复杂度匹配

---

### 终极测试

**向 Agent 描述一个在你的应用领域内但你没有为其构建特定功能的结果。**

它能想出如何完成它，在循环中运行直到成功吗？

如果可以，你已经构建了 Agent 原生的东西。

如果它说"我没有这个功能"——你的架构仍然过于受限。
</success_criteria>
