<overview>
Mobile是Agent原生应用的第一类平台。它有独特的约束和机会。本指南涵盖为什么mobile重要、iOS存储架构、checkpoint/resume模式和成本感知设计。
</overview>

<why_mobile>
## 为什么Mobile重要

Mobile设备为Agent原生应用提供了独特的优势：

### 文件系统
Agent可以自然地使用文件，使用在其他地方工作的相同原始操作。文件系统是通用界面。

### 丰富的Context
一个你可以访问的围墙花园。健康数据、位置、照片、日历——在桌面或网络上不存在的context。这使得深度个性化的Agent体验成为可能。

### 本地应用
每个人都有自己的应用副本。这为尚未完全实现的机会打开了大门：应用可以修改自己、分叉自己、按用户演变。App Store政策目前限制了其中一些，但基础在那里。

### 跨设备同步
如果你与iCloud一起使用文件系统，所有设备共享相同的文件系统。Agent在一个设备上的工作会出现在所有设备上——无需你构建服务器。

### 挑战

**Agent是长期运行的。Mobile应用不是。**

Agent可能需要30秒、5分钟或一小时来完成一项任务。但iOS会在不活动数秒后将你的应用置于后台，并可能完全关闭它以回收内存。用户可能在任务中途切换应用、接听电话或锁定手机。

这意味着mobile Agent应用需要：
- **Checkpointing** — 保存状态以免工作丢失
- **恢复** — 在中断后从离开的地方继续
- **后台执行** — 明智地使用iOS给你的有限时间
- **设备上 vs. 云决定** — 什么在本地运行 vs. 什么需要服务器
</why_mobile>

<ios_storage>
## iOS存储架构

> **需要验证：** 这是一个行之有效的方法，但可能存在更好的解决方案。

对于Agent原生iOS应用，使用iCloud Drive的Documents文件夹作为你的共享工作区。这给你**免费、自动的多设备同步**，而无需构建同步层或运行服务器。

### 为什么选择iCloud Documents？

| Approach | Cost | Complexity | Offline | Multi-Device |
|----------|------|------------|---------|--------------|
| Custom backend + sync | $$$ | High | Manual | Yes |
| CloudKit database | Free tier limits | Medium | Manual | Yes |
| **iCloud Documents** | Free (user's storage) | Low | Automatic | Automatic |

iCloud Documents：
- 使用用户现有的iCloud存储（免费5GB，大多数用户有更多）
- 在用户所有设备间自动同步
- 离线工作，在线时同步
- 文件在Files.app中可见以确保透明性
- 无服务器成本，无同步代码需要维护

### 实现：iCloud优先，具有本地回退

```swift
// 获取iCloud Documents容器
func iCloudDocumentsURL() -> URL? {
    FileManager.default.url(forUbiquityContainerIdentifier: nil)?
        .appendingPathComponent("Documents")
}

// 你的共享工作区位于iCloud
class SharedWorkspace {
    let rootURL: URL

    init() {
        // 如果可用使用iCloud，否则回退到本地
        if let iCloudURL = iCloudDocumentsURL() {
            self.rootURL = iCloudURL
        } else {
            // 回退到本地Documents（用户未登录iCloud）
            self.rootURL = FileManager.default.urls(
                for: .documentDirectory,
                in: .userDomainMask
            ).first!
        }
    }

    // 所有文件操作都通过这个根进行
    func researchPath(for bookId: String) -> URL {
        rootURL.appendingPathComponent("Research/\(bookId)")
    }

    func journalPath() -> URL {
        rootURL.appendingPathComponent("Journal")
    }
}
```

### iCloud中的目录结构

```
iCloud Drive/
└── YourApp/                          # Your app's container
    └── Documents/                    # Visible in Files.app
        ├── Journal/
        │   ├── user/
        │   │   └── 2025-01-15.md     # 在设备间同步
        │   └── agent/
        │       └── 2025-01-15.md     # Agent观察也同步
        ├── Research/
        │   └── {bookId}/
        │       ├── full_text.txt
        │       └── sources/
        ├── Chats/
        │   └── {conversationId}.json
        └── context.md                # Agent's accumulated knowledge
```

### 处理iCloud文件状态

iCloud文件可能未在本地下载。处理方法：

```swift
func readFile(at url: URL) throws -> String {
    // iCloud可能会创建.icloud占位符文件
    if url.pathExtension == "icloud" {
        // 触发下载
        try FileManager.default.startDownloadingUbiquitousItem(at: url)
        throw FileNotYetAvailableError()
    }

    return try String(contentsOf: url, encoding: .utf8)
}

// 对于写入，使用协调的文件访问
func writeFile(_ content: String, to url: URL) throws {
    let coordinator = NSFileCoordinator()
    var error: NSError?

    coordinator.coordinate(
        writingItemAt: url,
        options: .forReplacing,
        error: &error
    ) { newURL in
        try? content.write(to: newURL, atomically: true, encoding: .utf8)
    }

    if let error = error { throw error }
}
```

### iCloud支持的功能

1. **用户在iPhone上开始实验** → Agent创建配置文件
2. **用户在iPad上打开应用** → 相同的实验可见，无需同步代码
3. **Agent在iPhone上记录观察** → 自动同步到iPad
4. **用户在iPad上编辑日记** → iPhone看到编辑

### 所需权利

添加到你的应用权利：

```xml
<key>com.apple.developer.icloud-container-identifiers</key>
<array>
    <string>iCloud.com.yourcompany.yourapp</string>
</array>
<key>com.apple.developer.icloud-services</key>
<array>
    <string>CloudDocuments</string>
</array>
<key>com.apple.developer.ubiquity-container-identifiers</key>
<array>
    <string>iCloud.com.yourcompany.yourapp</string>
</array>
```

### 何时不使用iCloud Documents

- **敏感数据** - 使用Keychain或加密的本地存储
- **高频写入** - iCloud同步有延迟；使用本地+定期同步
- **大型媒体文件** - 考虑CloudKit Assets或按需资源
- **用户间共享** - iCloud Documents是单用户的；使用CloudKit进行共享
</ios_storage>

<background_execution>
## 后台执行与恢复

> **需要验证：** 这些模式有效，但可能存在更好的解决方案。

Mobile应用可以随时挂起或终止。Agent必须优雅地处理这个问题。

### 挑战

```
用户启动研究Agent
     ↓
Agent开始网络搜索
     ↓
用户切换到另一个应用
     ↓
iOS挂起你的应用
     ↓
Agent正在执行中...会发生什么？
```

### Checkpoint/恢复模式

在后台前保存Agent状态，在前台恢复：

```swift
class AgentOrchestrator: ObservableObject {
    @Published var activeSessions: [AgentSession] = []

    // 当应用即将进入后台时调用
    func handleAppWillBackground() {
        for session in activeSessions {
            saveCheckpoint(session)
            session.transition(to: .backgrounded)
        }
    }

    // 当应用返回前台时调用
    func handleAppDidForeground() {
        for session in activeSessions where session.state == .backgrounded {
            if let checkpoint = loadCheckpoint(session.id) {
                resumeFromCheckpoint(session, checkpoint)
            }
        }
    }

    private func saveCheckpoint(_ session: AgentSession) {
        let checkpoint = AgentCheckpoint(
            sessionId: session.id,
            conversationHistory: session.messages,
            pendingToolCalls: session.pendingToolCalls,
            partialResults: session.partialResults,
            timestamp: Date()
        )
        storage.save(checkpoint, for: session.id)
    }

    private func resumeFromCheckpoint(_ session: AgentSession, _ checkpoint: AgentCheckpoint) {
        session.messages = checkpoint.conversationHistory
        session.pendingToolCalls = checkpoint.pendingToolCalls

        // Resume execution if there were pending tool calls
        if !checkpoint.pendingToolCalls.isEmpty {
            session.transition(to: .running)
            Task { await executeNextTool(session) }
        }
    }
}
```

### Agent生命周期的状态机

```swift
enum AgentState {
    case idle           // 未运行
    case running        // 主动执行
    case waitingForUser // 暂停，等待用户输入
    case backgrounded   // 应用进入后台，状态已保存
    case completed      // 成功完成
    case failed(Error)  // 因错误而完成
}

class AgentSession: ObservableObject {
    @Published var state: AgentState = .idle

    func transition(to newState: AgentState) {
        let validTransitions: [AgentState: Set<AgentState>] = [
            .idle: [.running],
            .running: [.waitingForUser, .backgrounded, .completed, .failed],
            .waitingForUser: [.running, .backgrounded],
            .backgrounded: [.running, .completed],
        ]

        guard validTransitions[state]?.contains(newState) == true else {
            logger.warning("Invalid transition: \(state) → \(newState)")
            return
        }

        state = newState
    }
}
```

### 后台任务扩展(iOS)

在关键操作期间进入后台时请求额外时间：

```swift
class AgentOrchestrator {
    private var backgroundTask: UIBackgroundTaskIdentifier = .invalid

    func handleAppWillBackground() {
        // 请求额外时间以保存状态
        backgroundTask = UIApplication.shared.beginBackgroundTask { [weak self] in
            self?.endBackgroundTask()
        }

        // 保存所有检查点
        Task {
            for session in activeSessions {
                await saveCheckpoint(session)
            }
            endBackgroundTask()
        }
    }

    private func endBackgroundTask() {
        if backgroundTask != .invalid {
            UIApplication.shared.endBackgroundTask(backgroundTask)
            backgroundTask = .invalid
        }
    }
}
```

### 用户通信

让用户知道发生了什么：

```swift
struct AgentStatusView: View {
    @ObservedObject var session: AgentSession

    var body: some View {
        switch session.state {
        case .backgrounded:
            Label("已暂停（应用在后台）", systemImage: "pause.circle")
                .foregroundColor(.orange)
        case .running:
            Label("正在工作...", systemImage: "ellipsis.circle")
                .foregroundColor(.blue)
        case .waitingForUser:
            Label("等待你的输入", systemImage: "person.circle")
                .foregroundColor(.green)
        // ...
        }
    }
}
```
</background_execution>

<permissions>
## 权限处理

Mobile Agent可能需要访问系统资源。优雅地处理权限请求。

### 常见权限

| 资源 | iOS权限 | 用例 |
|----------|---------------|----------|
| 照片库 | PHPhotoLibrary | 从照片生成配置 |
| 文件 | 文档选择器 | 读取用户文档 |
| 相机 | AVCaptureDevice | 扫描书籍封面 |
| 位置 | CLLocationManager | 位置感知建议 |
| 网络 | （自动） | 网络搜索、API调用 |

### 权限感知工具

执行前检查权限：

```swift
struct PhotoTools {
    static func readPhotos() -> AgentTool {
        tool(
            name: "read_photos",
            description: "Read photos from the user's photo library",
            parameters: [
                "limit": .number("Maximum photos to read"),
                "dateRange": .string("Date range filter").optional()
            ],
            execute: { params, context in
                // 首先检查权限
                let status = await PHPhotoLibrary.requestAuthorization(for: .readWrite)

                switch status {
                case .authorized, .limited:
                    // 继续读取照片
                    let photos = await fetchPhotos(params)
                    return ToolResult(text: "Found \(photos.count) photos", images: photos)

                case .denied, .restricted:
                    return ToolResult(
                        text: "Photo access needed. Please grant permission in Settings → Privacy → Photos.",
                        isError: true
                    )

                case .notDetermined:
                    return ToolResult(
                        text: "Photo permission required. Please try again.",
                        isError: true
                    )

                @unknown default:
                    return ToolResult(text: "Unknown permission status", isError: true)
                }
            }
        )
    }
}
```

### 优雅降级

当未授予权限时，提供替代方案：

```swift
func readPhotos() async -> ToolResult {
    let status = PHPhotoLibrary.authorizationStatus(for: .readWrite)

    switch status {
    case .denied, .restricted:
        // 建议替代方案
        return ToolResult(
            text: """
            我无法访问你的照片。你可以选择：
            1. 在设置中授予访问权限 → 隐私 → 照片
            2. 直接在我们的聊天中分享特定照片

            你想让我帮助其他事情吗？
            """,
            isError: false  // 不是硬错误，只是限制
        )
    // ...
    }
}
```

### 权限请求时间

直到需要时才请求权限：

```swift
// 不好：在启动时请求所有权限
func applicationDidFinishLaunching() {
    requestPhotoAccess()  // 请求照片访问
    requestCameraAccess()  // 请求相机访问
    requestLocationAccess()  // 请求位置访问
    // 用户被权限对话框淹没
}

// 好的：当使用该功能时请求
tool("analyze_book_cover", async ({ image }) => {
    // 仅当用户尝试扫描封面时请求相机访问
    let status = await AVCaptureDevice.requestAccess(for: .video)
    if status {
        return await scanCover(image)
    } else {
        return ToolResult(text: "Camera access needed for book scanning")
    }
})
```
</permissions>

<cost_awareness>
## 成本感知设计

Mobile用户可能使用蜂窝数据或关心API成本。设计高效的Agent。

### 模型等级选择

使用实现结果的最便宜的模型：

```swift
enum ModelTier {
    case fast      // claude-3-haiku：~$0.25/1M tokens
    case balanced  // claude-3-sonnet：~$3/1M tokens
    case powerful  // claude-3-opus：~$15/1M tokens

    var modelId: String {
        switch self {
        case .fast: return "claude-3-haiku-20240307"
        case .balanced: return "claude-3-sonnet-20240229"
        case .powerful: return "claude-3-opus-20240229"
        }
    }
}

// 将模型与任务复杂性匹配
let agentConfigs: [AgentType: ModelTier] = [
    .quickLookup: .fast,        // "我的库中有什么？"
    .chatAssistant: .balanced,  // 常规对话
    .researchAgent: .balanced,  // 网络搜索+合成
    .profileGenerator: .powerful, // 复杂照片分析
    .introductionWriter: .balanced,
]
```

### Token预算

限制每个Agent会话的token：

```swift
struct AgentConfig {
    let modelTier: ModelTier
    let maxInputTokens: Int
    let maxOutputTokens: Int
    let maxTurns: Int

    static let research = AgentConfig(
        modelTier: .balanced,
        maxInputTokens: 50_000,
        maxOutputTokens: 4_000,
        maxTurns: 20
    )

    static let quickChat = AgentConfig(
        modelTier: .fast,
        maxInputTokens: 10_000,
        maxOutputTokens: 1_000,
        maxTurns: 5
    )
}

class AgentSession {
    var totalTokensUsed: Int = 0

    func checkBudget() -> Bool {
        if totalTokensUsed > config.maxInputTokens {
            transition(to: .failed(AgentError.budgetExceeded))
            return false
        }
        return true
    }
}
```

### 网络感知执行

将繁重操作推迟到WiFi：

```swift
class NetworkMonitor: ObservableObject {
    @Published var isOnWiFi: Bool = false
    @Published var isExpensive: Bool = false  // 蜂窝或热点

    private let monitor = NWPathMonitor()

    func startMonitoring() {
        monitor.pathUpdateHandler = { [weak self] path in
            DispatchQueue.main.async {
                self?.isOnWiFi = path.usesInterfaceType(.wifi)
                self?.isExpensive = path.isExpensive
            }
        }
        monitor.start(queue: .global())
    }
}

class AgentOrchestrator {
    @ObservedObject var network = NetworkMonitor()

    func startResearchAgent(for book: Book) async {
        if network.isExpensive {
            // 警告用户或推迟
            let proceed = await showAlert(
                "研究使用数据",
                message: "这将使用大约1-2 MB的蜂窝数据。继续？"
            )
            if !proceed { return }
        }

        // Proceed with research
        await runAgent(ResearchAgent.create(book: book))
    }
}
```

### 批量API调用

组合多个小请求：

```swift
// 不好：许多小的API调用
for book in books {
    await agent.chat("摘要 \(book.title)")
}

// 好的：批量为一个请求
let bookList = books.map { $0.title }.joined(separator: ", ")
await agent.chat("简要摘要每本书：\(bookList)")
```

### 缓存

缓存昂贵的操作：

```swift
class ResearchCache {
    private var cache: [String: CachedResearch] = [:]

    func getCachedResearch(for bookId: String) -> CachedResearch? {
        guard let cached = cache[bookId] else { return nil }

        // 24小时后过期
        if Date().timeIntervalSince(cached.timestamp) > 86400 {
            cache.removeValue(forKey: bookId)
            return nil
        }

        return cached
    }

    func cacheResearch(_ research: Research, for bookId: String) {
        cache[bookId] = CachedResearch(
            research: research,
            timestamp: Date()
        )
    }
}

// 在研究工具中
tool("web_search", async ({ query, bookId }) => {
    // 首先检查缓存
    if let cached = cache.getCachedResearch(for: bookId) {
        return ToolResult(text: cached.research.summary, cached: true)
    }

    // 否则，执行搜索
    let results = await webSearch(query)
    cache.cacheResearch(results, for: bookId)
    return ToolResult(text: results.summary)
})
```

### 成本可见性

显示用户花费的内容：

```swift
struct AgentCostView: View {
    @ObservedObject var session: AgentSession

    var body: some View {
        VStack(alignment: .leading) {
            Text("会话统计")
                .font(.headline)

            HStack {
                Label("\(session.turnCount)轮", systemImage: "arrow.2.squarepath")
                Spacer()
                Label(formatTokens(session.totalTokensUsed), systemImage: "text.word.spacing")
            }

            if let estimatedCost = session.estimatedCost {
                Text("估计成本：\(estimatedCost, format: .currency(code: "USD"))")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
        }
    }
}
```
</cost_awareness>

<offline_handling>
## 离线优雅降级

优雅地处理离线场景：

```swift
class ConnectivityAwareAgent {
    @ObservedObject var network = NetworkMonitor()

    func executeToolCall(_ toolCall: ToolCall) async -> ToolResult {
        // 检查工具是否需要网络
        let requiresNetwork = ["web_search", "web_fetch", "call_api"]
            .contains(toolCall.name)

        if requiresNetwork && !network.isConnected {
            return ToolResult(
                text: """
                我现在无法访问互联网。以下是我可以离线做的事情：
                - 阅读你的库和现有研究
                - 回答来自缓存数据的问题
                - 为以后写笔记和草稿

                你想让我尝试离线工作的东西吗？
                """,
                isError: false
            )
        }

        return await executeOnline(toolCall)
    }
}
```

### 离线优先工具

某些工具应该完全离线工作：

```swift
let offlineTools: Set<String> = [
    "read_file",
    "write_file",
    "list_files",
    "read_library",  // 本地数据库
    "search_local",  // 本地搜索
]

let onlineTools: Set<String> = [
    "web_search",
    "web_fetch",
    "publish_to_cloud",
]

let hybridTools: Set<String> = [
    "publish_to_feed",  // 离线工作，稍后同步
]
```

### 排队的操作

排队需要连接的操作：

```swift
class OfflineQueue: ObservableObject {
    @Published var pendingActions: [QueuedAction] = []

    func queue(_ action: QueuedAction) {
        pendingActions.append(action)
        persist()
    }

    func processWhenOnline() {
        network.$isConnected
            .filter { $0 }
            .sink { [weak self] _ in
                self?.processPendingActions()
            }
    }

    private func processPendingActions() {
        for action in pendingActions {
            Task {
                try await execute(action)
                remove(action)
            }
        }
    }
}
```
</offline_handling>

<battery_awareness>
## 电池感知执行

尊重设备电池状态：

```swift
class BatteryMonitor: ObservableObject {
    @Published var batteryLevel: Float = 1.0
    @Published var isCharging: Bool = false
    @Published var isLowPowerMode: Bool = false

    var shouldDeferHeavyWork: Bool {
        return batteryLevel < 0.2 && !isCharging
    }

    func startMonitoring() {
        UIDevice.current.isBatteryMonitoringEnabled = true

        NotificationCenter.default.addObserver(
            forName: UIDevice.batteryLevelDidChangeNotification,
            object: nil,
            queue: .main
        ) { [weak self] _ in
            self?.batteryLevel = UIDevice.current.batteryLevel
        }

        NotificationCenter.default.addObserver(
            forName: NSNotification.Name.NSProcessInfoPowerStateDidChange,
            object: nil,
            queue: .main
        ) { [weak self] _ in
            self?.isLowPowerMode = ProcessInfo.processInfo.isLowPowerModeEnabled
        }
    }
}

class AgentOrchestrator {
    @ObservedObject var battery = BatteryMonitor()

    func startAgent(_ config: AgentConfig) async {
        if battery.shouldDeferHeavyWork && config.isHeavy {
            let proceed = await showAlert(
                "低电量",
                message: "此任务使用大量电池。继续还是推迟到充电？"
            )
            if !proceed { return }
        }

        // 根据电池调整模型等级
        let adjustedConfig = battery.isLowPowerMode
            ? config.withModelTier(.fast)
            : config

        await runAgent(adjustedConfig)
    }
}
```
</battery_awareness>

<on_device_vs_cloud>
## 设备上 vs. 云

理解在mobile Agent原生应用中哪里运行什么：

| 组件 | 设备上 | 云 |
|-----------|-----------|-------|
| 编排 | ✅ | |
| 工具执行 | ✅ (文件操作、照片访问、HealthKit) | |
| LLM调用 | | ✅ (Anthropic API) |
| 检查点 | ✅ (本地文件) | 可选通过iCloud |
| 长期运行的Agent | 受iOS限制 | 可能需要服务器 |

### 影响

**推理需要网络：**
- 应用需要网络连接以进行LLM调用
- 设计工具在网络不可用时优雅降级
- 考虑为常见查询进行离线缓存

**数据保留在本地：**
- 文件操作在设备上进行
- 敏感数据永远不会离开设备，除非明确同步
- 默认情况下保留隐私

**长期运行的Agent：**
对于真正的长期运行Agent（数小时），考虑一个可以无限期运行的服务器端编排器，mobile应用作为查看器和输入机制。
</on_device_vs_cloud>

<checklist>
## Mobile Agent原生检查清单

**iOS存储：**
- [ ] iCloud Documents作为主存储（或有意识的替代方案）
- [ ] 当iCloud不可用时本地Documents回退
- [ ] 处理`.icloud`占位符文件（触发下载）
- [ ] 对冲突安全写入使用NSFileCoordinator

**后台执行：**
- [ ] 为所有Agent会话实现了Checkpoint/恢复
- [ ] Agent生命周期的状态机（idle、running、backgrounded等）
- [ ] 关键保存的后台任务扩展（30秒窗口）
- [ ] 后台Agent的用户可见状态

**权限：**
- [ ] 仅在需要时请求权限，而不是在启动时
- [ ] 权限被拒绝时优雅降级
- [ ] 带有Settings深层链接的清晰错误消息
- [ ] 权限不可用时的替代路径

**成本感知：**
- [ ] 模型等级与任务复杂性相匹配
- [ ] 每个会话的Token预算
- [ ] 网络感知（将繁重工作推迟到WiFi）
- [ ] 昂贵操作的缓存
- [ ] 对用户的成本可见性

**离线处理：**
- [ ] 识别离线能力的工具
- [ ] 仅在线功能的优雅降级
- [ ] 在线时同步的操作队列
- [ ] 关于离线状态的清晰用户通信

**电池感知：**
- [ ] 繁重操作的电池监测
- [ ] 低电源模式检测
- [ ] 根据电池状态推迟或降级
</checklist>
