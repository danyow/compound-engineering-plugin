# Compounding Engineering Plugin（复合工程 Plugin）

AI 驱动的开发工具，每次使用都会变得更智能。让每一个工程工作单元都比上一个更容易。

## 组件

| Component | Count |
|-----------|-------|
| Agents | 27 |
| Commands | 20 |
| Skills | 13 |
| MCP Servers | 2 |

## Agent

Agent 按类别组织，便于发现。

### Review (14)

| Agent | Description |
|-------|-------------|
| `agent-native-reviewer` | 验证功能是否为 agent-native（action + context parity） |
| `architecture-strategist` | 分析架构决策和合规性 |
| `code-simplicity-reviewer` | 简洁性和极简主义的最终审查 |
| `data-integrity-guardian` | 数据库迁移和数据完整性 |
| `data-migration-expert` | 验证 ID 映射是否匹配生产环境，检查交换的值 |
| `deployment-verification-agent` | 为有风险的数据更改创建 Go/No-Go 部署清单 |
| `dhh-rails-reviewer` | 从 DHH 的角度审查 Rails |
| `kieran-rails-reviewer` | 使用严格约定的 Rails 代码审查 |
| `kieran-python-reviewer` | 使用严格约定的 Python 代码审查 |
| `kieran-typescript-reviewer` | 使用严格约定的 TypeScript 代码审查 |
| `pattern-recognition-specialist` | 分析代码模式和反模式 |
| `performance-oracle` | 性能分析和优化 |
| `security-sentinel` | 安全审计和漏洞评估 |
| `julik-frontend-races-reviewer` | 审查 JavaScript/Stimulus 代码的竞态条件 |

### Research (4)

| Agent | Description |
|-------|-------------|
| `best-practices-researcher` | 收集外部最佳实践和示例 |
| `framework-docs-researcher` | 研究框架文档和最佳实践 |
| `git-history-analyzer` | 分析 git 历史和代码演变 |
| `repo-research-analyst` | 研究仓库结构和约定 |

### Design (3)

| Agent | Description |
|-------|-------------|
| `design-implementation-reviewer` | 验证 UI 实现是否匹配 Figma 设计 |
| `design-iterator` | 通过系统化的设计迭代来迭代改进 UI |
| `figma-design-sync` | 将 Web 实现与 Figma 设计同步 |

### Workflow (5)

| Agent | Description |
|-------|-------------|
| `bug-reproduction-validator` | 系统化地重现和验证 bug 报告 |
| `every-style-editor` | 编辑内容以符合 Every 的风格指南 |
| `lint` | 在 Ruby 和 ERB 文件上运行 linting 和代码质量检查 |
| `pr-comment-resolver` | 处理 PR 评论并实现修复 |
| `spec-flow-analyzer` | 分析用户流程并识别规范中的差距 |

### Docs (1)

| Agent | Description |
|-------|-------------|
| `ankane-readme-writer` | 按照 Ankane 风格模板为 Ruby gem 创建 README |

## Command

### Workflow Commands

核心工作流 Command 使用 `workflows:` 前缀以避免与内置 Command 冲突：

| Command | Description |
|---------|-------------|
| `/workflows:plan` | 创建实施计划 |
| `/workflows:review` | 运行全面的代码审查 |
| `/workflows:work` | 系统化地执行工作项 |
| `/workflows:compound` | 记录已解决的问题以累积团队知识 |

### Utility Commands

| Command | Description |
|---------|-------------|
| `/deepen-plan` | 使用并行研究 Agent 增强每个部分的计划 |
| `/changelog` | 为最近的合并创建引人入胜的 changelog |
| `/create-agent-skill` | 创建或编辑 Claude Code Skill |
| `/generate_command` | 生成新的 slash Command |
| `/heal-skill` | 修复 Skill 文档问题 |
| `/plan_review` | 并行进行多 Agent 计划审查 |
| `/report-bug` | 报告 Plugin 中的 bug |
| `/reproduce-bug` | 使用日志和控制台重现 bug |
| `/resolve_parallel` | 并行解决 TODO 注释 |
| `/resolve_pr_parallel` | 并行解决 PR 评论 |
| `/resolve_todo_parallel` | 并行解决 todo |
| `/triage` | 分类和优先处理 Issue |
| `/playwright-test` | 在受 PR 影响的页面上运行浏览器测试 |
| `/xcode-test` | 在模拟器上构建和测试 iOS 应用 |
| `/feature-video` | 录制视频演练并添加到 PR 描述 |

## Skill

### Architecture & Design

| Skill | Description |
|-------|-------------|
| `agent-native-architecture` | 使用 prompt-native 架构构建 AI Agent |

### Development Tools

| Skill | Description |
|-------|-------------|
| `andrew-kane-gem-writer` | 遵循 Andrew Kane 模式编写 Ruby gem |
| `compound-docs` | 将已解决的问题捕获为分类文档 |
| `create-agent-skills` | 创建 Claude Code Skill 的专家指导 |
| `dhh-rails-style` | 以 DHH 的 37signals 风格编写 Ruby/Rails 代码 |
| `dspy-ruby` | 使用 DSPy.rb 构建类型安全的 LLM 应用程序 |
| `frontend-design` | 创建生产级前端界面 |
| `skill-creator` | 创建有效 Claude Code Skill 的指南 |

### Content & Workflow

| Skill | Description |
|-------|-------------|
| `every-style-editor` | 审查文案是否符合 Every 的风格指南 |
| `file-todos` | 基于文件的 todo 跟踪系统 |
| `git-worktree` | 管理 Git worktree 以进行并行开发 |

### File Transfer

| Skill | Description |
|-------|-------------|
| `rclone` | 将文件上传到 S3、Cloudflare R2、Backblaze B2 和云存储 |

### Image Generation

| Skill | Description |
|-------|-------------|
| `gemini-imagegen` | 使用 Google 的 Gemini API 生成和编辑图像 |

**gemini-imagegen 功能：**
- 文本到图像生成
- 图像编辑和处理
- 多轮改进
- 多参考图像合成（最多 14 张图像）

**要求：**
- `GEMINI_API_KEY` 环境变量
- Python 包：`google-genai`、`pillow`

## MCP Server

| Server | Description |
|--------|-------------|
| `playwright` | 通过 `@playwright/mcp` 进行浏览器自动化 |
| `context7` | 通过 Context7 查找框架文档 |

### Playwright

**提供的工具：**
- `browser_navigate` - 导航到 URL
- `browser_take_screenshot` - 截屏
- `browser_click` - 点击元素
- `browser_fill_form` - 填写表单字段
- `browser_snapshot` - 获取可访问性快照
- `browser_evaluate` - 执行 JavaScript

### Context7

**提供的工具：**
- `resolve-library-id` - 查找框架/包的库 ID
- `get-library-docs` - 获取特定库的文档

支持 100+ 框架，包括 Rails、React、Next.js、Vue、Django、Laravel 等。

MCP Server 在启用 Plugin 时自动启动。

## 安装

```bash
claude /plugin install compound-engineering
```

## 已知问题

### MCP Server 未自动加载

**问题：** 捆绑的 MCP Server（Playwright 和 Context7）可能不会在安装 Plugin 时自动加载。

**解决方法：** 手动将它们添加到项目的 `.claude/settings.json`：

```json
{
  "mcpServers": {
    "playwright": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest"],
      "env": {}
    },
    "context7": {
      "type": "http",
      "url": "https://mcp.context7.com/mcp"
    }
  }
}
```

或者在 `~/.claude/settings.json` 中全局添加它们以供所有项目使用。

## 版本历史

详细版本历史见 [CHANGELOG.md](CHANGELOG.md)。

## 许可证

MIT
