# Workflow：审计 Skill

<required_reading>
**立即阅读这些参考文件：**
1. references/recommended-structure.md
2. references/skill-structure.md
3. references/use-xml-tags.md
</required_reading>

<process>
## 步骤 1：列出可用的 Skill

**不要使用 AskUserQuestion** - 可能有很多 skill。

在聊天中将 skill 枚举为编号列表：
```bash
ls ~/.claude/skills/
```

显示为：
```
可用的 skill：
1. create-agent-skills
2. build-macos-apps
3. manage-stripe
...
```

询问："您想审计哪个 skill？（输入数字或名称）"

## 步骤 2：读取 Skill

用户选择后，读取完整的 skill 结构：
```bash
# 读取主文件
cat ~/.claude/skills/{skill-name}/SKILL.md

# 检查 workflow 和 reference
ls ~/.claude/skills/{skill-name}/
ls ~/.claude/skills/{skill-name}/workflows/ 2>/dev/null
ls ~/.claude/skills/{skill-name}/references/ 2>/dev/null
```

## 步骤 3：运行审计检查清单

针对每个标准进行评估：

### YAML Frontmatter
- [ ] 有 `name:` 字段（lowercase-with-hyphens）
- [ ] 名称与目录名称匹配
- [ ] 有 `description:` 字段
- [ ] 描述说明它做什么以及何时使用它
- [ ] 描述是第三人称（"Use when..."）

### 结构
- [ ] SKILL.md 少于 500 行
- [ ] 纯 XML 结构（主体中没有 markdown 标题 #）
- [ ] 所有 XML 标签正确关闭
- [ ] 有必需的标签：objective 或 essential_principles
- [ ] 有 success_criteria

### Router 模式（如果是复杂 skill）
- [ ] Essential principles 内联在 SKILL.md 中（不在单独的文件中）
- [ ] 有 intake 问题
- [ ] 有 routing 表
- [ ] 所有引用的 workflow 文件都存在
- [ ] 所有引用的 reference 文件都存在

### Workflows（如果存在）
- [ ] 每个都有 required_reading 部分
- [ ] 每个都有 process 部分
- [ ] 每个都有 success_criteria 部分
- [ ] Required reading 引用存在

### 内容质量
- [ ] 原则是可操作的（不是模糊的陈词滥调）
- [ ] 步骤是具体的（不是"做这件事"）
- [ ] 成功标准是可验证的
- [ ] 文件之间没有冗余内容

## 步骤 4：生成报告

将调查结果显示为：

```
## 审计报告：{skill-name}

### ✅ 通过
- [列出通过的项目]

### ⚠️ 发现问题
1. **[问题名称]**：[描述]
   → 修复：[具体操作]

2. **[问题名称]**：[描述]
   → 修复：[具体操作]

### 📊 得分：X/Y 标准通过
```

## 步骤 5：提供修复

如果发现问题，询问：
"您想让我修复这些问题吗？"

选项：
1. **全部修复** - 应用所有推荐的修复
2. **逐个修复** - 在应用之前审查每个修复
3. **仅报告** - 不需要更改

如果修复：
- 进行每个更改
- 在每次更改后验证文件有效性
- 报告已修复的内容
</process>

<audit_anti_patterns>
## 要标记的常见反模式

**可跳过的原则**：Essential principles 在单独的文件中而不是内联
**单片 skill**：单个文件超过 500 行
**混合关注点**：程序和知识在同一个文件中
**模糊的步骤**："适当地处理错误"
**不可测试的标准**："用户满意"
**主体中的 Markdown 标题**：使用 # 而不是 XML 标签
**缺少 routing**：没有 intake/routing 的复杂 skill
**断开的引用**：提到但不存在的文件
**冗余内容**：相同的信息在多个地方
</audit_anti_patterns>

<success_criteria>
审计在以下情况下完成：
- [ ] Skill 已完全读取和分析
- [ ] 所有检查清单项目已评估
- [ ] 报告已呈现给用户
- [ ] 修复已应用（如果请求）
- [ ] 用户清楚了解 skill 的健康状况
</success_criteria>
