---
name: compound-docs
description: 将已解决的问题捕获为带有 YAML frontmatter 的分类文档，以便快速查找
allowed-tools:
  - Read # 解析对话上下文
  - Write # 创建解决方案文档
  - Bash # 创建目录
  - Grep # 搜索现有文档
preconditions:
  - 问题已解决（非进行中）
  - 解决方案已验证可工作
---

# compound-docs Skill

**目的：**在确认后立即自动记录已解决的问题，构建具有基于类别组织（枚举验证的问题类型）的可搜索机构知识。

## 概述

此 skill 在确认后立即捕获问题解决方案，创建结构化文档，作为未来会话的可搜索知识库。

**组织方式：**单文件架构 - 每个问题记录为其症状类别目录中的一个 markdown 文件（例如，`docs/solutions/performance-issues/n-plus-one-briefs.md`）。文件使用 YAML frontmatter 存储元数据和可搜索性。

---

<critical_sequence name="documentation-capture" enforce_order="strict">

## 7 步流程

<step number="1" required="true">
### 步骤 1：检测确认

**在以下短语后自动调用：**

- "that worked"（成功了）
- "it's fixed"（修好了）
- "working now"（现在可以工作了）
- "problem solved"（问题已解决）
- "that did it"（就是这样）

**或手动：** `/doc-fix` 命令

**仅非平凡问题：**

- 需要多次调查尝试
- 耗时的棘手调试
- 非显而易见的解决方案
- 未来会话会受益

**跳过以下情况的文档：**

- 简单的拼写错误
- 明显的语法错误
- 立即纠正的平凡修复
</step>

<step number="2" required="true" depends_on="1">
### 步骤 2：收集上下文

从对话历史中提取：

**必需信息：**

- **模块名称**：哪个 CORA 模块有问题
- **症状**：可观察的错误/行为（确切的错误消息）
- **调查尝试**：什么没有起作用以及为什么
- **根本原因**：实际问题的技术解释
- **解决方案**：修复它的方法（代码/配置更改）
- **预防**：如何在未来避免

**环境详细信息：**

- Rails 版本
- 阶段（0-6 或实施后）
- 操作系统版本
- 文件/行引用

**阻塞要求：**如果缺少关键上下文（模块名称、确切错误、阶段或解决步骤），询问用户并等待响应后再继续步骤 3：

```
我需要一些细节来正确记录这个：

1. 哪个模块有这个问题？[模块名称]
2. 确切的错误消息或症状是什么？
3. 你在哪个阶段？（0-6 或实施后）

[在用户提供详细信息后继续]
```
</step>

<step number="3" required="false" depends_on="2">
### 步骤 3：检查现有文档

搜索 docs/solutions/ 中的类似问题：

```bash
# 按错误消息关键字搜索
grep -r "exact error phrase" docs/solutions/

# 按症状类别搜索
ls docs/solutions/[category]/
```

**如果找到类似问题：**

则呈现决策选项：

```
找到类似问题：docs/solutions/[path]

接下来做什么？
1. 创建带交叉引用的新文档（推荐）
2. 更新现有文档（仅当根本原因相同时）
3. 其他

选择 (1-3): _
```

等待用户响应，然后执行选择的操作。

**否则**（未找到类似问题）：

直接进入步骤 4（无需用户交互）。
</step>

<step number="4" required="true" depends_on="2">
### 步骤 4：生成文件名

格式：`[sanitized-symptom]-[module]-[YYYYMMDD].md`

**清理规则：**

- 小写
- 用连字符替换空格
- 删除特殊字符（连字符除外）
- 截断到合理长度（< 80 字符）

**示例：**

- `missing-include-BriefSystem-20251110.md`
- `parameter-not-saving-state-EmailProcessing-20251110.md`
- `webview-crash-on-resize-Assistant-20251110.md`
</step>

<step number="5" required="true" depends_on="4" blocking="true">
### 步骤 5：验证 YAML Schema

**关键：**所有文档都需要经过验证的 YAML frontmatter 和枚举验证。

<validation_gate name="yaml-schema" blocking="true">

**针对 schema 验证：**
加载 `schema.yaml` 并根据 [yaml-schema.md](./references/yaml-schema.md) 中定义的枚举值对问题进行分类。确保所有必需字段都存在并完全匹配允许的值。

**如果验证失败则阻塞：**

```
❌ YAML 验证失败

错误：
- problem_type: 必须是 schema 枚举之一，得到 "compilation_error"
- severity: 必须是 [critical, moderate, minor] 之一，得到 "high"
- symptoms: 必须是包含 1-5 个项目的数组，得到字符串

请提供更正的值。
```

**门控强制：**在 YAML frontmatter 通过 `schema.yaml` 中定义的所有验证规则之前，不要进入步骤 6（创建文档）。

</validation_gate>
</step>

<step number="6" required="true" depends_on="5">
### 步骤 6：创建文档

**从 problem_type 确定类别：**使用 [yaml-schema.md](./references/yaml-schema.md)（第 49-61 行）中定义的类别映射。

**创建文档文件：**

```bash
PROBLEM_TYPE="[from validated YAML]"
CATEGORY="[mapped from problem_type]"
FILENAME="[generated-filename].md"
DOC_PATH="docs/solutions/${CATEGORY}/${FILENAME}"

# 如果需要则创建目录
mkdir -p "docs/solutions/${CATEGORY}"

# 使用 assets/resolution-template.md 中的模板编写文档
# (使用步骤 2 的上下文和验证的 YAML frontmatter 填充内容)
```

**结果：**
- 类别目录中的单个文件
- 枚举验证确保一致的分类

**创建文档：**使用步骤 2 收集的上下文和步骤 5 验证的 YAML frontmatter 填充 `assets/resolution-template.md` 中的结构。
</step>

<step number="7" required="false" depends_on="6">
### 步骤 7：交叉引用和关键模式检测

如果在步骤 3 中找到类似问题：

**更新现有文档：**

```bash
# 向类似文档添加相关问题链接
echo "- See also: [$FILENAME]($REAL_FILE)" >> [similar-doc.md]
```

**更新新文档：**
已包含步骤 6 的交叉引用。

**如适用则更新模式：**

如果这代表一个常见模式（3+ 个类似问题）：

```bash
# 添加到 docs/solutions/patterns/common-solutions.md
cat >> docs/solutions/patterns/common-solutions.md << 'EOF'

## [模式名称]

**常见症状：** [描述]
**根本原因：** [技术解释]
**解决方案模式：** [通用方法]

**示例：**
- [链接到文档 1]
- [链接到文档 2]
- [链接到文档 3]
EOF
```

**关键模式检测（可选的主动建议）：**

如果此问题具有表明可能是关键的自动指标：
- 严重性：YAML 中的 `critical`
- 影响多个模块或基础阶段（阶段 2 或 3）
- 非显而易见的解决方案

则在决策菜单（步骤 8）中添加注释：
```
💡 这可能值得添加到必读内容（选项 2）
```

但**永远不要自动提升**。用户通过决策菜单决定（选项 2）。

**关键模式添加的模板：**

当用户选择选项 2（添加到必读内容）时，使用 `assets/critical-pattern-template.md` 中的模板来构建模式条目。根据 `docs/solutions/patterns/cora-critical-patterns.md` 中的现有模式按顺序编号。
</step>

</critical_sequence>

---

<decision_gate name="post-documentation" wait_for_user="true">

## 捕获后的决策菜单

成功记录后，呈现选项并等待用户响应：

```
✓ 解决方案已记录

创建的文件：
- docs/solutions/[category]/[filename].md

接下来做什么？
1. 继续工作流（推荐）
2. 添加到必读内容 - 提升到关键模式（cora-critical-patterns.md）
3. 链接相关问题 - 连接到类似问题
4. 添加到现有 skill - 添加到学习 skill（例如，hotwire-native）
5. 创建新 skill - 提取到新的学习 skill
6. 查看文档 - 查看捕获的内容
7. 其他
```

**处理响应：**

**选项 1：继续工作流**

- 返回到调用 skill/工作流
- 文档已完成

**选项 2：添加到必读内容** ⭐ 关键模式的主要路径

用户在以下情况下选择此项：
- 系统在不同模块中多次犯此错误
- 解决方案非显而易见但每次都必须遵循
- 基础要求（Rails、Rails API、线程等）

操作：
1. 从文档中提取模式
2. 格式化为 ❌ 错误 vs ✅ 正确，带代码示例
3. 添加到 `docs/solutions/patterns/cora-critical-patterns.md`
4. 添加回此文档的交叉引用
5. 确认："✓ 已添加到必读内容。所有子 Agent 将在代码生成前看到此模式。"

**选项 3：链接相关问题**

- 提示："要链接哪个文档？（提供文件名或描述）"
- 在 docs/solutions/ 中搜索文档
- 向两个文档添加交叉引用
- 确认："✓ 已添加交叉引用"

**选项 4：添加到现有 skill**

当记录的解决方案与现有学习 skill 相关时，用户选择此项：

操作：
1. 提示："哪个 skill？（hotwire-native 等）"
2. 确定要更新哪个参考文件（resources.md、patterns.md 或 examples.md）
3. 向适当部分添加链接和简要描述
4. 确认："✓ 已添加到 [skill-name] skill 的 [file]"

示例：对于 Hotwire Native Tailwind 变体解决方案：
- 添加到 `hotwire-native/references/resources.md` 的"CORA 特定资源"下
- 添加到 `hotwire-native/references/examples.md`，带解决方案文档的链接

**选项 5：创建新 skill**

当解决方案代表新学习领域的开始时，用户选择此项：

操作：
1. 提示："新 skill 应该叫什么？（例如，stripe-billing、email-processing）"
2. 运行 `python3 .claude/skills/skill-creator/scripts/init_skill.py [skill-name]`
3. 以此解决方案作为第一个示例创建初始参考文件
4. 确认："✓ 已创建新的 [skill-name] skill，以此解决方案作为第一个示例"

**选项 6：查看文档**

- 显示创建的文档
- 再次呈现决策菜单

**选项 7：其他**

- 询问他们想做什么

</decision_gate>

---

<integration_protocol>

## 集成点

**调用者：**
- /compound 命令（主要接口）
- 解决方案确认后在对话中手动调用
- 可以通过检测确认短语触发，如"that worked"、"it's fixed"等

**调用：**
- 无（终端 skill - 不委托给其他 skill）

**交接期望：**
在调用之前，文档所需的所有上下文应该存在于对话历史中。

</integration_protocol>

---

<success_criteria>

## 成功标准

当以下所有条件都为真时，文档记录成功：

- ✅ YAML frontmatter 已验证（所有必需字段、正确格式）
- ✅ 在 docs/solutions/[category]/[filename].md 中创建文件
- ✅ 枚举值完全匹配 schema.yaml
- ✅ 解决方案部分包含代码示例
- ✅ 如果找到相关问题则添加交叉引用
- ✅ 向用户呈现决策菜单并确认操作

</success_criteria>

---

## 错误处理

**缺失上下文：**

- 向用户询问缺失的详细信息
- 在提供关键信息之前不要继续

**YAML 验证失败：**

- 显示具体错误
- 呈现带更正值的重试
- 阻塞直到有效

**类似问题歧义：**

- 呈现多个匹配
- 让用户选择：新文档、更新现有文档或作为重复链接

**模块不在 CORA-MODULES.md 中：**

- 警告但不阻塞
- 继续文档记录
- 建议："如果 [模块] 不在其中，添加到 CORA-MODULES.md"

---

## 执行指南

**必须做：**
- 验证 YAML frontmatter（如果按照步骤 5 验证门控无效则阻塞）
- 从对话中提取确切的错误消息
- 在解决方案部分包含代码示例
- 在写入文件之前创建目录（`mkdir -p`）
- 如果缺少关键上下文，询问用户并等待

**不得做：**
- 跳过 YAML 验证（验证门控是阻塞的）
- 使用模糊描述（不可搜索）
- 省略代码示例或交叉引用

---

## 质量指南

**好的文档具有：**

- ✅ 确切的错误消息（从输出复制粘贴）
- ✅ 具体的文件:行引用
- ✅ 可观察的症状（你看到的，而非解释）
- ✅ 记录失败的尝试（帮助避免错误路径）
- ✅ 技术解释（不仅是"什么"还有"为什么"）
- ✅ 代码示例（如适用，之前/之后）
- ✅ 预防指导（如何早期发现）
- ✅ 交叉引用（相关问题）

**避免：**

- ❌ 模糊描述（"出了些问题"）
- ❌ 缺少技术细节（"修复了代码"）
- ❌ 无上下文（哪个版本？哪个文件？）
- ❌ 只是代码转储（解释为什么有效）
- ❌ 无预防指导
- ❌ 无交叉引用

---

## 示例场景

**用户：**"成功了！N+1 查询已修复。"

**Skill 激活：**

1. **检测确认：**"成功了！"触发自动调用
2. **收集上下文：**
   - 模块：Brief System
   - 症状：Brief 生成耗时 >5 秒，加载电子邮件线程时出现 N+1 查询
   - 失败尝试：添加分页（没有帮助）、检查后台作业性能
   - 解决方案：在 Brief 模型上添加 `includes(:emails)` 急加载
   - 根本原因：缺少急加载导致每个电子邮件线程单独数据库查询
3. **检查现有：**未找到类似问题
4. **生成文件名：**`n-plus-one-brief-generation-BriefSystem-20251110.md`
5. **验证 YAML：**
   ```yaml
   module: Brief System
   date: 2025-11-10
   problem_type: performance_issue
   component: rails_model
   symptoms:
     - "N+1 query when loading email threads"
     - "Brief generation taking >5 seconds"
   root_cause: missing_include
   severity: high
   tags: [n-plus-one, eager-loading, performance]
   ```
   ✅ 有效
6. **创建文档：**
   - `docs/solutions/performance-issues/n-plus-one-brief-generation-BriefSystem-20251110.md`
7. **交叉引用：**不需要（无类似问题）

**输出：**

```
✓ 解决方案已记录

创建的文件：
- docs/solutions/performance-issues/n-plus-one-brief-generation-BriefSystem-20251110.md

接下来做什么？
1. 继续工作流（推荐）
2. 添加到必读内容 - 提升到关键模式（cora-critical-patterns.md）
3. 链接相关问题 - 连接到类似问题
4. 添加到现有 skill - 添加到学习 skill（例如，hotwire-native）
5. 创建新 skill - 提取到新的学习 skill
6. 查看文档 - 查看捕获的内容
7. 其他
```

---

## 未来增强

**不在阶段 7 范围内，但有潜力：**

- 按日期范围搜索
- 按严重性过滤
- 基于标签的搜索界面
- 指标（最常见问题、解决时间）
- 导出为可共享格式（社区知识共享）
- 导入社区解决方案
