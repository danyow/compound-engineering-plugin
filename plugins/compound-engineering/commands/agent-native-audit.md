---
name: agent-native-audit
description: 使用评分原则运行全面的 agent-native 架构审查
argument-hint: "[可选：要审计的特定原则]"
---

# Agent-Native 架构审计

根据 agent-native 架构原则对代码库进行全面审查，为每个原则启动并行子 agent 并生成评分报告。

## 要审计的核心原则

1. **动作对等** - "用户能做什么，agent 就能做什么"
2. **工具作为原语** - "工具提供能力，而非行为"
3. **上下文注入** - "系统提示包含关于应用状态的动态上下文"
4. **共享工作空间** - "Agent 和用户在相同的数据空间中工作"
5. **CRUD 完整性** - "每个实体都有完整的 CRUD（创建、读取、更新、删除）"
6. **UI 集成** - "Agent 操作立即反映在 UI 中"
7. **能力发现** - "用户可以发现 agent 能做什么"
8. **提示原生特性** - "特性是定义结果的提示，而非代码"

## 工作流

### 步骤 1：加载 Agent-Native Skill

首先，调用 agent-native-architecture skill 以理解所有原则：

```
/compound-engineering:agent-native-architecture
```

选择选项 7（动作对等）以加载完整参考材料。

### 步骤 2：启动并行子 Agent

使用 Task 工具启动 8 个并行子 agent（`subagent_type: Explore`），每个原则一个。每个 agent 应该：

1. 枚举代码库中的所有实例（用户操作、工具、上下文、数据存储等）
2. 检查是否符合原则
3. 提供具体评分，如 "X / Y（百分比%）"
4. 列出具体差距和建议

<sub-agents>

**Agent 1：动作对等**
```
审计动作对等 - "用户能做什么，agent 就能做什么。"

任务：
1. 枚举前端中的所有用户操作（API 调用、按钮点击、表单提交）
   - 搜索 API 服务文件、fetch 调用、表单处理器
   - 检查路由和组件中的用户交互
2. 检查哪些有对应的 agent 工具
   - 搜索 agent 工具定义
   - 将用户操作映射到 agent 能力
3. 评分："Agent 可以做 X / Y 用户操作"

格式：
## 动作对等审计
### 发现的用户操作
| 操作 | 位置 | Agent 工具 | 状态 |
### 评分：X/Y（百分比%）
### 缺失的 Agent 工具
### 建议
```

**Agent 2：工具作为原语**
```
审计工具作为原语 - "工具提供能力，而非行为。"

任务：
1. 查找并阅读所有 agent 工具文件
2. 将每个分类为：
   - 原语（好）：read、write、store、list - 提供能力而无业务逻辑
   - 工作流（坏）：编码业务逻辑、做出决策、编排步骤
3. 评分："X / Y 工具是正确的原语"

格式：
## 工具作为原语审计
### 工具分析
| 工具 | 文件 | 类型 | 理由 |
### 评分：X/Y（百分比%）
### 有问题的工具（应该是原语的工作流）
### 建议
```

**Agent 3：上下文注入**
```
审计上下文注入 - "系统提示包含关于应用状态的动态上下文"

任务：
1. 查找上下文注入代码（搜索 "context"、"system prompt"、"inject"）
2. 阅读 agent 提示和系统消息
3. 枚举已注入的内容与应该注入的内容：
   - 可用资源（文件、草稿、文档）
   - 用户偏好/设置
   - 最近活动
   - 列出的可用能力
   - 会话历史
   - 工作空间状态

格式：
## 上下文注入审计
### 上下文类型分析
| 上下文类型 | 是否已注入？ | 位置 | 备注 |
### 评分： X/Y (百分比%)
### 缺失的上下文
### 建议
```

**Agent 4：共享工作空间**
```
审计SHARED WORKSPACE - "Agent and user work in the same data space"

任务：
1. Identify all data stores/tables/models
2. Check if agents read/write to SAME tables or separate ones
3. Look for sandbox isolation anti-pattern (agent has separate data space)

格式：
## 共享工作空间审计
### 数据存储分析
| 数据存储 | 用户访问 | Agent 访问 | 是否共享？ |
### 评分： X/Y (百分比%)
### 隔离数据（反模式）
### 建议
```

**Agent 5：CRUD 完整性**
```
审计CRUD COMPLETENESS - "Every entity has full CRUD"

任务：
1. Identify all entities/models in the codebase
2. For each entity, check if agent tools exist for:
   - 创建
   - 读取
   - 更新
   - 删除
3. Score per entity and overall

格式：
## CRUD 完整性审计
### 实体 CRUD 分析
| 实体 | 创建 | 读取 | 更新 | 删除 | Score |
### Overall 评分： X/Y entities with full CRUD (百分比%)
### 不完整实体（列出缺失操作）
### 建议
```

**Agent 6：UI 集成**
```
审计UI INTEGRATION - "Agent actions immediately reflected in UI"

任务：
1. Check how agent writes/changes propagate to frontend
2. Look for:
   - Streaming updates (SSE, WebSocket)
   - Polling mechanisms
   - Shared state/services
   - Event buses
   - File watching
3. Identify "silent actions" anti-pattern (agent changes state but UI doesn't update)

格式：
## UI 集成审计
### Agent 操作 → UI 更新 Analysis
| Agent 操作 | UI 机制 | 是否立即？ | 备注 |
### 评分： X/Y (百分比%)
### 静默操作（反模式）
### 建议
```

**Agent 7：能力发现**
```
审计CAPABILITY DISCOVERY - "Users can discover what the agent can do"

任务：
1. Check for these 7 discovery mechanisms:
   - Onboarding flow showing agent capabilities
   - Help documentation
   - Capability hints in UI
   - Agent self-describes in responses
   - Suggested prompts/actions
   - Empty state guidance
   - Slash commands (/help, /tools)
2. Score against 7 mechanisms

格式：
## 能力发现审计
### 发现机制分析
| 机制 | 是否存在？ | 位置 | 质量 |
### 评分： X/7 (百分比%)
### 缺失的发现
### 建议
```

**Agent 8：提示原生特性**
```
审计PROMPT-NATIVE FEATURES - "特性s are prompts defining outcomes, not code"

任务：
1. 读取 all agent prompts
2. Classify each feature/behavior as defined in:
   - PROMPT (good): outcomes defined in natural language
   - CODE (bad): business logic hardcoded
3. Check if behavior changes require prompt edit vs code change

格式：
## 提示原生特性审计
### 特性定义分析
| 特性 | 定义于 | 类型 | 备注 |
### 评分： X/Y (百分比%)
### Code-Defined 特性s (anti-pattern)
### 建议
```

</sub-agents>

### 步骤 3：编译摘要报告

所有 agent 完成后，编译摘要：

```markdown
## Agent-Native Architecture Review: [Project Name]

### 总体评分摘要

| 核心原则 | Score | 百分比 | 状态 |
|----------------|-------|------------|--------|
| 动作对等 | X/Y | Z% | ✅/⚠️/❌ |
| 工具作为原语 | X/Y | Z% | ✅/⚠️/❌ |
| 上下文注入 | X/Y | Z% | ✅/⚠️/❌ |
| 共享工作空间 | X/Y | Z% | ✅/⚠️/❌ |
| CRUD 完整性 | X/Y | Z% | ✅/⚠️/❌ |
| UI 集成 | X/Y | Z% | ✅/⚠️/❌ |
| 能力发现 | X/Y | Z% | ✅/⚠️/❌ |
| Prompt-Native 特性s | X/Y | Z% | ✅/⚠️/❌ |

**Overall Agent-Native 评分： X%**

### 状态 Legend
- ✅ 优秀 (80%+)
- ⚠️ 部分 (50-79%)
- ❌ 需要改进 (<50%)

### 前 10 建议 按影响

| 优先级 | 操作 | 原则 | 工作量 |
|----------|--------|-----------|--------|

### What's Working 优秀ly

[列出前 5 个优势]
```

## 成功标准

- [ ] 所有 8 个子 agent 完成审计
- [ ] 每个原则都有具体的数值评分（X/Y 格式）
- [ ] 摘要表显示所有评分和状态指示器
- [ ] 前 10 recommendations are prioritized by impact
- [ ] 报告确定优势和差距

## Optional: Single 原则 Audit

如果 $ARGUMENTS 指定单一原则 (e.g., "action parity"), 仅运行该子 agent 并为该原则提供详细发现.

有效参数：
- `action parity` or `1`
- `tools` or `primitives` or `2`
- `context` or `injection` or `3`
- `shared` or `workspace` or `4`
- `crud` or `5`
- `ui` or `integration` or `6`
- `discovery` or `7`
- `prompt` or `features` or `8`
