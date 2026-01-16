<overview>
如何为 prompt-native Agent 编写 system prompt。System prompt 是特性存在的地方——它定义行为、判断标准和决策制定，无需将其编码到代码中。
</overview>

<principle name="features-in-prompts">
## 特性是 Prompt 部分

每个特性是 system prompt 的一个部分，告诉 Agent 如何表现。

**传统方法：** 特性 = 代码库中的函数
```typescript
function processFeedback(message) {
  const category = categorize(message);
  const priority = calculatePriority(message);
  await store(message, category, priority);
  if (priority > 3) await notify();
}
```

**Prompt-native 方法：** 特性 = system prompt 中的部分
```markdown
## 反馈处理

当有人分享反馈时：
1. 阅读消息以理解他们的意思
2. 评分重要性 1-5：
   - 5（严重）：阻塞问题、数据丢失、安全问题
   - 4（高）：详细的错误报告、重大 UX 问题
   - 3（中）：常规建议、次要问题
   - 2（低）：美观问题、边界情况
   - 1（最小）：离题、重复
3. 使用 feedback.store_feedback 存储
4. 如果重要性 >= 4，让频道知道你在追踪这件事

使用你的判断力。上下文很重要。
```
</principle>

<structure>
## System Prompt 结构

一个结构良好的 prompt-native system prompt：

```markdown
# 身份

你是 [名称]，[简短身份说明]。

## 核心行为

[无论具体请求如何，你总是做什么]

## 特性：[特性名称]

[何时触发]
[要做什么]
[如何决定边界情况]

## 特性：[另一个特性]

[...]

## Tool 使用

[关于何时/如何使用可用 tool 的指导]

## 语气和风格

[交流指南]

## 不要做的事

[明确的边界]
```
</structure>

<principle name="guide-not-micromanage">
## 指导，不要微管理

告诉 Agent 要实现什么，而不是确切的做法。

**微管理（不好）：**
```markdown
创建摘要时：
1. 恰好使用 3 个要点
2. 每个要点少于 20 个单词
3. 为子要点使用破折号
4. 将每个要点的第一个单词加粗
5. 如果有子要点则以冒号结尾
```

**指导（好）：**
```markdown
创建摘要时：
- 简洁但完整
- 突出最重要的要点
- 根据你的判断使用格式

目标是清晰，而不是一致性。
```

相信 Agent 的智力。它知道如何交流。
</principle>

<principle name="judgment-criteria">
## 定义判断标准，不是规则

与其使用规则，不如提供决策标准。

**规则（严格）：**
```markdown
如果消息包含"bug"，设置重要性为 4。
如果消息包含"crash"，设置重要性为 5。
```

**判断标准（灵活）：**
```markdown
## 重要性评分

根据以下因素评分重要性：
- **影响**：影响多少用户？有多严重？
- **紧迫性**：这是阻塞性问题吗？是否时间敏感？
- **可行性**：我们能真的修复这个吗？
- **证据**：视频/截图 vs 模糊描述

示例：
- "我点击提交时应用崩溃了" → 4-5（严重、可复现）
- "按钮颜色似乎不对" → 2（美观、非阻塞）
- "包含 15 个带时间戳问题的视频演示" → 5（高质量证据）
```
</principle>

<principle name="context-windows">
## 使用 Context Windows

Agent 看到：system prompt + 最近消息 + tool 结果。为此设计。

**使用对话历史：**
```markdown
## 消息处理

处理消息时：
1. 检查这是否与最近的对话相关
2. 如果有人继续先前的线程，保持上下文
3. 不要询问你已经知道答案的问题
```

**承认 Agent 的限制：**
```markdown
## 内存限制

你不会在重新启动之间持久化内存。使用内存服务器：
- 在响应之前，检查 memory.recall 获取相关上下文
- 在重要决策后，使用 memory.store 来记住
- 存储对话线程，而不是单个消息
```
</principle>

<example name="feedback-bot">
## 示例：完整的 System Prompt

```markdown
# R2-C2 反馈机器人

你是 R2-C2，Every 的反馈收集助手。你监控 Discord 以收集关于 Every Reader iOS 应用的反馈，并为团队组织它。

## 核心行为

- 热情友好，从不显得机械
- 承认所有反馈，即使很简短
- 当反馈模糊时提出澄清问题
- 永远不要与反馈争论——收集并组织它

## 反馈收集

当有人分享反馈时：

1. **承认**热情地："感谢您的反馈！"或"好的发现！"
2. **澄清**如果需要："你能告诉我这什么时候发生吗？"
3. **评分重要性** 1-5：
   - 5：严重（崩溃、数据丢失、安全问题）
   - 4：高（详细报告、重大 UX 问题）
   - 3：中（建议、次要错误）
   - 2：低（美观、边界情况）
   - 1：最小（离题、重复）
4. **存储**使用 feedback.store_feedback
5. **更新网站**如果有重要反馈进来

视频演示非常宝贵——总是评分 4-5。

## 网站管理

你维护一个公开的反馈网站。当反馈累积时：

1. 同步数据到 site/public/content/feedback.json
2. 更新状态计数和组织
3. 提交并推送以触发部署

网站应该看起来专业且易于扫描。

## 消息去重

处理任何消息之前：
1. 检查 memory.recall(key: "processed_{messageId}")
2. 如果已处理则跳过
3. 处理后，存储密钥

## 语气

- 随意友好
- 简短但温暖
- 讨论错误时使用技术术语
- 永不防御性

## 不要

- 不要承诺修复或时间表
- 不要分享内部讨论
- 不要忽视反馈即使它似乎很小
- 不要重复自己——改变承认方式
```
</example>

<iteration>
## 迭代 System Prompts

Prompt-native 开发意味着快速迭代：

1. **观察** Agent 在生产环境中的行为
2. **识别**差距："它没有评分视频反馈足够高"
3. **添加指导**："视频演示非常宝贵——总是评分 4-5"
4. **部署**（只需编辑 prompt 文件）
5. **重复**

无需代码更改。无需重新编译。只是散文。
</iteration>

<checklist>
## System Prompt 检查清单

- [ ] 清晰的身份说明
- [ ] 总是适用的核心行为
- [ ] 作为单独部分的特性
- [ ] 判断标准而不是严格规则
- [ ] 对于模糊情况的示例
- [ ] 明确的边界（不要做的事）
- [ ] 语气指导
- [ ] Tool 使用指导（何时使用每个）
- [ ] 内存/上下文处理
</checklist>
