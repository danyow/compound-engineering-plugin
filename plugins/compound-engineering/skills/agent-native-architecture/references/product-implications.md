<overview>
Agent原生架构对产品的感受有影响，不仅仅是构建方式。本文档涵盖复杂性的渐进式披露、通过Agent使用发现潜在需求，以及设计与风险和可逆性相匹配的审批流程。
</overview>

<progressive_disclosure>
## 复杂性的渐进式披露

最好的Agent原生应用开始很简单但功能无尽。

### Excel类比

Excel是标准示例：你可以用它来列购物清单，或者构建复杂的财务模型。相同的工具，使用深度截然不同。

Claude Code具有这种品质：修复打字错误或重构整个代码库。接口相同——自然语言——但能力随着请求而扩展。

### 模式

Agent原生应用应该渴望这样做：

**简单入口：** 基本请求立即工作，无需学习曲线
```
用户："整理我的下载"
Agent：[立即执行，无需配置]
```

**可发现的深度：** 用户在探索时发现他们可以做得更多
```
用户："按项目整理我的下载"
Agent：[适应偏好]

用户："每个周一，回顾上周的下载"
Agent：[设置重复工作流]
```

**无上限：** 高级用户可以以你未预料的方式推动系统
```
用户："交叉引用我的下载和日历，并标记
       在会议期间下载的任何我还没有
       跟进的内容"
Agent：[组合能力来实现这个]
```

### 这是如何出现的

这不是你直接设计的。它**从架构中自然出现：**

1. 当功能是prompt且工具是可组合的...
2. 用户可以从简单开始（"整理我的下载"）...
3. 并逐步发现复杂性（"每周一，回顾上周..."）...
4. 无需你显式构建每个级别

Agent在用户所在的地方与他们相遇。

### 设计含义

- **不要强制前期配置** - 让用户立即开始
- **不要隐藏功能** - 通过使用使其可发现
- **不要限制复杂性** - 如果Agent能做，就让用户问
- **提供提示** - 帮助用户发现可能的内容
</progressive_disclosure>

<latent_demand_discovery>
## 潜在需求发现

传统产品开发：想象用户想要什么，构建它，看看你是否正确。

Agent原生产品开发：构建一个有能力的基础，观察用户要求Agent做什么，形式化出现的模式。

### 转变

**传统方法：**
```
1. 想象用户可能想要的功能
2. 构建它们
3. 发布
4. 希望你猜对了
5. 如果错了，重建
```

**Agent原生方法：**
```
1. 构建有能力的基础（原子工具、奇偶性）
2. 发布
3. 用户向Agent要求东西
4. 观察他们要求什么
5. 模式出现
6. 将模式形式化为领域工具或prompt
7. 重复
```

### 飞轮

```
用原子工具和奇偶性构建
           ↓
用户要求你没有预料到的东西
           ↓
Agent组合工具来完成它们
（或失败，暴露能力差距）
           ↓
你观察所要求内容中的模式
           ↓
添加领域工具或prompt来优化常见模式
           ↓
(Repeat)
```

### 你学到什么

**当用户问且Agent成功时：**
- 这是真实的需求
- 你的架构支持它
- 如果很常见，考虑用领域工具优化

**当用户问且Agent失败时：**
- 这是真实的需求
- 你有能力差距
- 修复差距：添加工具、修复奇偶性、改进context

**当用户不要求某些东西时：**
- 也许他们不需要
- 或者也许他们不知道这是可能的（能力隐藏）

### 实现

**记录Agent请求：**
```typescript
async function handleAgentRequest(request: string) {
  // 记录用户要求什么
  await analytics.log({
    type: 'agent_request',
    request: request,
    timestamp: Date.now(),
  });

  // Process request...
}
```

**跟踪成功/失败：**
```typescript
async function completeAgentSession(session: AgentSession) {
  await analytics.log({
    type: 'agent_session',
    request: session.initialRequest,
    succeeded: session.status === 'completed',
    toolsUsed: session.toolCalls.map(t => t.name),
    iterations: session.iterationCount,
  });
}
```

**审查模式：**
- 用户最常问什么？
- 什么失败了？为什么？
- 什么会从领域工具中受益？
- 什么需要更好的context注入？

### 示例：发现"周评论"

```
周1：用户开始问"总结我这周的活动"
        Agent：组合list_files + read_file，工作但缓慢

周2：更多用户问类似的事情
        模式出现：周评论很常见

周3：添加周评论的prompt部分
        更快、更一致、仍然灵活

周4：如果仍然常见且性能很重要
        添加领域工具：generate_weekly_summary
```

你不必猜测周评论会很受欢迎。你发现了它。
</latent_demand_discovery>

<approval_and_agency>
## 审批和用户代理

当Agent采取无声请求的操作时——自己做事而不是响应显式请求——你需要决定给予多少自主权。

> **注意：** 此框架适用于无声请求的Agent操作。如果用户明确要求Agent做某事（"发送那封电子邮件"），那已经是批准——Agent只需做就可以。

### 风险/可逆性矩阵

考虑两个维度：
- **风险：** 如果这出错，会有多大关系？
- **可逆性：** 撤销有多容易？

| 风险 | 可逆性 | 模式 | 示例 |
|--------|---------------|---------|---------|
| 低 | 容易 | **自动应用** | 组织文件 |
| 低 | 困难 | **快速确认** | 发布到私有feed |
| 高 | 容易 | **建议+应用** | 代码更改带撤销 |
| 高 | 困难 | **明确批准** | 发送电子邮件、付款 |

### 详细的模式

**自动应用（低风险，容易撤销）：**
```
Agent：[将文件组织到文件夹中]
Agent："我按类型将你的下载组织到文件夹中。
        你可以用Cmd+Z撤销或将它们移回。"
```
用户不需要批准——很容易撤销，也不太重要。

**快速确认（低风险，困难撤销）：**
```
Agent："我起草了一篇关于你的阅读见解的帖子。
        发布到你的feed？"
        [发布] [先编辑] [取消]
```
一键确认因为风险低，但取消发布很困难。

**建议+应用（高风险，容易撤销）：**
```
Agent："我建议这些代码更改来修复bug：
        [显示diff]
        应用？更改可以用git撤销。"
        [应用] [修改] [取消]
```
显示会发生什么，使撤销清晰。

**明确批准（高风险，困难撤销）：**
```
Agent："我起草了这封关于截止日期更改的电子邮件给你的团队：
        [显示完整电子邮件]
        这会立即发送，无法撤销。
        输入"send"来确认。"
```
需要明确的操作，明确后果。

### 实现

```swift
enum ApprovalLevel {
    case autoApply       // 直接做
    case quickConfirm    // 一键批准
    case suggestApply    // 显示预览，询问是否应用
    case explicitApproval // 需要明确确认
}

func approvalLevelFor(action: AgentAction) -> ApprovalLevel {
    let stakes = assessStakes(action)
    let reversibility = assessReversibility(action)

    switch (stakes, reversibility) {
    case (.low, .easy): return .autoApply
    case (.low, .hard): return .quickConfirm
    case (.high, .easy): return .suggestApply
    case (.high, .hard): return .explicitApproval
    }
}

func assessStakes(_ action: AgentAction) -> Stakes {
    switch action {
    case .organizeFiles: return .low
    case .publishToFeed: return .low
    case .modifyCode: return .high
    case .sendEmail: return .high
    case .makePayment: return .high
    }
}

func assessReversibility(_ action: AgentAction) -> Reversibility {
    switch action {
    case .organizeFiles: return .easy  // Can move back
    case .publishToFeed: return .hard  // People might see it
    case .modifyCode: return .easy     // Git revert
    case .sendEmail: return .hard      // Can't unsend
    case .makePayment: return .hard    // Money moved
    }
}
```

### 自修改考虑

当Agent可以修改自己的行为时——改变prompt、更新偏好、调整工作流——目标是：

1. **可见性：** 用户可以看到什么改变了
2. **理解：** 用户理解效果
3. **回滚：** 用户可以撤销更改

审批流程是实现这一目标的一种方式。带有轻松回滚的审计日志可能是另一种。**原则是：使其可读。**

```swift
// 当Agent修改自己的prompt时
func agentSelfModify(change: PromptChange) async {
    // Log the change
    await auditLog.record(change)

    // Create checkpoint for rollback
    await createCheckpoint(currentState)

    // Notify user (could be async/batched)
    await notifyUser("我已调整我的方法：\(change.summary)")

    // Apply change
    await applyChange(change)
}
```
</approval_and_agency>

<capability_visibility>
## 能力可见性

用户需要发现Agent能做什么。隐藏的能力导致未被充分利用。

### 问题

```
用户："帮助我阅读"
Agent："你需要什么帮助？"
// Agent不提及它可以发布到feed、研究书籍、
// 生成介绍、分析主题...
```

Agent可以做这些事情，但用户不知道。

### 解决方案

**入职提示：**
```
Agent："我可以通过多种方式帮助你阅读：
        - 研究任何书籍（网络搜索+保存发现）
        - 生成个性化介绍
        - 将见解发布到你的阅读feed
        - 分析你的库中的主题
        什么让你感兴趣？"
```

**上下文建议：**
```
用户："我刚读完《1984》"
Agent："很好的选择！你想让我：
        - 研究历史背景？
        - 将它与你的库中的其他书籍进行比较？
        - 将关于它的见解发布到你的feed？"
```

**渐进式披露：**
```
// 用户使用基本功能后
Agent："顺便说一下，你也可以要求我设置
        重复任务，比如"每周一，回顾我的
        阅读进度。"只要告诉我就可以了！"
```

### 平衡

- **不要用所有前期能力压倒** 用户
- **确实通过使用自然地披露**能力
- **不要假设** 用户会自己发现事情
- **确实使** 能力在相关时可见
</capability_visibility>

<designing_for_trust>
## 为信任设计

Agent原生应用需要信任。用户给了AI重要能力。通过以下方式建立信任：

### 透明度

- 显示Agent在做什么（工具调用、进度）
- 在重要时解释推理
- 使所有Agent工作可检查（文件、日志）

### 可预测性

- 类似请求的一致行为
- 何时需要批准的清晰模式
- Agent可以访问什么没有惊喜

### 可逆性

- 轻松撤销Agent操作
- 在显著更改前检查点
- 清晰的回滚路径

### 控制

- 用户可以随时停止Agent
- 用户可以调整Agent行为（prompt、偏好）
- 用户可以根据需要限制功能

### Implementation

```swift
struct AgentTransparency {
    // 显示发生了什么
    func onToolCall(_ tool: ToolCall) {
        showInUI("使用 \(tool.name)...")
    }

    // 解释推理
    func onDecision(_ decision: AgentDecision) {
        if decision.needsExplanation {
            showInUI("我选择这个是因为：\(decision.reasoning)")
        }
    }

    // 使工作可检查
    func onOutput(_ output: AgentOutput) {
        // 所有输出都在用户可以看到的文件中
        // 或在可见的UI状态中
    }
}
```
</designing_for_trust>

<checklist>
## 产品设计检查清单

### 渐进式披露
- [ ] 基本请求立即工作（无配置）
- [ ] 深度可通过使用发现
- [ ] 复杂性没有人工上限
- [ ] 提供能力提示

### 潜在需求发现
- [ ] Agent请求被记录
- [ ] 成功/失败被跟踪
- [ ] 模式定期审查
- [ ] 常见模式形式化为工具/prompt

### 审批与代理
- [ ] 评估每个操作类型的风险
- [ ] 评估每个操作类型的可逆性
- [ ] 审批模式与风险/可逆性匹配
- [ ] 自修改是可读的（可见、可理解、可逆）

### 能力可见性
- [ ] 入职揭示关键能力
- [ ] 提供上下文建议
- [ ] 不希望用户猜测什么是可能的

### 信任
- [ ] Agent操作是透明的
- [ ] 行为是可预测的
- [ ] 操作是可逆的
- [ ] 用户有控制权
</checklist>
