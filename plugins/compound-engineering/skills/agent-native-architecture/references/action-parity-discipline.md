<overview>
一个结构化的规则,确保 agent 能够执行用户可以执行的所有操作。每个 UI 操作都应该有对应的 agent tool。这不是一次性的检查——而是集成到开发工作流中的持续实践。

**核心原则:**添加 UI 功能时,在同一个 PR 中添加相应的 tool。
</overview>

<why_parity>
## 为什么操作对等性很重要

**失败案例:**
```
用户: "在我的阅读动态中写一些关于叶卡捷琳娜大帝的内容"
Agent: "你指的是什么系统?我不确定阅读动态是什么意思。"
```

用户可以通过 UI 发布到他们的动态。但 agent 没有 `publish_to_feed` tool。修复很简单——添加这个 tool。但这个洞察意义深远:

**用户可以通过 UI 执行的每个操作,都必须有 agent 可以调用的等价 tool。**

没有这种对等性会导致:
- 用户要求 agent 做它做不到的事情
- Agent 对本应理解的功能询问澄清问题
- 相比直接使用应用,agent 感觉受限
- 用户对 agent 的能力失去信任
</why_parity>

<capability_mapping>
## 能力映射表

维护一个 UI 操作到 agent tool 的结构化映射:

| UI 操作 | UI 位置 | Agent Tool | System Prompt 引用 |
|-----------|-------------|------------|-------------------------|
| 查看图书馆 | Library 标签 | `read_library` | "查看书籍和高亮" |
| 添加书籍 | Library → Add | `add_book` | "添加书籍到图书馆" |
| 发布洞察 | 分析视图 | `publish_to_feed` | "创建 Feed 标签的洞察" |
| 开始研究 | 书籍详情 | `start_research` | "通过网络搜索研究书籍" |
| 编辑个人资料 | 设置 | `write_file(profile.md)` | "更新阅读个人资料" |
| 拍摄截图 | 相机 | N/A (用户操作) | — |
| 搜索网络 | 聊天 | `web_search` | "搜索互联网" |

**添加功能时更新此表。**

### 你的应用模板

```markdown
# 能力映射表 - [你的应用名称]

| UI 操作 | UI 位置 | Agent Tool | System Prompt | 状态 |
|-----------|-------------|------------|---------------|--------|
| | | | | ⚠️ 缺失 |
| | | | | ✅ 完成 |
| | | | | 🚫 N/A |
```

状态含义:
- ✅ 完成: Tool 存在且已在 system prompt 中文档化
- ⚠️ 缺失: UI 操作存在但没有 agent 等价物
- 🚫 N/A: 仅用户操作(例如生物识别认证、相机拍摄)
</capability_mapping>

<parity_workflow>
## 操作对等性工作流

### 添加新功能时

在合并任何添加 UI 功能的 PR 之前:

```
1. 这是什么操作?
   → "用户可以向他们的阅读动态发布洞察"

2. 是否存在 agent tool?
   → 检查 tool 定义
   → 如果没有: 创建 tool

3. 是否在 system prompt 中文档化?
   → 检查 system prompt 能力部分
   → 如果没有: 添加文档

4. 上下文是否可用?
   → Agent 是否知道"动态"的含义?
   → Agent 是否看到可用的书籍?
   → 如果没有: 添加到上下文注入

5. 更新能力映射表
   → 向跟踪文档添加行
```

### PR 检查清单

添加到你的 PR 模板:

```markdown
## Agent-Native 检查清单

- [ ] 每个新的 UI 操作都有对应的 agent tool
- [ ] System prompt 已更新以提及新能力
- [ ] Agent 可以访问 UI 使用的相同数据
- [ ] 能力映射表已更新
- [ ] 使用自然语言请求进行测试
```
</parity_workflow>

<parity_audit>
## 对等性审计

定期审计你的应用中的操作对等性差距:

### 步骤 1: 列出所有 UI 操作

浏览每个界面并列出用户可以执行的操作:

```
图书馆界面:
- 查看书籍列表
- 搜索书籍
- 按类别筛选
- 添加新书籍
- 删除书籍
- 打开书籍详情

书籍详情界面:
- 查看书籍信息
- 开始研究
- 查看高亮
- 添加高亮
- 分享书籍
- 从图书馆移除

动态界面:
- 查看洞察
- 创建新洞察
- 编辑洞察
- 删除洞察
- 分享洞察

设置:
- 编辑个人资料
- 更改主题
- 导出数据
- 删除账户
```

### 步骤 2: 检查 Tool 覆盖

对于每个操作,验证:

```
✅ 查看书籍列表      → read_library
✅ 搜索书籍          → read_library (带查询参数)
⚠️ 按类别筛选       → 缺失 (需要向 read_library 添加 filter 参数)
⚠️ 添加新书籍       → 缺失 (需要 add_book tool)
✅ 删除书籍          → delete_book
✅ 打开书籍详情      → read_library (单本书)

✅ 开始研究          → start_research
✅ 查看高亮          → read_library (包含高亮)
⚠️ 添加高亮         → 缺失 (需要 add_highlight tool)
⚠️ 分享书籍         → 缺失 (或 N/A 如果分享仅限 UI)

✅ 查看洞察          → read_library (包含动态)
✅ 创建新洞察        → publish_to_feed
⚠️ 编辑洞察         → 缺失 (需要 update_feed_item tool)
⚠️ 删除洞察         → 缺失 (需要 delete_feed_item tool)
```

### 步骤 3: 优先处理差距

并非所有差距都同等重要:

**高优先级 (用户会要求这个):**
- 添加新书籍
- 创建/编辑/删除内容
- 核心工作流操作

**中等优先级 (偶尔请求):**
- 筛选/搜索变体
- 导出功能
- 分享功能

**低优先级 (很少通过 agent 请求):**
- 主题更改
- 账户删除
- UI 偏好设置
</parity_audit>

<tool_design_for_parity>
## 为对等性设计 Tool

### Tool 粒度要匹配 UI 粒度

如果 UI 有独立的"编辑"和"删除"按钮,考虑使用独立的 tool:

```typescript
// 匹配 UI 粒度
tool("update_feed_item", { id, content, headline }, ...);
tool("delete_feed_item", { id }, ...);

// vs. 合并的(agent 更难发现)
tool("modify_feed_item", { id, action: "update" | "delete", ... }, ...);
```

### Tool 名称使用用户词汇

```typescript
// 好: 匹配用户所说的
tool("publish_to_feed", ...);  // "发布到我的动态"
tool("add_book", ...);         // "添加这本书"
tool("start_research", ...);   // "研究这个"

// 不好: 技术术语
tool("create_analysis_record", ...);
tool("insert_library_item", ...);
tool("initiate_web_scrape_workflow", ...);
```

### 返回 UI 显示的内容

如果 UI 显示带详情的确认信息,tool 也应该这样:

```typescript
// UI 显示: "已将'白鲸记'添加到你的图书馆"
// Tool 应该返回相同内容:
tool("add_book", async ({ title, author }) => {
  const book = await library.add({ title, author });
  return {
    text: `已将"${book.title}"(作者:${book.author})添加到你的图书馆 (id: ${book.id})`
  };
});
```
</tool_design_for_parity>

<context_parity>
## 上下文对等性

无论用户看到什么,Agent 都应该能够访问。

### 问题

```swift
// UI 在列表中显示最近的分析
ForEach(analysisRecords) { record in
    AnalysisRow(record: record)
}

// 但 system prompt 只提到书籍,不提到分析
let systemPrompt = """
## 可用书籍
\(books.map { $0.title })
// 缺失:最近的分析!
"""
```

用户看到他们的阅读日记。Agent 看不到。这会产生不一致。

### 解决方案

```swift
// System prompt 包含 UI 显示的内容
let systemPrompt = """
## 可用书籍
\(books.map { "- \($0.title)" }.joined(separator: "\n"))

## 最近的阅读日记
\(analysisRecords.prefix(10).map { "- \($0.summary)" }.joined(separator: "\n"))
"""
```

### 上下文对等性检查清单

对于应用中的每个屏幕:
- [ ] 此屏幕显示什么数据?
- [ ] Agent 可以访问该数据吗?
- [ ] Agent 可以访问相同的详细程度吗?
</context_parity>

<continuous_parity>
## 长期维护对等性

### Git Hook 和 CI 检查

```bash
#!/bin/bash
# 预提交钩子:检查没有 tool 的新 UI 操作

# 查找新的 SwiftUI Button/onTapGesture 添加
NEW_ACTIONS=$(git diff --cached --name-only | xargs grep -l "Button\|onTapGesture")

if [ -n "$NEW_ACTIONS" ]; then
    echo "⚠️  检测到新的 UI 操作。你是否添加了相应的 agent tool?"
    echo "文件: $NEW_ACTIONS"
    echo ""
    echo "检查清单:"
    echo "  [ ] Agent tool 存在于新操作"
    echo "  [ ] System prompt 文档化了新能力"
    echo "  [ ] 能力映射表已更新"
fi
```

### 自动化对等性测试

```typescript
// parity.test.ts
describe('操作对等性', () => {
  const capabilityMap = loadCapabilityMap();

  for (const [action, toolName] of Object.entries(capabilityMap)) {
    if (toolName === 'N/A') continue;

    test(`${action} 有 agent tool: ${toolName}`, () => {
      expect(agentTools.map(t => t.name)).toContain(toolName);
    });

    test(`${toolName} 在 system prompt 中有文档`, () => {
      expect(systemPrompt).toContain(toolName);
    });
  }
});
```

### 定期审计

定期安排复查:

```markdown
## 月度对等性审计

1. 检查本月合并的所有 PR
2. 检查每个 PR 中的新 UI 操作
3. 验证 tool 覆盖
4. 更新能力映射表
5. 使用自然语言请求进行测试
```
</continuous_parity>

<examples>
## 真实例子:动态间隙

**之前:** 每个阅读应用都有一个动态,其中的洞察会出现,但没有 agent tool 来发布。

```
用户: "在我的阅读动态中写一些关于叶卡捷琳娜大帝的内容"
Agent: "我不确定你指的是什么系统。你能澄清一下吗?"
```

**诊断:**
- ✅ UI 操作:用户可以从分析视图发布洞察
- ❌ Agent tool: 没有 `publish_to_feed` tool
- ❌ System prompt: 没有提到"动态"或如何发布
- ❌ Context: Agent 不知道"动态"的含义

**修复:**

```swift
// 1. 添加 tool
tool("publish_to_feed",
    "发布洞察到用户的阅读动态",
    {
        bookId: z.string().describe("书籍 ID"),
        content: z.string().describe("洞察内容"),
        headline: z.string().describe("吸引人的标题")
    },
    async ({ bookId, content, headline }) => {
        await feedService.publish({ bookId, content, headline });
        return { text: `已发布"${headline}"到你的阅读动态` };
    }
);

// 2. 更新 system prompt
"""
## 你的能力

- **发布到动态**: 使用 `publish_to_feed` 创建在动态标签页中出现的洞察。
  包括 book_id、content 和吸引人的标题。
"""

// 3. 添加到上下文注入
"""
当用户提到"动态"或"阅读动态"时,他们指的是显示洞察的动态标签页。
使用 `publish_to_feed` 在那里创建内容。
"""
```

**之后:**
```
用户: "在我的阅读动态中写一些关于叶卡捷琳娜大帝的内容"
Agent: [使用 publish_to_feed 创建洞察]
       "完成!我已发布'开明女皇'到你的阅读动态。"
```
</examples>

<checklist>
## 操作对等性检查清单

对于每个带 UI 变更的 PR:
- [ ] 列出所有新的 UI 操作
- [ ] 验证每个操作都有对应的 agent tool
- [ ] 更新 system prompt 中的新能力
- [ ] 添加到能力映射表
- [ ] 使用自然语言请求进行测试

对于定期审计:
- [ ] 浏览每个屏幕
- [ ] 列出所有可能的用户操作
- [ ] 检查每个操作的 tool 覆盖
- [ ] 按用户请求的可能性优先处理差距
- [ ] 为高优先级差距创建任务
</checklist>
