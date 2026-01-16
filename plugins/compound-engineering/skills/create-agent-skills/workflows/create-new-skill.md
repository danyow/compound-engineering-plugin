# Workflow：创建新 Skill

<required_reading>
**立即阅读这些参考文件：**
1. references/recommended-structure.md
2. references/skill-structure.md
3. references/core-principles.md
4. references/use-xml-tags.md
</required_reading>

<process>
## 步骤 1：自适应需求收集

**如果用户提供了上下文**（例如，"为 X 构建一个 skill"）：
→ 分析所述内容、可以推断的内容、不清楚的内容
→ 跳过仅询问真正的空白

**如果用户只是调用 skill 而没有上下文：**
→ 询问他们想构建什么

### 使用 AskUserQuestion

根据实际差距询问 2-4 个特定领域的问题。每个问题应该：
- 有带描述的特定选项
- 专注于范围、复杂性、输出、边界
- 不询问从上下文中显而易见的事情

示例问题：
- "此 skill 应处理哪些特定操作？"（基于领域的选项）
- "这是否还应处理 [相关事物] 或保持专注于 [核心事物]？"
- "成功时用户应该看到什么？"

### 决策门

在初始问题之后，询问：
"准备好继续构建，还是您想让我询问更多问题？"

选项：
1. **继续构建** - 我有足够的上下文
2. **询问更多问题** - 有更多细节需要澄清
3. **让我添加详细信息** - 我想提供额外的上下文

## 步骤 2：研究触发器（如果是外部 API）

**当检测到外部服务时**，使用 AskUserQuestion 询问：
"这涉及 [service name] API。您想让我在构建之前研究当前端点和模式吗？"

选项：
1. **是，先研究** - 获取当前文档以进行准确实施
2. **否，使用通用模式继续** - 使用常见模式而不进行特定 API 研究

如果请求研究：
- 使用 Context7 MCP 获取当前库文档
- 或使用 WebSearch 获取最近的 API 文档
- 专注于 2024-2025 来源
- 存储发现以用于内容生成

## 步骤 3：确定结构

**简单 skill（单个 workflow，<200 行）：**
→ 包含所有内容的单个 SKILL.md 文件

**复杂 skill（多个 workflow 或领域知识）：**
→ Router 模式：
```
skill-name/
├── SKILL.md (router + principles)
├── workflows/ (procedures - FOLLOW)
├── references/ (knowledge - READ)
├── templates/ (output structures - COPY + FILL)
└── scripts/ (reusable code - EXECUTE)
```

支持 router 模式的因素：
- 多个不同的用户意图（create vs debug vs ship）
- 跨 workflow 共享的领域知识
- 不能跳过的 essential principles
- Skill 可能随时间增长

**何时考虑 templates/：**
- Skill 产生一致的输出结构（计划、规范、报告）
- 结构比创意生成更重要

**何时考虑 scripts/：**
- 相同的代码在调用之间运行（deploy、setup、API 调用）
- 每次重写时操作容易出错

参见 references/recommended-structure.md 获取 template。

## 步骤 4：创建目录

```bash
mkdir -p ~/.claude/skills/{skill-name}
# 如果复杂：
mkdir -p ~/.claude/skills/{skill-name}/workflows
mkdir -p ~/.claude/skills/{skill-name}/references
# 如果需要：
mkdir -p ~/.claude/skills/{skill-name}/templates  # 用于输出结构
mkdir -p ~/.claude/skills/{skill-name}/scripts    # 用于可重用代码
```

## 步骤 5：编写 SKILL.md

**简单 skill：**编写包含以下内容的完整 skill 文件：
- YAML frontmatter（name、description）
- `<objective>`
- `<quick_start>`
- 带有纯 XML 的内容部分
- `<success_criteria>`

**复杂 skill：**编写带有以下内容的 router：
- YAML frontmatter
- `<essential_principles>`（内联，不可避免）
- `<intake>`（询问用户的问题）
- `<routing>`（将答案映射到 workflow）
- `<reference_index>` 和 `<workflows_index>`

## 步骤 6：编写 Workflow（如果复杂）

对于每个 workflow：
```xml
<required_reading>
此 workflow 要加载哪些 reference
</required_reading>

<process>
逐步过程
</process>

<success_criteria>
如何知道此 workflow 已完成
</success_criteria>
```

## 步骤 7：编写 Reference（如果需要）

领域知识：
- 多个 workflow 可能需要
- 不会根据 workflow 改变
- 包含模式、示例、技术细节

## 步骤 8：验证结构

检查：
- [ ] YAML frontmatter 有效
- [ ] 名称与目录匹配（lowercase-with-hyphens）
- [ ] 描述说明它做什么以及何时使用它（第三人称）
- [ ] 主体中没有 markdown 标题（#）- 使用 XML 标签
- [ ] 存在必需的标签：objective、quick_start、success_criteria
- [ ] 所有引用的文件都存在
- [ ] SKILL.md 少于 500 行
- [ ] XML 标签正确关闭

## 步骤 9：创建 Slash Command

```bash
cat > ~/.claude/commands/{skill-name}.md << 'EOF'
---
description: {简要描述}
argument-hint: [{参数提示}]
allowed-tools: Skill({skill-name})
---

为以下内容调用 {skill-name} skill：$ARGUMENTS
EOF
```

## 步骤 10：测试

调用 skill 并观察：
- 它是否询问正确的 intake 问题？
- 它是否加载正确的 workflow？
- workflow 是否加载正确的 reference？
- 输出是否符合预期？

根据实际使用迭代，而不是假设。
</process>

<success_criteria>
Skill 在以下情况下完成：
- [ ] 使用适当的问题收集需求
- [ ] 如果涉及外部服务，则完成 API 研究
- [ ] 目录结构正确
- [ ] SKILL.md 有有效的 frontmatter
- [ ] Essential principles 内联（如果是复杂 skill）
- [ ] Intake 问题路由到正确的 workflow
- [ ] 所有 workflow 都有 required_reading + process + success_criteria
- [ ] Reference 包含可重用的领域知识
- [ ] Slash command 存在并工作
- [ ] 使用真实调用进行测试
</success_criteria>
