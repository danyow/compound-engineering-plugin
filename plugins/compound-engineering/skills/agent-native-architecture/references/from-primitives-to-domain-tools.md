<overview>
从纯原始操作开始：bash、文件操作、基本存储。这证明了架构是否可行，并揭示了Agent实际需要什么。随着模式的出现，有意地添加领域特定的工具。本文档涵盖何时以及如何从原始操作演进到领域工具，以及何时升级到优化代码。
</overview>

<start_with_primitives>
## 从纯原始操作开始

从最原子化的工具开始每个Agent原生系统：

- `read_file` / `write_file` / `list_files`
- `bash`（用于其他所有操作）
- 基本存储（`store_item` / `get_item`）
- HTTP请求（`fetch_url`）

**为什么从这里开始：**

1. **证明架构** - 如果它能与原始操作一起工作，你的prompt就在发挥作用
2. **揭示实际需求** - 你会发现哪些领域概念很重要
3. **最大灵活性** - Agent可以做任何事情，而不仅仅是你预期的事情
4. **强制编写好的prompt** - 你不能把工具逻辑当作拐杖

### 示例：从原始操作开始

```typescript
// 只从这些开始
const tools = [
  tool("read_file", { path: z.string() }, ...),
  tool("write_file", { path: z.string(), content: z.string() }, ...),
  tool("list_files", { path: z.string() }, ...),
  tool("bash", { command: z.string() }, ...),
];

// Prompt处理领域逻辑
const prompt = `
处理反馈时：
1. 从data/feedback.json读取现有反馈
2. 添加新反馈并根据你的重要性评估（1-5）
3. 写入更新的文件
4. 如果重要性 >= 4，在data/alerts/中创建通知文件
`;
```
</start_with_primitives>

<when_to_add_domain_tools>
## 何时添加领域工具

随着模式的出现，你会想要添加领域特定的工具。这很好——但要有意为之。

### 词汇锚定

**何时添加领域工具：** Agent需要理解领域概念时。

`create_note`工具比"将文件写入笔记目录并采用这种格式"更好地教Agent"笔记"在你系统中的含义。

```typescript
// 没有领域工具 - Agent必须推断结构
await agent.chat("创建一个关于会议的笔记");
// Agent：写入...笔记/?文档/?什么格式？

// 有领域工具 - 词汇被锚定
tool("create_note", {
  title: z.string(),
  content: z.string(),
  tags: z.array(z.string()).optional(),
}, async ({ title, content, tags }) => {
  // Tool强制执行结构，Agent理解"笔记"
});
```

### 护栏

**何时添加领域工具：** 某些操作需要不应该留给Agent判断的验证或约束。

```typescript
// publish_to_feed可能强制执行格式要求或内容政策
tool("publish_to_feed", {
  bookId: z.string(),
  content: z.string(),
  headline: z.string().max(100),  // 强制标题长度
}, async ({ bookId, content, headline }) => {
  // 验证内容符合指导原则
  if (containsProhibitedContent(content)) {
    return { text: "内容不符合指导原则", isError: true };
  }
  // 强制执行适当的结构
  await feedService.publish({ bookId, content, headline, publishedAt: new Date() });
});
```

### 效率

**何时添加领域工具：** 常见操作会需要许多原始调用。

```typescript
// 原始方法：多次调用
await agent.chat("获取书籍详情");
// Agent：读取library.json、解析、查找书籍、读取full_text.txt、读取introduction.md...

// 领域工具：一次调用常见操作
tool("get_book_with_content", { bookId: z.string() }, async ({ bookId }) => {
  const book = await library.getBook(bookId);
  const fullText = await readFile(`Research/${bookId}/full_text.txt`);
  const intro = await readFile(`Research/${bookId}/introduction.md`);
  return { text: JSON.stringify({ book, fullText, intro }) };
});
```
</when_to_add_domain_tools>

<the_rule>
## 领域工具的规则

**领域工具应该代表用户角度的一个概念操作。**

它们可以包含机械验证，但**关于做什么或是否做的判断属于prompt中**。

### 错误：捆绑判断

```typescript
// 错误 - analyze_and_publish将判断捆绑到工具中
tool("analyze_and_publish", async ({ input }) => {
  const analysis = analyzeContent(input);      // Tool决定如何分析
  const shouldPublish = analysis.score > 0.7;  // Tool决定是否发布
  if (shouldPublish) {
    await publish(analysis.summary);            // Tool决定发布什么
  }
});
```

### 正确：一个操作，Agent决定

```typescript
// 正确 - 分离的工具，Agent决定
tool("analyze_content", { content: z.string() }, ...);  // 返回分析
tool("publish", { content: z.string() }, ...);          // 发布Agent提供的内容

// Prompt："分析内容。如果质量很高，发布摘要。"
// Agent决定"高质量"意味着什么以及写什么摘要。
```

### 测试

问：谁在做决定？

- 如果答案是"工具代码" → 你已经编码了判断，需要重构
- 如果答案是"基于prompt的Agent" → 很好
</the_rule>

<keep_primitives_available>
## 保持原始操作可用

**领域工具是快捷方式，不是门卫。**

除非有特定理由限制访问（安全、数据完整性），否则Agent仍然应该能够为边缘情况使用底层原始操作。

```typescript
// 常见情况的领域工具
tool("create_note", { title, content }, ...);

// 但原始操作仍然可用于边缘情况
tool("read_file", { path }, ...);
tool("write_file", { path, content }, ...);

// Agent可以正常使用create_note，但对于奇怪的边缘情况：
// "在非标准位置创建带有自定义元数据的笔记"
// → Agent直接使用write_file
```

### 何时限制

限制（使领域工具成为唯一方式）适合于：

- **安全：** 用户认证、支付处理
- **数据完整性：** 必须维护不变量的操作
- **审计要求：** 必须以特定方式记录的操作

**默认是开放的。** 当你确实限制某些东西时，要有明确的理由。
</keep_primitives_available>

<graduating_to_code>
## 升级到代码

某些操作将需要从Agent编排的转移到优化代码，以获得性能或可靠性。

### 进展

```
阶段1：Agent在循环中使用原始操作
       → 灵活，证明概念
       → 缓慢，可能昂贵

阶段2：为常见操作添加领域工具
       → 更快，仍由Agent编排
       → Agent仍然决定何时/是否使用

阶段3：对于热路径，在优化代码中实现
       → 快速、确定性
       → Agent仍可以触发，但执行是代码
```

### 示例进展

**阶段1：纯原始操作**
```markdown
Prompt："当用户要求摘要时，读取/notes中的所有笔记，
        分析它们，并将摘要写入/summaries/{date}.md"

Agent：调用read_file 20次，推断内容，编写摘要
时间：30秒，50k tokens
```

**阶段2：领域工具**
```typescript
tool("get_all_notes", {}, async () => {
  const notes = await readAllNotesFromDirectory();
  return { text: JSON.stringify(notes) };
});

// Agent仍然决定如何摘要，但检索更快
// 时间：10秒，30k tokens
```

**阶段3：优化代码**
```typescript
tool("generate_weekly_summary", {}, async () => {
  // 整个操作在热路径代码中
  const notes = await getNotes({ since: oneWeekAgo });
  const summary = await generateSummary(notes);  // 可能使用更便宜的模型
  await writeSummary(summary);
  return { text: "摘要已生成" };
});

// Agent只是触发它
// 时间：2秒，5k tokens
```

### 注意事项

**即使操作升级到代码，Agent仍然应该能够：**

1. 触发优化的操作本身
2. 对于优化路径不处理的边缘情况回退到原始操作

升级是关于效率。**奇偶性仍然成立。** 当你优化时，Agent不会失去能力。
</graduating_to_code>

<decision_framework>
## Decision Framework

### 应该添加领域工具吗？

| 问题 | 如果是 |
|----------|--------|
| Agent是否对这个概念的含义感到困惑？ | 为词汇锚定添加 |
| 这个操作是否需要Agent不应该决定的验证？ | 添加护栏 |
| 这是一个常见的多步操作吗？ | 为效率添加 |
| 改变行为是否需要代码更改？ | 改为保持在prompt中 ||## 应该添加领域工具吗？

| 问题 | 如果是 |
|----------|--------|
| Agent是否对这个概念的含义感到困惑？ | 为词汇锚定添加 |
| 这个操作是否需要Agent不应该决定的验证？ | 添加护栏 |
| 这是一个常见的多步操作吗？ | 为效率添加 |
| 改变行为是否需要代码更改？ | 改为保持在prompt中 |

### 应该升级到代码吗？

| 问题 | 如果是 |
|----------|--------|
| 这个操作是否被调用得非常频繁？ | 考虑升级 |
| 延迟是否显著重要？ | 考虑升级 |
| Token成本是否有问题？ | 考虑升级 |
| 你是否需要确定性行为？ | 升级到代码 |
| 这个操作是否需要复杂的状态管理？ | 升级到代码 ||### 应该升级到代码吗？

| 问题 | 如果是 |
|----------|--------|
| 这个操作是否被调用得非常频繁？ | 考虑升级 |
| 延迟是否显著重要？ | 考虑升级 |
| Token成本是否有问题？ | 考虑升级 |
| 你是否需要确定性行为？ | 升级到代码 |
| 这个操作是否需要复杂的状态管理？ | 升级到代码 |

### 应该限制访问吗？

| 问题 | 如果是 |
|----------|--------|
| 是否有安全要求？ | 适当地限制 |
| 这个操作是否必须保持数据完整性？ | 适当地限制 |
| 是否有审计/合规要求？ | 适当地限制 |
| 是否只是"更安全"没有特定风险？ | 保持原始操作可用 ||### 应该限制访问吗？

| 问题 | 如果是 |
|----------|--------|
| 是否有安全要求？ | 适当地限制 |
| 这个操作是否必须保持数据完整性？ | 适当地限制 |
| 是否有审计/合规要求？ | 适当地限制 |
| 是否只是"更安全"没有特定风险？ | 保持原始操作可用 |
</decision_framework>

<examples>
## 示例

### 反馈处理演变

**阶段1：仅原始操作**
```typescript
tools: [read_file, write_file, bash]
prompt: "将反馈存储在data/feedback.json，如果重要则通知"
// Agent解决JSON结构、重要性标准、通知方法
```

**阶段2：词汇的领域工具**
```typescript
tools: [
  store_feedback,      // 用适当的结构锚定"反馈"概念
  send_notification,   // 用正确的渠道锚定"通知"
  read_file,           // 仍然可用于边缘情况
  write_file,
]
prompt: "使用store_feedback存储反馈。如果重要性 >= 4则通知。"
// Agent仍然决定重要性，但词汇被锚定
```

**阶段3：升级的热路径**
```typescript
tools: [
  process_feedback_batch,  // 针对高容量处理优化
  store_feedback,          // 用于单个项
  send_notification,
  read_file,
  write_file,
]
// 批处理是代码，但Agent仍然可以为特殊情况使用store_feedback
```

### 何时不添加领域工具

**不要只为了让事情"更清洁"而添加领域工具：**
```typescript
// 不必要 - Agent可以组合原始操作
tool("organize_files_by_date", ...)  // 只需使用move_file + 判断

// 不必要 - 把决定放在错误的地方
tool("decide_file_importance", ...)  // 这是prompt领地
```

**如果行为可能改变，不要添加领域工具：**
```typescript
// 不好 - 锁定在代码中
tool("generate_standard_report", ...)  // 如果报告格式演变怎么办？

// 更好 - 保持在prompt中
prompt: "生成涵盖X、Y、Z的报告。格式以提高可读性。"
// 可以通过编辑prompt调整格式
```
</examples>

<checklist>
## 检查清单：原始操作到领域工具

### 开始
- [ ] 从纯原始操作开始（读、写、列表、bash）
- [ ] 在prompt中编写行为，不是在工具逻辑中
- [ ] 让模式从实际使用中出现

### 添加领域工具
- [ ] 清晰的理由：词汇锚定、护栏或效率
- [ ] 工具代表一个概念操作
- [ ] 判断保留在prompt中，不是工具代码
- [ ] 原始操作与领域工具一起保持可用

### 升级到代码
- [ ] 识别的热路径（频繁、延迟敏感或昂贵）
- [ ] 优化版本不删除Agent能力
- [ ] 为边缘情况的原始操作回退仍然有效

### 限制决定
- [ ] 每个限制的具体理由（安全、完整性、审计）
- [ ] 默认是开放访问
- [ ] 限制是有意识的决定，不是默认行为
</checklist>
