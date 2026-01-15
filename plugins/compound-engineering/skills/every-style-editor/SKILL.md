---
name: every-style-editor
description: 用于审查或编辑文案以确保符合 Every 风格指南。提供系统化的逐行审查流程，涵盖语法、标点、格式和风格指南合规性。
---

# Every 风格编辑器

这个 skill 提供了一套系统化方法，用于根据 Every 的全面风格指南审查文案。它将 Claude 转变为专精于语法、格式和风格指南合规性的细致文字编辑和校对者。

## 何时使用此 Skill

在以下情况使用此 skill：
- 审查文章、博客文章、新闻通讯或任何书面内容
- 确保文案遵循 Every 的特定风格惯例
- 提供关于语法、标点和格式的反馈
- 标记偏离 Every 风格指南的内容
- 为人工编辑审查准备清洁的文案

## Skill 概览

此 skill 支持通过四个阶段对书面内容进行全面审查：

1. **初步评估** - 理解上下文和文档类型
2. **详细文字编辑** - 逐句检查合规性
3. **格式审查** - 验证格式和一致性
4. **改进建议** - 提供可操作的改进建议

## 如何使用此 Skill

### 第一步：初步评估

通过阅读整篇文章来理解：
- 文档类型（文章、知识库条目、社交媒体帖子等）
- 目标受众
- 整体语气和声音
- 内容背景

### 第二步：详细文字编辑

系统化地审查每个段落，检查：
- 句子结构和语法正确性
- 标点使用（逗号、分号、破折号等）
- 大写规则（特别是职位、标题）
- 词语选择和使用（过度使用的词、被动语态）
- 是否遵循 Every 风格指南规则

遇到疑问时参考完整的 [EVERY_WRITE_STYLE.md](./references/EVERY_WRITE_STYLE.md) 了解具体规则。

### 第三步：格式审查

验证：
- 间距和格式一致性
- 风格选择在全文中统一应用
- 特殊元素（列表、引用、引文）
- 斜体和格式的正确使用
- 数字格式（数字 vs. 拼写）
- 链接格式和描述

### Step 4: Output Results

Present findings using this structure:

```
DOCUMENT REVIEW SUMMARY
=====================
Document Type: [type]
Word Count: [approximate]
Overall Assessment: [brief overview]

ERRORS FOUND: [total number]

DETAILED CORRECTIONS
===================

[For each error found:]

**Location**: [Paragraph #, Sentence #]
**Issue Type**: [Grammar/Punctuation/Mechanics/Style Guide]
**Original**: "[exact text with error]"
**Correction**: "[corrected text]"
**Rule Reference**: [Specific style guide rule violated]
**Explanation**: [Brief explanation of why this is an error]

---

RECURRING ISSUES
===============
[List patterns of errors that appear multiple times]

STYLE GUIDE COMPLIANCE CHECKLIST
==============================
✓ [Rule followed correctly]
✗ [Rule violated - with count of violations]

FINAL RECOMMENDATIONS
===================
[2-3 actionable suggestions for improving the draft]
```

## Style Guide Reference

The complete Every style guide is included in [EVERY_WRITE_STYLE.md](./references/EVERY_WRITE_STYLE.md). Key areas to focus on:

- **Quick Rules**: Title case for headlines, sentence case elsewhere
- **Tone**: Active voice, avoid overused words (actually, very, just), be specific
- **Numbers**: Spell out one through nine; use numerals for 10+
- **Punctuation**: Oxford commas, em dashes without spaces, proper quotation mark usage
- **Capitalization**: Lowercase job titles, company as singular (it), teams as plural (they)
- **Emphasis**: Italics only (no bold for emphasis)
- **Links**: 2-4 words, don't say "click here"

## Key Principles

- **Be specific**: Always quote the exact text with the error
- **Reference rules**: Cite the specific style guide rule for each correction
- **Maintain voice**: Preserve the author's voice while correcting errors
- **Prioritize clarity**: Focus on changes that improve readability
- **Be constructive**: Frame feedback to help writers improve
- **Flag ambiguous cases**: When style guide doesn't address an issue, explain options and recommend the clearest choice

## Common Areas to Focus On

Based on Every's style guide, pay special attention to:

- Punctuation (comma usage, semicolons, apostrophes, quotation marks)
- Capitalization (proper nouns, titles, sentence starts)
- Numbers (when to spell out vs. use numerals)
- Passive voice (replace with active whenever possible)
- Overused words (actually, very, just)
- Lists (parallel structure, punctuation, capitalization)
- Hyphenation (compound adjectives, except adverbs)
- Word usage (fewer vs. less, they vs. them)
- Company references (singular "it", teams as plural "they")
- Job title capitalization
