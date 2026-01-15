# Workflow：向现有 Skill 添加 Reference

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

显示编号列表，询问："哪个 skill 需要新的 reference？"

## 步骤 2：分析当前结构

```bash
cat ~/.claude/skills/{skill-name}/SKILL.md
ls ~/.claude/skills/{skill-name}/references/ 2>/dev/null
```

确定：
- **有 references/ 文件夹？** → 好，可以直接添加
- **简单的 skill？** → 可能需要先创建 references/
- **存在哪些 reference？** → 了解知识格局

向用户报告当前的 reference。

## 步骤 3：收集 Reference 需求

询问：
- 这个 reference 应包含什么知识？
- 哪些 workflow 会使用它？
- 这是跨 workflow 可重用的还是特定于一个的？

**如果特定于一个 workflow** → 考虑将其内联在该 workflow 中。

## 步骤 4：创建 Reference 文件

创建 `references/{reference-name}.md`：

使用语义 XML 标签来构建内容：
```xml
<overview>
此 reference 涵盖内容的简要描述
</overview>

<patterns>
## 常见模式
[可重用的模式、示例、代码片段]
</patterns>

<guidelines>
## 指南
[最佳实践、规则、约束]
</guidelines>

<examples>
## 示例
[带有解释的具体示例]
</examples>
```

## 步骤 5：更新 SKILL.md

将新 reference 添加到 `<reference_index>`：
```markdown
**类别：** existing.md, new-reference.md
```

## 步骤 6：更新需要它的 Workflow

对于应该使用此 reference 的每个 workflow：

1. 读取 workflow 文件
2. 添加到其 `<required_reading>` 部分
3. 验证添加后 workflow 仍然合理

## 步骤 7：验证

- [ ] Reference 文件存在且结构良好
- [ ] Reference 在 SKILL.md 的 reference_index 中
- [ ] 相关 workflow 在 required_reading 中有它
- [ ] 没有断开的引用
</process>

<success_criteria>
Reference 添加在以下情况下完成：
- [ ] 使用有用内容创建了 reference 文件
- [ ] 已添加到 SKILL.md 的 reference_index
- [ ] 相关 workflow 已更新为读取它
- [ ] 内容是可重用的（不特定于 workflow）
</success_criteria>
