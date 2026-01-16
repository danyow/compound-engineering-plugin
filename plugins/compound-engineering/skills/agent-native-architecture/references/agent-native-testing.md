<overview>
Agent-native 应用的测试与传统单元测试需要采用不同的方法。您需要测试 Agent 是否实现了目标，而不是测试它是否调用了特定函数。本指南提供了具体的测试模式，用于验证您的应用是否真正实现了 Agent-native。
</overview>

<testing_philosophy>
## 测试哲学

### 测试结果，而不是过程

**传统方法（过程导向）：**
```typescript
// 测试特定函数是否被以特定参数调用
expect(mockProcessFeedback).toHaveBeenCalledWith({
  message: "Great app!",
  category: "praise",
  priority: 2
});
```

**Agent-native 方法（结果导向）：**
```typescript
// 测试结果是否实现
const result = await agent.process("Great app!");
const storedFeedback = await db.feedback.getLatest();

expect(storedFeedback.content).toContain("Great app");
expect(storedFeedback.importance).toBeGreaterThanOrEqual(1);
expect(storedFeedback.importance).toBeLessThanOrEqual(5);
// 我们不在乎它如何分类——只要分类是合理的即可
```

### 接受可变性

Agent 可能每次都以不同的方式解决问题。您的测试应该：
- 验证最终状态，而不是路径
- 接受合理的范围，而不是精确值
- 检查必需元素的存在，而不是精确格式
</testing_philosophy>

<can_agent_do_it_test>
## "Agent 能做到吗？"测试

针对每个 UI 功能，编写测试提示并验证 Agent 是否能完成它。

### 模板

```typescript
describe('Agent 能力测试', () => {
  test('Agent 可以将书籍添加到库', async () => {
    const result = await agent.chat("Add 'Moby Dick' by Herman Melville to my library");

    // 验证结果
    const library = await libraryService.getBooks();
    const mobyDick = library.find(b => b.title.includes("Moby Dick"));

    expect(mobyDick).toBeDefined();
    expect(mobyDick.author).toContain("Melville");
  });

  test('Agent 可以发布到信息流', async () => {
    // 设置：确保书籍存在
    await libraryService.addBook({ id: "book_123", title: "1984" });

    const result = await agent.chat("Write something about surveillance themes in my feed");

    // 验证结果
    const feed = await feedService.getItems();
    const newItem = feed.find(item => item.bookId === "book_123");

    expect(newItem).toBeDefined();
    expect(newItem.content.toLowerCase()).toMatch(/surveillance|watching|control/);
  });

  test('Agent 可以搜索和保存研究资料', async () => {
    await libraryService.addBook({ id: "book_456", title: "Moby Dick" });

    const result = await agent.chat("Research whale symbolism in Moby Dick");

    // 验证文件是否被创建
    const files = await fileService.listFiles("Research/book_456/");
    expect(files.length).toBeGreaterThan(0);

    // 验证内容相关性
    const content = await fileService.readFile(files[0]);
    expect(content.toLowerCase()).toMatch(/whale|symbolism|melville/);
  });
});
```

### "写入位置"测试

一个关键的测试：Agent 能否在特定应用位置创建内容？

```typescript
describe('位置感知测试', () => {
  const locations = [
    { userPhrase: "my reading feed", expectedTool: "publish_to_feed" },
    { userPhrase: "my library", expectedTool: "add_book" },
    { userPhrase: "my research folder", expectedTool: "write_file" },
    { userPhrase: "my profile", expectedTool: "write_file" },
  ];

  for (const { userPhrase, expectedTool } of locations) {
    test(`Agent 知道如何写入 "${userPhrase}"`, async () => {
      const prompt = `Write a test note to ${userPhrase}`;
      const result = await agent.chat(prompt);

      // 检查 Agent 是否使用了正确的工具（或实现了结果）
      expect(result.toolCalls).toContainEqual(
        expect.objectContaining({ name: expectedTool })
      );

      // 或者直接验证结果
      // expect(await locationHasNewContent(userPhrase)).toBe(true);
    });
  }
});
```
</can_agent_do_it_test>

<surprise_test>
## "惊喜测试"

良好设计的 Agent-native 应用让 Agent 能够想出创意方案。通过给出开放式请求来测试这一点。

### 测试

```typescript
describe('Agent 创意测试', () => {
  test('Agent 可以处理开放式请求', async () => {
    // 设置：用户有一些书籍
    await libraryService.addBook({ id: "1", title: "1984", author: "Orwell" });
    await libraryService.addBook({ id: "2", title: "Brave New World", author: "Huxley" });
    await libraryService.addBook({ id: "3", title: "Fahrenheit 451", author: "Bradbury" });

    // 开放式请求
    const result = await agent.chat("Help me organize my reading for next month");

    // Agent 应该做一些有用的事
    // 我们没有具体指定是什么——这才是要点
    expect(result.toolCalls.length).toBeGreaterThan(0);

    // 它应该与库进行交互
    const libraryTools = ["read_library", "write_file", "publish_to_feed"];
    const usedLibraryTool = result.toolCalls.some(
      call => libraryTools.includes(call.name)
    );
    expect(usedLibraryTool).toBe(true);
  });

  test('Agent 找到创意解决方案', async () => {
    // 不指定"如何"完成任务
    const result = await agent.chat(
      "I want to understand the dystopian themes across my sci-fi books"
    );

    // Agent 可能会：
    // - 阅读所有书籍并创建比较文档
    // - 研究反乌托邦文学并将其与用户的书籍联系起来
    // - 在 markdown 文件中创建思维导图
    // - 向信息流发布一系列见解

    // 我们只验证它做了实质性的工作
    expect(result.response.length).toBeGreaterThan(100);
    expect(result.toolCalls.length).toBeGreaterThan(0);
  });
});
```

### 失败的样子

```typescript
// 失败：Agent 只能说它无法做到
const result = await agent.chat("Help me prepare for a book club discussion");

// 不好的结果：
expect(result.response).not.toContain("I can't");
expect(result.response).not.toContain("I don't have a tool");
expect(result.response).not.toContain("Could you clarify");

// 如果 Agent 询问某件它应该理解的事情的澄清，
// 你就有上下文注入或能力差距问题
```
</surprise_test>

<parity_testing>
## 自动化平等测试

确保每个 UI 操作都有 Agent 等价物。

### 能力映射测试

```typescript
// capability-map.ts
export const capabilityMap = {
  // UI 操作：Agent Tool
  "View library": "read_library",
  "Add book": "add_book",
  "Delete book": "delete_book",
  "Publish insight": "publish_to_feed",
  "Start research": "start_research",
  "View highlights": "read_library",  // 同一工具，不同查询
  "Edit profile": "write_file",
  "Search web": "web_search",
  "Export data": "N/A",  // 仅 UI 操作
};

// parity.test.ts
import { capabilityMap } from './capability-map';
import { getAgentTools } from './agent-config';
import { getSystemPrompt } from './system-prompt';

describe('操作平等性', () => {
  const agentTools = getAgentTools();
  const systemPrompt = getSystemPrompt();

  for (const [uiAction, toolName] of Object.entries(capabilityMap)) {
    if (toolName === 'N/A') continue;

    test(`"${uiAction}" 有 Agent tool：${toolName}`, () => {
      const toolNames = agentTools.map(t => t.name);
      expect(toolNames).toContain(toolName);
    });

    test(`${toolName} 在 system prompt 中有文档`, () => {
      expect(systemPrompt).toContain(toolName);
    });
  }
});
```

### 上下文平等性测试

```typescript
describe('上下文平等性', () => {
  test('Agent 看到 UI 显示的所有数据', async () => {
    // 设置：创建一些数据
    await libraryService.addBook({ id: "1", title: "Test Book" });
    await feedService.addItem({ id: "f1", content: "Test insight" });

    // 获取 system prompt（包括上下文）
    const systemPrompt = await buildSystemPrompt();

    // 验证数据是否被包括
    expect(systemPrompt).toContain("Test Book");
    expect(systemPrompt).toContain("Test insight");
  });

  test('最近的活动对 Agent 可见', async () => {
    // 执行一些操作
    await activityService.log({ action: "highlighted", bookId: "1" });
    await activityService.log({ action: "researched", bookId: "2" });

    const systemPrompt = await buildSystemPrompt();

    // 验证活动是否被包括
    expect(systemPrompt).toMatch(/highlighted|researched/);
  });
});
```
</parity_testing>

<integration_testing>
## 集成测试

从用户请求到结果的完整流程测试。

### 端到端流程测试

```typescript
describe('端到端流程', () => {
  test('研究流程：请求 → 网络搜索 → 文件创建', async () => {
    // 设置
    const bookId = "book_123";
    await libraryService.addBook({ id: bookId, title: "Moby Dick" });

    // 用户请求
    await agent.chat("Research the historical context of whaling in Moby Dick");

    // 验证：网络搜索被执行
    const searchCalls = mockWebSearch.mock.calls;
    expect(searchCalls.length).toBeGreaterThan(0);
    expect(searchCalls.some(call =>
      call[0].query.toLowerCase().includes("whaling")
    )).toBe(true);

    // 验证：文件被创建
    const researchFiles = await fileService.listFiles(`Research/${bookId}/`);
    expect(researchFiles.length).toBeGreaterThan(0);

    // 验证：内容相关
    const content = await fileService.readFile(researchFiles[0]);
    expect(content.toLowerCase()).toMatch(/whale|whaling|nantucket|melville/);
  });

  test('发布流程：请求 → 工具调用 → 信息流更新 → UI 反映', async () => {
    // 设置
    await libraryService.addBook({ id: "book_1", title: "1984" });

    // 初始状态
    const feedBefore = await feedService.getItems();

    // 用户请求
    await agent.chat("Write something about Big Brother for my reading feed");

    // 验证信息流已更新
    const feedAfter = await feedService.getItems();
    expect(feedAfter.length).toBe(feedBefore.length + 1);

    // 验证内容
    const newItem = feedAfter.find(item =>
      !feedBefore.some(old => old.id === item.id)
    );
    expect(newItem).toBeDefined();
    expect(newItem.content.toLowerCase()).toMatch(/big brother|surveillance|watching/);
  });
});
```

### 失败恢复测试

```typescript
describe('失败恢复', () => {
  test('Agent 优雅地处理缺失的书籍', async () => {
    const result = await agent.chat("Tell me about 'Nonexistent Book'");

    // Agent 不应该崩溃
    expect(result.error).toBeUndefined();

    // Agent 应该确认问题
    expect(result.response.toLowerCase()).toMatch(
      /not found|don't see|can't find|library/
    );
  });

  test('Agent 从 API 失败中恢复', async () => {
    // 模拟 API 失败
    mockWebSearch.mockRejectedValueOnce(new Error("Network error"));

    const result = await agent.chat("Research this topic");

    // Agent 应该优雅地处理
    expect(result.error).toBeUndefined();
    expect(result.response).not.toContain("unhandled exception");

    // Agent 应该传达问题
    expect(result.response.toLowerCase()).toMatch(
      /couldn't search|unable to|try again/
    );
  });
});
```
</integration_testing>

<snapshot_testing>
## System Prompt 快照测试

跟踪 system prompt 和上下文注入随时间的变化。

```typescript
describe('System Prompt 稳定性', () => {
  test('System prompt 结构与快照匹配', async () => {
    const systemPrompt = await buildSystemPrompt();

    // 提取结构（删除动态数据）
    const structure = systemPrompt
      .replace(/id: \w+/g, 'id: [ID]')
      .replace(/"[^"]+"/g, '"[TITLE]"')
      .replace(/\d{4}-\d{2}-\d{2}/g, '[DATE]');

    expect(structure).toMatchSnapshot();
  });

  test('所有能力部分都存在', async () => {
    const systemPrompt = await buildSystemPrompt();

    const requiredSections = [
      "Your Capabilities",
      "Available Books",
      "Recent Activity",
    ];

    for (const section of requiredSections) {
      expect(systemPrompt).toContain(section);
    }
  });
});
```
</snapshot_testing>

<manual_testing>
## 手动测试清单

某些事情最好在开发过程中手动测试：

### 自然语言变体测试

尝试多个相同请求的表述方式：

```
"Add this to my feed"
"Write something in my reading feed"
"Publish an insight about this"
"Put this in the feed"
"I want this in my feed"
```

如果上下文注入正确，所有这些都应该有效。

### 边界情况提示

```
"What can you do?"
→ Agent 应该描述能力

"Help me with my books"
→ Agent 应该与库互动，而不是问"书籍"是什么意思

"Write something"
→ Agent 应该询问在哪里（信息流、文件等）（如果不明确）

"Delete everything"
→ Agent 应该在执行破坏性操作前确认
```

### 混淆测试

问一些应该存在但可能没有正确连接的内容：

```
"What's in my research folder?"
→ 应该列出文件，而不是问"什么研究文件夹？"

"Show me my recent reading"
→ 应该显示活动，而不是问"你的意思是什么？"

"Continue where I left off"
→ 如果可用，应该参考最近的活动
```
</manual_testing>

<ci_integration>
## CI/CD 集成

将 Agent-native 测试添加到您的 CI 流程：

```yaml
# .github/workflows/test.yml
name: Agent-Native 测试

on: [push, pull_request]

jobs:
  agent-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: 设置
        run: npm install

      - name: 运行平等性测试
        run: npm run test:parity

      - name: 运行能力测试
        run: npm run test:capabilities
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}

      - name: 检查 System Prompt 完整性
        run: npm run test:system-prompt

      - name: 验证能力映射
        run: |
          # 确保能力映射是最新的
          npm run generate:capability-map
          git diff --exit-code capability-map.ts
```

### 成本感知测试

Agent 测试需要消耗 API token。管理策略：

```typescript
// 对基本测试使用较小的模型
const testConfig = {
  model: process.env.CI ? "claude-3-haiku" : "claude-3-opus",
  maxTokens: 500,  // 限制输出长度
};

// 为确定性测试缓存响应
const cachedAgent = new CachedAgent({
  cacheDir: ".test-cache",
  ttl: 24 * 60 * 60 * 1000,  // 24 小时
});

// 仅在主分支运行昂贵的测试
if (process.env.GITHUB_REF === 'refs/heads/main') {
  describe('完整集成测试', () => { ... });
}
```
</ci_integration>

<test_utilities>
## 测试工具类

### Agent 测试工具

```typescript
class AgentTestHarness {
  private agent: Agent;
  private mockServices: MockServices;

  async setup() {
    this.mockServices = createMockServices();
    this.agent = await createAgent({
      services: this.mockServices,
      model: "claude-3-haiku",  // 测试用成本更低
    });
  }

  async chat(message: string): Promise<AgentResponse> {
    return this.agent.chat(message);
  }

  async expectToolCall(toolName: string) {
    const lastResponse = this.agent.getLastResponse();
    expect(lastResponse.toolCalls.map(t => t.name)).toContain(toolName);
  }

  async expectOutcome(check: () => Promise<boolean>) {
    const result = await check();
    expect(result).toBe(true);
  }

  getState() {
    return {
      library: this.mockServices.library.getBooks(),
      feed: this.mockServices.feed.getItems(),
      files: this.mockServices.files.listAll(),
    };
  }
}

// 使用示例
test('完整流程', async () => {
  const harness = new AgentTestHarness();
  await harness.setup();

  await harness.chat("Add 'Moby Dick' to my library");
  await harness.expectToolCall("add_book");
  await harness.expectOutcome(async () => {
    const state = harness.getState();
    return state.library.some(b => b.title.includes("Moby"));
  });
});
```
</test_utilities>

<checklist>
## 测试清单

自动化测试：
- [ ] 针对每个 UI 操作的 "Agent 能做到吗？" 测试
- [ ] 位置感知测试（"写入我的信息流"）
- [ ] 平等性测试（工具存在，在 prompt 中有文档）
- [ ] 上下文平等性测试（Agent 看到 UI 显示的内容）
- [ ] 端到端流程测试
- [ ] 失败恢复测试

手动测试：
- [ ] 自然语言变体（多个表述方式有效）
- [ ] 边界情况提示（开放式请求）
- [ ] 混淆测试（Agent 知道应用术语）
- [ ] 惊喜测试（Agent 可以创意思考）

CI 集成：
- [ ] 平等性测试在每个 PR 上运行
- [ ] 能力测试使用 API 密钥运行
- [ ] System prompt 完整性检查
- [ ] 能力映射漂移检测
</checklist>
