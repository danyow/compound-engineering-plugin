---
name: triage
description: 为 CLI 待办系统对发现的问题进行分类和归类
argument-hint: "[发现列表或来源类型]"
---

- 首先设置 /model 为 Haiku
- 然后读取 todos/ 目录中所有待处理的待办事项

逐一展示所有发现、决策或问题以进行分类。目标是遍历每个项目并决定是否将其添加到 CLI 待办系统。

**重要提示：分类期间不要编写任何代码！**

此命令用于：

- 对代码审查发现进行分类
- 处理安全审计结果
- 审查性能分析
- 处理任何其他需要跟踪的分类发现

## 工作流

### 步骤 1：展示每个发现

对于每个发现，以此格式展示：

```
---
问题 #X：[简短标题]

严重程度：🔴 P1（严重）/ 🟡 P2（重要）/ 🔵 P3（可选）

类别：[安全/性能/架构/Bug/特性/等]

描述：
[问题或改进的详细说明]

位置：[file_path:line_number]

问题场景：
[逐步说明问题所在或可能发生的情况]

建议解决方案：
[如何修复]

预估工作量：[小型（< 2 小时）/ 中型（2-8 小时）/ 大型（> 8 小时）]

---
是否要将此项添加到待办列表？
1. yes - 创建待办文件
2. next - 跳过此项
3. custom - 修改后再创建
```

### 步骤 2：处理用户决策

**当用户选择 "yes"：**

1. **更新现有待办文件**（如果存在）或**创建新文件名：**

   如果待办已存在（来自代码审查）：

   - 重命名文件：`{id}-pending-{priority}-{desc}.md` → `{id}-ready-{priority}-{desc}.md`
   - 更新 YAML frontmatter：`status: pending` → `status: ready`
   - 保持 issue_id、priority 和 description 不变

   如果创建新待办：

   ```
   {next_id}-ready-{priority}-{brief-description}.md
   ```

   优先级映射：

   - 🔴 P1（严重）→ `p1`
   - 🟡 P2（重要）→ `p2`
   - 🔵 P3（可选）→ `p3`

   示例：`042-ready-p1-transaction-boundaries.md`

2. **更新 YAML frontmatter：**

   ```yaml
   ---
   status: ready # 重要：从 "pending" 改为 "ready"
   priority: p1 # 或 p2、p3，基于严重程度
   issue_id: "042"
   tags: [category, relevant-tags]
   dependencies: []
   ---
   ```

3. **填充或更新文件：**

   ```yaml
   # [问题标题]

   ## 问题陈述
   [来自发现的描述]

   ## 发现
   - [关键发现]
   - 位置：[file_path:line_number]
   - [场景详情]

   ## 建议解决方案

   ### 方案 1：[主要解决方案]
   - **优点**：[好处]
   - **缺点**：[缺点（如有）]
   - **工作量**：[小型/中型/大型]
   - **风险**：[低/中/高]

   ## 推荐行动
   [在分类期间填写 - 具体行动计划]

   ## 技术细节
   - **受影响文件**：[列出文件]
   - **相关组件**：[受影响的组件]
   - **数据库变更**：[是/否 - 如果是则描述]

   ## 资源
   - 原始发现：[此问题的来源]
   - 相关问题：[如有]

   ## 验收标准
   - [ ] [具体成功标准]
   - [ ] 测试通过
   - [ ] 代码已审查

   ## 工作日志

   ### {date} - 批准开始工作
   **审批人：** Claude Triage System
   **操作：**
   - 问题在分类会议期间批准
   - 状态从 pending 更改为 ready
   - 准备好被领取和处理

   **经验教训：**
   - [上下文和见解]

   ## 备注
   来源：{date} 的分类会议
   ```

4. **确认批准：** "✅ 已批准：`{new_filename}`（问题 #{issue_id}）- 状态：**ready** → 准备开始工作"

**当用户选择 "next"：**

- **删除待办文件** - 从 todos/ 目录中删除，因为它不相关
- 跳到下一项
- 跟踪跳过的项目以供摘要

**当用户选择 "custom"：**

- 询问要修改什么（优先级、描述、详情）
- 更新信息
- 展示修订版本
- 再次询问：yes/next/custom

### 步骤 3：继续处理直到全部完成

- 逐一处理所有项目
- 使用 TodoWrite 跟踪以提高可见性
- 不要在项目之间等待批准 - 继续前进

### 步骤 4：最终摘要

所有项目处理完成后：

````markdown
## 分类完成

**总项目数：** [X] **已批准待办（准备就绪）：** [Y] **已跳过：** [Z]

### 已批准待办（准备开始工作）：

- `042-ready-p1-transaction-boundaries.md` - 事务边界问题
- `043-ready-p2-cache-optimization.md` - 缓存性能改进 ...

### 已跳过项目（已删除）：

- 项目 #5：[原因] - 已从 todos/ 中删除
- 项目 #12：[原因] - 已从 todos/ 中删除

### 所做更改摘要：

在分类过程中，发生了以下状态更新：

- **Pending → Ready：** 文件名和 frontmatter 已更新以反映批准状态
- **已删除：** 已跳过发现的待办文件已从 todos/ 目录中删除
- 每个批准的文件现在在 YAML frontmatter 中都有 `status: ready`

### 后续步骤：

1. 查看准备工作的已批准待办：
   ```bash
   ls todos/*-ready-*.md
   ```
````

2. 开始处理已批准的项目：

   ```bash
   /resolve_todo_parallel  # 高效处理多个已批准项目
   ```

3. 或选择单个项目进行处理

4. 在工作过程中，更新待办状态：
   - Ready → In Progress（在工作时在本地上下文中）
   - In Progress → Complete（重命名文件：ready → complete，更新 frontmatter）

```

## 响应格式示例

```

---

问题 #5：多步操作缺少事务边界

严重程度：🔴 P1（严重）

类别：数据完整性 / 安全

描述：GoogleOauthCallbacks concern 中的 google_oauth2_connected 回调执行多个数据库操作，没有事务保护。如果任何步骤在中途失败，数据库将处于不一致状态。

位置：app/controllers/concerns/google_oauth_callbacks.rb:13-50

问题场景：

1. User.update 成功（邮箱已更改）
2. Account.save! 失败（验证错误）
3. 结果：用户已更改邮箱但没有关联的 Account
4. 下次登录尝试完全失败

没有事务的操作：

- 用户确认（第 13 行）
- 移除等待列表（第 14 行）
- 用户资料更新（第 21-23 行）
- Account 创建（第 28-37 行）
- Avatar 附件（第 39-45 行）
- Journey 创建（第 47 行）

建议解决方案：将所有操作包装在 ApplicationRecord.transaction do ... end 块中

预估工作量：小型（30 分钟）

---

是否要将此项添加到待办列表？

1. yes - 创建待办文件
2. next - 跳过此项
3. custom - 修改后再创建

```

## 重要实施细节

### 分类期间的状态转换

**当选择 "yes"：**
1. 重命名文件：`{id}-pending-{priority}-{desc}.md` → `{id}-ready-{priority}-{desc}.md`
2. 更新 YAML frontmatter：`status: pending` → `status: ready`
3. 使用分类批准条目更新工作日志
4. 确认："✅ 已批准：`{filename}`（问题 #{issue_id}）- 状态：**ready**"

**当选择 "next"：**
1. 从 todos/ 目录删除待办文件
2. 跳到下一项
3. 系统中不保留文件

### 进度跟踪

每次将待办作为标题展示时，包括：
- **进度：** X/Y 已完成（例如，"3/10 已完成"）
- **预计剩余时间：** 基于进展速度
- **节奏：** 监控每个发现的时间并相应调整估计

示例：
```

进度：3/10 已完成 | 预计时间：约 2 分钟剩余

```

### 分类期间不要编码

- ✅ 展示发现
- ✅ 做出 yes/next/custom 决策
- ✅ 更新待办文件（重命名、frontmatter、工作日志）
- ❌ 不要实施修复或编写代码
- ❌ 不要添加详细的实施细节
- ❌ 那是 /resolve_todo_parallel 阶段的事

```

完成后提供这些选项

```markdown
接下来您想做什么？

1. 运行 /resolve_todo_parallel 解决待办
2. 提交待办
3. 什么都不做，休息一下
```
