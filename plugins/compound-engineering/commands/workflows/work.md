---
name: workflows:work
description: 高效执行工作计划，同时保持质量并完成功能
argument-hint: "[计划文件、规范或todo文件路径]"
---

# 工作计划执行Command

高效执行工作计划，同时保持质量并完成功能。

## 介绍

此命令接受一个工作文档（计划、规范或todo文件）并系统地执行它。重点是通过快速理解需求、遵循现有模式并在整个过程中保持质量来**交付完整的功能**。

## 输入文档

<input_document> #$ARGUMENTS </input_document>

## 执行工作流

### Phase 1: 快速启动

1. **阅读计划并澄清**

   - 完整阅读工作文档
   - 审查计划中提供的任何引用或链接
   - 如果有任何不清楚或含糊不清的地方，现在就提出澄清问题
   - 获得用户批准继续
   - **不要跳过这一步** - 现在提问比构建错误的东西更好

2. **设置环境**

   选择您的工作方式：

   **选项A：在当前分支上实时工作**
   ```bash
   git checkout main && git pull origin main
   git checkout -b feature-branch-name
   ```

   **选项B：使用worktree并行工作（推荐用于并行开发）**
   ```bash
   # 首先询问用户："使用worktree并行工作还是在当前分支上工作？"
   # 如果是worktree：
   skill: git-worktree
   # 该skill将从main在隔离的worktree中创建新分支
   ```

   **建议**：在以下情况下使用worktree：
   - 您想同时处理多个功能
   - 您想在实验时保持main干净
   - 您计划经常在分支之间切换

   在以下情况下使用实时分支：
   - 您正在处理单个功能
   - 您更喜欢留在主仓库中

3. **创建Todo列表**
   - 使用TodoWrite将计划分解为可操作的任务
   - 包含任务之间的依赖关系
   - 根据需要首先完成的内容进行优先级排序
   - 包含测试和质量检查任务
   - 保持任务具体且可完成

### Phase 2: 执行

1. **任务执行循环**

   按优先级顺序执行每个任务：

   ```
   while (tasks remain):
     - 在TodoWrite中将任务标记为in_progress
     - 从计划中读取任何引用的文件
     - 在代码库中查找类似模式
     - 遵循现有约定实施
     - 为新功能编写测试
     - 更改后运行测试
     - 将任务标记为completed
   ```

2. **遵循现有模式**

   - 计划应引用类似代码 - 首先阅读这些文件
   - 完全匹配命名约定
   - 尽可能重用现有组件
   - 遵循项目编码标准（参见CLAUDE.md）
   - 如有疑问，grep查找类似实现

3. **持续测试**

   - 每次重大更改后运行相关测试
   - 不要等到最后才测试
   - 立即修复失败
   - 为新功能添加新测试

4. **Figma设计同步**（如果适用）

   对于使用Figma设计的UI工作：

   - 按照设计规范实施组件
   - 迭代使用figma-design-sync Agent进行比较
   - 修复识别出的视觉差异
   - 重复直到实现与设计匹配

5. **跟踪进度**
   - 在完成任务时保持TodoWrite更新
   - 记录任何阻碍或意外发现
   - 如果范围扩大，创建新任务
   - 让用户了解主要里程碑

### Phase 3: 质量检查

1. **运行核心质量检查**

   提交前始终运行：

   ```bash
   # 运行完整测试套件
   bin/rails test

   # 运行linting（根据CLAUDE.md）
   # 推送到origin前使用linting-agent
   ```

2. **考虑审查者Agent**（可选）

   用于复杂、有风险或大型更改：

   - **code-simplicity-reviewer**：检查不必要的复杂性
   - **kieran-rails-reviewer**：验证Rails约定（Rails项目）
   - **performance-oracle**：检查性能问题
   - **security-sentinel**：扫描安全漏洞
   - **cora-test-reviewer**：审查测试质量（CORA项目）

   使用Task工具并行运行审查者：

   ```
   Task(code-simplicity-reviewer): "审查更改的简单性"
   Task(kieran-rails-reviewer): "检查Rails约定"
   ```

   向用户呈现发现并解决关键问题。

3. **最终验证**
   - 所有TodoWrite任务标记为completed
   - 所有测试通过
   - Linting通过
   - 代码遵循现有模式
   - Figma设计匹配（如果适用）
   - 没有控制台错误或警告

### Phase 4: 交付

1. **创建Commit**

   ```bash
   git add .
   git status  # 审查正在提交的内容
   git diff --staged  # 检查更改

   # 使用常规格式提交
   git commit -m "$(cat <<'EOF'
   feat(scope): 描述做了什么和为什么

   如有需要，简要说明。

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>
   EOF
   )"
   ```

2. **为UI更改捕获并上传截图**（任何UI工作都必需）

   对于**任何**设计更改、新视图或UI修改，您必须捕获并上传截图：

   **Step 1: 启动开发服务器**（如果尚未运行）
   ```bash
   bin/dev  # 在后台运行
   ```

   **Step 2: 使用Playwright MCP工具捕获截图**
   - `browser_navigate` 导航到受影响的页面
   - `browser_resize` 设置视口（根据需要为桌面或移动设备）
   - `browser_snapshot` 验证页面状态
   - `browser_take_screenshot` 捕获图像

   **Step 3: 使用imgup skill上传**
   ```bash
   skill: imgup
   # 然后上传每个截图：
   imgup -h pixhost screenshot.png  # pixhost无需API密钥即可工作
   # 替代托管：catbox、imagebin、beeimg
   ```

   **捕获内容：**
   - **新屏幕**：新UI的截图
   - **修改的屏幕**：之前和之后的截图
   - **设计实现**：显示Figma设计匹配的截图

   **重要**：始终在PR描述中包含上传的图像URL。这为审查者提供视觉上下文并记录更改。

3. **创建Pull Request**

   ```bash
   git push -u origin feature-branch-name

   gh pr create --title "Feature: [描述]" --body "$(cat <<'EOF'
   ## Summary
   - 构建了什么
   - 为什么需要它
   - 做出的关键决策

   ## Testing
   - 添加/修改的测试
   - 执行的手动测试

   ## Before / After Screenshots
   | Before | After |
   |--------|-------|
   | ![before](URL) | ![after](URL) |

   ## Figma Design
   [如果适用，提供链接]

   🤖 Generated with [Claude Code](https://claude.com/claude-code)
   EOF
   )"
   ```

4. **通知用户**
   - 总结完成的内容
   - 链接到PR
   - 记录任何需要的后续工作
   - 如果适用，建议下一步

---

## 关键原则

### 快速启动，更快执行

- 在开始时获得一次澄清，然后执行
- 不要等待完美的理解 - 提问并继续
- 目标是**完成功能**，而不是创建完美的流程

### 计划是您的指南

- 工作文档应引用类似的代码和模式
- 加载这些引用并遵循它们
- 不要重新发明 - 匹配现有的内容

### 边做边测试

- 每次更改后运行测试，而不是最后
- 立即修复失败
- 持续测试可防止大的意外

### 质量是内置的

- 遵循现有模式
- 为新代码编写测试
- 推送前运行linting
- 仅对复杂/有风险的更改使用审查者Agent

### 交付完整的功能

- 在继续之前标记所有任务为已完成
- 不要让功能停留在80%完成
- 交付的完成功能胜过不交付的完美功能

## 质量检查清单

创建PR前，验证：

- [ ] 所有澄清问题都已提出并回答
- [ ] 所有TodoWrite任务标记为completed
- [ ] 测试通过（运行 `bin/rails test`）
- [ ] Linting通过（使用linting-agent）
- [ ] 代码遵循现有模式
- [ ] Figma设计与实现匹配（如果适用）
- [ ] 已捕获并上传之前/之后的截图（对于UI更改）
- [ ] Commit消息遵循常规格式
- [ ] PR描述包含摘要、测试说明和截图

## 何时使用审查者Agent

**默认不使用。** 仅在以下情况下使用审查者Agent：

- 影响许多文件的大型重构（10+）
- 安全敏感的更改（身份验证、权限、数据访问）
- 性能关键的代码路径
- 复杂的算法或业务逻辑
- 用户明确请求彻底审查

对于大多数功能：测试 + linting + 遵循模式就足够了。

## 要避免的常见陷阱

- **分析瘫痪** - 不要过度思考，阅读计划并执行
- **跳过澄清问题** - 现在就问，而不是在构建错误的东西之后
- **忽略计划引用** - 计划有链接是有原因的
- **最后才测试** - 持续测试或以后受苦
- **忘记TodoWrite** - 跟踪进度或失去对已完成内容的跟踪
- **80%完成综合症** - 完成功能，不要提前继续
- **过度审查简单更改** - 为复杂工作保留审查者Agent
