<overview>
如何按照prompt原生原则设计MCP工具。工具应该是启用能力的原始操作，而不是编码决定的工作流。

**核心原则：** 用户能做什么，Agent就应该能做什么。不要人为限制Agent——给它与高级用户相同的原始操作。
</overview>

<principle name="primitives-not-workflows">
## 工具是原始操作，不是工作流

**错误方法：** 编码业务逻辑的工具
```typescript
tool("process_feedback", {
  feedback: z.string(),
  category: z.enum(["bug", "feature", "question"]),
  priority: z.enum(["low", "medium", "high"]),
}, async ({ feedback, category, priority }) => {
  // Tool决定如何处理
  const processed = categorize(feedback);
  const stored = await saveToDatabase(processed);
  const notification = await notify(priority);
  return { processed, stored, notification };
});
```

**正确方法：** 启用任何工作流的原始操作
```typescript
tool("store_item", {
  key: z.string(),
  value: z.any(),
}, async ({ key, value }) => {
  await db.set(key, value);
  return { text: `已存储${key}` };
});

tool("send_message", {
  channel: z.string(),
  content: z.string(),
}, async ({ channel, content }) => {
  await messenger.send(channel, content);
  return { text: "已发送" };
});
```

Agent根据系统prompt决定分类、优先级以及何时通知。
</principle>

<principle name="descriptive-names">
## 工具应具有描述性的原始操作名称

名称应描述能力，而不是用例：

| 错误 | 正确 |
|-------|-------|
| `process_user_feedback` | `store_item` |
| `create_feedback_summary` | `write_file` |
| `send_notification` | `send_message` |
| `deploy_to_production` | `git_push` |

prompt告诉Agent何时使用原始操作。工具只是提供能力。
</principle>

<principle name="simple-inputs">
## 输入应该简单

Tool接受数据。它们不接受决定。

**错误：** Tool接受决定
```typescript
tool("format_content", {
  content: z.string(),
  format: z.enum(["markdown", "html", "json"]),
  style: z.enum(["formal", "casual", "technical"]),
}, ...)
```

**正确：** Tool接受数据，Agent决定格式
```typescript
tool("write_file", {
  path: z.string(),
  content: z.string(),
}, ...)
// Agent决定用HTML内容写入index.html，或用JSON写入data.json
```
</principle>

<principle name="rich-outputs">
## 输出应该丰富

返回足够的信息供Agent验证和迭代。

**错误：** 最小输出
```typescript
async ({ key }) => {
  await db.delete(key);
  return { text: "已删除" };
}
```

**正确：** 丰富输出
```typescript
async ({ key }) => {
  const existed = await db.has(key);
  if (!existed) {
    return { text: `Key ${key}不存在` };
  }
  await db.delete(key);
  return { text: `已删除${key}。${await db.count()}个项目仍存在。` };
}
```
</principle>

<design_template>
## 工具设计模板

```typescript
import { createSdkMcpServer, tool } from "@anthropic-ai/claude-agent-sdk";
import { z } from "zod";

export const serverName = createSdkMcpServer({
  name: "server-name",
  version: "1.0.0",
  tools: [
    // READ operations
    tool(
      "read_item",
      "Read an item by key",
      { key: z.string().describe("Item key") },
      async ({ key }) => {
        const item = await storage.get(key);
        return {
          content: [{
            type: "text",
            text: item ? JSON.stringify(item, null, 2) : `Not found: ${key}`,
          }],
          isError: !item,
        };
      }
    ),

    tool(
      "list_items",
      "List all items, optionally filtered",
      {
        prefix: z.string().optional().describe("Filter by key prefix"),
        limit: z.number().default(100).describe("Max items"),
      },
      async ({ prefix, limit }) => {
        const items = await storage.list({ prefix, limit });
        return {
          content: [{
            type: "text",
            text: `Found ${items.length} items:\n${items.map(i => i.key).join("\n")}`,
          }],
        };
      }
    ),

    // WRITE operations
    tool(
      "store_item",
      "Store an item",
      {
        key: z.string().describe("Item key"),
        value: z.any().describe("Item data"),
      },
      async ({ key, value }) => {
        await storage.set(key, value);
        return {
          content: [{ type: "text", text: `Stored ${key}` }],
        };
      }
    ),

    tool(
      "delete_item",
      "Delete an item",
      { key: z.string().describe("Item key") },
      async ({ key }) => {
        const existed = await storage.delete(key);
        return {
          content: [{
            type: "text",
            text: existed ? `Deleted ${key}` : `${key} did not exist`,
          }],
        };
      }
    ),

    // EXTERNAL operations
    tool(
      "call_api",
      "Make an HTTP request",
      {
        url: z.string().url(),
        method: z.enum(["GET", "POST", "PUT", "DELETE"]).default("GET"),
        body: z.any().optional(),
      },
      async ({ url, method, body }) => {
        const response = await fetch(url, { method, body: JSON.stringify(body) });
        const text = await response.text();
        return {
          content: [{
            type: "text",
            text: `${response.status} ${response.statusText}\n\n${text}`,
          }],
          isError: !response.ok,
        };
      }
    ),
  ],
});
```
</design_template>

<example name="feedback-server">
## 示例：反馈存储服务器

此服务器提供用于存储反馈的原始操作。它不决定如何分类或组织反馈——那是Agent通过prompt的工作。

```typescript
export const feedbackMcpServer = createSdkMcpServer({
  name: "feedback",
  version: "1.0.0",
  tools: [
    tool(
      "store_feedback",
      "Store a feedback item",
      {
        item: z.object({
          id: z.string(),
          author: z.string(),
          content: z.string(),
          importance: z.number().min(1).max(5),
          timestamp: z.string(),
          status: z.string().optional(),
          urls: z.array(z.string()).optional(),
          metadata: z.any().optional(),
        }).describe("Feedback item"),
      },
      async ({ item }) => {
        await db.feedback.insert(item);
        return {
          content: [{
            type: "text",
            text: `Stored feedback ${item.id} from ${item.author}`,
          }],
        };
      }
    ),

    tool(
      "list_feedback",
      "List feedback items",
      {
        limit: z.number().default(50),
        status: z.string().optional(),
      },
      async ({ limit, status }) => {
        const items = await db.feedback.list({ limit, status });
        return {
          content: [{
            type: "text",
            text: JSON.stringify(items, null, 2),
          }],
        };
      }
    ),

    tool(
      "update_feedback",
      "Update a feedback item",
      {
        id: z.string(),
        updates: z.object({
          status: z.string().optional(),
          importance: z.number().optional(),
          metadata: z.any().optional(),
        }),
      },
      async ({ id, updates }) => {
        await db.feedback.update(id, updates);
        return {
          content: [{ type: "text", text: `Updated ${id}` }],
        };
      }
    ),
  ],
});
```

系统prompt然后告诉Agent如何使用这些原始操作：

```markdown
## 反馈处理

当有人分享反馈时：
1. 提取作者、内容和任何URL
2. 根据可行性将重要性评为1-5
3. 使用feedback.store_feedback存储
4. 如果重要性高（4-5），通知渠道

对重要性评级使用你的判断。
```
</example>

<principle name="dynamic-capability-discovery">
## 动态能力发现 vs 静态工具映射

**这个模式专门用于Agent原生应用**，你希望Agent能够完全访问外部API——与用户相同的访问权限。它遵循Agent原生的核心原则："用户能做什么，Agent就能做什么"。

如果你正在构建具有有限功能的受限Agent，静态工具映射可能是故意的。但对于与HealthKit、HomeKit、GraphQL或类似API集成的Agent原生应用：

**静态工具映射（Agent原生的反模式）：**
为每个API功能构建单独的工具。总是过时，将Agent限制于你预期的内容。

```typescript
// ❌ 静态：每个API类型需要一个硬编码的工具
tool("read_steps", async ({ startDate, endDate }) => {
  return healthKit.query(HKQuantityType.stepCount, startDate, endDate);
});

tool("read_heart_rate", async ({ startDate, endDate }) => {
  return healthKit.query(HKQuantityType.heartRate, startDate, endDate);
});

tool("read_sleep", async ({ startDate, endDate }) => {
  return healthKit.query(HKCategoryType.sleepAnalysis, startDate, endDate);
});

// 当HealthKit添加葡萄糖跟踪时...你需要代码更改
```

**动态能力发现（优选）：**
构建一个元工具来发现什么是可用的，以及一个通用工具来访问任何东西。

```typescript
// ✅ 动态：Agent发现并使用任何能力

// 发现工具 - 返回运行时可用的内容
tool("list_available_capabilities", async () => {
  const quantityTypes = await healthKit.availableQuantityTypes();
  const categoryTypes = await healthKit.availableCategoryTypes();

  return {
    text: `Available health metrics:\n` +
          `Quantity types: ${quantityTypes.join(", ")}\n` +
          `Category types: ${categoryTypes.join(", ")}\n` +
          `\nUse read_health_data with any of these types.`
  };
});

// 通用访问工具 - 类型是字符串，API验证
tool("read_health_data", {
  dataType: z.string(),  // NOT z.enum - let HealthKit validate
  startDate: z.string(),
  endDate: z.string(),
  aggregation: z.enum(["sum", "average", "samples"]).optional()
}, async ({ dataType, startDate, endDate, aggregation }) => {
  // HealthKit validates the type, returns helpful error if invalid
  const result = await healthKit.query(dataType, startDate, endDate, aggregation);
  return { text: JSON.stringify(result, null, 2) };
});
```

**When to Use Each Approach:**

| Dynamic (Agent-Native) | Static (Constrained Agent) |
|------------------------|---------------------------|
| Agent should access anything user can | Agent has intentionally limited scope |
| External API with many endpoints (HealthKit, HomeKit, GraphQL) | Internal domain with fixed operations |
| API evolves independently of your code | Tightly coupled domain logic |
| You want full action parity | You want strict guardrails |

**The agent-native default is Dynamic.** Only use Static when you're intentionally limiting the agent's capabilities.

**Complete Dynamic Pattern:**

```swift
// 1. Discovery tool: What can I access?
tool("list_health_types", "Get available health data types") { _ in
    let store = HKHealthStore()

    let quantityTypes = HKQuantityTypeIdentifier.allCases.map { $0.rawValue }
    let categoryTypes = HKCategoryTypeIdentifier.allCases.map { $0.rawValue }
    let characteristicTypes = HKCharacteristicTypeIdentifier.allCases.map { $0.rawValue }

    return ToolResult(text: """
        Available HealthKit types:

        ## Quantity Types (numeric values)
        \(quantityTypes.joined(separator: ", "))

        ## Category Types (categorical data)
        \(categoryTypes.joined(separator: ", "))

        ## Characteristic Types (user info)
        \(characteristicTypes.joined(separator: ", "))

        Use read_health_data or write_health_data with any of these.
        """)
}

// 2. Generic read: Access any type by name
tool("read_health_data", "Read any health metric", {
    dataType: z.string().describe("Type name from list_health_types"),
    startDate: z.string(),
    endDate: z.string()
}) { request in
    // Let HealthKit validate the type name
    guard let type = HKQuantityTypeIdentifier(rawValue: request.dataType)
                     ?? HKCategoryTypeIdentifier(rawValue: request.dataType) else {
        return ToolResult(
            text: "Unknown type: \(request.dataType). Use list_health_types to see available types.",
            isError: true
        )
    }

    let samples = try await healthStore.querySamples(type: type, start: startDate, end: endDate)
    return ToolResult(text: samples.formatted())
}

// 3. Context injection: Tell agent what's available in system prompt
func buildSystemPrompt() -> String {
    let availableTypes = healthService.getAuthorizedTypes()

    return """
    ## Available Health Data

    You have access to these health metrics:
    \(availableTypes.map { "- \($0)" }.joined(separator: "\n"))

    Use read_health_data with any type above. For new types not listed,
    use list_health_types to discover what's available.
    """
}
```

**Benefits:**
- Agent can use any API capability, including ones added after your code shipped
- API is the validator, not your enum definition
- Smaller tool surface (2-3 tools vs N tools)
- Agent naturally discovers capabilities by asking
- Works with any API that has introspection (HealthKit, GraphQL, OpenAPI)
</principle>

<principle name="crud-completeness">
## CRUD完整性

Agent能创建的每个数据类型，它都应该能够读取、更新和删除。不完整的CRUD =破损的操作奇偶性。

**反模式：仅创建的工具**
```typescript
// ❌ 可以创建但不能修改或删除
tool("create_experiment", { hypothesis, variable, metric })
tool("write_journal_entry", { content, author, tags })
// 用户："删除那个实验" → Agent："我不能做到"
```

**正确：每个实体的完整CRUD**
```typescript
// ✅ 完整CRUD
tool("create_experiment", { hypothesis, variable, metric })
tool("read_experiment", { id })
tool("update_experiment", { id, updates: { hypothesis?, status?, endDate? } })
tool("delete_experiment", { id })

tool("create_journal_entry", { content, author, tags })
tool("read_journal", { query?, dateRange?, author? })
tool("update_journal_entry", { id, content, tags? })
tool("delete_journal_entry", { id })
```

**CRUD审计：**
对于应用中的每个实体类型，验证：
- [ ] 创建：Agent可以创建新实例
- [ ] 读取：Agent可以查询/搜索/列表实例
- [ ] 更新：Agent可以修改现有实例
- [ ] 删除：Agent可以删除实例

如果任何操作缺失，用户最终会要求它，Agent将失败。
</principle>

<checklist>
## MCP工具设计检查清单

**基础：**
- [ ] 工具名称描述能力，而不是用例
- [ ] 输入是数据，不是决定
- [ ] 输出是丰富的（足以供Agent验证）
- [ ] CRUD操作是分离的工具（而不是一个超级工具）
- [ ] 工具实现中没有业务逻辑
- [ ] 错误状态通过`isError`清晰地沟通
- [ ] 描述解释工具做什么，而不是何时使用它

**动态能力发现（针对Agent原生应用）：**
- [ ] 对于Agent应该拥有完全访问权限的外部API，使用动态发现
- [ ] 为每个API表面包含`list_*`或`discover_*`工具
- [ ] 当API验证时使用字符串输入（不是枚举）
- [ ] 在运行时将可用功能注入系统prompt中
- [ ] 仅在有意限制Agent范围时才使用静态工具映射

**CRUD完整性：**
- [ ] 每个实体都有创建、读取、更新、删除操作
- [ ] 每个UI操作都有对应的Agent工具
- [ ] 测试："Agent能撤销它刚刚所做的吗？"
</checklist>
