---
name: feature-video
description: 录制功能演示视频并将其添加到 PR 描述
argument-hint: "[PR 编号或 'current'] [可选：基础 URL，默认 localhost:3000]"
---

# 功能视频演示

<command_purpose>录制功能演示视频，上传视频并将其添加到 PR 描述。</command_purpose>

## 简介

<role>创建功能演示视频的开发者关系工程师</role>

此命令为 PR 文档创建专业的功能视频演示：
- 使用 Playwright 视频捕获录制浏览器交互
- 演示完整的用户流程
- 上传视频以便分享
- 使用嵌入视频更新 PR 描述

## 前置条件

<requirements>
- 本地开发服务器正在运行（例如 `bin/dev`、`rails server`）
- Playwright MCP server 已连接
- Git 仓库包含要记录的 PR
- 已安装 `ffmpeg`（用于视频转换）
- 已配置 `rclone`（可选，用于云上传 - 参见 rclone skill）
</requirements>

## 主要任务

### 1. 解析参数

<parse_args>

**参数：** $ARGUMENTS

解析输入：
- 第一个参数：PR 编号或 "current"（默认为当前分支的 PR）
- 第二个参数：基础 URL（默认为 `http://localhost:3000`）

```bash
# 如果需要，获取当前分支的 PR 编号
gh pr view --json number -q '.number'
```

</parse_args>

### 2. 收集功能上下文

<gather_context>

**获取 PR 详情：**
```bash
gh pr view [number] --json title,body,files,headRefName -q '.'
```

**获取更改的文件：**
```bash
gh pr view [number] --json files -q '.files[].path'
```

**将文件映射到可测试的路由**（与 playwright-test 相同）：

| 文件模式 | 路由 |
|-------------|----------|
| `app/views/users/*` | `/users`, `/users/:id`, `/users/new` |
| `app/controllers/settings_controller.rb` | `/settings` |
| `app/javascript/controllers/*_controller.js` | 使用该 Stimulus controller 的页面 |
| `app/components/*_component.rb` | 渲染该组件的页面 |

</gather_context>

### 3. 规划视频流程

<plan_flow>

录制前，创建镜头列表：

1. **开场镜头**：首页或起点（2-3 秒）
2. **导航**：用户如何到达功能
3. **功能演示**：核心功能（主要重点）
4. **边界情况**：错误状态、验证等（如适用）
5. **成功状态**：完成的操作/结果

询问用户确认或调整流程：

```markdown
**建议的视频流程**

基于 PR #[number]：[title]

1. 开始于：/[starting-route]
2. 导航到：/[feature-route]
3. 演示：
   - [操作 1]
   - [操作 2]
   - [操作 3]
4. 显示结果：[成功状态]

预估时长：约 [X] 秒

看起来正确吗？
1. 是，开始录制
2. 修改流程（描述更改）
3. 添加要演示的特定交互
```

</plan_flow>

### 4. 设置视频录制

<setup_recording>

**创建视频目录：**
```bash
mkdir -p tmp/videos
```

**使用 Playwright MCP 启动带视频录制的浏览器：**

注意：Playwright MCP 的 browser_navigate 将被使用，我们将使用 browser_run_code 启用视频录制：

```javascript
// 启用视频录制上下文
mcp__plugin_compound-engineering_pw__browser_run_code({
  code: `async (page) => {
    // 视频录制在上下文级别启用
    // MCP server 会自动处理
    return 'Video recording active';
  }`
})
```

**备选方案：使用浏览器截图作为帧**

如果无法通过 MCP 进行视频录制，回退到：
1. 在关键时刻截图
2. 使用 ffmpeg 组合成 GIF

```bash
ffmpeg -framerate 2 -pattern_type glob -i 'tmp/screenshots/*.png' -vf "scale=1280:-1" tmp/videos/feature-demo.gif
```

</setup_recording>

### 5. 录制演示

<record_walkthrough>

执行计划的流程，捕获每个步骤：

**步骤 1：导航到起点**
```
mcp__plugin_compound-engineering_pw__browser_navigate({ url: "[base-url]/[start-route]" })
mcp__plugin_compound-engineering_pw__browser_wait_for({ time: 2 })
mcp__plugin_compound-engineering_pw__browser_take_screenshot({ filename: "tmp/screenshots/01-start.png" })
```

**步骤 2：执行导航/交互**
```
mcp__plugin_compound-engineering_pw__browser_click({ element: "[description]", ref: "[ref]" })
mcp__plugin_compound-engineering_pw__browser_wait_for({ time: 1 })
mcp__plugin_compound-engineering_pw__browser_take_screenshot({ filename: "tmp/screenshots/02-navigate.png" })
```

**步骤 3：演示功能**
```
mcp__plugin_compound-engineering_pw__browser_snapshot({})
// 识别交互元素
mcp__plugin_compound-engineering_pw__browser_click({ element: "[feature element]", ref: "[ref]" })
mcp__plugin_compound-engineering_pw__browser_wait_for({ time: 1 })
mcp__plugin_compound-engineering_pw__browser_take_screenshot({ filename: "tmp/screenshots/03-feature.png" })
```

**步骤 4：捕获结果**
```
mcp__plugin_compound-engineering_pw__browser_wait_for({ time: 2 })
mcp__plugin_compound-engineering_pw__browser_take_screenshot({ filename: "tmp/screenshots/04-result.png" })
```

**从截图创建视频/GIF：**

```bash
# 创建目录
mkdir -p tmp/videos tmp/screenshots

# 创建 MP4 视频（推荐 - 更好的质量，更小的大小）
# -framerate 0.5 = 每帧 2 秒（较慢的播放）
# -framerate 1 = 每帧 1 秒
ffmpeg -y -framerate 0.5 -pattern_type glob -i '.playwright-mcp/tmp/screenshots/*.png' \
  -c:v libx264 -pix_fmt yuv420p -vf "scale=1280:-2" \
  tmp/videos/feature-demo.mp4

# 创建低质量 GIF 预览（小文件，用于 GitHub 嵌入）
ffmpeg -y -framerate 0.5 -pattern_type glob -i '.playwright-mcp/tmp/screenshots/*.png' \
  -vf "scale=640:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse" \
  -loop 0 tmp/videos/feature-demo-preview.gif

# 将截图复制到项目文件夹以便访问
cp -r .playwright-mcp/tmp/screenshots tmp/
```

**注意：**
- MP4 缩放中的 `-2` 确保高度可被 2 整除（H.264 所需）
- 预览 GIF 使用 640px 宽度和 128 色以保持文件大小小（约 100-200KB）

</record_walkthrough>

### 6. 上传视频

<upload_video>

**使用 rclone 上传：**

```bash
# 检查 rclone 是否已配置
rclone listremotes

# 将视频、预览 GIF 和截图上传到云存储
# 使用 --s3-no-check-bucket 避免权限错误
rclone copy tmp/videos/ r2:kieran-claude/pr-videos/pr-[number]/ --s3-no-check-bucket --progress
rclone copy tmp/screenshots/ r2:kieran-claude/pr-videos/pr-[number]/screenshots/ --s3-no-check-bucket --progress

# 列出已上传的文件
rclone ls r2:kieran-claude/pr-videos/pr-[number]/
```

公开 URL（带公共访问的 R2）：
```
视频：https://pub-4047722ebb1b4b09853f24d3b61467f1.r2.dev/pr-videos/pr-[number]/feature-demo.mp4
预览：https://pub-4047722ebb1b4b09853f24d3b61467f1.r2.dev/pr-videos/pr-[number]/feature-demo-preview.gif
```

</upload_video>

### 7. 更新 PR 描述

<update_pr>

**获取当前 PR body：**
```bash
gh pr view [number] --json body -q '.body'
```

**向 PR 描述添加视频部分：**

如果 PR 已经有视频部分，则替换它。否则，追加：

**重要提示：** GitHub 无法直接嵌入外部 MP4。使用可点击的 GIF 链接到视频：

```markdown
## 演示

[![功能演示]([preview-gif-url])]([video-mp4-url])

*点击查看完整视频*
```

示例：
```markdown
[![功能演示](https://pub-4047722ebb1b4b09853f24d3b61467f1.r2.dev/pr-videos/pr-137/feature-demo-preview.gif)](https://pub-4047722ebb1b4b09853f24d3b61467f1.r2.dev/pr-videos/pr-137/feature-demo.mp4)
```

**更新 PR：**
```bash
gh pr edit [number] --body "[updated body with video section]"
```

**或者如果首选作为评论添加：**
```bash
gh pr comment [number] --body "## 功能演示

![演示]([video-url])

_此 PR 中更改的自动演示_"
```

</update_pr>

### 8. 清理

<cleanup>

```bash
# 可选：清理截图
rm -rf tmp/screenshots

# 保留视频以供参考
echo "视频保存在：tmp/videos/feature-demo.gif"
```

</cleanup>

### 9. 摘要

<summary>

展示完成摘要：

```markdown
## 功能视频完成

**PR：** #[number] - [title]
**视频：** [url or local path]
**时长：** 约 [X] 秒
**格式：** [GIF/MP4]

### 捕获的镜头
1. [起点] - [描述]
2. [导航] - [描述]
3. [功能演示] - [描述]
4. [结果] - [描述]

### PR 已更新
- [x] 视频部分已添加到 PR 描述
- [ ] 准备审查

**后续步骤：**
- 审查视频以确保准确演示功能
- 与审查者分享以获取上下文
```

</summary>

## 快速使用示例

```bash
# 为当前分支的 PR 录制视频
/feature-video

# 为特定 PR 录制视频
/feature-video 847

# 使用自定义基础 URL 录制
/feature-video 847 http://localhost:5000

# 为暂存环境录制
/feature-video current https://staging.example.com
```

## 提示

- **保持简短**：10-30 秒是 PR 演示的理想时长
- **聚焦于更改**：不要包含无关的 UI
- **显示前后对比**：如果修复 bug，先显示损坏状态（如果可能）
- **如需要添加注释**：为复杂功能添加文本叠加
