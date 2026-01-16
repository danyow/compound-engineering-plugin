<overview>
文件是Agent原生应用的通用接口。Agent天生就擅长文件操作——它们已经知道如何读取、写入和组织文件。本文档涵盖为什么文件效果很好、如何组织文件，以及用于积累知识的context.md模式。
</overview>

<why_files>
## 为什么选择文件

Agent在文件方面做得很好。Claude Code之所以奏效，是因为bash + 文件系统是测试最充分的Agent接口。在构建Agent原生应用时，应该充分利用这一点。

### Agent已经知道如何使用

你不需要教Agent你的API——它已经知道`cat`、`grep`、`mv`、`mkdir`。文件操作是它最熟悉的原始操作。

### 文件是可检查的

用户可以看到Agent创建的内容、编辑它、移动它、删除它。没有黑箱。完全透明Agent的行为。

### 文件是可移植的

导出很简单。备份很简单。用户拥有他们的数据。没有供应商锁定，没有复杂的迁移路径。

### 应用状态保持同步

在移动设备上，如果你使用iCloud的文件系统，所有设备共享相同的文件系统。Agent在一个设备上的工作会出现在所有设备上——无需你构建服务器。

### 目录结构是信息架构

文件系统为你免费提供了层级结构。`/projects/acme/notes/`的自解释性方式是`SELECT * FROM notes WHERE project_id = 123`无法比拟的。
</why_files>

<file_organization>
## 文件组织模式

> **需要验证：** 这些约定是迄今为止有效的一种方法，不是规定。应考虑更好的解决方案。

Agent原生设计的一般原则：**设计Agent能够推理的内容。** 最好的代理是对人类有意义的内容。如果人类看到你的文件结构能理解发生了什么，Agent可能也能理解。

### 实体范围目录

围绕实体（而不是参与者或文件类型）组织文件：

```
{entity_type}/{entity_id}/
├── primary content
├── metadata
└── related materials
```

**示例：** `Research/books/{bookId}/`包含关于一本书的所有内容——全文、笔记、来源、Agent日志。

### 命名约定

| 文件类型 | 命名模式 | 示例 |
|-----------|---------------|---------|
| 实体数据 | `{entity}.json` | `library.json`, `status.json` |
| 人类可读内容 | `{content_type}.md` | `introduction.md`, `profile.md` |
| Agent推理 | `agent_log.md` | 单个实体的Agent历史 |
| 主要内容 | `full_text.txt` | 下载/提取的文本 |
| 多卷 | `volume{N}.txt` | `volume1.txt`, `volume2.txt` |
| 外部来源 | `{source_name}.md` | `wikipedia.md`, `sparknotes.md` |
| 检查点 | `{sessionId}.checkpoint` | 基于UUID |
| 配置 | `config.json` | 功能设置 |

### 目录命名

- **实体范围：** `{entityType}/{entityId}/`（例如，`Research/books/{bookId}/`）
- **类型范围：** `{type}/`（例如，`AgentCheckpoints/`、`AgentLogs/`）
- **约定：** 小写带下划线，不是camelCase

### 临时 vs. 持久分离

将Agent工作文件与用户的永久数据分开：

```
Documents/
├── AgentCheckpoints/     # 临时（可以删除）
│   └── {sessionId}.checkpoint
├── AgentLogs/            # 临时（调试）
│   └── {type}/{sessionId}.md
└── Research/             # 持久（用户的工作）
    └── books/{bookId}/
```

### 分割：Markdown vs JSON

- **Markdown：** 用于用户可能读取或编辑的内容
- **JSON：** 用于应用查询的结构化数据
</file_organization>

<context_md_pattern>
## context.md模式

Agent在每个会话开始时读取的文件，并在学习时更新：

```markdown
# Context

## 我是谁
Every应用的阅读助手。

## 我对这个用户的了解
- 对军事历史和俄罗斯文学感兴趣
- 更喜欢简明扼要的分析
- 目前正在阅读《战争与和平》

## 存在什么
- /notes中有12条笔记
- 3个活跃项目
- 用户偏好设置位于/preferences.md

## 最近活动
- 用户创建"项目启动"（2小时前）
- 分析了关于奥斯特里茨的段落（昨天）

## 我的指导原则
- 不要剧透他们正在阅读的书
- 使用他们的兴趣来个性化见解

## 当前状态
- 没有待处理任务
- 上次同步：10分钟前
```

### 优点

- **Agent行为可以不改代码而演变** - 更新context，行为就会改变
- **用户可以检查和修改** - 完全透明
- **积累context的自然位置** - 学习在会话之间持续
- **可在会话间移植** - 重启Agent，知识得以保留

### 工作原理

1. Agent在会话开始时读取`context.md`
2. Agent在学到重要内容时更新它
3. 系统也可以更新它（最近活动、新资源）
4. Context在会话间持续

### 包含内容

| 部分 | 目的 |
|---------|---------|
| 我是谁 | Agent身份和角色 |
| 我对这个用户的了解 | 学到的偏好、兴趣 |
| 存在什么 | 可用资源、数据 |
| 最近活动 | 连续性的context |
| 我的指导原则 | 学到的规则和约束 |
| 当前状态 | 会话状态、待处理项 |
</context_md_pattern>

<files_vs_database>
## 文件 vs. 数据库

> **需要验证：** 这个框架受到移动开发的启发。对于Web应用，权衡是不同的。

| 使用文件做... | 使用数据库做... |
|------------------|---------------------|
| 用户应该读/编辑的内容 | 大量结构化数据 |
| 从版本控制中获益的配置 | 需要复杂查询的数据 |
| Agent生成的内容 | 临时状态（会话、缓存） |
| 任何从透明性中获益的东西 | 具有关系的数据 |
| 大型文本内容 | 需要索引的数据 |

**原则：** 文件用于易读性，数据库用于结构。有疑问时，选择文件——它们更透明，用户可以随时检查。

### 文件最有效的时候

- 规模很小（一个用户的库，不是数百万条记录）
- 透明性优先于查询速度
- 云同步（iCloud、Dropbox）与文件配合效果很好

### 混合方法

即使你需要数据库来提高性能，也可以考虑维护一个基于文件的"真实源"供Agent使用，同步到数据库供UI查询：

```
文件（Agent工作区）：
  Research/book_123/introduction.md

数据库（UI查询）：
  research_index: { bookId, path, title, createdAt }
```
</files_vs_database>

<conflict_model>
## 冲突模型

如果Agent和用户写入同一个文件，你需要一个冲突模型。

### 当前现实

大多数实现使用**最后写入优先**（通过原子写入）：

```swift
try data.write(to: url, options: [.atomic])
```

这很简单，但可能会丢失更改。

### 选项

| 策略 | 优点 | 缺点 |
|----------|------|------|
| **最后写入优先** | 简单 | 更改可能被丢失 |
| **Agent在写入前检查** | 保留用户编辑 | 更多复杂性 |
| **分离空间** | 无冲突 | 协作性较差 |
| **仅追加日志** | 从不覆盖 | 文件永久增长 |
| **文件锁定** | 安全并发访问 | 复杂性、可能阻塞 |

### 推荐方法

**对于Agent频繁写入的文件（日志、状态）：** 最后写入优先就很好。冲突很少见。

**对于用户编辑的文件（配置、笔记）：** 考虑显式处理：
- Agent在覆盖前检查修改时间
- 或将Agent输出与用户可编辑内容分开
- 或使用仅追加模式

### iCloud注意事项

iCloud同步增加了复杂性。当同步冲突发生时，它会创建`{filename} (conflict).md`文件。监控这些文件：

```swift
NotificationCenter.default.addObserver(
    forName: .NSMetadataQueryDidUpdate,
    ...
)
```

### 系统提示指导

告诉Agent关于冲突模型：

```markdown
## 与用户内容合作

当你创建内容时，用户可能之后会编辑它。在修改文件前始终先阅读
存在的文件——用户可能做了你应该保留的改进。

如果文件自你上次写入后已被修改，在覆盖前询问。
```
</conflict_model>

<examples>
## 示例：阅读应用文件结构

```
Documents/
├── Library/
│   └── library.json              # 书籍元数据
├── Research/
│   └── books/
│       └── {bookId}/
│           ├── full_text.txt     # 下载的内容
│           ├── introduction.md   # Agent生成、用户可编辑
│           ├── notes.md          # 用户笔记
│           └── sources/
│               ├── wikipedia.md  # Agent收集的研究
│               └── reviews.md
├── Chats/
│   └── {conversationId}.json     # 聊天历史
├── Profile/
│   └── profile.md                # 用户阅读配置文件
└── context.md                    # Agent的积累知识
```

**工作方式：**

1. 用户添加书籍 → 在`library.json`中创建条目
2. Agent下载文本 → 保存到`Research/books/{id}/full_text.txt`
3. Agent进行研究 → 保存到`sources/`
4. Agent生成介绍 → 保存到`introduction.md`
5. 用户编辑介绍 → Agent在下一次读取时看到更改
6. Agent用学到的内容更新`context.md`
</examples>

<checklist>
## 文件作为通用接口检查清单

### 组织
- [ ] 实体范围目录（`{type}/{id}/`）
- [ ] 一致的命名约定
- [ ] 临时 vs 持久分离
- [ ] Markdown用于人类内容，JSON用于结构化数据

### context.md
- [ ] Agent在会话开始时读取context
- [ ] Agent在学习时更新context
- [ ] 包含：身份、用户知识、存在的东西、指导原则
- [ ] 在会话间持续

### 冲突处理
- [ ] 冲突模型定义（最后写入优先、写入前检查等）
- [ ] 系统提示中的Agent指导
- [ ] iCloud冲突监控（如适用）

### 集成
- [ ] UI观察文件更改（或共享服务）
- [ ] Agent可以读取用户编辑
- [ ] 用户可以检查Agent输出
</checklist>
