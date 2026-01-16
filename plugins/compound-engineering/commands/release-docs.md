---
name: release-docs
description: 使用当前插件组件构建和更新文档站点
argument-hint: "[可选: --dry-run 预览更改而不写入]"
---

# 发布文档 Command

你是 compound-engineering 插件的文档生成器。你的任务是确保 `plugins/compound-engineering/docs/` 目录中的文档站点始终与实际插件组件保持同步。

## 概述

文档站点是基于 Evil Martians LaunchKit 模板的静态 HTML/CSS/JS 站点。在以下情况下需要重新生成：

- 添加、删除或修改 Agent
- 添加、删除或修改 Command
- 添加、删除或修改 Skill
- 添加、删除或修改 MCP server

## 步骤 1: 清点当前组件

首先，统计并列出所有当前组件：

```bash
# Count agents
ls plugins/compound-engineering/agents/*.md | wc -l

# Count commands
ls plugins/compound-engineering/commands/*.md | wc -l

# Count skills
ls -d plugins/compound-engineering/skills/*/ 2>/dev/null | wc -l

# Count MCP servers
ls -d plugins/compound-engineering/mcp-servers/*/ 2>/dev/null | wc -l
```

读取所有组件文件以获取元数据：

### Agent
对于 `plugins/compound-engineering/agents/*.md` 中的每个 agent 文件：
- 提取 frontmatter（name, description）
- 记录类别（Review, Research, Workflow, Design, Docs）
- 从内容中获取关键职责

### Command
对于 `plugins/compound-engineering/commands/*.md` 中的每个 command 文件：
- 提取 frontmatter（name, description, argument-hint）
- 分类为 Workflow 或 Utility command

### Skill
对于 `plugins/compound-engineering/skills/*/` 中的每个 skill 目录：
- 读取 SKILL.md 文件的 frontmatter（name, description）
- 记录任何脚本或支持文件

### MCP Server
对于 `plugins/compound-engineering/mcp-servers/*/` 中的每个 MCP server：
- 读取配置和 README
- 列出提供的工具

## 步骤 2: 更新文档页面

### 2a. 更新 `docs/index.html`

使用准确的计数更新统计部分：
```html
<div class="stats-grid">
  <div class="stat-card">
    <span class="stat-number">[AGENT_COUNT]</span>
    <span class="stat-label">Specialized Agents</span>
  </div>
  <!-- Update all stat cards -->
</div>
```

确保组件摘要部分准确列出关键组件。

### 2b. 更新 `docs/pages/agents.html`

重新生成完整的 agent 参考页面：
- 按类别分组 agent（Review, Research, Workflow, Design, Docs）
- 每个 agent 包括：
  - 名称和描述
  - 关键职责（项目列表）
  - 使用示例：`claude agent [agent-name] "your message"`
  - 使用场景

### 2c. 更新 `docs/pages/commands.html`

重新生成完整的 command 参考页面：
- 按类型分组 command（Workflow, Utility）
- 每个 command 包括：
  - 名称和描述
  - 参数（如有）
  - 流程/工作流步骤
  - 使用示例

### 2d. 更新 `docs/pages/skills.html`

重新生成完整的 skill 参考页面：
- 按类别分组 skill（Development Tools, Content & Workflow, Image Generation）
- 每个 skill 包括：
  - 名称和描述
  - 使用方式：`claude skill [skill-name]`
  - 特性和功能

### 2e. 更新 `docs/pages/mcp-servers.html`

重新生成 MCP server 参考页面：
- 每个 server：
  - 名称和用途
  - 提供的工具
  - 配置详情
  - 支持的框架/服务

## 步骤 3: 更新元数据文件

确保计数在以下位置保持一致：

1. **`plugins/compound-engineering/.claude-plugin/plugin.json`**
   - 使用正确的计数更新 `description`
   - 使用计数更新 `components` 对象
   - 使用当前项目更新 `agents`、`commands` 数组

2. **`.claude-plugin/marketplace.json`**
   - 使用正确的计数更新插件 `description`

3. **`plugins/compound-engineering/README.md`**
   - 使用计数更新介绍段落
   - 更新组件列表

## 步骤 4: 验证

运行验证检查：

```bash
# Validate JSON files
cat .claude-plugin/marketplace.json | jq .
cat plugins/compound-engineering/.claude-plugin/plugin.json | jq .

# Verify counts match
echo "Agents in files: $(ls plugins/compound-engineering/agents/*.md | wc -l)"
grep -o "[0-9]* specialized agents" plugins/compound-engineering/docs/index.html

echo "Commands in files: $(ls plugins/compound-engineering/commands/*.md | wc -l)"
grep -o "[0-9]* slash commands" plugins/compound-engineering/docs/index.html
```

## 步骤 5: 报告更改

提供更新内容的摘要：

```
## 文档发布摘要

### 组件计数
- Agent: X（之前为 Y）
- Command: X（之前为 Y）
- Skill: X（之前为 Y）
- MCP Server: X（之前为 Y）

### 更新的文件
- docs/index.html - 更新了统计和组件摘要
- docs/pages/agents.html - 使用 X 个 agent 重新生成
- docs/pages/commands.html - 使用 X 个 command 重新生成
- docs/pages/skills.html - 使用 X 个 skill 重新生成
- docs/pages/mcp-servers.html - 使用 X 个 server 重新生成
- plugin.json - 更新了计数和组件列表
- marketplace.json - 更新了描述
- README.md - 更新了组件列表

### 新增组件
- [列出任何新的 agent/command/skill]

### 删除的组件
- [列出任何删除的 agent/command/skill]
```

## 试运行模式

如果指定了 `--dry-run`：
- 执行所有清点和验证步骤
- 报告将要更新的内容
- 不写入任何文件
- 显示建议更改的差异预览

## 错误处理

- 如果组件文件的 frontmatter 无效，报告错误并跳过
- 如果 JSON 验证失败，报告并中止
- 始终保持有效状态 - 不要部分更新

## 发布后

成功发布后：
1. 建议使用文档更改更新 CHANGELOG.md
2. 提醒使用消息提交：`docs: Update documentation site to match plugin components`
3. 提醒推送更改

## 使用示例

```bash
# 完整的文档发布
claude /release-docs

# 预览更改而不写入
claude /release-docs --dry-run

# 添加新 agent 后
claude /release-docs
```
