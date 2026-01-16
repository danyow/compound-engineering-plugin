# 在 Skill 中使用模板

<purpose>
模板是 Claude 复制并填充的可重用输出结构。它们确保一致、高质量的输出，而无需每次都重新生成结构。
</purpose>

<when_to_use>
在以下情况下使用模板：
- 输出应在调用之间具有一致的结构
- 结构比创意生成更重要
- 填充占位符比从空白页生成更可靠
- 用户期望可预测、专业的输出

常见的模板类型：
- **计划** - 项目计划、实施计划、迁移计划
- **规范** - 技术规范、功能规范、API 规范
- **文档** - 报告、提案、摘要
- **配置** - 配置文件、设置、环境设置
- **脚手架** - 文件结构、样板代码
</when_to_use>

<template_structure>
模板位于 skill 目录内的 `templates/` 中：

```
skill-name/
├── SKILL.md
├── workflows/
├── references/
└── templates/
    ├── plan-template.md
    ├── spec-template.md
    └── report-template.md
```

模板文件包含：
1. 清晰的章节标记
2. 占位符指示器（使用 `{{placeholder}}` 或 `[PLACEHOLDER]`）
3. 关于什么放在哪里的内联指导
4. 有用的示例内容
</template_structure>

<template_example>
```markdown
# {{PROJECT_NAME}} 实施计划

## 概述
{{此计划涵盖内容的 1-2 句摘要}}

## 目标
- {{主要目标}}
- {{次要目标...}}

## 范围
**范围内：**
- {{包括什么}}

**范围外：**
- {{明确排除什么}}

## 阶段

### Phase 1: {{Phase name}}
**持续时间：** {{估计持续时间}}
**交付物：**
- {{交付物 1}}
- {{交付物 2}}

### Phase 2: {{Phase name}}
...

## 成功标准
- [ ] {{可衡量的标准 1}}
- [ ] {{可衡量的标准 2}}

## 风险
| 风险 | 可能性 | 影响 | 缓解 |
|------|------------|--------|------------|
| {{Risk}} | {{H/M/L}} | {{H/M/L}} | {{Strategy}} |
```
</template_example>

<workflow_integration>
工作流像这样引用模板：

```xml
<process>
## Step 3: 生成计划

1. 读取 `templates/plan-template.md`
2. 复制模板结构
3. 根据收集的需求填充每个占位符
4. 审查完整性
</process>
```

工作流告诉 Claude 何时使用模板。模板提供要生成什么结构。
</workflow_integration>

<best_practices>
**应该：**
- 保持模板专注于结构，而不是内容
- 一致使用清晰的占位符语法
- 在章节可能不明确的地方包含简短的内联指导
- 使模板完整但最小

**不应该：**
- 放置可能被逐字复制的过多示例内容
- 为真正需要创意生成的输出创建模板
- 使用太多必需章节过度约束
- 忘记在需求更改时更新模板
</best_practices>
