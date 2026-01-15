# Compounding Engineering Plugin 开发指南

## 版本管理要求

**重要**: 对此 Plugin 的每个更改都必须更新以下三个文件：

1. **`.claude-plugin/plugin.json`** - 使用 semver 提升版本
2. **`CHANGELOG.md`** - 使用 Keep a Changelog 格式记录更改
3. **`README.md`** - 验证/更新组件计数和表格

### 版本提升规则

- **MAJOR** (1.0.0 → 2.0.0): 破坏性更改、重大重组
- **MINOR** (1.0.0 → 1.1.0): 新增 Agent、Command 或 Skill
- **PATCH** (1.0.0 → 1.0.1): Bug 修复、文档更新、小改进

### 提交前检查清单

在提交任何更改之前：

- [ ] 在 `.claude-plugin/plugin.json` 中提升版本
- [ ] 在 CHANGELOG.md 中更新更改
- [ ] 验证 README.md 组件计数
- [ ] README.md 表格准确（agents、commands、skills）
- [ ] plugin.json description 与当前计数匹配

### 目录结构

```
agents/
├── review/     # 代码审查 Agent
├── research/   # 研究和分析 Agent
├── design/     # 设计和 UI Agent
├── workflow/   # 工作流自动化 Agent
└── docs/       # 文档 Agent

commands/
├── workflows/  # 核心工作流 Command (workflows:plan, workflows:review 等)
└── *.md        # 实用 Command

skills/
└── *.md        # 所有 Skill 位于根级别
```

## Command 命名约定

**Workflow Command** 使用 `workflows:` 前缀以避免与内置 Command 冲突：
- `/workflows:plan` - 创建实施计划
- `/workflows:review` - 运行全面代码审查
- `/workflows:work` - 系统化执行工作项
- `/workflows:compound` - 记录已解决的问题

**为什么使用 `workflows:`?** Claude Code 有内置的 `/plan` 和 `/review` Command。在 frontmatter 中使用 `name: workflows:plan` 创建唯一的 `/workflows:plan` Command，无冲突。

## Skill 合规检查清单

添加或修改 Skill 时，验证是否符合 skill-creator 规范：

### YAML Frontmatter（必需）

- [ ] `name:` 存在且与目录名匹配（lowercase-with-hyphens）
- [ ] `description:` 存在且使用**第三人称**（"This skill should be used when..." 而不是 "Use this skill when..."）

### 引用链接（如果 references/ 存在则必需）

- [ ] `references/` 中的所有文件都以 `[filename.md](./references/filename.md)` 形式链接
- [ ] `assets/` 中的所有文件都以 `[filename](./assets/filename)` 形式链接
- [ ] `scripts/` 中的所有文件都以 `[filename](./scripts/filename)` 形式链接
- [ ] 没有裸反引号引用如 `` `references/file.md` `` - 使用正确的 markdown 链接

### 写作风格

- [ ] 使用祈使/不定式形式（动词优先的指令）
- [ ] 避免第二人称（"you should"）- 使用客观语言（"To accomplish X, do Y"）

### 快速验证命令

```bash
# 检查 Skill 中未链接的引用
grep -E '`(references|assets|scripts)/[^`]+`' skills/*/SKILL.md
# 如果所有引用都正确链接，应返回空

# 检查 description 格式
grep -E '^description:' skills/*/SKILL.md | grep -v 'This skill'
# 如果所有都使用第三人称，应返回空
```

## 文档

详细的版本管理工作流请参见 `docs/solutions/plugin-versioning-requirements.md`。
