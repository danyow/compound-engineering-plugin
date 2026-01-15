# 更新日志

compound-engineering Plugin 的所有重要更改都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)，
此项目遵循 [Semantic Versioning](https://semver.org/spec/v2.0.0.html)。

## [2.23.2] - 2026-01-09

### 更改

- **`/reproduce-bug` Command** - 使用 Playwright 可视化重现功能增强：
  - 添加第 2 阶段：使用浏览器自动化进行可视化 bug 重现
  - 导航到受影响区域的分步指南
  - 在每个重现步骤捕获屏幕截图
  - Console 错误检查
  - 使用点击、输入和快照重现用户流程
  - 包含 4 个清晰阶段的更好文档结构

### 摘要

- 27 个 Agent，21 个 Command，13 个 Skill，2 个 MCP Server

---

## [2.23.1] - 2026-01-08

### 更改

- **Agent 模型继承** - 所有 26 个 Agent 现在使用 `model: inherit`，因此它们与用户配置的模型匹配。只有 `lint` 保持 `model: haiku` 以提高成本效率。（修复 #69）

### 摘要

- 27 个 Agent，21 个 Command，13 个 Skill，2 个 MCP Server

---

## [2.23.0] - 2026-01-08

### 新增

- **`/agent-native-audit` Command** - 全面的 agent-native 架构审查
  - 启动 8 个并行子 Agent，每个核心原则一个
  - 原则：Action Parity、Tools as Primitives、Context Injection、Shared Workspace、CRUD Completeness、UI Integration、Capability Discovery、Prompt-Native Features
  - 每个 Agent 生成特定分数（X/Y 格式，带百分比）
  - 生成带有总分和前 10 项建议的摘要报告
  - 通过参数支持单个原则审计

### 摘要

- 27 个 Agent，21 个 Command，13 个 Skill，2 个 MCP Server

---

## [2.22.0] - 2026-01-05

### 新增

- **`rclone` Skill** - 将文件上传到 S3、Cloudflare R2、Backblaze B2 和其他云存储提供商

### 更改

- **`/feature-video` Command** - 增强功能：
  - 更好的 ffmpeg 命令用于视频/GIF 创建（适当的缩放、帧率控制）
  - rclone 集成用于云上传
  - 将屏幕截图复制到项目文件夹
  - 改进的上传选项工作流

### 摘要

- 27 个 Agent，20 个 Command，13 个 Skill，2 个 MCP Server

---

## [2.21.0] - 2026-01-05

### 修复

- 合并冲突解决后的版本历史清理

### 摘要

此版本整合了所有最近的工作：
- `/feature-video` Command 用于录制 PR 演示
- `/deepen-plan` Command 用于增强规划
- `create-agent-skills` Skill 重写（符合官方规范）
- `agent-native-architecture` Skill 大幅扩展
- `dhh-rails-style` Skill 整合（合并 dhh-ruby-style）
- 27 个 Agent，20 个 Command，12 个 Skill，2 个 MCP Server

---

## [2.20.0] - 2026-01-05

### 新增

- **`/feature-video` Command** - 使用 Playwright 录制功能演示视频

### 更改

- **`create-agent-skills` Skill** - 完全重写以匹配 Anthropic 的官方 Skill 规范

### 移除

- **`dhh-ruby-style` Skill** - 合并到 `dhh-rails-style` Skill

---

## [2.19.0] - 2025-12-31

### 新增

- **`/deepen-plan` Command** - 计划的强力增强。接受现有计划并为每个主要部分运行并行研究子 Agent 以添加：
  - 最佳实践和行业模式
  - 性能优化
  - UI/UX 改进（如适用）
  - 质量增强和边缘情况
  - 实际实施示例

  结果是一个深入基础的、生产就绪的计划，具有具体的实施细节。

### 更改

- **`/workflows:plan` Command** - 在生成后菜单中添加 `/deepen-plan` 作为选项 2。添加说明：如果启用 ultrathink 运行，自动运行 deepen-plan 以获得最大深度。

## [2.18.0] - 2025-12-25

### 新增

- **`agent-native-architecture` Skill** - 添加**动态能力发现**模式和**架构审查清单**：

  **mcp-tool-design.md 中的新模式：**
  - **动态能力发现** - 对于外部 API（HealthKit、HomeKit、GraphQL），构建一个发现工具（`list_*`），在运行时返回可用功能，加上一个接受字符串（非枚举）的通用访问工具。API 验证，而不是您的代码。这意味着 Agent 可以在不更改代码的情况下使用新的 API 功能。
  - **CRUD 完整性** - Agent 可以创建的每个实体也必须是可读、可更新和可删除的。不完整的 CRUD = 破坏的 action parity。

  **SKILL.md 中的新内容：**
  - **架构审查清单** - 将审查者的发现更早地推入设计阶段。涵盖工具设计（动态与静态、CRUD 完整性）、action parity（能力图、编辑/删除）、UI 集成（Agent → UI 通信）和上下文注入。
  - **选项 11：API 集成** - 用于连接外部 API（如 HealthKit、HomeKit、GraphQL）的新接收选项
  - **新反模式：** 静态工具映射（为每个 API 端点构建单独的工具）、不完整的 CRUD（仅创建工具）
  - **工具设计标准**部分添加到成功标准检查清单

  **shared-workspace-architecture.md 中的新内容：**
  - **用于多设备同步的 iCloud 文件存储** - 对共享工作区使用 iCloud Documents 以获得免费、自动的多设备同步，而无需构建同步层。包括实施模式、冲突处理、权限和何时不使用它。

### 理念

此更新编纂了**agent-native 应用**的关键见解：当集成外部 API 时，Agent 应该拥有与用户相同的访问权限，使用**动态能力发现**而不是静态工具映射。不要构建 `read_steps`、`read_heart_rate`、`read_sleep`...而是构建 `list_health_types` + `read_health_data(dataType: string)`。Agent 发现可用内容，API 验证类型。

注意：此模式专门用于遵循"用户可以做什么，Agent 就可以做什么"理念的 agent-native 应用。对于具有故意限制功能的受约束 Agent，静态工具映射可能是合适的。

---

## [2.17.0] - 2025-12-25

### 增强

- **`agent-native-architecture` Skill** - 基于构建 Every Reader iOS 应用的实际经验进行重大扩展。添加了 5 个新的参考文档并扩展了现有文档：

  **新参考文档：**
  - **dynamic-context-injection.md** - 如何将运行时应用状态注入 Agent 系统提示。涵盖上下文注入模式、要注入什么上下文（资源、活动、功能、词汇）、Swift/iOS 和 TypeScript 的实施模式以及上下文新鲜度。
  - **action-parity-discipline.md** - 确保 Agent 可以执行用户可以执行的所有操作的工作流。包括能力映射模板、对等审计流程、PR 检查清单、对等的工具设计和上下文对等指南。
  - **shared-workspace-architecture.md** - Agent 和用户在同一数据空间中工作的模式。涵盖目录结构、文件工具、UI 集成（文件监视、共享存储）、Agent-用户协作模式和安全考虑。
  - **agent-native-testing.md** - agent-native 应用的测试模式。包括"Agent 能做到吗？"测试、惊喜测试、自动化对等测试、集成测试和 CI/CD 集成。
  - **mobile-patterns.md** - iOS/Android 的移动特定模式。涵盖后台执行（检查点/恢复）、权限处理、成本感知设计（模型层、token 预算、网络感知）、离线处理和电池感知。

  **更新的参考文档：**
  - **architecture-patterns.md** - 添加了 3 个新模式：统一 Agent 架构（一个编排器，多个 Agent 类型）、Agent 到 UI 通信（共享数据存储、文件监视、事件总线）和模型层选择（快速/平衡/强大）。

  **更新的 Skill 根目录：**
  - **SKILL.md** - 扩展的接收菜单（现在有 10 个选项，包括上下文注入、action parity、共享工作区、测试、移动模式）。添加了 5 个新的 agent-native 反模式（上下文饥饿、孤立功能、沙盒隔离、静默操作、能力隐藏）。扩展了包含 agent-native 和移动特定检查清单的成功标准。

- **`agent-native-reviewer` Agent** - 通过涵盖所有新模式的综合审查流程显著增强。现在检查 action parity、上下文对等、共享工作区、工具设计（原语与工作流）、动态上下文注入和移动特定问题。包括详细的反模式、输出格式模板、快速检查（"写入位置"测试、惊喜测试）和移动特定验证。

### 理念

这些更新将构建 agent-native 移动应用的关键见解操作化：**"Agent 应该能够通过镜像 UI 功能的工具执行用户可以执行的任何操作，并完全了解应用状态的上下文。"** 促使这些更改的失败案例：当用户说"在我的阅读提要中写点东西"时，Agent 问"什么阅读提要？" - 因为它没有 `publish_to_feed` 工具，也没有关于"提要"含义的上下文。

## [2.16.0] - 2025-12-21

### 增强

- **`dhh-rails-style` Skill** - 大幅扩展参考文档，纳入来自 Marc Köhlbrugge 的非官方 37signals 编码风格指南的模式：
  - **controllers.md** - 添加授权模式、速率限制、Sec-Fetch-Site CSRF 保护、请求上下文 concern
  - **models.md** - 添加验证理念、让它崩溃理念（bang 方法）、带 lambda 的默认值、Rails 7.1+ 模式（normalizes、delegated types、store accessor）、带 touch 链的 concern 指南
  - **frontend.md** - 添加 Turbo morphing 最佳实践、Turbo frames 模式、6 个新 Stimulus Controller（auto-submit、dialog、local-time 等）、Stimulus 最佳实践、view helper、带个性化的缓存、broadcasting 模式
  - **architecture.md** - 添加基于路径的多租户、数据库模式（UUID、状态作为记录、硬删除、计数器缓存）、后台作业模式（事务安全、错误处理、批处理）、电子邮件模式、安全模式（XSS、SSRF、CSP）、Active Storage 模式
  - **gems.md** - 添加扩展的他们避免的内容部分（service object、form object、decorator、CSS 预处理器、React/Vue）、使用 Minitest/fixtures 模式的测试理念

### 致谢

- 参考模式源自 [Marc Köhlbrugge 的非官方 37signals 编码风格指南](https://github.com/marckohlbrugge/unofficial-37signals-coding-style-guide)

## [2.15.2] - 2025-12-21

### 修复

- **所有 Skill** - 修复 12 个 Skill 的规范合规性问题：
  - 参考文件现在使用正确的 markdown 链接（`[file.md](./references/file.md)`）而不是反引号文本
  - 描述现在使用第三人称（"This skill should be used when..."）符合 skill-creator 规范
  - 受影响的 Skill：agent-native-architecture、andrew-kane-gem-writer、compound-docs、create-agent-skills、dhh-rails-style、dspy-ruby、every-style-editor、file-todos、frontend-design、gemini-imagegen

### 新增

- **CLAUDE.md** - 添加 Skill 合规检查清单，包含用于确保新 Skill 满足规范要求的验证命令

## [2.15.1] - 2025-12-18

### 更改

- **`/workflows:review` Command** - 第 7 部分现在检测项目类型（Web、iOS 或 Hybrid）并提供适当的测试。Web 项目获得 `/playwright-test`，iOS 项目获得 `/xcode-test`，hybrid 项目可以运行两者。

## [2.15.0] - 2025-12-18

### 新增

- **`/xcode-test` Command** - 使用 XcodeBuildMCP 在模拟器上构建和测试 iOS 应用。自动检测 Xcode 项目、构建应用、启动模拟器并运行测试套件。包括针对不稳定测试的重试。

- **`/playwright-test` Command** - 在当前 PR 或分支影响的页面上运行 Playwright 浏览器测试。检测更改的文件、映射到受影响的路由、生成/运行目标测试，并报告带有屏幕截图的结果。
