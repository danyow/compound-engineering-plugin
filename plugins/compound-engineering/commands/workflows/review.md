---
name: workflows:review
description: 使用多Agent分析、超级思考和worktree执行全面的代码审查
argument-hint: "[PR编号、GitHub URL、分支名称或latest]"
---

# Review Command

<command_purpose> 使用多Agent分析、超级思考和Git worktree执行全面的代码审查，进行深入的本地检查。 </command_purpose>

## 介绍

<role>资深代码审查架构师，具有安全、性能、架构和质量保证专业知识</role>

## 先决条件

<requirements>
- 安装并认证了GitHub CLI (`gh`) 的Git仓库
- 干净的main/master分支
- 创建worktree和访问仓库的适当权限
- 对于文档审查：markdown文件或文档的路径
</requirements>

## 主要任务

### 1. 确定审查目标并设置（始终首先执行）

<review_target> #$ARGUMENTS </review_target>

<thinking>
首先，我需要确定审查目标类型并设置代码进行分析。
</thinking>

#### 立即操作：

<task_list>

- [ ] 确定审查类型：PR编号（数字）、GitHub URL、文件路径（.md）或为空（当前分支）
- [ ] 检查当前git分支
- [ ] 如果已经在PR分支上 → 在当前分支上继续分析
- [ ] 如果在不同分支上 → 提供使用worktree："使用git-worktree skill进行隔离，调用 `skill: git-worktree` 并提供分支名称
- [ ] 使用 `gh pr view --json` 获取PR元数据，包括标题、正文、文件、链接的issue
- [ ] 设置特定语言的分析工具
- [ ] 准备安全扫描环境
- [ ] 确保我们在正在审查的分支上。使用gh pr checkout切换到分支或手动切换分支。

确保代码已准备好进行分析（在worktree中或在当前分支上）。只有这样才能继续下一步。

</task_list>

#### 并行Agent审查PR：

<parallel_tasks>

同时运行所有或大部分这些Agent：

1. Task kieran-rails-reviewer(PR content)
2. Task dhh-rails-reviewer(PR title)
3. 如果使用turbo：Task rails-turbo-expert(PR content)
4. Task git-history-analyzer(PR content)
5. Task dependency-detective(PR content)
6. Task pattern-recognition-specialist(PR content)
7. Task architecture-strategist(PR content)
8. Task code-philosopher(PR content)
9. Task security-sentinel(PR content)
10. Task performance-oracle(PR content)
11. Task devops-harmony-analyst(PR content)
12. Task data-integrity-guardian(PR content)
13. Task agent-native-reviewer(PR content) - 验证新功能是否可被Agent访问

</parallel_tasks>

#### 条件Agent（如果适用则运行）：

<conditional_agents>

这些Agent仅在PR符合特定条件时运行。检查PR文件列表以确定是否适用：

**如果PR包含数据库迁移（db/migrate/*.rb文件）或数据回填：**

14. Task data-migration-expert(PR content) - 验证ID映射与生产环境匹配，检查交换的值，验证回滚安全性
15. Task deployment-verification-agent(PR content) - 创建带有SQL验证查询的Go/No-Go部署检查清单

**何时运行迁移Agent：**
- PR包含匹配 `db/migrate/*.rb` 的文件
- PR修改存储ID、枚举或映射的列
- PR包含数据回填脚本或rake任务
- PR更改数据读取/写入方式（例如，从FK更改为字符串列）
- PR标题/正文提及：migration、backfill、data transformation、ID mapping

**这些Agent检查什么：**
- `data-migration-expert`：验证硬编码映射与生产环境实际情况匹配（防止ID交换），检查孤立关联，验证双写模式
- `deployment-verification-agent`：生成可执行的部署前/后检查清单，包含SQL查询、回滚程序和监控计划

</conditional_agents>

### 4. 超级思考深入阶段

<ultrathink_instruction> 对于以下每个阶段，花费最大的认知努力。逐步思考。考虑所有角度。质疑假设。并将所有审查综合呈现给用户。</ultrathink_instruction>

<deliverable>
完整的系统上下文映射与组件交互
</deliverable>

#### Phase 3: 利益相关者视角分析

<thinking_prompt> 超级思考：站在每个利益相关者的立场上。什么对他们重要？他们的痛点是什么？ </thinking_prompt>

<stakeholder_perspectives>

1. **开发者视角** <questions>

   - 理解和修改有多容易？
   - API是否直观？
   - 调试是否简单明了？
   - 是否容易测试？ </questions>

2. **运维视角** <questions>

   - 如何安全地部署？
   - 有哪些指标和日志可用？
   - 如何排查问题？
   - 资源需求是什么？ </questions>

3. **最终用户视角** <questions>

   - 功能是否直观？
   - 错误消息是否有帮助？
   - 性能是否可接受？
   - 是否解决了我的问题？ </questions>

4. **安全团队视角** <questions>

   - 攻击面是什么？
   - 是否有合规要求？
   - 数据如何受保护？
   - 审计能力如何？ </questions>

5. **业务视角** <questions>
   - ROI是多少？
   - 是否存在法律/合规风险？
   - 这如何影响上市时间？
   - 总拥有成本是多少？ </questions> </stakeholder_perspectives>

#### Phase 4: 场景探索

<thinking_prompt> 超级思考：探索边界情况和失败场景。可能出什么问题？系统在压力下如何表现？ </thinking_prompt>

<scenario_checklist>

- [ ] **正常路径**：使用有效输入的正常操作
- [ ] **无效输入**：Null、空值、格式错误的数据
- [ ] **边界条件**：最小/最大值、空集合
- [ ] **并发访问**：竞态条件、死锁
- [ ] **规模测试**：10倍、100倍、1000倍正常负载
- [ ] **网络问题**：超时、部分失败
- [ ] **资源耗尽**：内存、磁盘、连接
- [ ] **安全攻击**：注入、溢出、DoS
- [ ] **数据损坏**：部分写入、不一致性
- [ ] **级联故障**：下游服务问题 </scenario_checklist>

### 6. 多角度审查视角

#### 技术卓越角度

- 代码工艺评估
- 工程最佳实践
- 技术文档质量
- 工具和自动化评估

#### 业务价值角度

- 功能完整性验证
- 对用户的性能影响
- 成本效益分析
- 上市时间考虑

#### 风险管理角度

- 安全风险评估
- 运营风险评估
- 合规风险验证
- 技术债务累积

#### 团队动态角度

- 代码审查礼仪
- 知识共享有效性
- 协作模式
- 指导机会

### 4. 简化和极简主义审查

运行Task code-simplicity-reviewer()以查看我们是否可以简化代码。

### 5. 使用file-todos Skill进行发现综合和Todo创建

<critical_requirement> 所有发现必须使用file-todos skill存储在todos/目录中。在综合后立即创建todo文件 - 不要先向用户呈现发现以获得批准。使用该skill进行结构化todo管理。 </critical_requirement>

#### Step 1: 综合所有发现

<thinking>
将所有Agent报告整合成分类的发现列表。
删除重复项，按严重性和影响进行优先级排序。
</thinking>

<synthesis_tasks>

- [ ] 从所有并行Agent收集发现
- [ ] 按类型分类：security、performance、architecture、quality等
- [ ] 分配严重性级别：🔴 CRITICAL (P1)、🟡 IMPORTANT (P2)、🔵 NICE-TO-HAVE (P3)
- [ ] 删除重复或重叠的发现
- [ ] 估算每个发现的工作量（Small/Medium/Large）

</synthesis_tasks>

#### Step 2: 使用file-todos Skill创建Todo文件

<critical_instruction> 使用file-todos skill立即为所有发现创建todo文件。不要逐一向用户呈现发现以征求批准。使用该skill并行创建所有todo文件，然后向用户总结结果。 </critical_instruction>

**实现选项：**

**选项A：直接文件创建（快速）**

- 使用Write工具直接创建todo文件
- 所有发现并行处理以提高速度
- 使用来自 `.claude/skills/file-todos/assets/todo-template.md` 的标准模板
- 遵循命名约定：`{issue_id}-pending-{priority}-{description}.md`

**选项B：并行子Agent（推荐用于大规模）** 对于有15个以上发现的大型PR，使用子Agent并行创建发现文件：

```bash
# 并行启动多个发现创建器Agent
Task() - 为第一个发现创建todo
Task() - 为第二个发现创建todo
Task() - 为第三个发现创建todo
等等，为每个发现。
```

子Agent可以：

- 同时处理多个发现
- 编写填写所有部分的详细todo文件
- 按严重性组织发现
- 创建全面的建议解决方案
- 添加验收标准和工作日志
- 比顺序处理快得多

**执行策略：**

1. 将所有发现综合到类别中（P1/P2/P3）
2. 按严重性分组发现
3. 启动3个并行子Agent（每个严重性级别一个）
4. 每个子Agent使用file-todos skill创建其批次的todo
5. 整合结果并呈现摘要

**流程（使用file-todos Skill）：**

1. 对于每个发现：

   - 确定严重性（P1/P2/P3）
   - 编写详细的问题陈述和发现
   - 创建2-3个带有优缺点/工作量/风险的建议解决方案
   - 估算工作量（Small/Medium/Large）
   - 添加验收标准和工作日志

2. 使用file-todos skill进行结构化todo管理：

   ```bash
   skill: file-todos
   ```

   该skill提供：

   - 模板位置：`.claude/skills/file-todos/assets/todo-template.md`
   - 命名约定：`{issue_id}-{status}-{priority}-{description}.md`
   - YAML frontmatter结构：status、priority、issue_id、tags、dependencies
   - 所有必需部分：Problem Statement、Findings、Solutions等

3. 并行创建todo文件：

   ```bash
   {next_id}-pending-{priority}-{description}.md
   ```

4. 示例：

   ```
   001-pending-p1-path-traversal-vulnerability.md
   002-pending-p1-api-response-validation.md
   003-pending-p2-concurrency-limit.md
   004-pending-p3-unused-parameter.md
   ```

5. 遵循file-todos skill的模板结构：`.claude/skills/file-todos/assets/todo-template.md`

**Todo文件结构（来自模板）：**

每个todo必须包含：

- **YAML frontmatter**：status、priority、issue_id、tags、dependencies
- **Problem Statement**：什么被破坏/缺失，为什么重要
- **Findings**：来自Agent的发现，带有证据/位置
- **Proposed Solutions**：2-3个选项，每个都有优缺点/工作量/风险
- **Recommended Action**：（在分类期间填写，最初留空）
- **Technical Details**：受影响的文件、组件、数据库更改
- **Acceptance Criteria**：可测试的检查清单项
- **Work Log**：带有操作和学习的日期记录
- **Resources**：PR链接、issue、文档、类似模式

**文件命名约定：**

```
{issue_id}-{status}-{priority}-{description}.md

示例：
- 001-pending-p1-security-vulnerability.md
- 002-pending-p2-performance-optimization.md
- 003-pending-p3-code-cleanup.md
```

**状态值：**

- `pending` - 新发现，需要分类/决策
- `ready` - 经理批准，准备工作
- `complete` - 工作完成

**优先级值：**

- `p1` - 关键（阻止合并，安全/数据问题）
- `p2` - 重要（应该修复，架构/性能）
- `p3` - 锦上添花（增强、清理）

**标记：** 始终添加 `code-review` 标签，加上：`security`、`performance`、`architecture`、`rails`、`quality` 等。

#### Step 3: 摘要报告

创建所有todo文件后，呈现全面摘要：

````markdown
## ✅ 代码审查完成

**审查目标：** PR #XXXX - [PR标题] **分支：** [branch-name]

### 发现摘要：

- **总发现数：** [X]
- **🔴 CRITICAL (P1)：** [count] - 阻止合并
- **🟡 IMPORTANT (P2)：** [count] - 应该修复
- **🔵 NICE-TO-HAVE (P3)：** [count] - 增强

### 已创建的Todo文件：

**P1 - 关键（阻止合并）：**

- `001-pending-p1-{finding}.md` - {description}
- `002-pending-p1-{finding}.md` - {description}

**P2 - 重要：**

- `003-pending-p2-{finding}.md` - {description}
- `004-pending-p2-{finding}.md` - {description}

**P3 - 锦上添花：**

- `005-pending-p3-{finding}.md` - {description}

### 使用的审查Agent：

- kieran-rails-reviewer
- security-sentinel
- performance-oracle
- architecture-strategist
- agent-native-reviewer
- [其他Agent]

### 下一步：

1. **处理P1发现**：关键 - 合并前必须修复

   - 详细审查每个P1 todo
   - 实施修复或请求豁免
   - 合并PR前验证修复

2. **分类所有Todo**：
   ```bash
   ls todos/*-pending-*.md  # 查看所有待处理todo
   /triage                  # 使用斜杠命令进行交互式分类
   ```
````

3. **处理已批准的Todo**：

   ```bash
   /resolve_todo_parallel  # 高效修复所有已批准项
   ```

4. **跟踪进度**：
   - 状态更改时重命名文件：pending → ready → complete
   - 工作时更新Work Log
   - 提交todo：`git add todos/ && git commit -m "refactor: add code review findings"`

### 严重性细分：

**🔴 P1（关键 - 阻止合并）：**

- 安全漏洞
- 数据损坏风险
- 破坏性变更
- 关键架构问题

**🟡 P2（重要 - 应该修复）：**

- 性能问题
- 重大架构问题
- 主要代码质量问题
- 可靠性问题

**🔵 P3（锦上添花）：**

- 小的改进
- 代码清理
- 优化机会
- 文档更新

```

### 7. 端到端测试（可选）

<detect_project_type>

**首先，从PR文件检测项目类型：**

| 指示器 | 项目类型 |
|--------|----------|
| `*.xcodeproj`、`*.xcworkspace`、`Package.swift` (iOS) | iOS/macOS |
| `Gemfile`、`package.json`、`app/views/*`、`*.html.*` | Web |
| iOS文件和web文件都有 | 混合（两者都测试） |

</detect_project_type>

<offer_testing>

呈现摘要报告后，根据项目类型提供适当的测试：

**对于Web项目：**
```markdown
**"想在受影响的页面上运行Playwright浏览器测试吗？"**
1. 是 - 运行 `/playwright-test`
2. 否 - 跳过
```

**对于iOS项目：**
```markdown
**"想在应用上运行Xcode模拟器测试吗？"**
1. 是 - 运行 `/xcode-test`
2. 否 - 跳过
```

**对于混合项目（例如Rails + Hotwire Native）：**
```markdown
**"想运行端到端测试吗？"**
1. 仅Web - 运行 `/playwright-test`
2. 仅iOS - 运行 `/xcode-test`
3. 两者 - 运行两个命令
4. 否 - 跳过
```

</offer_testing>

#### 如果用户接受Web测试：

生成子Agent运行Playwright测试（保留主上下文）：

```
Task general-purpose("为PR #[number]运行/playwright-test。测试所有受影响的页面，检查控制台错误，通过创建todo和修复来处理失败。")
```

子Agent将：
1. 识别PR影响的页面
2. 导航到每个页面并捕获快照
3. 检查控制台错误
4. 测试关键交互
5. 在OAuth/email/支付流程上暂停以进行人工验证
6. 为任何失败创建P1 todo
7. 修复并重试直到所有测试通过

**独立命令：** `/playwright-test [PR number]`

#### 如果用户接受iOS测试：

生成子Agent运行Xcode测试（保留主上下文）：

```
Task general-purpose("为scheme [name]运行/xcode-test。为模拟器构建，安装，启动，截图，检查崩溃。")
```

子Agent将：
1. 验证XcodeBuildMCP已安装
2. 发现项目和scheme
3. 为iOS模拟器构建
4. 安装并启动应用
5. 截取关键屏幕的截图
6. 捕获控制台日志以查找错误
7. 暂停以进行人工验证（Sign in with Apple、推送、IAP）
8. 为任何失败创建P1 todo
9. 修复并重试直到所有测试通过

**独立命令：** `/xcode-test [scheme]`

### 重要提示：P1发现阻止合并

任何 **🔴 P1（CRITICAL）** 发现必须在合并PR之前得到解决。突出呈现这些内容，并确保在接受PR之前解决它们。
```
