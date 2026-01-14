---
name: deploy-docs
description: 验证并准备文档以部署到 GitHub Pages
---

# 部署文档 Command

验证文档站点并准备其部署到 GitHub Pages。

## 步骤 1：验证文档

运行这些检查：

```bash
# 计数组件
echo "Agents: $(ls plugins/compound-engineering/agents/*.md | wc -l)"
echo "Commands: $(ls plugins/compound-engineering/commands/*.md | wc -l)"
echo "Skills: $(ls -d plugins/compound-engineering/skills/*/ 2>/dev/null | wc -l)"

# 验证 JSON
cat .claude-plugin/marketplace.json | jq . > /dev/null && echo "✓ marketplace.json valid"
cat plugins/compound-engineering/.claude-plugin/plugin.json | jq . > /dev/null && echo "✓ plugin.json valid"

# 检查所有 HTML 文件是否存在
for page in index agents commands skills mcp-servers changelog getting-started; do
  if [ -f "plugins/compound-engineering/docs/pages/${page}.html" ] || [ -f "plugins/compound-engineering/docs/${page}.html" ]; then
    echo "✓ ${page}.html exists"
  else
    echo "✗ ${page}.html MISSING"
  fi
done
```

## 步骤 2：检查未提交的更改

```bash
git status --porcelain plugins/compound-engineering/docs/
```

如果有未提交的更改，警告用户先提交。

## 步骤 3：部署说明

由于 GitHub Pages 部署需要具有特殊权限的工作流文件，请提供以下说明：

### 首次设置

1. 使用 GitHub Pages 工作流创建 `.github/workflows/deploy-docs.yml`
2. 转到仓库 Settings > Pages
3. 将 Source 设置为 "GitHub Actions"

### 部署

合并到 `main` 后，文档将自动部署。或者：

1. 转到 Actions 标签
2. 选择 "Deploy Documentation to GitHub Pages"
3. 点击 "Run workflow"

### 工作流文件内容

```yaml
name: Deploy Documentation to GitHub Pages

on:
  push:
    branches: [main]
    paths:
      - 'plugins/compound-engineering/docs/**'
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v4
      - uses: actions/upload-pages-artifact@v3
        with:
          path: 'plugins/compound-engineering/docs'
      - uses: actions/deploy-pages@v4
```

## 步骤 4：报告状态

提供摘要：

```
## 部署准备情况

✓ 所有 HTML 页面都存在
✓ JSON 文件有效
✓ 组件计数匹配

### 后续步骤
- [ ] 提交任何待处理的更改
- [ ] 推送到 main 分支
- [ ] 验证 GitHub Pages 工作流是否存在
- [ ] 在 https://everyinc.github.io/every-marketplace/ 检查部署
```
