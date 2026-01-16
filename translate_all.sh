#!/bin/bash

# List of 13 SKILL.md files to translate
files=(
  "plugins/compound-engineering/skills/agent-native-architecture/SKILL.md"
  "plugins/compound-engineering/skills/andrew-kane-gem-writer/SKILL.md"
  "plugins/compound-engineering/skills/compound-docs/SKILL.md"
  "plugins/compound-engineering/skills/create-agent-skills/SKILL.md"
  "plugins/compound-engineering/skills/dhh-rails-style/SKILL.md"
  "plugins/compound-engineering/skills/dspy-ruby/SKILL.md"
  "plugins/compound-engineering/skills/every-style-editor/SKILL.md"
  "plugins/compound-engineering/skills/file-todos/SKILL.md"
  "plugins/compound-engineering/skills/frontend-design/SKILL.md"
  "plugins/compound-engineering/skills/gemini-imagegen/SKILL.md"
  "plugins/compound-engineering/skills/git-worktree/SKILL.md"
  "plugins/compound-engineering/skills/rclone/SKILL.md"
  "plugins/compound-engineering/skills/skill-creator/SKILL.md"
)

echo "Files to translate:"
for file in "${files[@]}"; do
  echo "  - $file"
done
