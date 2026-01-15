# Workflow：获取 Skill 设计指导

<required_reading>
**立即阅读这些参考文件：**
1. references/core-principles.md
2. references/recommended-structure.md
</required_reading>

<process>
## 步骤 1：了解问题空间

询问用户：
- 您试图支持什么任务或领域？
- 这是您重复做的事情吗？
- 是什么让它复杂到需要一个 skill？

## 步骤 2：确定 Skill 是否合适

**创建 skill 当：**
- 任务在多个会话中重复
- 领域知识不经常更改
- 复杂到足以从结构中受益
- 如果自动化可以节省大量时间

**不要创建 skill 当：**
- 一次性任务（直接做）
- 经常变化（很快就会过时）
- 太简单（开销不值得）
- 更适合作为 slash command（用户触发，无需上下文）

与用户分享此评估。

## 步骤 3：映射 Workflow

询问："有人可能想用此 skill 做哪些不同的事情？"

常见模式：
- Create / Read / Update / Delete
- Build / Debug / Ship
- Setup / Use / Troubleshoot
- Import / Process / Export

每个不同的 workflow = 潜在的 workflow 文件。

## 步骤 4：识别领域知识

询问："无论哪个 workflow，都需要什么知识？"

这成为 reference：
- API 模式
- 最佳实践
- 常见示例
- 配置细节

## 步骤 5：起草结构

根据答案，推荐结构：

**如果 1 个 workflow，简单知识：**
```
skill-name/
└── SKILL.md (所有内容在一个文件中)
```

**如果 2+ workflow，共享知识：**
```
skill-name/
├── SKILL.md (router)
├── workflows/
│   ├── workflow-a.md
│   └── workflow-b.md
└── references/
    └── shared-knowledge.md
```

## 步骤 6：识别 Essential Principles

询问："无论哪个 workflow，什么规则应该始终适用？"

这些成为 SKILL.md 中的 `<essential_principles>`。

示例：
- "在报告成功之前始终验证"
- "永远不要在代码中存储凭据"
- "在进行破坏性更改之前询问"

## 步骤 7：提出建议

总结：
- 推荐的结构（简单 vs router 模式）
- Workflow 列表
- Reference 列表
- Essential principles

询问："此结构有意义吗？准备好构建它了吗？"

如果是 → 提供切换到"创建新 skill"workflow
如果否 → 澄清并迭代
</process>

<decision_framework>
## 快速决策框架

| 情况 | 建议 |
|-----------|----------------|
| 单一任务，经常重复 | 简单 skill |
| 多个相关任务 | Router + workflows |
| 复杂领域，许多模式 | Router + workflows + references |
| 用户触发，新鲜上下文 | Slash command，而不是 skill |
| 一次性任务 | 不需要 skill |
</decision_framework>

<success_criteria>
指导在以下情况下完成：
- [ ] 用户了解他们是否需要 skill
- [ ] 结构已推荐并解释
- [ ] Workflow 已识别
- [ ] Reference 已识别
- [ ] Essential principles 已识别
- [ ] 用户准备好构建（或决定不构建）
</success_criteria>
