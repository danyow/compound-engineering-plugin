<overview>
如何将动态运行时上下文注入到 Agent 系统 prompt 中。Agent 需要知道应用中存在什么才能了解可以处理什么。静态 prompt 是不够的——Agent 需要看到用户看到的相同上下文。

**核心原则：** 用户的上下文 IS Agent 的上下文。
</overview>

<why_context_matters>
## 为什么需要动态上下文注入？

静态 system prompt 告诉 Agent 它能做什么。动态上下文告诉它在用户实际数据的基础上现在能做什么。

**失败案例：**
```
User: "Write a little thing about Catherine the Great in my reading feed"
Agent: "What system are you referring to? I'm not sure what reading feed means."
```

Agent 失败是因为它不知道：
- 用户库中存在哪些书籍
- "reading feed"是什么
- 它有什么工具可以在那里发布内容

**解决方案：** 将关于应用状态的运行时上下文注入到 system prompt 中。
</why_context_matters>

<pattern name="context-injection">
## 上下文注入模式

动态构建 system prompt，包含当前应用状态：

```swift
func buildSystemPrompt() -> String {
    // 收集当前状态
    let availableBooks = libraryService.books
    let recentActivity = analysisService.recentRecords(limit: 10)
    let userProfile = profileService.currentProfile

    return """
    # Your Identity

    You are a reading assistant for \(userProfile.name)'s library.

    ## Available Books in User's Library

    \(availableBooks.map { "- \"\($0.title)\" by \($0.author) (id: \($0.id))" }.joined(separator: "\n"))

    ## Recent Reading Activity

    \(recentActivity.map { "- Analyzed \"\($0.bookTitle)\": \($0.excerptPreview)" }.joined(separator: "\n"))

    ## Your Capabilities

    - **publish_to_feed**: Create insights that appear in the Feed tab
    - **read_library**: View books, highlights, and analyses
    - **web_search**: Search the internet for research
    - **write_file**: Save research to Documents/Research/{bookId}/

    When the user mentions "the feed" or "reading feed", they mean the Feed tab
    where insights appear. Use `publish_to_feed` to create content there.
    """
}
```
</pattern>

<what_to_inject>
## 注入什么上下文

### 1. 可用资源
Agent 可以访问的数据/文件有哪些？

```swift
## Available in User's Library

Books:
- "Moby Dick" by Herman Melville (id: book_123)
- "1984" by George Orwell (id: book_456)

Research folders:
- Documents/Research/book_123/ (3 files)
- Documents/Research/book_456/ (1 file)
```

### 2. 当前状态
用户最近做了什么？当前的上下文是什么？

```swift
## Recent Activity

- 2 hours ago: Highlighted passage in "1984" about surveillance
- Yesterday: Completed research on "Moby Dick" whale symbolism
- This week: Added 3 new books to library
```

### 3. 功能映射
什么 tool 映射到什么 UI 功能？使用用户的语言。

```swift
## What You Can Do

| User Says | You Should Use | Result |
|-----------|----------------|--------|
| "my feed" / "reading feed" | `publish_to_feed` | Creates insight in Feed tab |
| "my library" / "my books" | `read_library` | Shows their book collection |
| "research this" | `web_search` + `write_file` | Saves to Research folder |
| "my profile" | `read_file("profile.md")` | Shows reading profile |
```

### 4. 域名词汇
解释用户可能使用的特定于应用的术语。

```swift
## Vocabulary

- **Feed**: The Feed tab showing reading insights and analyses
- **Research folder**: Documents/Research/{bookId}/ where research is stored
- **Reading profile**: A markdown file describing user's reading preferences
- **Highlight**: A passage the user marked in a book
```
</what_to_inject>

<implementation_patterns>
## 实现模式

### 模式 1：基于服务的注入 (Swift/iOS)

```swift
class AgentContextBuilder {
    let libraryService: BookLibraryService
    let profileService: ReadingProfileService
    let activityService: ActivityService

    func buildContext() -> String {
        let books = libraryService.books
        let profile = profileService.currentProfile
        let activity = activityService.recent(limit: 10)

        return """
        ## Library (\(books.count) books)
        \(formatBooks(books))

        ## Profile
        \(profile.summary)

        ## Recent Activity
        \(formatActivity(activity))
        """
    }

    private func formatBooks(_ books: [Book]) -> String {
        books.map { "- \"\($0.title)\" (id: \($0.id))" }.joined(separator: "\n")
    }
}

// 在 Agent 初始化中使用
let context = AgentContextBuilder(
    libraryService: .shared,
    profileService: .shared,
    activityService: .shared
).buildContext()

let systemPrompt = basePrompt + "\n\n" + context
```

### 模式 2：基于 Hook 的注入 (TypeScript)

```typescript
interface ContextProvider {
  getContext(): Promise<string>;
}

class LibraryContextProvider implements ContextProvider {
  async getContext(): Promise<string> {
    const books = await db.books.list();
    const recent = await db.activity.recent(10);

    return `
## Library
${books.map(b => `- "${b.title}" (${b.id})`).join('\n')}

## Recent
${recent.map(r => `- ${r.description}`).join('\n')}
    `.trim();
  }
}

// 组合多个提供器
async function buildSystemPrompt(providers: ContextProvider[]): Promise<string> {
  const contexts = await Promise.all(providers.map(p => p.getContext()));
  return [BASE_PROMPT, ...contexts].join('\n\n');
}
```

### 模式 3：基于模板的注入

```markdown
# System Prompt Template (system-prompt.template.md)

You are a reading assistant.

## Available Books

{{#each books}}
- "{{title}}" by {{author}} (id: {{id}})
{{/each}}

## Capabilities

{{#each capabilities}}
- **{{name}}**: {{description}}
{{/each}}

## Recent Activity

{{#each recentActivity}}
- {{timestamp}}: {{description}}
{{/each}}
```

```typescript
// 在运行时进行渲染
const prompt = Handlebars.compile(template)({
  books: await libraryService.getBooks(),
  capabilities: getCapabilities(),
  recentActivity: await activityService.getRecent(10),
});
```
</implementation_patterns>

<context_freshness>
## 上下文新鲜度

上下文应该在 Agent 初始化时注入，并可选地在长时间的会话中刷新。

**在初始化时：**
```swift
// 启动 Agent 时始终注入新鲜的上下文
func startChatAgent() async -> AgentSession {
    let context = await buildCurrentContext()  // 新鲜的上下文
    return await AgentOrchestrator.shared.startAgent(
        config: ChatAgent.config,
        systemPrompt: basePrompt + context
    )
}
```

**在长时间会话期间（可选）：**
```swift
// 对于长时间运行的 Agent，提供一个刷新 tool
tool("refresh_context", "Get current app state") { _ in
    let books = libraryService.books
    let recent = activityService.recent(10)
    return """
    Current library: \(books.count) books
    Recent: \(recent.map { $0.summary }.joined(separator: ", "))
    """
}
```

**不应该做什么：**
```swift
// 不要：使用来自应用启动的过时上下文
let cachedContext = appLaunchContext  // 过时！
// 书籍可能已添加，活动可能已更改
```
</context_freshness>

<examples>
## 真实案例：Every Reader

Every Reader 应用为其聊天 Agent 注入上下文：

```swift
func getChatAgentSystemPrompt() -> String {
    // 获取当前库状态
    let books = BookLibraryService.shared.books
    let analyses = BookLibraryService.shared.analysisRecords.prefix(10)
    let profile = ReadingProfileService.shared.getProfileForSystemPrompt()

    let bookList = books.map { book in
        "- \"\(book.title)\" by \(book.author) (id: \(book.id))"
    }.joined(separator: "\n")

    let recentList = analyses.map { record in
        let title = books.first { $0.id == record.bookId }?.title ?? "Unknown"
        return "- From \"\(title)\": \"\(record.excerptPreview)\""
    }.joined(separator: "\n")

    return """
    # Reading Assistant

    You help the user with their reading and book research.

    ## Available Books in User's Library

    \(bookList.isEmpty ? "No books yet." : bookList)

    ## Recent Reading Journal (Latest Analyses)

    \(recentList.isEmpty ? "No analyses yet." : recentList)

    ## Reading Profile

    \(profile)

    ## Your Capabilities

    - **Publish to Feed**: Create insights using `publish_to_feed` that appear in the Feed tab
    - **Library Access**: View books and highlights using `read_library`
    - **Research**: Search web and save to Documents/Research/{bookId}/
    - **Profile**: Read/update the user's reading profile

    When the user asks you to "write something for their feed" or "add to my reading feed",
    use the `publish_to_feed` tool with the relevant book_id.
    """
}
```

**结果：** 当用户说"write a little thing about Catherine the Great in my reading feed"时，Agent：
1. 看到"reading feed"→ 知道使用 `publish_to_feed`
2. 看到可用的书籍 → 找到相关的 book ID
3. 为 Feed 标签创建适当的内容
</examples>

<checklist>
## 上下文注入检查清单

启动 Agent 前：
- [ ] System prompt 包含当前资源（书籍、文件、数据）
- [ ] 最近的活动对 Agent 可见
- [ ] 功能被映射到用户词汇
- [ ] 特定于域的术语已解释
- [ ] 上下文是新鲜的（在 Agent 启动时收集，不缓存）

添加新功能时：
- [ ] 新资源包含在上下文注入中
- [ ] 新功能在 system prompt 中被记录
- [ ] 为该功能的用户词汇被映射
</checklist>
