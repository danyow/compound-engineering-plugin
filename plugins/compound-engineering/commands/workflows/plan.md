---
name: workflows:plan
description: 将功能描述转换为遵循约定的结构良好的项目计划
argument-hint: "[功能描述、bug报告或改进建议]"
---

# 为新功能或bug修复创建计划

## 介绍

**注意：当前年份是 2026 年。** 在标注计划日期和搜索最新文档时使用此信息。

将功能描述、bug报告或改进建议转换为结构良好的markdown文件issue，遵循项目约定和最佳实践。此命令提供灵活的详细程度级别以匹配您的需求。

## 功能描述

<feature_description> #$ARGUMENTS </feature_description>

**如果上面的功能描述为空，请询问用户：** "您想规划什么？请描述您想到的功能、bug修复或改进。"

在获得用户明确的功能描述之前不要继续。

## 主要任务

### 1. 仓库研究与上下文收集

<thinking>
首先，我需要了解项目的约定和现有模式，利用所有可用资源，并使用并行子Agent来完成此任务。
</thinking>

同时并行运行这三个Agent：

- Task repo-research-analyst(feature_description)
- Task best-practices-researcher(feature_description)
- Task framework-docs-researcher(feature_description)

**参考资料收集：**

- [ ] 记录所有研究发现，包含具体文件路径（例如 `app/services/example_service.rb:42`）
- [ ] 包含外部文档和最佳实践指南的URL
- [ ] 创建类似issue或PR的参考列表（例如 `#123`、`#456`）
- [ ] 记录在 `CLAUDE.md` 或团队文档中发现的任何团队约定

### 2. Issue 规划与结构

<thinking>
像产品经理一样思考 - 什么能让这个issue清晰且可操作？考虑多个角度
</thinking>

**标题与分类：**

- [ ] 使用常规格式（例如 `feat:`、`fix:`、`docs:`）起草清晰、可搜索的issue标题
- [ ] 确定issue类型：enhancement、bug、refactor

**利益相关者分析：**

- [ ] 确定谁将受到此issue影响（最终用户、开发人员、运维人员）
- [ ] 考虑实现复杂度和所需专业知识

**内容规划：**

- [ ] 根据issue复杂度和受众选择适当的详细程度级别
- [ ] 列出所选模板的所有必需部分
- [ ] 收集支持材料（错误日志、截图、设计稿）
- [ ] 如果适用，准备代码示例或复现步骤，在列表中命名模拟文件名

### 3. SpecFlow 分析

规划issue结构后，运行SpecFlow Analyzer来验证和完善功能规范：

- Task spec-flow-analyzer(feature_description, research_findings)

**SpecFlow Analyzer 输出：**

- [ ] 审查SpecFlow分析结果
- [ ] 将识别出的任何缺口或边界情况纳入issue
- [ ] 根据SpecFlow发现更新验收标准

### 4. 选择实现详细程度

选择您希望issue有多全面，通常越简单越好。

#### 📄 MINIMAL（快速Issue）

**最适合：** 简单的bug、小的改进、明确的功能

**包含：**

- 问题陈述或功能描述
- 基本验收标准
- 仅必要的上下文

**结构：**

````markdown
[简要问题/功能描述]

## Acceptance Criteria

- [ ] 核心需求1
- [ ] 核心需求2

## Context

[任何关键信息]

## MVP

### test.rb

```ruby
class Test
  def initialize
    @name = "test"
  end
end
```

## References

- Related issue: #[issue_number]
- Documentation: [relevant_docs_url]
````

#### 📋 MORE（标准Issue）

**最适合：** 大多数功能、复杂的bug、团队协作

**包含MINIMAL的所有内容加上：**

- 详细的背景和动机
- 技术考虑因素
- 成功指标
- 依赖和风险
- 基本实现建议

**结构：**

```markdown
## Overview

[全面的描述]

## Problem Statement / Motivation

[为什么这很重要]

## Proposed Solution

[高层方法]

## Technical Considerations

- 架构影响
- 性能影响
- 安全考虑因素

## Acceptance Criteria

- [ ] 详细需求1
- [ ] 详细需求2
- [ ] 测试需求

## Success Metrics

[如何衡量成功]

## Dependencies & Risks

[什么可能阻碍或使其复杂化]

## References & Research

- Similar implementations: [file_path:line_number]
- Best practices: [documentation_url]
- Related PRs: #[pr_number]
```

#### 📚 A LOT（全面Issue）

**最适合：** 主要功能、架构变更、复杂集成

**包含MORE的所有内容加上：**

- 分阶段的详细实现计划
- 考虑的备选方法
- 广泛的技术规范
- 资源需求和时间表
- 未来考虑和可扩展性
- 风险缓解策略
- 文档要求

**结构：**

```markdown
## Overview

[执行摘要]

## Problem Statement

[详细的问题分析]

## Proposed Solution

[全面的解决方案设计]

## Technical Approach

### Architecture

[详细的技术设计]

### Implementation Phases

#### Phase 1: [基础]

- 任务和交付物
- 成功标准
- 预计工作量

#### Phase 2: [核心实现]

- 任务和交付物
- 成功标准
- 预计工作量

#### Phase 3: [完善与优化]

- 任务和交付物
- 成功标准
- 预计工作量

## Alternative Approaches Considered

[评估过的其他解决方案及为何被拒绝]

## Acceptance Criteria

### Functional Requirements

- [ ] 详细的功能标准

### Non-Functional Requirements

- [ ] 性能目标
- [ ] 安全要求
- [ ] 可访问性标准

### Quality Gates

- [ ] 测试覆盖率要求
- [ ] 文档完整性
- [ ] 代码审查批准

## Success Metrics

[详细的KPI和测量方法]

## Dependencies & Prerequisites

[详细的依赖分析]

## Risk Analysis & Mitigation

[全面的风险评估]

## Resource Requirements

[团队、时间、基础设施需求]

## Future Considerations

[可扩展性和长期愿景]

## Documentation Plan

[需要更新哪些文档]

## References & Research

### Internal References

- Architecture decisions: [file_path:line_number]
- Similar features: [file_path:line_number]
- Configuration: [file_path:line_number]

### External References

- Framework documentation: [url]
- Best practices guide: [url]
- Industry standards: [url]

### Related Work

- Previous PRs: #[pr_numbers]
- Related issues: #[issue_numbers]
- Design documents: [links]
```

### 5. Issue 创建与格式化

<thinking>
应用最佳实践以提高清晰度和可操作性，使issue易于浏览和理解
</thinking>

**内容格式化：**

- [ ] 使用清晰、描述性的标题，保持适当的层次结构（##、###）
- [ ] 在三个反引号中包含代码示例，带有语言语法高亮
- [ ] 如果与UI相关，添加截图/原型（拖放或使用图片托管）
- [ ] 使用任务列表（- [ ]）用于可追踪的可勾选项目
- [ ] 使用 `<details>` 标签为冗长日志或可选细节添加可折叠部分
- [ ] 为视觉扫描应用适当的emoji（🐛 bug、✨ feature、📚 docs、♻️ refactor）

**交叉引用：**

- [ ] 使用#number格式链接到相关issue/PR
- [ ] 在相关时使用SHA哈希引用特定commit
- [ ] 使用GitHub的永久链接功能链接到代码（按'y'获取永久链接）
- [ ] 如有需要，用@username提及相关团队成员
- [ ] 添加带描述文本的外部资源链接

**代码与示例：**

````markdown
# 带语法高亮和行引用的良好示例


```ruby
# app/services/user_service.rb:42
def process_user(user)

# Implementation here

end
```

# 可折叠的错误日志

<details>
<summary>完整错误堆栈跟踪</summary>

`Error details here...`

</details>
````

**AI 时代考虑因素：**

- [ ] 考虑AI配对编程加速的开发
- [ ] 包含在研究期间效果良好的提示或指令
- [ ] 注明用于初步探索的AI工具（Claude、Copilot等）
- [ ] 鉴于快速实现，强调全面测试
- [ ] 记录任何需要人工审查的AI生成代码

### 6. 最终审查与提交

**提交前检查清单：**

- [ ] 标题可搜索且具有描述性
- [ ] 标签准确分类issue
- [ ] 所有模板部分都已完成
- [ ] 链接和引用可用
- [ ] 验收标准是可衡量的
- [ ] 在伪代码示例和todo列表中添加文件名
- [ ] 如果适用于新模型变更，添加ERD mermaid图

## 输出格式

将计划写入 `plans/<issue_title>.md`

## 生成后选项

写入计划文件后，使用 **AskUserQuestion tool** 呈现这些选项：

**问题：** "计划已就绪，位于 `plans/<issue_title>.md`。您接下来想做什么？"

**选项：**
1. **在编辑器中打开计划** - 打开计划文件进行审查
2. **运行 `/deepen-plan`** - 使用并行研究Agent（最佳实践、性能、UI）增强每个部分
3. **运行 `/plan_review`** - 从审查者（DHH、Kieran、Simplicity）获得反馈
4. **启动 `/workflows:work`** - 在本地开始实施此计划
5. **在远程启动 `/workflows:work`** - 在网页版Claude Code中开始实施（使用 `&` 在后台运行）
6. **创建Issue** - 在项目跟踪器中创建issue（GitHub/Linear）
7. **简化** - 降低详细程度

根据选择：
- **在编辑器中打开计划** → 运行 `open plans/<issue_title>.md` 在用户的默认编辑器中打开文件
- **`/deepen-plan`** → 使用计划文件路径调用/deepen-plan命令以通过研究增强
- **`/plan_review`** → 使用计划文件路径调用/plan_review命令
- **`/workflows:work`** → 使用计划文件路径调用/workflows:work命令
- **在远程启动 `/workflows:work`** → 运行 `/workflows:work plans/<issue_title>.md &` 为网页版Claude Code在后台启动工作
- **创建Issue** → 参见下面的"Issue创建"部分
- **简化** → 询问"我应该简化什么？"然后重新生成更简单的版本
- **其他**（自动提供）→ 接受自由文本以进行重做或特定更改

**注意：** 如果在启用ultrathink的情况下运行 `/workflows:plan`，在计划创建后自动运行 `/deepen-plan` 以获得最大深度和基础。

在简化或其他更改后循环回到选项，直到用户选择 `/workflows:work` 或 `/plan_review`。

## Issue 创建

当用户选择"创建Issue"时，从CLAUDE.md检测他们的项目跟踪器：

1. **在用户的CLAUDE.md（全局或项目）中检查跟踪器偏好：**
   - 查找 `project_tracker: github` 或 `project_tracker: linear`
   - 或在其工作流部分查找"GitHub Issues"或"Linear"的提及

2. **如果是GitHub：**
   ```bash
   # 从计划文件名提取标题（kebab-case 转 Title Case）
   # 读取计划内容作为正文
   gh issue create --title "feat: [Plan Title]" --body-file plans/<issue_title>.md
   ```

3. **如果是Linear：**
   ```bash
   # 如果可用，使用linear CLI，或提供说明
   # linear issue create --title "[Plan Title]" --description "$(cat plans/<issue_title>.md)"
   ```

4. **如果未配置跟踪器：**
   询问用户："您使用哪个项目跟踪器？（GitHub/Linear/其他）"
   - 建议在其CLAUDE.md中添加 `project_tracker: github` 或 `project_tracker: linear`

5. **创建后：**
   - 显示issue URL
   - 询问他们是否想继续 `/workflows:work` 或 `/plan_review`

永远不要编码！只做研究并撰写计划。
