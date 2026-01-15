<overview>
Skill 通过迭代和测试改进。此参考涵盖评估驱动开发、Claude A/B 测试模式以及测试期间的 XML 结构验证。
</overview>

<evaluation_driven_development>
<principle>
在编写大量文档之前创建评估。这确保你的 skill 解决实际问题而不是记录想象的问题。
</principle>

<workflow>
<step_1>
**识别差距**：在没有 skill 的情况下对代表性任务运行 Claude。记录特定的失败或缺失的上下文。
</step_1>

<step_2>
**创建评估**：构建测试这些差距的三个场景。
</step_2>

<step_3>
**建立基线**：测量没有 skill 的 Claude 性能。
</step_3>

<step_4>
**编写最小指令**：创建足够的内容来解决差距并通过评估。
</step_4>

<step_5>
**迭代**：执行评估，与基线比较并改进。
</step_5>
</workflow>

<evaluation_structure>
```json
{
  "skills": ["pdf-processing"],
  "query": "Extract all text from this PDF file and save it to output.txt",
  "files": ["test-files/document.pdf"],
  "expected_behavior": [
    "Successfully reads the PDF file using appropriate library",
    "Extracts text content from all pages without missing any",
    "Saves extracted text to output.txt in clear, readable format"
  ]
}
```
</evaluation_structure>

<why_evaluations_first>
- 防止记录想象的问题
- 强制明确成功的样子
- 提供 skill 效果的客观测量
- 保持 skill 专注于实际需求
- 实现定量改进跟踪
</why_evaluations_first>
</evaluation_driven_development>

<iterative_development_with_claude>
<principle>
最有效的 skill 开发使用 Claude 本身。与"Claude A"（帮助改进的专家）合作，创建"Claude B"（执行任务的代理）使用的 skill。
</principle>

<creating_skills>
<workflow>
<step_1>
**在没有 skill 的情况下完成任务**：与 Claude A 一起解决问题，注意你反复提供的上下文。
</step_1>

<step_2>
**要求 Claude A 创建 skill**："创建一个捕捉我们刚刚使用的模式的 skill"
</step_2>

<step_3>
**审查简洁性**：删除不必要的解释。
</step_3>

<step_4>
**改进架构**：使用渐进式披露组织内容。
</step_4>

<step_5>
**使用 Claude B 测试**：使用新实例在实际任务上测试。
</step_5>

<step_6>
**基于观察迭代**：带着观察到的具体问题返回 Claude A。
</step_6>
</workflow>

<insight>
Claude 模型本地理解 skill 格式。只需要求 Claude 创建 skill，它就会生成正确结构的 SKILL.md 内容。
</insight>
</creating_skills>

<improving_skills>
<workflow>
<step_1>
**在实际工作流中使用 skill**：给 Claude B 实际任务。
</step_1>

<step_2>
**观察行为**：它在哪里挣扎、成功或做出意外选择？
</step_2>

<step_3>
**返回 Claude A**：分享观察和当前的 SKILL.md。
</step_3>

<step_4>
**审查建议**：Claude A 可能建议重组、更强的语言或工作流重组。
</step_4>

<step_5>
**应用和测试**：更新 skill 并再次测试。
</step_5>

<step_6>
**重复**：基于实际使用继续，而不是假设。
</step_6>
</workflow>

<what_to_watch_for>
- **意外的探索路径**：结构可能不直观
- **错过的连接**：链接可能需要更明确
- **过度依赖章节**：考虑将频繁阅读的内容移到主 SKILL.md
- **忽略的内容**：信号不良或不必要的文件
- **关键元数据**：skill 元数据中的名称和描述对发现至关重要
</what_to_watch_for>
</improving_skills>
</iterative_development_with_claude>

<model_testing>
<principle>
使用你计划使用的所有模型进行测试。不同的模型有不同的优势，需要不同级别的细节。
</principle>

<haiku_testing>
**Claude Haiku**（快速、经济）

要问的问题：
- skill 是否提供足够的指导？
- 示例是否清晰完整？
- 隐含的假设是否变得明确？
- Haiku 是否需要更多结构？

Haiku 受益于：
- 更明确的指令
- 完整的示例（没有部分代码）
- 清晰的成功标准
- 分步工作流
</haiku_testing>

<sonnet_testing>
**Claude Sonnet**（平衡）

要问的问题：
- skill 是否清晰高效？
- 它是否避免过度解释？
- 工作流是否结构良好？
- 渐进式披露是否有效？

Sonnet 受益于：
- 平衡的细节级别
- 用于清晰的 XML 结构
- 渐进式披露
- 简洁但完整的指导
</sonnet_testing>

<opus_testing>
**Claude Opus**（强大的推理）

要问的问题：
- skill 是否避免过度解释？
- Opus 能否推断明显的步骤？
- 约束是否清晰？
- 上下文是否最小但足够？

Opus 受益于：
- 简洁的指令
- 原则而不是程序
- 高度的自由
- 信任推理能力
</opus_testing>

<balancing_across_models>
对 Opus 有效的可能需要为 Haiku 提供更多细节。目标是在所有目标模型上都能很好地工作的指令。找到为目标受众服务的平衡。

参见 [core-principles.md](core-principles.md) 了解模型测试示例。
</balancing_across_models>
</model_testing>

<xml_structure_validation>
<principle>
在测试期间，验证你的 skill 的 XML 结构是正确和完整的。
</principle>

<validation_checklist>
更新 skill 后，验证：

<required_tags_present>
- ✅ `<objective>` 标签存在并定义 skill 的作用
- ✅ `<quick_start>` 标签存在即时指导
- ✅ `<success_criteria>` 或 `<when_successful>` 标签存在
</required_tags_present>

<no_markdown_headings>
- ✅ skill 主体中没有 `#`、`##` 或 `###` 标题
- ✅ 所有章节改用 XML 标签
- ✅ 保留标签内的 markdown 格式（粗体、斜体、列表、代码块）
</no_markdown_headings>

<proper_xml_nesting>
- ✅ 所有 XML 标签正确关闭
- ✅ 嵌套标签有正确的层次结构
- ✅ 没有未关闭的标签
</proper_xml_nesting>

<conditional_tags_appropriate>
- ✅ 条件标签与 skill 复杂度匹配
- ✅ 简单的 skill 仅使用必需标签
- ✅ 复杂的 skill 添加适当的条件标签
- ✅ 没有过度工程或规格不足
</conditional_tags_appropriate>

<reference_files_check>
- ✅ 参考文件也使用纯 XML 结构
- ✅ 到参考文件的链接是正确的
- ✅ 从 SKILL.md 一级深度的参考
</reference_files_check>
</validation_checklist>

<testing_xml_during_iteration>
在迭代 skill 时：

1. 对 XML 结构进行更改
2. **验证 XML 结构**（检查标签、嵌套、完整性）
3. 在代表性任务上使用 Claude 测试
4. 观察 XML 结构是帮助还是阻碍 Claude 的理解
5. 基于实际性能迭代结构
</testing_xml_during_iteration>
</xml_structure_validation>

<observation_based_iteration>
<principle>
基于你观察到的而不是你假设的进行迭代。实际使用揭示假设会错过的问题。
</principle>

<observation_categories>
<what_claude_reads>
Claude 实际读取哪些章节？哪些被忽略了？这揭示了：
- 内容的相关性
- 渐进式披露的有效性
- 章节名称是否清晰
</what_claude_reads>

<where_claude_struggles>
哪些任务导致混淆或错误？这揭示了：
- 缺失的上下文
- 不清楚的指令
- 不充分的示例
- 模糊的要求
</where_claude_struggles>

<where_claude_succeeds>
哪些任务进展顺利？这揭示了：
- 有效的模式
- 好的示例
- 清晰的指令
- 适当的细节级别
</where_claude_succeeds>

<unexpected_behaviors>
Claude 做了什么让你惊讶的事情？这揭示了：
- 未声明的假设
- 模糊的措辞
- 缺失的约束
- 替代解释
</unexpected_behaviors>
</observation_categories>

<iteration_pattern>
1. **观察**：在当前 skill 的实际任务上运行 Claude
2. **记录**：注意具体问题，而不是一般感觉
3. **假设**：为什么会出现这个问题？
4. **修复**：进行有针对性的更改以解决具体问题
5. **测试**：验证修复在相同场景上有效
6. **验证**：确保修复不会破坏其他场景
7. **重复**：继续下一个观察到的问题
</iteration_pattern>
</observation_based_iteration>

<progressive_refinement>
<principle>
Skill 最初不需要完美。从最小开始，观察使用，添加缺失的内容。
</principle>

<initial_version>
开始时包括：
- 有效的 YAML frontmatter
- 必需的 XML 标签：objective、quick_start、success_criteria
- 最小工作示例
- 基本成功标准

最初跳过：
- 大量示例
- 边缘情况文档
- 高级功能
- 详细的参考文件
</initial_version>

<iteration_additions>
通过迭代添加：
- 当从描述中看不清模式时添加示例
- 在实际使用中观察到时添加边缘情况
- 当用户需要时添加高级功能
- 当 SKILL.md 接近 500 行时添加参考文件
- 当错误常见时添加验证脚本
</iteration_additions>

<benefits>
- 更快达到初始工作版本
- 添加解决实际需求，而不是想象的需求
- 保持 skill 专注和简洁
- 渐进式披露自然出现
- 文档与实际使用保持一致
</benefits>
</progressive_refinement>

<testing_discovery>
<principle>
测试 Claude 在适当的时候可以发现和使用你的 skill。
</principle>

<discovery_testing>
<test_description>
测试 Claude 是否在应该加载 skill 时加载：

1. 开始新对话（Claude B）
2. 提出应该触发 skill 的问题
3. 检查 skill 是否已加载
4. 验证 skill 使用是否适当
</test_description>

<description_quality>
如果 skill 未被发现：
- 检查描述是否包含触发关键词
- 验证描述具体，而不是模糊
- 确保描述解释何时使用 skill
- 使用相同请求的不同措辞测试

描述是 Claude 的主要发现机制。
</description_quality>
</discovery_testing>
</testing_discovery>

<common_iteration_patterns>
<pattern name="too_verbose">
**观察**：Skill 有效但使用大量 token

**修复**：
- 删除明显的解释
- 假设 Claude 知道常见概念
- 使用示例而不是冗长的描述
- 将高级内容移到参考文件
</pattern>

<pattern name="too_minimal">
**观察**：Claude 做出错误假设或错过步骤

**修复**：
- 在假设失败的地方添加明确指令
- 提供完整的工作示例
- 定义边缘情况
- 添加验证步骤
</pattern>

<pattern name="poor_discovery">
**观察**：Skill 存在但 Claude 在需要时不加载它

**修复**：
- 使用特定触发器改进描述
- 添加相关关键词
- 针对实际用户查询测试描述
- 使描述更具体地说明用例
</pattern>

<pattern name="unclear_structure">
**观察**：Claude 读取错误的章节或错过相关内容

**修复**：
- 使用更清晰的 XML 标签名称
- 重组内容层次结构
- 将频繁需要的内容移到更早
- 添加到相关章节的明确链接
</pattern>

<pattern name="incomplete_examples">
**观察**：Claude 产生的输出与预期模式不匹配

**修复**：
- 添加更多显示模式的示例
- 使示例更完整
- 在示例中显示边缘情况
- 添加反模式示例（不该做什么）
</pattern>
</common_iteration_patterns>

<iteration_velocity>
<principle>
小而频繁的迭代胜过大而不频繁的重写。
</principle>

<fast_iteration>
**好的方法**：
1. 进行一次有针对性的更改
2. 在特定场景上测试
3. 验证改进
4. 提交更改
5. 转到下一个问题

总时间：每次迭代几分钟
每天迭代次数：10-20
学习率：高
</fast_iteration>

<slow_iteration>
**有问题的方法**：
1. 积累许多问题
2. 进行大规模重构
3. 一次测试所有内容
4. 同时调试多个问题
5. 很难知道什么修复了什么

总时间：每次迭代几小时
每天迭代次数：1-2
学习率：低
</slow_iteration>

<benefits_of_fast_iteration>
- 隔离因果关系
- 更快建立模式识别
- 减少错误方向的浪费工作
- 如果需要更容易恢复
- 保持动力
</benefits_of_fast_iteration>
</iteration_velocity>

<success_metrics>
<principle>
定义如何衡量 skill 是否有效。量化成功。
</principle>

<objective_metrics>
- **成功率**：正确完成任务的百分比
- **Token 使用**：每个任务消耗的平均 token
- **迭代次数**：获得正确输出需要多少次尝试
- **错误率**：有错误的任务百分比
- **发现率**：skill 在应该加载时的加载频率
</objective_metrics>

<subjective_metrics>
- **输出质量**：输出是否满足要求？
- **适当的细节**：太冗长还是太简略？
- **Claude 的信心**：Claude 似乎不确定吗？
- **用户满意度**：Skill 是否解决了实际问题？
</subjective_metrics>

<tracking_improvement>
比较更改前后的指标：
- 基线：没有 skill 的测量
- 初始：第一个版本的测量
- 迭代 N：每次更改后的测量

跟踪哪些更改改进了哪些指标。加倍有效的模式。
</tracking_improvement>
</success_metrics>
