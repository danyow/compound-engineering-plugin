<overview>
用于构建强大 Agent 循环的执行模式。涵盖 Agent 如何信号完成、跟踪部分进度以支持恢复、选择合适的模型层级以及处理上下文限制。
</overview>

<completion_signals>
## 完成信号

Agent 需要一个明确的方式来表示"我完成了"。

### 反面模式：启发式检测

通过启发式检测完成是脆弱的：

- 连续迭代没有工具调用
- 检查预期的输出文件
- 跟踪"无进度"状态
- 基于时间的超时

这些方法在边界情况下会失败并创建不可预测的行为。

### 模式：显式完成工具

提供一个 `complete_task` 工具，它：
- 接受完成工作的总结
- 返回一个停止循环的信号
- 在所有 Agent 类型中工作方式相同

```typescript
tool("complete_task", {
  summary: z.string().describe("Summary of what was accomplished"),
  status: z.enum(["success", "partial", "blocked"]).optional(),
}, async ({ summary, status = "success" }) => {
  return {
    text: summary,
    shouldContinue: false,  // 关键：信号循环应该停止
  };
});
```

### ToolResult 模式

构建工具结果以将成功与继续分开：

```swift
struct ToolResult {
    let success: Bool           // 工具是否成功？
    let output: String          // 发生了什么？
    let shouldContinue: Bool    // Agent 循环应该继续吗？
}

// 三个常见情况：
extension ToolResult {
    static func success(_ output: String) -> ToolResult {
        // 工具成功，继续进行
        ToolResult(success: true, output: output, shouldContinue: true)
    }

    static func error(_ message: String) -> ToolResult {
        // 工具失败但可恢复，Agent 可以尝试其他方法
        ToolResult(success: false, output: message, shouldContinue: true)
    }

    static func complete(_ summary: String) -> ToolResult {
        // 任务完成，停止循环
        ToolResult(success: true, output: summary, shouldContinue: false)
    }
}
```

### 关键洞察

**这不同于成功/失败：**

- 一个工具可以**成功**且**信号停止**（任务完成）
- 一个工具可以**失败**且**信号继续**（可恢复错误，尝试其他方法）

```typescript
// 示例：
read_file("/missing.txt")
// → { success: false, output: "File not found", shouldContinue: true }
// Agent 可以尝试不同的文件或寻求澄清

complete_task("Organized all downloads into folders")
// → { success: true, output: "...", shouldContinue: false }
// Agent 完成了

write_file("/output.md", content)
// → { success: true, output: "Wrote file", shouldContinue: true }
// Agent 继续朝着目标工作
```

### 系统提示指导

告诉 Agent 何时完成：

```markdown
## 完成任务

当你完成了用户的请求时：
1. 验证你的工作（重新读取你创建的文件，检查结果）
2. 调用 `complete_task` 并提供你所做工作的总结
3. 不要在目标达成后继续工作

如果你遇到阻碍且无法继续：
- 调用 `complete_task`，状态设为 "blocked"，并解释原因
- 不要无限循环尝试相同的事情
```
</completion_signals>

<partial_completion>
## 部分完成

对于多步任务，在任务级别跟踪进度以支持恢复能力。

### 任务状态跟踪

```swift
enum TaskStatus {
    case pending      // 尚未开始
    case inProgress   // 目前正在进行
    case completed    // 成功完成
    case failed       // 无法完成（带原因）
    case skipped      // 有意未完成
}

struct AgentTask {
    let id: String
    let description: String
    var status: TaskStatus
    var notes: String?  // 失败原因，已完成的内容
}

struct AgentSession {
    var tasks: [AgentTask]

    var isComplete: Bool {
        tasks.allSatisfy { $0.status == .completed || $0.status == .skipped }
    }

    var progress: (completed: Int, total: Int) {
        let done = tasks.filter { $0.status == .completed }.count
        return (done, tasks.count)
    }
}
```

### UI 进度显示

向用户显示发生了什么：

```
进度：3/5 任务完成 (60%)
✅ [1] 查找源材料
✅ [2] 下载全文
✅ [3] 提取关键段落
❌ [4] 生成摘要 - 错误：超出上下文限制
⏳ [5] 创建大纲 - 待处理
```

### 部分完成场景

**Agent 在完成前达到最大迭代次数：**
- 某些任务已完成，某些待处理
- 已保存 Checkpoint 并记录当前状态
- 恢复从中断处继续，而不是从头开始

**Agent 在某个任务上失败：**
- 任务标记为 `.failed`，在 notes 中记录错误
- 其他任务可能继续（由 Agent 决定）
- Orchestrator 不会自动中止整个会话

**网络错误在任务中途发生：**
- 当前迭代抛出异常
- 会话标记为 `.failed`
- Checkpoint 保留该点之前的所有消息
- 可从 Checkpoint 恢复

### Checkpoint 结构

```swift
struct AgentCheckpoint: Codable {
    let sessionId: String
    let agentType: String
    let messages: [Message]          // 完整的对话历史
    let iterationCount: Int
    let tasks: [AgentTask]           // 任务状态
    let customState: [String: Any]   // 特定于 Agent 的状态
    let timestamp: Date

    var isValid: Bool {
        // Checkpoint 会过期（默认 1 小时）
        Date().timeIntervalSince(timestamp) < 3600
    }
}
```

### 恢复流程

1. 在应用启动时扫描有效的 Checkpoint
2. 向用户显示："你有一个未完成的会话。是否恢复？"
3. 恢复时：
   - 将消息恢复到对话中
   - 恢复任务状态
   - 从中断处继续 Agent 循环
4. 忽略时：
   - 删除 Checkpoint
   - 如果用户再次尝试，则重新开始
</partial_completion>

<model_tier_selection>
## 模型层级选择

不同的 Agent 需要不同的智能水平。使用能够达到成果的最便宜的模型。

### 层级指南

| Agent 类型 | 推荐层级 | 原因 |
|------------|---------|------|
| 聊天/对话 | 平衡 (Sonnet) | 快速响应，良好推理能力 |
| 研究 | 平衡 (Sonnet) | 工具循环，不是超复杂综合 |
| 内容生成 | 平衡 (Sonnet) | 创意工作但不需要大量综合 |
| 复杂分析 | 强大 (Opus) | 多文档综合，微妙判断 |
| 概要生成 | 强大 (Opus) | 照片分析，复杂模式识别 |
| 快速查询 | 快速 (Haiku) | 简单查询，快速转换 |
| 简单分类 | 快速 (Haiku) | 高容量，简单决策 |

### 实现

```swift
enum ModelTier {
    case fast      // claude-3-haiku: 快速、便宜、简单任务
    case balanced  // claude-sonnet: 大多数任务的良好平衡
    case powerful  // claude-opus: 复杂推理、综合

    var modelId: String {
        switch self {
        case .fast: return "claude-3-haiku-20240307"
        case .balanced: return "claude-sonnet-4-20250514"
        case .powerful: return "claude-opus-4-20250514"
        }
    }
}

struct AgentConfig {
    let name: String
    let modelTier: ModelTier
    let tools: [AgentTool]
    let systemPrompt: String
    let maxIterations: Int
}

// 示例
let researchConfig = AgentConfig(
    name: "research",
    modelTier: .balanced,
    tools: researchTools,
    systemPrompt: researchPrompt,
    maxIterations: 20
)

let quickLookupConfig = AgentConfig(
    name: "lookup",
    modelTier: .fast,
    tools: [readLibrary],
    systemPrompt: "Answer quick questions about the user's library.",
    maxIterations: 3
)
```

### 成本优化策略

1. **从平衡开始，如果质量不足则升级**
2. **对工具密集型循环使用快速层级**，每次转换都很简单
3. **为综合任务保留强大层级**（比较多个来源）
4. **考虑每次转换的令牌限制**以控制成本
5. **缓存昂贵操作**以避免重复调用
</model_tier_selection>

<context_limits>
## 上下文限制

Agent 会话可以无限期延伸，但上下文窗口则不行。从一开始就为有界上下文进行设计。

### 问题

```
第 1 轮：用户提问 → 500 令牌
第 2 轮：Agent 读取文件 → 10,000 令牌
第 3 轮：Agent 读取另一个文件 → 10,000 令牌
第 4 轮：Agent 研究 → 20,000 令牌
...
第 10 轮：超出上下文窗口
```

### 设计原则

**1. 工具应该支持迭代优化**

不是全有或全无，而是为总结 → 详情 → 完整进行设计：

```typescript
// 良好：支持迭代优化
tool("read_file", {
  path: z.string(),
  preview: z.boolean().default(true),  // 默认返回前 1000 个字符
  full: z.boolean().default(false),    // 选择性接收完整内容
}, ...);

tool("search_files", {
  query: z.string(),
  summaryOnly: z.boolean().default(true),  // 返回匹配项，不是完整文件
}, ...);
```

**2. 提供整合工具**

给 Agent 一个在会话中途整合学习的方式：

```typescript
tool("summarize_and_continue", {
  keyPoints: z.array(z.string()),
  nextSteps: z.array(z.string()),
}, async ({ keyPoints, nextSteps }) => {
  // 存储总结，可能截断较早的消息
  await saveSessionSummary({ keyPoints, nextSteps });
  return { text: "Summary saved. Continuing with focus on: " + nextSteps.join(", ") };
});
```

**3. 为截断进行设计**

假设 Orchestrator 可能截断早期消息。重要上下文应该：
- 在系统提示中（始终存在）
- 在文件中（可以重新读取）
- 在 context.md 中总结

### 实现策略

```swift
class AgentOrchestrator {
    let maxContextTokens = 100_000
    let targetContextTokens = 80_000  // 留出空间

    func shouldTruncate() -> Bool {
        estimateTokens(messages) > targetContextTokens
    }

    func truncateIfNeeded() {
        if shouldTruncate() {
            // 保留系统提示 + 最近的消息
            // 总结或删除较早的消息
            messages = [systemMessage] + summarizeOldMessages() + recentMessages
        }
    }
}
```

### 系统提示指导

```markdown
## 管理上下文

对于长任务，定期整合你学到的内容：
1. 如果你收集了大量信息，总结关键点
2. 将重要发现保存到文件（超越上下文持久存在）
3. 如果对话变得太长，使用 `summarize_and_continue`

不要试图把所有东西都保存在内存中。把它写下来。
```
</context_limits>

<orchestrator_pattern>
## 统一 Agent Orchestrator

一个执行引擎，多种 Agent 类型。所有 Agent 使用相同的 Orchestrator，只是配置不同。

```swift
class AgentOrchestrator {
    static let shared = AgentOrchestrator()

    func run(config: AgentConfig, userMessage: String) async -> AgentResult {
        var messages: [Message] = [
            .system(config.systemPrompt),
            .user(userMessage)
        ]

        var iteration = 0

        while iteration < config.maxIterations {
            // 获取 Agent 响应
            let response = await claude.message(
                model: config.modelTier.modelId,
                messages: messages,
                tools: config.tools
            )

            messages.append(.assistant(response))

            // 处理工具调用
            for toolCall in response.toolCalls {
                let result = await executeToolCall(toolCall, config: config)
                messages.append(.toolResult(result))

                // 检查完成信号
                if !result.shouldContinue {
                    return AgentResult(
                        status: .completed,
                        output: result.output,
                        iterations: iteration + 1
                    )
                }
            }

            // 无工具调用 = Agent 正在响应，可能完成了
            if response.toolCalls.isEmpty {
                // 可能完成，或等待用户
                break
            }

            iteration += 1
        }

        return AgentResult(
            status: iteration >= config.maxIterations ? .maxIterations : .responded,
            output: messages.last?.content ?? "",
            iterations: iteration
        )
    }
}
```

### 优点

- 所有 Agent 类型的一致生命周期管理
- 自动 Checkpoint/恢复（对移动端至关重要）
- 共享工具协议
- 易于添加新 Agent 类型
- 集中式错误处理和日志
</orchestrator_pattern>

<checklist>
## Agent 执行检查清单

### 完成信号
- [ ] 提供 `complete_task` 工具（显式完成）
- [ ] 没有启发式完成检测
- [ ] 工具结果包含 `shouldContinue` 标志
- [ ] 系统提示指导何时完成

### 部分完成
- [ ] 任务通过状态跟踪（待处理、进行中、已完成、失败）
- [ ] 为恢复保存 Checkpoint
- [ ] 进度对用户可见
- [ ] 恢复从中断处继续

### 模型层级
- [ ] 层级基于任务复杂度选择
- [ ] 考虑成本优化
- [ ] 快速层级用于简单操作
- [ ] 强大层级保留用于综合

### 上下文限制
- [ ] 工具支持迭代优化（预览 vs 完整）
- [ ] 提供整合机制
- [ ] 重要上下文持久保存到文件
- [ ] 定义截断策略
</checklist>
