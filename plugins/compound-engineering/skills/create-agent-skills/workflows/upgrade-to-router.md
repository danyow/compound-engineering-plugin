# Workflow：将 Skill 升级到 Router 模式

<required_reading>
**立即阅读这些参考文件：**
1. references/recommended-structure.md
2. references/skill-structure.md
</required_reading>

<process>
## 步骤 1：选择 Skill

```bash
ls ~/.claude/skills/
```

显示编号列表，询问："应将哪个 skill 升级到 router 模式？"

## 步骤 2：验证它需要升级

读取 skill：
```bash
cat ~/.claude/skills/{skill-name}/SKILL.md
ls ~/.claude/skills/{skill-name}/
```

**已经是 router？**（有 workflows/ 和 intake 问题）
→ 告诉用户它已经在使用 router 模式，提供添加 workflow

**应该保持简单的简单 skill？**（少于 200 行，单个 workflow）
→ 解释 router 模式可能是过度的，询问是否仍想继续

**升级的好候选：**
- 超过 200 行
- 多个不同的用例
- 不应跳过的 essential principles
- 复杂性不断增长

## 步骤 3：识别组件

分析当前 skill 并识别：

1. **Essential principles** - 适用于所有用例的规则
2. **不同的 workflow** - 用户可能想做的不同事情
3. **可重用的知识** - 模式、示例、技术细节

显示发现：
```
## 分析

**我发现的 essential principles：**
- [Principle 1]
- [Principle 2]

**我识别的不同 workflow：**
- [Workflow A]：[描述]
- [Workflow B]：[描述]

**可以成为 reference 的知识：**
- [Reference topic 1]
- [Reference topic 2]
```

询问："此分解看起来对吗？有任何调整吗？"

## 步骤 4：创建目录结构

```bash
mkdir -p ~/.claude/skills/{skill-name}/workflows
mkdir -p ~/.claude/skills/{skill-name}/references
```

## 步骤 5：提取 Workflow

对于每个识别的 workflow：

1. 创建 `workflows/{workflow-name}.md`
2. 添加 required_reading 部分（它需要的 reference）
3. 添加 process 部分（来自原始 skill 的步骤）
4. 添加 success_criteria 部分

## 步骤 6：提取 Reference

对于每个识别的 reference 主题：

1. 创建 `references/{reference-name}.md`
2. 从原始 skill 移动相关内容
3. 使用语义 XML 标签构建

## 步骤 7：将 SKILL.md 重写为 Router

用 router 结构替换 SKILL.md：

```markdown
---
name: {skill-name}
description: {existing description}
---

<essential_principles>
[提取的原则 - 内联，不能跳过]
</essential_principles>

<intake>
**询问用户：**

您想做什么？
1. [Workflow A option]
2. [Workflow B option]
...

**在继续之前等待响应。**
</intake>

<routing>
| 响应 | Workflow |
|----------|----------|
| 1, "keywords" | `workflows/workflow-a.md` |
| 2, "keywords" | `workflows/workflow-b.md` |
</routing>

<reference_index>
[按类别列出所有 reference]
</reference_index>

<workflows_index>
| Workflow | 用途 |
|----------|---------|
| workflow-a.md | [它做什么] |
| workflow-b.md | [它做什么] |
</workflows_index>
```

## 步骤 8：验证没有丢失任何内容

将原始 skill 内容与新结构进行比较：
- [ ] 所有 principle 都保留（现在内联）
- [ ] 所有 procedure 都保留（现在在 workflow 中）
- [ ] 所有知识都保留（现在在 reference 中）
- [ ] 没有孤立的内容

## 步骤 9：测试

调用升级的 skill：
- Intake 问题是否出现？
- 每个 routing 选项是否有效？
- Workflow 是否加载正确的 reference？
- 行为是否与原始 skill 匹配？

报告任何问题。
</process>

<success_criteria>
升级在以下情况下完成：
- [ ] 使用 workflow 文件创建了 workflows/ 目录
- [ ] 创建了 references/ 目录（如果需要）
- [ ] SKILL.md 重写为 router
- [ ] Essential principles 内联在 SKILL.md 中
- [ ] 所有原始内容都保留
- [ ] Intake 问题正确路由
- [ ] 测试并工作
</success_criteria>
