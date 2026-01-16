# Workflow: 验证 Skill 内容准确性

<required_reading>
**立即阅读这些参考文件：**
1. references/skill-structure.md
</required_reading>

<purpose>
Audit 检查结构。**Verify 检查真实性。**

Skills 包含关于外部事物的声明：API、CLI 工具、框架、服务。这些会随时间变化。此 workflow 检查 skill 的内容是否仍然准确。
</purpose>

<process>
## 步骤 1：选择 Skill

```bash
ls ~/.claude/skills/
```

呈现编号列表，询问："我应该验证哪个 skill 的准确性？"

## 步骤 2：读取和分类

读取整个 skill (SKILL.md + workflows/ + references/):
```bash
cat ~/.claude/skills/{skill-name}/SKILL.md
cat ~/.claude/skills/{skill-name}/workflows/*.md 2>/dev/null
cat ~/.claude/skills/{skill-name}/references/*.md 2>/dev/null
```

按主要依赖类型分类：

| 类型 | 示例 | 验证方法 |
|------|----------|---------------------|
| **API/Service** | manage-stripe, manage-gohighlevel | Context7 + WebSearch |
| **CLI Tools** | build-macos-apps (xcodebuild, swift) | 运行命令 |
| **Framework** | build-iphone-apps (SwiftUI, UIKit) | Context7 获取文档 |
| **Integration** | setup-stripe-payments | WebFetch + Context7 |
| **Pure Process** | create-agent-skills | 无外部依赖 |

报告："此 skill 主要基于 [type]。我将使用 [method] 进行验证。"

## 步骤 3：提取可验证声明

扫描 skill 内容并提取：

**提及的 CLI 工具：**
- 工具名称 (xcodebuild, swift, npm, 等)
- 文档中的特定标志/选项
- 预期的输出模式

**API 端点：**
- 服务名称 (Stripe, Meta, 等)
- 文档中的特定端点
- 认证方法
- SDK 版本

**Framework 模式：**
- Framework 名称 (SwiftUI, React, 等)
- 文档中的特定 API/模式
- 特定版本的功能

**文件路径/结构：**
- 预期的项目结构
- 配置文件位置

呈现："发现 X 个可验证声明需要检查。"

## 步骤 4：按类型验证

### 对于 CLI 工具
```bash
# 检查工具是否存在
which {tool-name}

# 检查版本
{tool-name} --version

# 验证文档中的标志是否有效
{tool-name} --help | grep "{documented-flag}"
```

### 对于 API/Service Skills
使用 Context7 获取当前文档：
```
mcp__context7__resolve-library-id: {service-name}
mcp__context7__get-library-docs: {library-id}, topic: {relevant-topic}
```

将 skill 文档中的模式与当前文档进行比较：
- 端点是否仍然有效？
- 认证是否已更改？
- 是否使用了已弃用的方法？

### 对于 Framework Skills
使用 Context7:
```
mcp__context7__resolve-library-id: {framework-name}
mcp__context7__get-library-docs: {library-id}, topic: {specific-api}
```

检查：
- 文档中的 API 是否仍是最新的？
- 模式是否已更改？
- 是否有更新的推荐方法？

### 对于 Integration Skills
WebSearch 查找最近的更改：
```
"[service name] API changes 2025"
"[service name] breaking changes"
"[service name] deprecated endpoints"
```

然后使用 Context7 获取当前 SDK 模式。

### 对于有状态页面的服务
如果可用，WebFetch 官方文档/变更日志。

## 步骤 5：生成新鲜度报告

呈现发现：

```
## 验证报告：{skill-name}

### ✅ 已验证为最新
- [声明]: [证明其仍然准确的证据]

### ⚠️ 可能已过时
- [声明]: [什么发生了变化 / 发现的更新信息]
  → 当前：[文档现在说什么]

### ❌ 已损坏 / 无效
- [声明]: [为什么它是错误的]
  → 修复：[应该是什么]

### ℹ️ 无法验证
- [声明]: [为什么无法验证]

---
**整体状态：** [新鲜 / 需要更新 / 严重过时]
**最后验证：** [今天的日期]
```

## 步骤 6：提供更新

如果发现问题：

"发现 [N] 项需要更新。您希望我："

1. **全部更新** - 应用所有更正
2. **逐项审查** - 在应用前显示每个更改
3. **仅报告** - 不进行更改

如果更新：
- 基于验证的当前信息进行更改
- 如适当，添加验证日期注释
- 报告更新的内容

## 步骤 7：建议验证时间表

根据 skill 类型，推荐：

| Skill 类型 | 推荐频率 |
|------------|----------------------|
| API/Service | 每 1-2 个月 |
| Framework | 每 3-6 个月 |
| CLI Tools | 每 6 个月 |
| Pure Process | 每年 |

"此 skill 应在大约 [时间范围] 内重新验证。"
</process>

<verification_shortcuts>
## 快速验证命令

**检查 CLI 工具是否存在并获取版本：**
```bash
which {tool} && {tool} --version
```

**Context7 模式用于任何库：**
```
1. resolve-library-id: "{library-name}"
2. get-library-docs: "{id}", topic: "{specific-feature}"
```

**WebSearch 模式：**
- 破坏性更改："{service} breaking changes 2025"
- 弃用："{service} deprecated API"
- 当前最佳实践："{framework} best practices 2025"
</verification_shortcuts>

<success_criteria>
验证完成的标准：
- [ ] Skill 按依赖类型分类
- [ ] 可验证声明已提取
- [ ] 每个声明使用适当方法检查
- [ ] 新鲜度报告已生成
- [ ] 更新已应用（如请求）
- [ ] 用户知道何时重新验证
</success_criteria>
