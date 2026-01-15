# Workflow：创建详尽的领域专业知识 Skill

<objective>
构建一个在特定领域执行实际工作的综合执行 skill。领域专业知识 skill 是功能齐全的构建 skill，reference 中包含详尽的领域知识，涵盖完整生命周期的完整 workflow（build → debug → optimize → ship），既可以由用户直接调用，也可以由其他 skill（如 create-plans）加载以获取领域知识。
</objective>

<critical_distinction>
**常规 skill：**"执行一个特定任务"
**领域专业知识 skill：**"在这个领域执行所有事情，具备完整的从业者知识"

示例：
- `expertise/macos-apps` - 从头构建 macOS 应用程序到发布
- `expertise/python-games` - 构建完整的 Python 游戏与完整的游戏开发生命周期
- `expertise/rust-systems` - 构建 Rust 系统程序，具备详尽的系统知识
- `expertise/web-scraping` - 构建爬虫、处理所有边缘情况、大规模部署

领域专业知识 skill：
- ✅ 执行任务（build、debug、optimize、ship）
- ✅ reference 中有全面的领域知识
- ✅ 由用户直接调用（"构建一个 macOS 应用"）
- ✅ 可以被其他 skill 加载（create-plans 读取 reference 进行规划）
- ✅ 涵盖完整的生命周期，不仅仅是入门
</critical_distinction>

<required_reading>
**立即阅读这些参考文件：**
1. references/recommended-structure.md
2. references/core-principles.md
3. references/use-xml-tags.md
</required_reading>

<process>
## 步骤 1：识别领域

询问用户要构建什么领域专业知识：

**示例领域：**
- macOS/iOS 应用开发
- Python 游戏开发
- Rust 系统编程
- 机器学习 / AI
- Web 爬虫和自动化
- 数据工程管道
- 音频处理 / DSP
- 3D 图形 / 着色器
- Unity/Unreal 游戏开发
- 嵌入式系统

具体化："Python 游戏"还是"专门使用 Pygame 的 Python 游戏"？

## 步骤 2：确认目标位置

解释：
```
领域专业知识 skill 放在：~/.claude/skills/expertise/{domain-name}/

这些是综合的构建 skill，它们：
- 执行任务（build、debug、optimize、ship）
- 包含详尽的领域知识
- 可以由用户直接调用
- 可以被其他 skill 加载以获取领域知识

名称建议：{suggested-name}
位置：~/.claude/skills/expertise/{suggested-name}/
```

确认或调整名称。

## 步骤 3：识别 Workflow

领域专业知识 skill 涵盖完整的生命周期。识别需要哪些 workflow。

**大多数领域的常见 workflow：**
1. **build-new-{thing}.md** - 从头创建
2. **add-feature.md** - 扩展现有的 {thing}
3. **debug-{thing}.md** - 查找和修复错误
4. **write-tests.md** - 测试正确性
5. **optimize-performance.md** - 分析和加速
6. **ship-{thing}.md** - 部署/分发

**特定领域的 workflow：**
- 游戏：`implement-game-mechanic.md`、`add-audio.md`、`polish-ui.md`
- Web 应用：`setup-auth.md`、`add-api-endpoint.md`、`setup-database.md`
- 系统：`optimize-memory.md`、`profile-cpu.md`、`cross-compile.md`

每个 workflow = 用户实际执行的一种完整任务类型。

## 步骤 4：详尽的研究阶段

**关键：**此研究必须全面，而不是肤浅的。

### 研究策略

运行多次 web 搜索以确保覆盖：

**搜索 1：当前生态系统**
- "best {domain} libraries 2024 2025"
- "popular {domain} frameworks comparison"
- "{domain} tech stack recommendations"

**搜索 2：架构模式**
- "{domain} architecture patterns"
- "{domain} best practices design patterns"
- "how to structure {domain} projects"

**搜索 3：生命周期和工具**
- "{domain} development workflow"
- "{domain} testing debugging best practices"
- "{domain} deployment distribution"

**搜索 4：常见陷阱**
- "{domain} common mistakes avoid"
- "{domain} anti-patterns"
- "what not to do {domain}"

**搜索 5：实际使用**
- "{domain} production examples GitHub"
- "{domain} case studies"
- "successful {domain} projects"

### 验证要求

对于找到的每个主要库/工具/模式：
- **检查时效性：**最后一次更新是什么时候？
- **检查采用情况：**是否积极维护？社区规模？
- **检查替代方案：**还有什么存在？何时使用每个？
- **检查弃用：**是否有东西正在被替换？

**过时内容的危险信号：**
- 2023 年之前的文章（除非是基本概念）
- 废弃的库（12 个月以上没有提交）
- 已弃用的 API 或模式
- "这曾经很流行，但是..."

### 文档来源

在可用时使用 Context7 MCP：
```
mcp__context7__resolve-library-id: {library-name}
mcp__context7__get-library-docs: {library-id}
```

专注于官方文档，而不是教程。

## 步骤 5：将知识组织到领域区域

按领域关注点构建 reference，而不是按任意类别。

**游戏开发示例：**
```
references/
├── architecture.md         # ECS、基于组件、状态机
├── libraries.md           # Pygame、Arcade、Panda3D（何时使用每个）
├── graphics-rendering.md  # 2D/3D 渲染、精灵、着色器
├── physics.md             # 碰撞、物理引擎
├── audio.md               # 音效、音乐、空间音频
├── input.md               # 键盘、鼠标、游戏手柄、触摸
├── ui-menus.md            # HUD、菜单、对话框
├── game-loop.md           # 更新/渲染循环、固定时间步长
├── state-management.md    # 游戏状态、场景管理
├── networking.md          # 多人游戏、客户端-服务器、P2P
├── asset-pipeline.md      # 加载、缓存、优化
├── testing-debugging.md   # 单元测试、分析、调试工具
├── performance.md         # 优化、分析、基准测试
├── packaging.md           # 构建可执行文件、安装程序
├── distribution.md        # Steam、itch.io、应用商店
└── anti-patterns.md       # 常见错误、不应该做的事情
```

**macOS 应用开发示例：**
```
references/
├── app-architecture.md     # 状态管理、依赖注入
├── swiftui-patterns.md     # 声明式 UI 模式
├── appkit-integration.md   # 将 AppKit 与 SwiftUI 一起使用
├── concurrency-patterns.md # Async/await、actor、结构化并发
├── data-persistence.md     # 存储策略
├── networking.md           # URLSession、异步网络
├── system-apis.md          # macOS 特定的 framework
├── testing-tdd.md          # 测试模式
├── testing-debugging.md    # 调试工具和技术
├── performance.md          # 分析、优化
├── design-system.md        # 平台约定
├── macos-polish.md         # 原生感觉、可访问性
├── security-code-signing.md # 签名、公证
└── project-scaffolding.md  # 基于 CLI 的设置
```

**对于每个 reference 文件：**
- 纯 XML 结构
- 决策树："如果 X，使用 Y。如果 Z，使用 A。"
- 比较表：库 vs 库（速度、功能、学习曲线）
- 显示模式的代码示例
- "何时使用"指导
- 平台特定的考虑因素
- 当前版本和兼容性

## 步骤 6：创建 SKILL.md

领域专业知识 skill 使用带有 essential principles 的 router 模式：

```yaml
---
name: build-{domain-name}
description: 从头构建 {domain things} 到发布。完整生命周期 - build、debug、test、optimize、ship。{任何特定约束，如"仅 CLI，无 IDE"}。
---

<essential_principles>
## {此领域} 如何工作

{始终适用的特定领域原则}

### 1. {第一个原则}
{不能跳过的关键实践}

### 2. {第二个原则}
{另一个基本实践}

### 3. {第三个原则}
{核心 workflow 模式}
</essential_principles>

<intake>
**询问用户：**

您想做什么？
1. 构建新的 {thing}
2. 调试现有的 {thing}
3. 添加功能
4. 编写/运行测试
5. 优化性能
6. 发布/发行
7. 其他

**然后从 `workflows/` 读取匹配的 workflow 并遵循它。**
</intake>

<routing>
| 响应 | Workflow |
|----------|----------|
| 1, "new", "create", "build", "start" | `workflows/build-new-{thing}.md` |
| 2, "broken", "fix", "debug", "crash", "bug" | `workflows/debug-{thing}.md` |
| 3, "add", "feature", "implement", "change" | `workflows/add-feature.md` |
| 4, "test", "tests", "TDD", "coverage" | `workflows/write-tests.md` |
| 5, "slow", "optimize", "performance", "fast" | `workflows/optimize-performance.md` |
| 6, "ship", "release", "deploy", "publish" | `workflows/ship-{thing}.md` |
| 7, other | 澄清，然后选择 workflow 或 reference |
</routing>

<verification_loop>
## 每次更改后

{特定领域的验证步骤}

编译语言的示例：
```bash
# 1. 它能构建吗？
{build command}

# 2. 测试通过了吗？
{test command}

# 3. 它能运行吗？
{run command}
```

向用户报告：
- "Build: ✓"
- "Tests: X pass, Y fail"
- "Ready for you to check [specific thing]"
</verification_loop>

<reference_index>
## 领域知识

全部在 `references/` 中：

**架构：** {list files}
**{领域区域}：** {list files}
**{领域区域}：** {list files}
**开发：** {list files}
**发布：** {list files}
</reference_index>

<workflows_index>
## Workflows

全部在 `workflows/` 中：

| 文件 | 用途 |
|------|---------|
| build-new-{thing}.md | 从头创建新的 {thing} |
| debug-{thing}.md | 查找和修复错误 |
| add-feature.md | 添加到现有的 {thing} |
| write-tests.md | 编写和运行测试 |
| optimize-performance.md | 分析和加速 |
| ship-{thing}.md | 部署/分发 |
</workflows_index>
```

## 步骤 7：编写 Workflow

对于步骤 3 中确定的每个 workflow：

### Workflow 模板

```markdown
# Workflow：{Workflow 名称}

<required_reading>
**在 {执行任务} 之前立即阅读这些参考文件：**
1. references/{relevant-file}.md
2. references/{another-relevant-file}.md
3. references/{third-relevant-file}.md
</required_reading>

<process>
## 步骤 1：{第一个操作}

{要做什么}

## 步骤 2：{第二个操作}

{要做什么 - 实际的实施步骤}

## 步骤 3：{第三个操作}

{要做什么}

## 步骤 4：验证

{如何证明它有效}

```bash
{verification commands}
```
</process>

<anti_patterns>
避免：
- {常见错误 1}
- {常见错误 2}
- {常见错误 3}
</anti_patterns>

<success_criteria>
一个完成良好的 {completed task}：
- {标准 1}
- {标准 2}
- {标准 3}
- 构建/运行没有错误
- 测试通过
- 感觉 {native/professional/correct}
</success_criteria>
```

**关键 workflow 特征：**
- 从 required_reading 开始（加载哪些 reference）
- 包含实际的实施步骤（不仅仅是"阅读 reference"）
- 包括验证步骤
- 有成功标准
- 记录反模式

## 步骤 8：编写全面的 Reference

对于步骤 5 中确定的每个 reference 文件：

### 结构模板

```xml
<overview>
此领域区域的简要介绍
</overview>

<options>
## 可用的方法/库

<option name="Library A">
**何时使用：** [特定场景]
**优势：** [最擅长的地方]
**劣势：** [不适合的地方]
**当前状态：** v{version}，积极维护
**学习曲线：** [easy/medium/hard]

```code
# 示例用法
```
</option>

<option name="Library B">
[相同结构]
</option>
</options>

<decision_tree>
## 选择正确的方法

**如果您需要 [X]：** 使用 [Library A]
**如果您需要 [Y]：** 使用 [Library B]
**如果您有 [约束 Z]：** 使用 [Library C]

**避免 [Library D] 如果：** [特定场景]
</decision_tree>

<patterns>
## 常见模式

<pattern name="Pattern Name">
**何时使用：** [场景]
**实施：** [代码示例]
**考虑因素：** [权衡]
</pattern>
</patterns>

<anti_patterns>
## 不应该做的事情

<anti_pattern name="Common Mistake">
**问题：** [人们做错的地方]
**为什么不好：** [后果]
**相反：** [正确的方法]
</anti_pattern>
</anti_patterns>

<platform_considerations>
## 平台特定说明

**Windows：** [考虑因素]
**macOS：** [考虑因素]
**Linux：** [考虑因素]
**Mobile：** [如果适用]
</platform_considerations>
```

### 质量标准

每个 reference 必须包括：
- **当前信息**（验证日期）
- **多个选项**（不仅仅是一个库）
- **决策指导**（何时使用每个）
- **真实示例**（工作代码，而不是伪代码）
- **权衡**（没有银弹）
- **反模式**（不应该做的事情）

### 常见 Reference 文件

大多数领域需要：
- **architecture.md** - 如何构建项目
- **libraries.md** - 生态系统概述与比较
- **patterns.md** - 特定领域的设计模式
- **testing-debugging.md** - 如何验证正确性
- **performance.md** - 优化策略
- **deployment.md** - 如何发布/分发
- **anti-patterns.md** - 常见错误汇总

## 步骤 9：验证完整性

### 完整性检查清单

询问："用户能否仅使用此 skill 从头构建专业的 {domain thing} 到发布？"

**必须回答"是"：**
- [ ] 涵盖所有主要库/framework？
- [ ] 记录所有架构方法？
- [ ] 解决完整生命周期（build → debug → test → optimize → ship）？
- [ ] 包括平台特定的考虑因素？
- [ ] 提供"何时使用 X vs Y"指导？
- [ ] 记录常见陷阱？
- [ ] 截至 2024-2025 是最新的？
- [ ] Workflow 实际执行任务（不仅仅是引用知识）？
- [ ] 每个 workflow 指定要读取哪些 reference？

**要检查的特定差距：**
- [ ] 涵盖测试策略？
- [ ] 列出调试/分析工具？
- [ ] 记录部署/分发方法？
- [ ] 解决性能优化？
- [ ] 安全考虑（如果适用）？
- [ ] 资产/资源管理（如果适用）？
- [ ] 网络（如果适用）？

### 双重用途测试

测试两个用例：

**直接调用：**"用户能否调用此 skill 并构建某些东西？"
- Intake 路由到适当的 workflow
- Workflow 加载相关 reference
- Workflow 提供实施步骤
- 成功标准清晰

**知识引用：**"create-plans 能否加载 reference 来规划项目？"
- Reference 包含决策指导
- 比较所有选项
- 涵盖完整生命周期
- 记录架构模式

## 步骤 10：创建目录和文件

```bash
# 创建结构
mkdir -p ~/.claude/skills/expertise/{domain-name}
mkdir -p ~/.claude/skills/expertise/{domain-name}/workflows
mkdir -p ~/.claude/skills/expertise/{domain-name}/references

# 编写 SKILL.md
# 编写所有 workflow 文件
# 编写所有 reference 文件

# 验证结构
ls -R ~/.claude/skills/expertise/{domain-name}
```

## 步骤 11：在 create-plans 中记录

更新 `~/.claude/skills/create-plans/SKILL.md` 以引用此新领域：

添加到领域推断表：
```markdown
| "{keyword}", "{domain term}" | expertise/{domain-name} |
```

这样 create-plans 可以自动检测并提供加载它。

## 步骤 12：最终质量检查

审查整个 skill：

**SKILL.md：**
- [ ] 名称与目录匹配（build-{domain-name}）
- [ ] 描述解释它从头构建到发布
- [ ] Essential principles 内联（始终加载）
- [ ] Intake 询问用户想做什么
- [ ] Routing 映射到 workflow
- [ ] Reference 索引完整且有组织
- [ ] Workflow 索引完整

**Workflows：**
- [ ] 每个 workflow 都从 required_reading 开始
- [ ] 每个 workflow 都有实际的实施步骤
- [ ] 每个 workflow 都有验证步骤
- [ ] 每个 workflow 都有成功标准
- [ ] Workflow 涵盖完整生命周期（build、debug、test、optimize、ship）

**References：**
- [ ] 纯 XML 结构（没有 markdown 标题）
- [ ] 每个文件中的决策指导
- [ ] 验证当前版本
- [ ] 代码示例有效
- [ ] 记录反模式
- [ ] 包括平台考虑因素

**完整性：**
- [ ] 专业从业者会发现这很全面
- [ ] 没有遗漏主要库/模式
- [ ] 涵盖完整生命周期
- [ ] 通过"从头构建到发布"测试
- [ ] 可以由用户直接调用
- [ ] 可以被 create-plans 加载以获取知识

</process>

<success_criteria>
领域专业知识 skill 在以下情况下完成：

- [ ] 完成全面研究（5 次以上 web 搜索）
- [ ] 验证所有来源的时效性（2024-2025）
- [ ] 按领域区域组织知识（不是任意的）
- [ ] SKILL.md 中的 Essential principles（始终加载）
- [ ] Intake 路由到适当的 workflow
- [ ] 每个 workflow 都有 required_reading + 实施步骤 + 验证
- [ ] 每个 reference 都有决策树和比较
- [ ] 全面记录反模式
- [ ] 涵盖完整生命周期（build → debug → test → optimize → ship）
- [ ] 包括平台特定的考虑因素
- [ ] 位于 ~/.claude/skills/expertise/{domain-name}/
- [ ] 在 create-plans 领域推断表中引用
- [ ] 通过双重用途测试：可以直接调用和加载知识
- [ ] 用户可以从头构建专业的东西到发布
</success_criteria>

<anti_patterns>
**不要：**
- 复制教程内容而不验证
- 仅包括"入门"材料
- 跳过"何时不使用"指导
- 忘记检查库是否仍在维护
- 按文档类型而不是领域关注点组织
- 使其仅包含知识而没有执行 workflow
- 跳过 workflow 中的验证步骤
- 包括来自旧博客文章的过时内容
- 跳过决策树和比较
- 创建只说"阅读 reference"的 workflow

**要：**
- 验证一切都是最新的
- 包括完整生命周期（build → ship）
- 提供决策指导
- 记录反模式
- 使 workflow 执行实际任务
- 从 required_reading 开始 workflow
- 在每个 workflow 中包含验证
- 使其详尽，而不是最小化
- 测试直接调用和知识引用用例
</anti_patterns>
