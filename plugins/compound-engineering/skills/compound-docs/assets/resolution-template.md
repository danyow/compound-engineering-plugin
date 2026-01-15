---
module: [模块名称或系统级使用 "CORA"]
date: [YYYY-MM-DD]
problem_type: [build_error|test_failure|runtime_error|performance_issue|database_issue|security_issue|ui_bug|integration_issue|logic_error]
component: [rails_model|rails_controller|rails_view|service_object|background_job|database|frontend_stimulus|hotwire_turbo|email_processing|brief_system|assistant|authentication|payments]
symptoms:
  - [可观察症状 1 - 具体的错误消息或行为]
  - [可观察症状 2 - 用户实际看到/经历的情况]
root_cause: [missing_association|missing_include|missing_index|wrong_api|scope_issue|thread_violation|async_timing|memory_leak|config_error|logic_error|test_isolation|missing_validation|missing_permission]
rails_version: [7.1.2 - 可选]
resolution_type: [code_fix|migration|config_change|test_fix|dependency_update|environment_setup]
severity: [critical|high|medium|low]
tags: [keyword1, keyword2, keyword3]
---

# 故障排查：[清晰的问题标题]

## 问题描述
[用 1-2 句话清楚描述问题以及用户遇到的情况]

## 环境信息
- 模块：[名称或 "CORA system"]
- Rails 版本：[例如 7.1.2]
- 受影响的组件：[例如 "Email Processing model"、"Brief System service"、"Authentication controller"]
- 日期：[问题解决的日期 YYYY-MM-DD]

## 症状表现
- [可观察症状 1 - 用户看到/经历的情况]
- [可观察症状 2 - 错误消息、视觉问题、意外行为]
- [根据需要继续补充 - 尽可能具体]

## 无效的尝试

**尝试方案 1：**[描述尝试的内容]
- **失败原因：**[该方案未能解决问题的技术原因]

**尝试方案 2：**[描述第二次尝试]
- **失败原因：**[技术原因]

[继续列出所有未成功的重要尝试]

[如果没有其他尝试，写：]
**直接解决：**问题在第一次尝试时就被识别并修复了。

## 解决方案

[实际有效的修复方法 - 提供具体细节]

**代码更改**（如适用）：
```ruby
# 修复前（有问题）：
[展示有问题的代码]

# 修复后（已修复）：
[展示修正后的代码并附上说明]
```

**数据库迁移**（如适用）：
```ruby
# 迁移变更：
[展示迁移中的更改内容]
```

**执行的命令**（如适用）：
```bash
# 修复步骤：
[命令或操作]
```

## 原理说明

[技术解释：]
1. 问题的根本原因是什么？
2. 为什么该解决方案能够解决根本原因？
3. 底层问题是什么（API 误用、配置错误、Rails 版本问题等）？

[提供足够详细的说明，让未来的开发者理解"为什么"，而不仅仅是"是什么"]

## 预防措施

[如何在未来的 CORA 开发中避免此问题：]
- [具体的编码实践、检查或需要遵循的模式]
- [需要注意的事项]
- [如何及早发现此问题]

## 相关问题

[如果 docs/solutions/ 中存在类似问题，链接到它们：]
- 另见：[another-related-issue.md](../category/another-related-issue.md)
- 类似问题：[related-problem.md](../category/related-problem.md)

[如果没有相关问题，写：]
暂无相关问题文档。
