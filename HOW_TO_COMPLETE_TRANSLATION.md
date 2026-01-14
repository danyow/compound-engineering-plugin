# 如何完成剩余翻译 / How to Complete Remaining Translation

## 当前状态 / Current Status

已手动翻译 **13 / 132 文件 (9.8%)**

- ✅ plans/ - 2 文件
- ✅ plugins/coding-tutor/ - 5 文件  
- ✅ plugins/compound-engineering/ - 6 文件（README + 5 个 command）

剩余 **119 文件**待翻译。

## 推荐解决方案：使用 GitHub Actions 自动翻译

仓库中已经配置了自动翻译工作流：`.github/workflows/translate-chinese.yml`

### 方法 1：通过 GitHub Web UI 触发（推荐）

1. 访问仓库的 Actions 页面：
   ```
   https://github.com/danyow/compound-engineering-plugin/actions
   ```

2. 选择 "Translate Documentation to Chinese" 工作流

3. 点击 "Run workflow" 按钮

4. 配置选项：
   - `target_path`: 
     - 全部翻译：`plugins/compound-engineering`
     - 仅 agents：`plugins/compound-engineering/agents`
     - 仅 commands：`plugins/compound-engineering/commands`
     - 仅 skills：`plugins/compound-engineering/skills`
   - `create_pr`: 选择 `true` 自动创建 PR

5. 点击 "Run workflow"

工作流将：
- 使用 OpenAI GPT-4o-mini API 翻译所有文件
- 保持代码块、技术术语和格式不变
- 创建 zh-CN 目录结构
- 自动创建 Pull Request

### 方法 2：通过命令行触发

如果您有 GitHub CLI：

```bash
# 翻译所有 compound-engineering 文件
gh workflow run "Translate Documentation to Chinese" \
  -f target_path="plugins/compound-engineering" \
  -f create_pr=true

# 或者仅翻译特定目录
gh workflow run "Translate Documentation to Chinese" \
  -f target_path="plugins/compound-engineering/agents" \
  -f create_pr=true
```

## 前置要求 / Prerequisites

⚠️ **重要**：工作流需要 `OPENAI_API_KEY` 密钥

### 设置 OpenAI API Key

1. 获取 OpenAI API key：https://platform.openai.com/api-keys

2. 在 GitHub 仓库设置中添加密钥：
   ```
   Settings → Secrets and variables → Actions → New repository secret
   ```
   
   Name: `OPENAI_API_KEY`
   Value: `your-openai-api-key`

## 工作流配置 / Workflow Configuration

工作流使用以下翻译规则（与我手动翻译使用的规则相同）：

```python
# 不翻译：
- 代码块 (```...```)
- 内联代码 (`...`)
- URL 和文件路径
- YAML frontmatter 键（仅翻译值）
- 技术术语：API, CLI, SDK, JSON, YAML, Markdown
- 编程术语：Rails, React, TypeScript, Python, Ruby, npm, pip, gem
- 功能名称：Agent, Command, Skill, Plugin, MCP Server
- Git 术语：PR, Issue, Commit

# 翻译：
- 描述性文本和说明
- 注释和文档
- 标题和标头
- 列表项和要点
- 表格内容（技术术语除外）
- YAML frontmatter 的值
```

## 手动翻译方法（可选）

如果您没有 OpenAI API 密钥或希望手动翻译，可以继续当前的方法：

```bash
# 1. 查看需要翻译的文件
find plugins/compound-engineering -name "*.md" | grep -v zh-CN | sort

# 2. 对每个文件：
#    - 阅读英文内容
#    - 创建对应的 zh-CN 路径
#    - 翻译内容，遵循上述规则
#    - 保存翻译文件

# 3. 提交更改
git add plugins/compound-engineering/zh-CN/
git commit -m "Add Chinese translations"
git push
```

预计手动翻译 119 个文件需要 **8-12 小时**。

## 混合方法（推荐）

1. ✅ 已手动翻译关键文件（README, 核心 commands）
2. 🔄 使用 GitHub Actions 自动翻译剩余文件
3. ✅ 人工审查自动翻译的质量
4. ✅ 根据需要进行调整

这种方法结合了手动翻译的质量控制和自动化的效率。

## plugin.json 文件

还需要翻译 2 个 plugin.json 文件中的 description 字段：

### plugins/compound-engineering/.claude-plugin/plugin.json

```json
{
  "description": "AI 驱动的开发工具。27 个 Agent、21 个 Command、13 个 Skill、2 个 MCP Server，用于代码审查、研究、设计和工作流自动化。"
}
```

### plugins/coding-tutor/.claude-plugin/plugin.json

```json
{
  "description": "基于您现有知识并使用您的实际代码库作为示例的个性化编程教程。使用 AI、间隔重复和测验的力量，创建随时间复合增长的持久学习轨迹。"
}
```

这些可以手动编辑，或者在运行 GitHub Actions 工作流时包含。

## 验证翻译 / Verify Translations

翻译完成后，验证：

```bash
# 检查所有文件是否已翻译
find plugins -name "*.md" | grep -v zh-CN | wc -l  # 应该是 0 或很少

# 检查 zh-CN 文件数量
find plugins -name "*.md" | grep zh-CN | wc -l  # 应该约等于英文文件数

# 验证代码块未被翻译
grep -r "```" plugins/*/zh-CN/ | head -10

# 验证技术术语保持英文
grep -r "Agent\|Command\|Skill" plugins/*/zh-CN/ | head -5
```

## 总结 / Summary

**最快方法：** 使用 GitHub Actions 工作流自动翻译所有剩余文件（需要 OPENAI_API_KEY）

**手动方法：** 继续逐个文件翻译（耗时 8-12 小时）

**推荐方法：** 混合 - 关键文件已手动完成，使用自动化完成其余部分

选择最适合您需求和资源的方法！
