# Workflow：向现有 Skill 添加 Workflow

<required_reading>
**立即阅读这些参考文件：**
1. references/recommended-structure.md
2. references/workflows-and-validation.md
</required_reading>

<process>
## 步骤 1：选择 Skill

**不要使用 AskUserQuestion** - 可能有很多 skill。

```bash
ls ~/.claude/skills/
```

显示编号列表，询问："哪个 skill 需要新的 workflow？"

## 步骤 2：分析当前结构

读取 skill：
```bash
cat ~/.claude/skills/{skill-name}/SKILL.md
ls ~/.claude/skills/{skill-name}/workflows/ 2>/dev/null
```

确定：
- **简单的 skill？** → 可能需要先升级到 router 模式
- **已经有 workflows/?** → 好，可以直接添加
- **存在哪些 workflow？** → 避免重复

向用户报告当前结构。

## 步骤 3：收集 Workflow 需求

使用 AskUserQuestion 或直接问题询问：
- 这个 workflow 应该做什么？
- 什么时候有人会使用它而不是现有的 workflow？
- 它需要哪些 reference？

## 步骤 4：升级到 Router 模式（如果需要）

**如果 skill 当前是简单的（没有 workflows/）：**

询问："此 skill 需要先升级到 router 模式。我应该重构它吗？"

如果是：
1. 创建 workflows/ 目录
2. 将现有的 process 内容移至 workflows/main.md
3. 将 SKILL.md 重写为带有 intake + routing 的 router
4. 在继续之前验证结构是否有效

## 步骤 5：创建 Workflow 文件

创建 `workflows/{workflow-name}.md`：

```markdown
# Workflow：{Workflow 名称}

<required_reading>
**立即阅读这些参考文件：**
1. references/{relevant-file}.md
</required_reading>

<process>
## 步骤 1：{第一步}
[要做什么]

## 步骤 2：{第二步}
[要做什么]

## 步骤 3：{第三步}
[要做什么]
</process>

<success_criteria>
此 workflow 在以下情况下完成：
- [ ] 标准 1
- [ ] 标准 2
- [ ] 标准 3
</success_criteria>
```

## 步骤 6：更新 SKILL.md

将新 workflow 添加到：

1. **Intake 问题** - 添加新选项
2. **Routing 表** - 将选项映射到 workflow 文件
3. **Workflows 索引** - 添加到列表

## 步骤 7：创建 Reference（如果需要）

如果 workflow 需要不存在的领域知识：
1. 创建 `references/{reference-name}.md`
2. 添加到 SKILL.md 的 reference_index
3. 在 workflow 的 required_reading 中引用它

## 步骤 8：测试

调用 skill：
- 新选项是否出现在 intake 中？
- 选择它是否路由到正确的 workflow？
- workflow 是否加载正确的 reference？
- workflow 是否正确执行？

向用户报告结果。
</process>

<success_criteria>
Workflow 添加在以下情况下完成：
- [ ] Skill 升级到 router 模式（如果需要）
- [ ] 使用 required_reading、process、success_criteria 创建了 workflow 文件
- [ ] SKILL.md intake 已更新新选项
- [ ] SKILL.md routing 已更新
- [ ] SKILL.md workflows_index 已更新
- [ ] 任何需要的 reference 已创建
- [ ] 测试并工作
</success_criteria>
