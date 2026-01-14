---
name: reproduce-bug
description: 使用日志、控制台检查和浏览器截图重现和调查 bug
argument-hint: "[GitHub Issue 编号]"
---

# 重现 Bug Command

查看 GitHub Issue #$ARGUMENTS 并阅读 Issue 描述和评论。

## 阶段 1：日志调查

并行运行以下 Agent 来调查 bug：

1. Task rails-console-explorer(issue_description)
2. Task appsignal-log-investigator(issue_description)

查看代码库，思考可能出错的地方。寻找可以查找的日志输出。

再次运行这些 Agent 以找到可以帮助我们重现 bug 的任何日志。

继续运行这些 Agent 直到您对正在发生的事情有一个好的了解。

## 阶段 2：使用 Playwright 进行可视化重现

如果 bug 与 UI 相关或涉及用户流程，使用 Playwright 可视化重现它：

### 步骤 1：验证服务器正在运行

```
mcp__plugin_compound-engineering_pw__browser_navigate({ url: "http://localhost:3000" })
mcp__plugin_compound-engineering_pw__browser_snapshot({})
```

如果服务器未运行，通知用户启动 `bin/dev`。

### 步骤 2：导航到受影响的区域

根据 Issue 描述，导航到相关页面：

```
mcp__plugin_compound-engineering_pw__browser_navigate({ url: "http://localhost:3000/[affected_route]" })
mcp__plugin_compound-engineering_pw__browser_snapshot({})
```

### 步骤 3：捕获截图

在重现 bug 的每个步骤中截图：

```
mcp__plugin_compound-engineering_pw__browser_take_screenshot({ filename: "bug-[issue]-step-1.png" })
```

### 步骤 4：跟随用户流程

重现 Issue 中的确切步骤：

1. **阅读 Issue 的重现步骤**
2. **使用 Playwright 执行每个步骤：**
   - `browser_click` 用于点击元素
   - `browser_type` 用于填写表单
   - `browser_snapshot` 查看当前状态
   - `browser_take_screenshot` 捕获证据

3. **检查控制台错误：**
   ```
   mcp__plugin_compound-engineering_pw__browser_console_messages({ level: "error" })
   ```

### 步骤 5：捕获 Bug 状态

当您重现 bug 时：

1. 截取 bug 状态的截图
2. 捕获控制台错误
3. 记录触发它的确切步骤

```
mcp__plugin_compound-engineering_pw__browser_take_screenshot({ filename: "bug-[issue]-reproduced.png" })
```

## 阶段 3：记录发现

**参考收集：**

- [ ] 用特定文件路径记录所有研究发现（例如，`app/services/example_service.rb:42`）
- [ ] 包含显示 bug 重现的截图
- [ ] 列出任何控制台错误
- [ ] 记录确切的重现步骤

## 阶段 4：报告

向 Issue 添加评论，包含：

1. **发现** - 您发现的关于原因的内容
2. **重现步骤** - 重现的确切步骤（已验证）
3. **截图** - bug 的视觉证据（上传捕获的截图）
4. **相关代码** - 文件路径和行号
5. **建议的修复** - 如果您有的话
