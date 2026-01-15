---
name: skill-creator
description: 创建有效 skill 的指南。当用户想要创建新 skill（或更新现有 skill）以通过专业知识、工作流程或工具集成扩展 Claude 的能力时，应使用此 skill。
license: 完整条款见 LICENSE.txt
---

# Skill Creator

此 skill 提供创建有效 skill 的指导。

## 关于 Skill

Skill 是模块化、自包含的包，通过提供专业知识、工作流程和工具来扩展 Claude 的能力。可以把它们看作特定领域或任务的"入职指南"——它们将 Claude 从通用 agent 转变为装备了任何模型都无法完全拥有的程序性知识的专业 agent。

### Skill 提供什么

1. 专业工作流程 - 特定领域的多步骤程序
2. 工具集成 - 处理特定文件格式或 API 的说明
3. 领域专业知识 - 公司特定知识、schema、业务逻辑
4. 捆绑资源 - 用于复杂和重复任务的脚本、参考资料和资源

### Skill 的结构

每个 skill 由必需的 SKILL.md 文件和可选的捆绑资源组成：

```
skill-name/
├── SKILL.md（必需）
│   ├── YAML frontmatter 元数据（必需）
│   │   ├── name:（必需）
│   │   └── description:（必需）
│   └── Markdown 说明（必需）
└── 捆绑资源（可选）
    ├── scripts/          - 可执行代码（Python/Bash 等）
    ├── references/       - 按需加载到上下文中的文档
    └── assets/           - 输出中使用的文件（模板、图标、字体等）
```

#### SKILL.md（必需）

**元数据质量：** YAML frontmatter 中的 `name` 和 `description` 决定 Claude 何时使用该 skill。具体说明 skill 的功能和使用时机。使用第三人称（例如"This skill should be used when..."而非"Use this skill when..."）。

#### 捆绑资源（可选）

##### Scripts (`scripts/`)

用于需要确定性可靠性或反复重写的任务的可执行代码（Python/Bash 等）。

- **何时包含**：当相同代码被反复重写或需要确定性可靠性时
- **示例**：`scripts/rotate_pdf.py` 用于 PDF 旋转任务
- **优势**：token 高效、确定性、可在不加载到上下文的情况下执行
- **注意**：Claude 可能仍需要读取脚本以进行修补或环境特定调整

##### References (`references/`)

按需加载到上下文中以指导 Claude 的流程和思考的文档和参考材料。

- **何时包含**：Claude 在工作时应该参考的文档
- **示例**：`references/finance.md` 用于财务 schema，`references/mnda.md` 用于公司 NDA 模板，`references/policies.md` 用于公司政策，`references/api_docs.md` 用于 API 规范
- **用例**：数据库 schema、API 文档、领域知识、公司政策、详细工作流程指南
- **优势**：保持 SKILL.md 精简，仅在 Claude 确定需要时加载
- **最佳实践**：如果文件较大（>10k 词），在 SKILL.md 中包含 grep 搜索模式
- **避免重复**：信息应该存在于 SKILL.md 或 references 文件中，而非两者都有。除非确实是 skill 的核心内容，否则优先使用 references 文件存储详细信息——这样可以保持 SKILL.md 精简，同时使信息可发现而不占用上下文窗口。在 SKILL.md 中仅保留基本的程序性说明和工作流程指导；将详细的参考材料、schema 和示例移至 references 文件。

##### Assets (`assets/`)

不打算加载到上下文中，而是在 Claude 生成的输出中使用的文件。

- **何时包含**：当 skill 需要在最终输出中使用的文件时
- **示例**：`assets/logo.png` 用于品牌资产，`assets/slides.pptx` 用于 PowerPoint 模板，`assets/frontend-template/` 用于 HTML/React 样板，`assets/font.ttf` 用于排版
- **用例**：模板、图像、图标、样板代码、字体、被复制或修改的示例文档
- **优势**：将输出资源与文档分离，使 Claude 可以使用文件而不将其加载到上下文中

### 渐进披露设计原则

Skill 使用三级加载系统来高效管理上下文：

1. **元数据（name + description）** - 始终在上下文中（~100 词）
2. **SKILL.md 正文** - 当 skill 触发时（<5k 词）
3. **捆绑资源** - 根据 Claude 需要（无限制*）

*无限制是因为脚本可以在不读入上下文窗口的情况下执行。

## Skill 创建流程

要创建 skill，请按顺序遵循"Skill 创建流程"，仅在有明确理由说明某步骤不适用时才跳过。

### 步骤 1：通过具体示例理解 Skill

仅当已清楚理解 skill 的使用模式时才跳过此步骤。即使在处理现有 skill 时，此步骤仍然有价值。

要创建有效的 skill，需清楚理解如何使用该 skill 的具体示例。这种理解可以来自用户直接提供的示例，或生成后通过用户反馈验证的示例。

例如，在构建 image-editor skill 时，相关问题包括：

- "image-editor skill 应该支持什么功能？编辑、旋转，还是其他？"
- "能给出一些如何使用此 skill 的示例吗？"
- "我可以想象用户会问'从这张图片中去除红眼'或'旋转这张图片'。你能想到其他使用此 skill 的方式吗？"
- "用户会说什么来触发此 skill？"

为避免让用户不知所措，避免在单条消息中提出太多问题。从最重要的问题开始，根据需要进行跟进以提高效果。

当清楚了解 skill 应该支持的功能时，结束此步骤。

### 步骤 2：规划可重用的 Skill 内容

要将具体示例转化为有效的 skill，通过以下方式分析每个示例：

1. 考虑如何从头开始执行该示例
2. 识别在重复执行这些工作流程时哪些脚本、参考资料和资源会有帮助

示例：构建 `pdf-editor` skill 来处理"帮我旋转这个 PDF"之类的查询时，分析显示：

1. 旋转 PDF 每次都需要重写相同的代码
2. `scripts/rotate_pdf.py` 脚本存储在 skill 中会有帮助

示例：设计 `frontend-webapp-builder` skill 来处理"给我构建一个待办事项应用"或"给我构建一个跟踪我步数的仪表板"之类的查询时，分析显示：

1. 编写前端 webapp 每次都需要相同的 HTML/React 样板
2. 包含样板 HTML/React 项目文件的 `assets/hello-world/` 模板存储在 skill 中会有帮助

示例：构建 `big-query` skill 来处理"今天有多少用户登录？"之类的查询时，分析显示：

1. 查询 BigQuery 每次都需要重新发现表 schema 和关系
2. 记录表 schema 的 `references/schema.md` 文件存储在 skill 中会有帮助

要确定 skill 的内容，分析每个具体示例，创建要包含的可重用资源列表：脚本、参考资料和资源。

### 步骤 3：初始化 Skill

此时，是时候实际创建 skill 了。

仅当正在开发的 skill 已存在且需要迭代或打包时才跳过此步骤。在这种情况下，继续下一步。

从头创建新 skill 时，始终运行 `init_skill.py` 脚本。该脚本方便地生成新的模板 skill 目录，自动包含 skill 所需的一切，使 skill 创建过程更加高效和可靠。

用法：

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

该脚本：

- 在指定路径创建 skill 目录
- 生成带有正确 frontmatter 和 TODO 占位符的 SKILL.md 模板
- 创建示例资源目录：`scripts/`、`references/` 和 `assets/`
- 在每个目录中添加可自定义或删除的示例文件

初始化后，根据需要自定义或删除生成的 SKILL.md 和示例文件。

### 步骤 4：编辑 Skill

编辑（新生成的或现有的）skill 时，记住该 skill 是为另一个 Claude 实例使用而创建的。专注于包含对 Claude 有益且非显而易见的信息。考虑哪些程序性知识、领域特定细节或可重用资源能帮助另一个 Claude 实例更有效地执行这些任务。

#### 从可重用的 Skill 内容开始

要开始实现，从上面识别的可重用资源开始：`scripts/`、`references/` 和 `assets/` 文件。注意此步骤可能需要用户输入。例如，实现 `brand-guidelines` skill 时，用户可能需要提供品牌资产或模板以存储在 `assets/` 中，或提供文档以存储在 `references/` 中。

另外，删除 skill 不需要的任何示例文件和目录。初始化脚本在 `scripts/`、`references/` 和 `assets/` 中创建示例文件以演示结构，但大多数 skill 不会需要所有这些。

#### 更新 SKILL.md

**写作风格：** 使用**祈使/不定式形式**（动词优先的说明）编写整个 skill，而非第二人称。使用客观、指导性的语言（例如"To accomplish X, do Y"而非"You should do X"或"If you need to do X"）。这保持了 AI 使用的一致性和清晰度。

要完成 SKILL.md，回答以下问题：

1. 该 skill 的目的是什么，用几句话说明？
2. 何时应使用该 skill？
3. 实际上，Claude 应该如何使用该 skill？上面开发的所有可重用 skill 内容都应被引用，以便 Claude 知道如何使用它们。

### 步骤 5：打包 Skill

一旦 skill 准备就绪，应将其打包成可分发的 zip 文件以与用户共享。打包过程会自动首先验证 skill 以确保满足所有要求：

```bash
scripts/package_skill.py <path/to/skill-folder>
```

可选的输出目录指定：

```bash
scripts/package_skill.py <path/to/skill-folder> ./dist
```

打包脚本将：

1. **验证** skill，自动检查：
   - YAML frontmatter 格式和必需字段
   - Skill 命名约定和目录结构
   - 描述的完整性和质量
   - 文件组织和资源引用

2. **打包** skill（如果验证通过），创建以 skill 命名的 zip 文件（例如 `my-skill.zip`），包含所有文件并保持适当的目录结构以供分发。

如果验证失败，脚本将报告错误并退出而不创建包。修复任何验证错误并再次运行打包命令。

### 步骤 6：迭代

测试 skill 后，用户可能会请求改进。这通常发生在使用 skill 之后，带着 skill 表现的新鲜上下文。

**迭代工作流程：**
1. 在实际任务中使用 skill
2. 注意困难或低效之处
3. 识别 SKILL.md 或捆绑资源应如何更新
4. 实施更改并再次测试
