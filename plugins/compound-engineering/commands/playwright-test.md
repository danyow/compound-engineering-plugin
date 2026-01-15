---
name: playwright-test
description: 对当前 PR 或分支影响的页面运行 Playwright 浏览器测试
argument-hint: "[PR 编号、分支名称，或 'current' 表示当前分支]"
---

# Playwright 测试 Command

<command_purpose>使用 Playwright MCP 对 PR 或分支更改影响的页面运行端到端浏览器测试。</command_purpose>

## 简介

<role>专注于基于浏览器的端到端测试的 QA 工程师</role>

此命令在真实浏览器中测试受影响的页面，捕获单元测试遗漏的问题：
- JavaScript 集成 bug
- CSS/布局回归
- 用户工作流中断
- 控制台错误

## 前置条件

<requirements>
- 本地开发服务器正在运行（例如 `bin/dev`、`rails server`）
- Playwright MCP server 已连接
- Git 仓库包含待测试的更改
</requirements>

## 主要任务

### 1. 确定测试范围

<test_target> $ARGUMENTS </test_target>

<determine_scope>

**如果提供了 PR 编号：**
```bash
gh pr view [number] --json files -q '.files[].path'
```

**如果是 'current' 或为空：**
```bash
git diff --name-only main...HEAD
```

**如果提供了分支名称：**
```bash
git diff --name-only main...[branch]
```

</determine_scope>

### 2. 将文件映射到路由

<file_to_route_mapping>

将更改的文件映射到可测试的路由：

| 文件模式 | 路由 |
|-------------|----------|
| `app/views/users/*` | `/users`, `/users/:id`, `/users/new` |
| `app/controllers/settings_controller.rb` | `/settings` |
| `app/javascript/controllers/*_controller.js` | 使用该 Stimulus controller 的页面 |
| `app/components/*_component.rb` | 渲染该组件的页面 |
| `app/views/layouts/*` | 所有页面（至少测试首页） |
| `app/assets/stylesheets/*` | 关键页面的视觉回归 |
| `app/helpers/*_helper.rb` | 使用该 helper 的页面 |

根据映射构建要测试的 URL 列表。

</file_to_route_mapping>

### 3. 验证服务器是否运行

<check_server>

测试前，验证本地服务器是否可访问：

```
mcp__playwright__browser_navigate({ url: "http://localhost:3000" })
mcp__playwright__browser_snapshot({})
```

如果服务器未运行，通知用户：
```markdown
**服务器未运行**

请启动开发服务器：
- Rails: `bin/dev` 或 `rails server`
- Node: `npm run dev`

然后再次运行 `/playwright-test`。
```

</check_server>

### 4. 测试每个受影响的页面

<test_pages>

对于每个受影响的路由：

**步骤 1：导航并捕获快照**
```
mcp__playwright__browser_navigate({ url: "http://localhost:3000/[route]" })
mcp__playwright__browser_snapshot({})
```

**步骤 2：检查错误**
```
mcp__playwright__browser_console_messages({ level: "error" })
```

**步骤 3：验证关键元素**
- 页面标题/标题存在
- 主要内容已渲染
- 无可见的错误消息
- 表单具有预期字段

**步骤 4：测试关键交互（如适用）**
```
mcp__playwright__browser_click({ element: "[description]", ref: "[ref]" })
mcp__playwright__browser_snapshot({})
```

</test_pages>

### 5. 人工验证（必要时）

<human_verification>

当测试涉及以下内容时暂停以获取人工输入：

| 流程类型 | 询问内容 |
|-----------|-------------|
| OAuth | "请使用 [provider] 登录并确认可用" |
| Email | "检查收件箱中的测试邮件并确认收到" |
| Payments | "在沙箱模式下完成测试购买" |
| SMS | "验证您收到了短信验证码" |
| External API | "确认 [service] 集成正常工作" |

使用 AskUserQuestion：
```markdown
**需要人工验证**

此测试涉及 [流程类型]。请：
1. [要采取的操作]
2. [要验证的内容]

是否正常工作？
1. 是 - 继续测试
2. 否 - 描述问题
```

</human_verification>

### 6. 处理失败

<failure_handling>

当测试失败时：

1. **记录失败：**
   - 截图错误状态
   - 捕获控制台错误
   - 记录准确的重现步骤

2. **询问用户如何处理：**
   ```markdown
   **测试失败：[route]**

   问题：[描述]
   控制台错误：[如有]

   如何处理？
   1. 立即修复 - 我会帮助调试和修复
   2. 创建待办 - 添加到 todos/ 稍后处理
   3. 跳过 - 继续测试其他页面
   ```

3. **如果选择"立即修复"：**
   - 调查问题
   - 提出修复方案
   - 应用修复
   - 重新运行失败的测试

4. **如果选择"创建待办"：**
   - 创建 `{id}-pending-p1-playwright-{description}.md`
   - 继续测试

5. **如果选择"跳过"：**
   - 记录为已跳过
   - 继续测试

</failure_handling>

### 7. 测试摘要

<test_summary>

所有测试完成后，展示摘要：

```markdown
## 🎭 Playwright 测试结果

**测试范围：** PR #[number] / [branch name]
**服务器：** http://localhost:3000

### 已测试页面：[count]

| 路由 | 状态 | 备注 |
|-------|--------|-------|
| `/users` | ✅ 通过 | |
| `/settings` | ✅ 通过 | |
| `/dashboard` | ❌ 失败 | 控制台错误：[msg] |
| `/checkout` | ⏭️ 跳过 | 需要支付凭证 |

### 控制台错误：[count]
- [列出发现的任何错误]

### 人工验证：[count]
- OAuth 流程：✅ 已确认
- 邮件发送：✅ 已确认

### 失败：[count]
- `/dashboard` - [问题描述]

### 创建的待办：[count]
- `005-pending-p1-playwright-dashboard-error.md`

### 结果：[通过 / 失败 / 部分通过]
```

</test_summary>

## 快速使用示例

```bash
# 测试当前分支的更改
/playwright-test

# 测试特定 PR
/playwright-test 847

# 测试特定分支
/playwright-test feature/new-dashboard
```
