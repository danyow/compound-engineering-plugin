# 翻译状态 / Translation Status

## 已完成 / Completed: 14/132 files (10.6%)

### plans/ - 2 files ✅
- grow-your-own-garden-plugin-architecture.md
- landing-page-launchkit-refresh.md

### plugins/coding-tutor/ - 5 files ✅
- README.md
- commands/teach-me.md
- commands/quiz-me.md
- commands/sync-tutorials.md
- skills/coding-tutor/SKILL.md

### plugins/compound-engineering/ - 7 files ✅
- README.md
- commands/plan_review.md
- commands/create-agent-skill.md
- commands/resolve_parallel.md
- commands/resolve_todo_parallel.md
- commands/resolve_pr_parallel.md
- commands/reproduce-bug.md

## 待翻译 / Remaining: 118 files

### plugins/compound-engineering/

#### commands/ - 13 files
- agent-native-audit.md (277 lines)
- changelog.md (137 lines)
- deepen-plan.md (546 lines)
- deploy-docs.md (112 lines)
- feature-video.md (348 lines)
- generate_command.md (162 lines)
- heal-skill.md (142 lines)
- playwright-test.md (248 lines)
- release-docs.md (211 lines)
- report-bug.md (150 lines)
- triage.md (310 lines)
- xcode-test.md (331 lines)
- agent-native-audit.md (277 lines)

#### commands/workflows/ - 4 files
- compound.md (202 lines)
- plan.md (432 lines)
- review.md (515 lines)
- work.md (309 lines)

#### agents/ - 27 files
- agents/design/ (3 files)
- agents/docs/ (1 file)
- agents/research/ (4 files)
- agents/review/ (14 files)
- agents/workflow/ (5 files)

#### skills/ - 71 files
- SKILL.md files (13 files)
- references/ (57 files)
- assets/ (3 files)
- templates/ (2 files)
- workflows/ (10 files)

#### 文档 - 2 files
- CHANGELOG.md
- CLAUDE.md

### plugin.json files - 2 files
- plugins/compound-engineering/.claude-plugin/plugin.json (description field)
- plugins/coding-tutor/.claude-plugin/plugin.json (description field)

## 翻译方法 / Translation Approach

所有已完成的翻译遵循统一规则：
- ✅ 代码块和内联代码保持不变
- ✅ 技术术语保持英文 (Agent, Command, Skill, Rails, React, TypeScript, Python, Ruby, npm, pip, gem, Turbo, Stimulus, Hotwire)
- ✅ URL、文件路径、YAML frontmatter 键保持不变
- ✅ 使用简体中文，自然流畅
- ✅ 直接替换原文件，不使用 zh-CN 目录

## 继续翻译建议 / Recommendations for Completion

由于剩余 118 个文件，建议：

1. **优先级顺序**：
   - 先翻译 workflow commands (4 files) - 最核心的工作流命令
   - 然后翻译其他 commands (13 files)
   - 接着翻译 agents (27 files)
   - 最后翻译 skills 和 references (71 files)

2. **批量翻译**：
   - 每批 10-15 个文件
   - 翻译后立即提交
   - 保持进度可见

3. **质量保证**：
   - 确保技术术语一致性
   - 保持 markdown 格式完整
   - 验证代码块未被翻译

## 分支信息 / Branch Info

- 当前分支：`main-cn`
- 翻译方式：直接替换原文件
- 不再使用 zh-CN 子目录结构
