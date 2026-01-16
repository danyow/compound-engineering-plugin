# Workflow：向 Skill 添加 Template

<required_reading>
**立即阅读这些参考文件：**
1. references/using-templates.md
</required_reading>

<process>
## 步骤 1：识别 Skill

询问（如果尚未提供）：
- 哪个 skill 需要 template？
- 此 template 构建什么输出？

## 步骤 2：分析 Template 需求

确认这是一个好的 template 候选：
- [ ] 输出在各种使用中具有一致的结构
- [ ] 结构比创意生成更重要
- [ ] 填充占位符比空白页生成更可靠

如果不合适，建议替代方案（workflow 指导、reference 示例）。

## 步骤 3：创建 Templates 目录

```bash
mkdir -p ~/.claude/skills/{skill-name}/templates
```

## 步骤 4：设计 Template 结构

收集需求：
- 输出需要哪些部分？
- 哪些信息在不同使用之间变化？（→ 占位符）
- 什么保持不变？（→ 静态结构）

## 步骤 5：编写 Template 文件

创建 `templates/{template-name}.md`，包含：
- 清晰的部分标记
- `{{PLACEHOLDER}}` 语法用于可变内容
- 在有用的地方提供简短的内联指导
- 最少的示例内容

## 步骤 6：更新 Workflow 以使用 Template

找到生成此输出的 workflow。添加：
```xml
<process>
...
N. 读取 `templates/{template-name}.md`
N+1. 复制 template 结构
N+2. 根据收集的上下文填充每个占位符
...
</process>
```

## 步骤 7：测试

调用 skill workflow 并验证：
- Template 在正确的步骤被读取
- 所有占位符都得到适当填充
- 输出结构与 template 匹配
- 没有留下未填充的占位符
</process>

<success_criteria>
Template 在以下情况下完成：
- [ ] templates/ 目录存在
- [ ] Template 文件具有带占位符的清晰结构
- [ ] 至少有一个 workflow 引用该 template
- [ ] Workflow 说明解释何时/如何使用 template
- [ ] 使用真实调用进行测试
</success_criteria>
