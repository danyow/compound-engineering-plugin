<overview>
用于构建Agent原生系统的架构模式。这些模式源于五个核心原则：平等性、粒度、可组合性、涌现能力和持续改进。

功能是Agent在循环中实现的结果，而不是你编写的函数。Tool是原子级别的原始操作。Agent应用判断力；提示语定义结果。

另见:
- [files-universal-interface.md](./files-universal-interface.md) 用于文件组织和context.md模式
- [agent-execution-patterns.md](./agent-execution-patterns.md) 用于完成信号和部分完成
- [product-implications.md](./product-implications.md) 用于渐进式披露和批准模式
</overview>

<pattern name="event-driven-agent">
## 事件驱动Agent架构

Agent作为一个长期运行的进程运行，响应事件。事件变成提示语。

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent Loop                                │
├─────────────────────────────────────────────────────────────┤
│  Event Source → Agent (Claude) → Tool Calls → Response      │
└─────────────────────────────────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
    ┌─────────┐    ┌──────────┐    ┌───────────┐
    │ Content │    │   Self   │    │   Data    │
    │  Tools  │    │  Tools   │    │   Tools   │
    └─────────┘    └──────────┘    └───────────┘
    (write_file)   (read_source)   (store_item)
                   (restart)       (list_items)
```

**关键特点：**
- 事件（消息、webhooks、定时器）触发Agent轮次
- Agent根据系统提示语决定如何响应
- Tool是IO的原始操作，不是业务逻辑
- 状态通过数据Tool在事件间保持

**示例：Discord反馈机器人**
```typescript
// 事件源
client.on("messageCreate", (message) => {
  if (!message.author.bot) {
    runAgent({
      userMessage: `New message from ${message.author}: "${message.content}"`,
      channelId: message.channelId,
    });
  }
});

// 系统提示语定义行为
const systemPrompt = `
When someone shares feedback:
1. Acknowledge their feedback warmly
2. Ask clarifying questions if needed
3. Store it using the feedback tools
4. Update the feedback site

Use your judgment about importance and categorization.
`;
```
</pattern>

<pattern name="two-layer-git">
## 双层Git架构

对于自修改的Agent，将代码（共享）与数据（实例特定）分开。

```
┌─────────────────────────────────────────────────────────────┐
│                     GitHub (共享仓库)                     │
│  - src/           (Agent代码)                              │
│  - site/          (网页界面)                           │
│  - package.json   (依赖)                            │
│  - .gitignore     (排除 data/, logs/)                   │
└─────────────────────────────────────────────────────────────┘
                          │
                     git clone
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                  实例 (服务器)                           │
│                                                              │
│  来自 GITHUB (跟踪):                                      │
│  - src/           → 代码变更时推送回去             │
│  - site/          → 推送，触发部署             │
│                                                              │
│  仅本地 (不跟踪):                                     │
│  - data/          → 实例特定的存储               │
│  - logs/          → 运行时日志                    │
│  - .env           → 密钥                                 │
└─────────────────────────────────────────────────────────────┘
```

**为什么有效：**
- 代码和网站都受版本控制（GitHub）
- 原始数据保持本地（实例特定）
- 网站由数据生成，因此可重现
- 通过git历史自动回滚
</pattern>

<pattern name="multi-instance">
## 多实例分支

每个Agent实例获得自己的分支，同时共享核心代码。

```
main                        # 共享功能、bug修复
├── instance/feedback-bot   # 每个Reader反馈机器人
├── instance/support-bot    # 客户支持机器人
└── instance/research-bot   # 研究助手
```

**变更流程：**
| 变更类型 | 在此处理 | 然后 |
|-------------|---------|------|
| 核心功能 | main | 合并到实例分支 |
| Bug修复 | main | 合并到实例分支 |
| 实例配置 | 实例分支 | 完成 |
| 实例数据 | 实例分支 | 完成 |

**同步工具：**
```typescript
tool("self_deploy", "从main拉取最新，重建，重启", ...)
tool("sync_from_instance", "从另一个实例合并", ...)
tool("propose_to_main", "创建PR来共享改进", ...)
```
</pattern>

<pattern name="site-as-output">
## 网站作为Agent输出

Agent生成并维护网站作为自然输出，而不是通过专门的网站工具。

```
Discord消息
      ↓
Agent处理，提取见解
      ↓
Agent决定需要什么网站更新
      ↓
Agent使用write_file原始操作写入文件
      ↓
Git提交+推送触发部署
      ↓
网站自动更新
```

**关键洞察：** 不要构建网站生成工具。给Agent文件工具，并在提示语中教它如何创建好的网站。

```markdown
## 网站管理

你维护一个公共反馈网站。当反馈到来时：
1. 使用write_file更新site/public/content/feedback.json
2. 如果网站的React组件需要改进，修改它们
3. 提交更改并推送以触发Vercel部署

网站应该是：
- 清洁、现代的仪表板美学
- 清晰的视觉层级
- 状态组织（收件箱、活跃、完成）

你决定结构。做好它。
```
</pattern>

<pattern name="approval-gates">
## 批准门控模式

对于危险的操作，将"提议"与"应用"分开。

```typescript
// 待处理更改单独存储
const pendingChanges = new Map<string, string>();

tool("write_file", async ({ path, content }) => {
  if (requiresApproval(path)) {
    // 存储以供批准
    pendingChanges.set(path, content);
    const diff = generateDiff(path, content);
    return {
      text: `Change requires approval.\n\n${diff}\n\nReply "yes" to apply.`
    };
  } else {
    // 立即应用
    writeFileSync(path, content);
    return { text: `Wrote ${path}` };
  }
});

tool("apply_pending", async () => {
  for (const [path, content] of pendingChanges) {
    writeFileSync(path, content);
  }
  pendingChanges.clear();
  return { text: "Applied all pending changes" };
});
```

**需要批准的内容：**
- src/*.ts (Agent代码)
- package.json (依赖)
- 系统提示语更改

**不需要的内容：**
- data/* (实例数据)
- site/* (生成的内容)
- docs/* (文档)
</pattern>

<pattern name="unified-agent-architecture">
## 统一Agent架构

一个执行引擎，多个Agent类型。所有Agent使用同一个orchestrator但配置不同。

```
┌─────────────────────────────────────────────────────────────┐
│                    AgentOrchestrator                         │
├─────────────────────────────────────────────────────────────┤
│  - 生命周期管理（启动、暂停、恢复、停止）        │
│  - Checkpoint/恢复（用于后台执行）            │
│  - Tool执行                                            │
│  - 聊天集成                                          │
└─────────────────────────────────────────────────────────────┘
          │                    │                    │
    ┌─────┴─────┐        ┌─────┴─────┐        ┌─────┴─────┐
    │ 研究  │        │   聊天    │        │  配置文件  │
    │   Agent   │        │   Agent   │        │   Agent   │
    └───────────┘        └───────────┘        └───────────┘
    - web_search         - read_library       - read_photos
    - write_file         - publish_to_feed    - write_file
    - read_file          - web_search         - analyze_image
```

**实现：**

```swift
// 所有Agent使用同一个orchestrator
let session = try await AgentOrchestrator.shared.startAgent(
    config: ResearchAgent.create(book: book),  // Config varies
    tools: ResearchAgent.tools,                 // Tools vary
    context: ResearchAgent.context(for: book)   // Context varies
)

// Agent类型定义自己的配置
struct ResearchAgent {
    static var tools: [AgentTool] {
        [
            FileTools.readFile(),
            FileTools.writeFile(),
            WebTools.webSearch(),
            WebTools.webFetch(),
        ]
    }

    static func context(for book: Book) -> String {
        """
        You are researching "\(book.title)" by \(book.author).
        Save findings to Documents/Research/\(book.id)/
        """
    }
}

struct ChatAgent {
    static var tools: [AgentTool] {
        [
            FileTools.readFile(),
            FileTools.writeFile(),
            BookTools.readLibrary(),
            BookTools.publishToFeed(),  // Chat can publish directly
            WebTools.webSearch(),
        ]
    }

    static func context(library: [Book]) -> String {
        """
        You help the user with their reading.
        Available books: \(library.map { $0.title }.joined(separator: ", "))
        """
    }
}
```

**优点：**
- 所有Agent类型的一致生命周期管理
- 自动checkpoint/恢复（对移动设备至关重要）
- 共享tool协议
- 易于添加新的Agent类型
- 集中化的错误处理和日志记录
</pattern>

<pattern name="agent-to-ui-communication">
## Agent到UI通信

当Agent采取行动时，UI应该立即反映它们。用户应该看到Agent做了什么。

**模式1：共享数据存储（推荐）**

Agent通过UI观察的同一服务进行写入：

```swift
// 共享服务
class BookLibraryService: ObservableObject {
    static let shared = BookLibraryService()
    @Published var books: [Book] = []
    @Published var feedItems: [FeedItem] = []

    func addFeedItem(_ item: FeedItem) {
        feedItems.append(item)
        persist()
    }
}

// Agent工具通过共享服务进行写入
tool("publish_to_feed", async ({ bookId, content, headline }) => {
    let item = FeedItem(bookId: bookId, content: content, headline: headline)
    BookLibraryService.shared.addFeedItem(item)  // Same service UI uses
    return { text: "Published to feed" }
})

// UI观察同一服务
struct FeedView: View {
    @StateObject var library = BookLibraryService.shared

    var body: some View {
        List(library.feedItems) { item in
            FeedItemRow(item: item)
            // 当Agent添加项时自动更新
        }
    }
}
```

**模式2：文件系统观察**

对于基于文件的数据，监视文件系统：

```swift
class ResearchWatcher: ObservableObject {
    @Published var files: [URL] = []
    private var watcher: DirectoryWatcher?

    func watch(bookId: String) {
        let path = documentsURL.appendingPathComponent("Research/\(bookId)")

        watcher = DirectoryWatcher(path: path) { [weak self] in
            self?.reload(from: path)
        }

        reload(from: path)
    }
}

// Agent写入文件
tool("write_file", { path, content }) -> {
    writeFile(documentsURL.appendingPathComponent(path), content)
    // DirectoryWatcher自动触发UI更新
}
```

**模式3：事件总线（跨组件）**

对于具有多个独立组件的复杂应用程序：

```typescript
// 共享事件总线
const agentEvents = new EventEmitter();

// Agent工具发出事件
tool("publish_to_feed", async ({ content }) => {
    const item = await feedService.add(content);
    agentEvents.emit('feed:new-item', item);
    return { text: "Published" };
});

// UI组件订阅
function FeedView() {
    const [items, setItems] = useState([]);

    useEffect(() => {
        const handler = (item) => setItems(prev => [...prev, item]);
        agentEvents.on('feed:new-item', handler);
        return () => agentEvents.off('feed:new-item', handler);
    }, []);

    return <FeedList items={items} />;
}
```

**要避免的事项：**

```swift
// 不好：UI不观察Agent变化
// Agent直接写入数据库
tool("publish_to_feed", { content }) {
    database.insert("feed", content)  // UI看不到
}

// UI在启动时加载一次，永不刷新
struct FeedView: View {
    let items = database.query("feed")  // 过期！
}
```
</pattern>

<pattern name="model-tier-selection">
## ModelTier选择

不同的Agent需要不同的智力水平。使用达到结果的最便宜模型。

| Agent类型 | 推荐层级 | 理由 |
|------------|-----------------|-----------|
| 聊天/对话 | 平衡 | 快速响应，良好推理 |
| 研究 | 平衡 | Tool循环，不是超复杂合成 |
| 内容生成 | 平衡 | 创意但不是合成密集 |
| 复杂分析 | 强大 | 多文档合成，细致判断 |
| 配置文件/入职 | 强大 | 照片分析，复杂模式识别 |
| 简单查询 | 快速/Haiku | 快速查询，简单转换 |

**实现：**

```swift
enum ModelTier {
    case fast      // claude-3-haiku: 快速、廉价、简单任务
    case balanced  // claude-3-sonnet: 对于大多数任务的良好平衡
    case powerful  // claude-3-opus: 复杂推理、合成
}

struct AgentConfig {
    let modelTier: ModelTier
    let tools: [AgentTool]
    let systemPrompt: String
}

// 研究Agent：平衡层级
let researchConfig = AgentConfig(
    modelTier: .balanced,
    tools: researchTools,
    systemPrompt: researchPrompt
)

// 配置文件分析：强大层级（复杂照片解释）
let profileConfig = AgentConfig(
    modelTier: .powerful,
    tools: profileTools,
    systemPrompt: profilePrompt
)

// 快速查询：快速层级
let lookupConfig = AgentConfig(
    modelTier: .fast,
    tools: [readLibrary],
    systemPrompt: "回答关于用户库的快速问题。"
)
```

**成本优化策略：**
- 从平衡层级开始，仅在质量不足时升级
- 对于工具密集型循环使用快速层级，其中每个转弯很简单
- 为合成任务保留强大层级（比较多个源）
- 考虑每个转弯的token限制以控制成本
</pattern>

<design_questions>
## 设计时要问的问题

1. **什么事件触发Agent轮次？** (消息、webhooks、定时器、用户请求)
2. **Agent需要什么原始操作？** (读、写、调用API、重启)
3. **Agent应该做什么决定？** (格式、结构、优先级、操作)
4. **什么决定应该硬编码？** (安全边界、批准要求)
5. **Agent如何验证其工作？** (健康检查、构建验证)
6. **Agent如何从错误中恢复？** (git回滚、批准门控)
7. **UI如何知道Agent何时改变状态？** (共享存储、文件监视、事件)
8. **每个Agent类型需要什么ModelTier？** (快速、平衡、强大)
9. **Agent如何共享基础设施？** (统一orchestrator、共享Tool)
</design_questions>
