<overview>
如何重构现有Agent代码以遵循prompt原生原则。目标：将行为从代码移动到prompt中，并将工具简化为原始操作。
</overview>

<diagnosis>
## 诊断非Prompt原生代码

你的Agent不是prompt原生的迹象：

**编码工作流的工具：**
```typescript
// 红旗：工具包含业务逻辑
tool("process_feedback", async ({ message }) => {
  const category = categorize(message);        // 代码中的逻辑
  const priority = calculatePriority(message); // 代码中的逻辑
  await store(message, category, priority);    // 代码中的编排
  if (priority > 3) await notify();            // 代码中的决定
});
```

**Agent调用函数而不是自己解决问题：**
```typescript
// 红旗：Agent只是一个函数调用者
"使用process_feedback处理传入消息"
// vs.
"当反馈来临时，决定重要性，存储它，如果很高则通知"
```

**Agent能力的人工限制：**
```typescript
// 红旗：工具阻止Agent做用户能做的事
tool("read_file", async ({ path }) => {
  if (!ALLOWED_PATHS.includes(path)) {
    throw new Error("不允许读取此文件");
  }
  return readFile(path);
});
```

**指定HOW而不是WHAT的Prompt：**
```markdown
// 红旗：微管理Agent
创建摘要时：
1. 使用恰好3个项目符号点
2. 每个项目符号必须在20个单词以下
3. 使用em破折号格式化子点
4. 每个项目符号的第一个单词加粗
```
</diagnosis>

<refactoring_workflow>
## 分步重构

**步骤1：识别工作流工具**

列出所有工具。标记任何：
- 具有业务逻辑（分类、计算、决定）
- 编排多个操作
- 代表Agent做决定
- 包含条件逻辑（基于内容的if/else）

**步骤2：提取原始操作**

对于每个工作流工具，识别底层原始操作：

| 工作流工具 | 隐藏的原始操作 |
|---------------|-------------------|
| `process_feedback` | `store_item`, `send_message` |
| `generate_report` | `read_file`, `write_file` |
| `deploy_and_notify` | `git_push`, `send_message` |

**步骤3：将行为移到prompt中**

从工作流工具中获取逻辑并用自然语言表示：

```typescript
// 之前（在代码中）：
async function processFeedback(message) {
  const priority = message.includes("crash") ? 5 :
                   message.includes("bug") ? 4 : 3;
  await store(message, priority);
  if (priority >= 4) await notify();
}
```

```markdown
// 之后（在prompt中）：
## 反馈处理

当有人分享反馈时：
1. 评价重要性1-5：
   - 5：崩溃、数据丢失、安全问题
   - 4：具有明确重现步骤的bug报告
   - 3：一般建议、次要问题
2. 使用store_item存储
3. 如果重要性 >= 4，通知团队

使用你的判断。Context比关键字更重要。
```

**步骤4：将工具简化为原始操作**

```typescript
// 之前：1个工作流工具
tool("process_feedback", { message, category, priority }, ...复杂逻辑...)

// 之后：2个原始工具
tool("store_item", { key: z.string(), value: z.any() }, ...简单存储...)
tool("send_message", { channel: z.string(), content: z.string() }, ...简单发送...)
```

**步骤5：删除人工限制**

```typescript
// 之前：能力受限
tool("read_file", async ({ path }) => {
  if (!isAllowed(path)) throw new Error("禁止");
  return readFile(path);
});

// 之后：完整能力
tool("read_file", async ({ path }) => {
  return readFile(path);  // Agent可以读取任何内容
});
// 对WRITES使用审批门，而不是对READS的人工限制
```

**步骤6：以结果而不是过程进行测试**

而不是测试"它是否调用正确的函数？"，测试"它是否实现结果？"

```typescript
// 之前：测试过程
expect(mockProcessFeedback).toHaveBeenCalledWith(...)

// 之后：测试结果
// 发送反馈 → 检查它是否以合理的重要性存储
// 发送高优先级反馈 → 检查是否发送了通知
```
</refactoring_workflow>

<before_after>
## 之前/之后示例

**示例1：反馈处理**

之前：
```typescript
tool("handle_feedback", async ({ message, author }) => {
  const category = detectCategory(message);
  const priority = calculatePriority(message, category);
  const feedbackId = await db.feedback.insert({
    id: generateId(),
    author,
    message,
    category,
    priority,
    timestamp: new Date().toISOString(),
  });

  if (priority >= 4) {
    await discord.send(ALERT_CHANNEL, `来自${author}的高优先级反馈`);
  }

  return { feedbackId, category, priority };
});
```

之后：
```typescript
// 简单的存储原始
tool("store_feedback", async ({ item }) => {
  await db.feedback.insert(item);
  return { text: `已存储反馈${item.id}` };
});

// 简单的消息原始
tool("send_message", async ({ channel, content }) => {
  await discord.send(channel, content);
  return { text: "已发送" };
});
```

系统prompt：
```markdown
## Feedback Processing

当有人分享反馈时：
1. 生成唯一ID
2. 根据影响和紧急性评价重要性1-5
3. 使用store_feedback存储完整项
4. 如果重要性 >= 4，向团队渠道发送通知

重要性指南：
- 5：关键（崩溃、数据丢失、安全）
- 4：高（详细的bug报告、阻塞问题）
- 3：中等（建议、次要bug）
- 2：低（装饰性、边界情况）
- 1：最小（离题、重复）
```

**示例2：报告生成**

Before:
```typescript
tool("generate_weekly_report", async ({ startDate, endDate, format }) => {
  const data = await fetchMetrics(startDate, endDate);
  const summary = summarizeMetrics(data);
  const charts = generateCharts(data);

  if (format === "html") {
    return renderHtmlReport(summary, charts);
  } else if (format === "markdown") {
    return renderMarkdownReport(summary, charts);
  } else {
    return renderPdfReport(summary, charts);
  }
});
```

After:
```typescript
tool("query_metrics", async ({ start, end }) => {
  const data = await db.metrics.query({ start, end });
  return { text: JSON.stringify(data, null, 2) };
});

tool("write_file", async ({ path, content }) => {
  writeFileSync(path, content);
  return { text: `已写入${path}` };
});
```

System prompt:
```markdown
## 报告生成

当被要求生成报告时：
1. 使用query_metrics查询相关指标
2. 分析数据并识别关键趋势
3. 创建清晰、格式良好的报告
4. 使用write_file以适当的格式写入

根据你的判断关于格式和结构。使其有用。
```
</before_after>

<common_challenges>
## 常见重构挑战

**"但Agent可能会犯错！"**

是的，你可以迭代。改变prompt来添加指导：
```markdown
// 之前
评价重要性1-5。

// 之后（如果Agent保持评级过高）
评价重要性1-5。保持保守——大多数反馈是2-3。
仅对真正的阻塞或关键问题使用4-5。
```

**"工作流很复杂！"**

复杂的工作流仍然可以在prompt中表示。Agent很聪明。
```markdown
处理视频反馈时：
1. 检查是否是Loom、YouTube或直接链接
2. 对于YouTube，直接将URL传递给视频分析
3. 对于其他人，首先下载，然后分析
4. 提取带时间戳的问题
5. 根据问题密度和严重性评价
```

**"我们需要确定性行为！"**

某些操作应该保留在代码中。没关系。Prompt原生不是全有或全无。

保持在代码中：
- 安全验证
- 速率限制
- 审计日志
- 精确的格式要求

移到prompt中：
- 分类决定
- 优先级判断
- 内容生成
- 工作流编排

**"测试呢？"**

测试结果而不是过程：
- "给定此输入，Agent是否实现了正确的结果？"
- "存储的反馈是否具有合理的重要性评级？"
- "真正的高优先级项目是否发送了通知？"
</common_challenges>

<checklist>
## 重构检查清单

诊断：
- [ ] 列出了所有具有业务逻辑的工具
- [ ] 识别了Agent能力的人工限制
- [ ] 找到了微管理HOW的prompt

重构：
- [ ] 从工作流工具中提取了原始操作
- [ ] 将业务逻辑移到系统prompt
- [ ] 删除了人工限制
- [ ] 简化了工具输入为数据，而不是决定

验证：
- [ ] Agent用原始操作实现了相同的结果
- [ ] 行为可以通过编辑prompt来改变
- [ ] 可以在没有新工具的情况下添加新功能
</checklist>
