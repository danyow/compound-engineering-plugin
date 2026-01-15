---
name: workflows:compound
description: 记录最近解决的问题以复合团队的知识
argument-hint: "[可选：关于修复的简要上下文]"
---

# /compound

协调多个子Agent并行工作以记录最近解决的问题。

## 目的

在上下文新鲜时捕获问题解决方案，在 `docs/solutions/` 中创建带有YAML frontmatter的结构化文档，以便搜索和未来参考。使用并行子Agent以获得最大效率。

**为什么叫"compound"？** 每个记录的解决方案都会复合团队的知识。第一次解决问题需要研究。记录下来，下次出现只需几分钟。知识复合增长。

## 使用方法

```bash
/workflows:compound                    # 记录最近的修复
/workflows:compound [简要上下文]       # 提供额外的上下文提示
```

## 执行策略：并行子Agent

此命令启动多个专门的子Agent并行工作以最大化效率：

### 1. **上下文分析器**（并行）
   - 提取对话历史
   - 识别问题类型、组件、症状
   - 针对CORA schema验证
   - 返回：YAML frontmatter骨架

### 2. **解决方案提取器**（并行）
   - 分析所有调查步骤
   - 识别根本原因
   - 提取带代码示例的工作解决方案
   - 返回：解决方案内容块

### 3. **相关文档查找器**（并行）
   - 搜索 `docs/solutions/` 以查找相关文档
   - 识别交叉引用和链接
   - 查找相关GitHub issue
   - 返回：链接和关系

### 4. **预防策略师**（并行）
   - 制定预防策略
   - 创建最佳实践指南
   - 如果适用，生成测试用例
   - 返回：预防/测试内容

### 5. **类别分类器**（并行）
   - 确定最佳 `docs/solutions/` 类别
   - 针对schema验证类别
   - 根据slug建议文件名
   - 返回：最终路径和文件名

### 6. **文档编写器**（并行）
   - 组装完整的markdown文件
   - 验证YAML frontmatter
   - 格式化内容以提高可读性
   - 在正确位置创建文件

### 7. **可选：专门Agent调用**（文档后）
   根据检测到的问题类型，自动调用适用的Agent：
   - **performance_issue** → `performance-oracle`
   - **security_issue** → `security-sentinel`
   - **database_issue** → `data-integrity-guardian`
   - **test_failure** → `cora-test-reviewer`
   - 任何代码密集型问题 → `kieran-rails-reviewer` + `code-simplicity-reviewer`

## 捕获的内容

- **问题症状**：确切的错误消息、可观察的行为
- **尝试的调查步骤**：什么不起作用以及为什么
- **根本原因分析**：技术解释
- **工作解决方案**：带代码示例的逐步修复
- **预防策略**：如何在未来避免
- **交叉引用**：相关issue和文档的链接

## 先决条件

<preconditions enforcement="advisory">
  <check condition="problem_solved">
    问题已解决（不是进行中）
  </check>
  <check condition="solution_verified">
    解决方案已验证有效
  </check>
  <check condition="non_trivial">
    非平凡问题（不是简单的拼写错误或明显错误）
  </check>
</preconditions>

## 创建的内容

**组织化的文档：**

- 文件：`docs/solutions/[category]/[filename].md`

**从问题自动检测的类别：**

- build-errors/
- test-failures/
- runtime-errors/
- performance-issues/
- database-issues/
- security-issues/
- ui-bugs/
- integration-issues/
- logic-errors/

## 成功输出

```
✓ 并行文档生成完成

主要子Agent结果：
  ✓ 上下文分析器：在brief_system中识别出performance_issue
  ✓ 解决方案提取器：提取了3个代码修复
  ✓ 相关文档查找器：找到2个相关issue
  ✓ 预防策略师：生成了测试用例
  ✓ 类别分类器：docs/solutions/performance-issues/
  ✓ 文档编写器：创建了完整的markdown

专门Agent审查（自动触发）：
  ✓ performance-oracle：验证了查询优化方法
  ✓ kieran-rails-reviewer：代码示例符合Rails标准
  ✓ code-simplicity-reviewer：解决方案适当简约
  ✓ every-style-editor：文档风格已验证

创建的文件：
- docs/solutions/performance-issues/n-plus-one-brief-generation.md

当Email Processing或Brief System模块中出现类似问题时，
此文档将可被搜索以供未来参考。

接下来做什么？
1. 继续工作流（推荐）
2. 链接相关文档
3. 更新其他引用
4. 查看文档
5. 其他
```

## 复合哲学

这创建了一个复合知识系统：

1. 第一次解决"brief生成中的N+1查询" → 研究（30分钟）
2. 记录解决方案 → docs/solutions/performance-issues/n-plus-one-briefs.md（5分钟）
3. 下次出现类似问题 → 快速查找（2分钟）
4. 知识复合增长 → 团队变得更聪明

反馈循环：

```
构建 → 测试 → 发现问题 → 研究 → 改进 → 记录 → 验证 → 部署
    ↑                                                      ↓
    └──────────────────────────────────────────────────────┘
```

**每单位工程工作都应该使后续工作变得更容易——而不是更难。**

## 自动调用

<auto_invoke> <trigger_phrases> - "that worked" - "it's fixed" - "working now" - "problem solved" </trigger_phrases>

<manual_override> 使用 /workflows:compound [context] 立即记录，无需等待自动检测。 </manual_override> </auto_invoke>

## 路由到

`compound-docs` skill

## 适用的专门Agent

根据问题类型，这些Agent可以增强文档：

### 代码质量与审查
- **kieran-rails-reviewer**：审查代码示例的Rails最佳实践
- **code-simplicity-reviewer**：确保解决方案代码简约清晰
- **pattern-recognition-specialist**：识别反模式或重复问题

### 特定领域专家
- **performance-oracle**：分析performance_issue类别解决方案
- **security-sentinel**：审查security_issue解决方案的漏洞
- **cora-test-reviewer**：为预防策略创建测试用例
- **data-integrity-guardian**：审查database_issue迁移和查询

### 增强与文档
- **best-practices-researcher**：用行业最佳实践丰富解决方案
- **every-style-editor**：审查文档风格和清晰度
- **framework-docs-researcher**：链接到Rails/gem文档引用

### 何时调用
- **自动触发**（可选）：Agent可以在文档后运行以进行增强
- **手动触发**：用户可以在 /workflows:compound 完成后调用Agent进行更深入的审查

## 相关命令

- `/research [topic]` - 深入调查（搜索docs/solutions/以查找模式）
- `/workflows:plan` - 规划工作流（引用已记录的解决方案）
