# Landing Page LaunchKit 刷新计划

## 概述

使用 LaunchKit 元素和实用技术写作风格（Hunt/Thomas、Joel Spolsky）审查并增强 `/docs/index.html` 着陆页。当前实现很强大，但可以逐节进行改进。

## 当前状态评估

### 运行良好的部分
- 具体的、结果导向的英雄标题（"30 秒内获得 12 位专家意见"）
- 开发者真实的文案（N+1 查询、CORS、SQL 注入）
- 统计部分，指标清晰（23 个 Agent、16 个 Command、11 个 Skill、2 个 MCP Server）
- 哲学部分，有具体故事（N+1 查询 bug）
- 三步安装，使用实际命令
- 按照 LaunchKit 模式的 FAQ 手风琴
- 分类的功能部分，带有代码示例

### 缺失元素（来自最佳实践研究）
1. **社会证明部分** - 没有推荐、GitHub 星标或用户指标
2. **视觉演示** - 没有显示工具运行的 GIF/动画
3. **CTA 上的箭头图标** - 研究显示转化率提升 26%
4. **信任指标** - 开源徽章、许可证信息

---

## 逐节审查计划

### 1. Hero 部分（第 56-78 行）

**当前：**
```html
<h1>Your Code Reviews Just Got 12 Expert Opinions. In 30 Seconds.</h1>
```

**审查清单：**
- [ ] 标题遵循实用写作（具体先于抽象）✅
- [ ] 眉线徽章是最新的（Version 2.6.0）- 需验证
- [ ] 描述段落少于 3 句 ✅
- [ ] 按钮组在主 CTA 上有箭头图标
- [ ] "Read the Docs" 辅助 CTA 存在 ✅

**可能的改进：**
- 在 "Install Plugin" 按钮上添加 `→` 箭头
- 考虑在按钮下方添加动画终端 GIF，展示 `/review` 的实际操作

### 2. 统计部分（第 81-104 行）

**当前：** 4 个统计卡片（23 个 Agent、16 个 Command、11 个 Skill、2 个 MCP Server）

**审查清单：**
- [ ] 数字准确（对照实际文件计数验证）
- [ ] 每个统计的图标都合适
- [ ] 悬停效果正常工作
- [ ] 移动布局（2x2 网格）可读

**可能的改进：**
- 如果有数据，添加"使用的开发者"或"运行的审查"指标
- 考虑在滚动时添加微妙动画

### 3. 哲学部分（第 107-192 行）

**当前：** "Why Your Third Code Review Should Be Easier Than Your First" 带有 N+1 查询故事

**审查清单：**
- [ ] 以具体故事开头（N+1 查询）✅
- [ ] 引用块令人难忘且可引用
- [ ] 四个支柱（Plan、Delegate、Assess、Codify）清晰
- [ ] 每个支柱有：标语、描述、工具标签
- [ ] 描述使用 "你" 的语气 ✅

**可能的改进：**
- 审查支柱描述中的被动语态
- 确保每个支柱描述遵循 PAS（问题、加剧、解决）模式
- 检查工具标签是否准确和最新

### 4. Agent 部分（第 195-423 行）

**当前：** 5 个类别中的 23 个 Agent（Review、Research、Design、Workflow、Docs）

**审查清单：**
- [ ] 列出所有 23 个 Agent（计算实际文件）
- [ ] 类别逻辑清晰且可扫描
- [ ] 每张卡片有：名称、徽章、描述、使用代码
- [ ] 描述是对话式的（非被动）
- [ ] 关键徽章（Security、Data）突出显示

**可能的改进：**
- 根据实用写作清单审查 Agent 描述
- 确保描述回答"我什么时候会使用这个？"
- 为通用描述添加具体场景

### 5. Command 部分（第 426-561 行）

**当前：** 2 个类别中的 16 个 Command（Workflow、Utility）

**审查清单：**
- [ ] 列出所有 16 个 Command（计算实际文件）
- [ ] 核心工作流 Command 突出显示
- [ ] 描述是面向行动的
- [ ] Command 名称与实际实现匹配

**可能的改进：**
- 审查 Command 描述中的被动语态
- 以结果而非功能为主导
- 在适当的地方添加"为您节省 X 分钟"的框架

### 6. Skill 部分（第 564-703 行）

**当前：** 3 个类别中的 11 个 Skill（Development、Content/Workflow、Image Generation）

**审查清单：**
- [ ] 列出所有 11 个 Skill（计算实际目录）
- [ ] 特色 Skill（gemini-imagegen）正确突出显示
- [ ] API 密钥要求清楚
- [ ] Skill 调用语法正确

**可能的改进：**
- 根据实用写作审查 Skill 描述
- 确保每个 Skill 回答"这解决了什么问题？"

### 7. MCP Server 部分（第 706-751 行）

**当前：** 2 个 MCP Server（Playwright、Context7）

**审查清单：**
- [ ] 工具列表准确
- [ ] 描述解释了为什么而不仅仅是什么
- [ ] 框架支持列表是最新的（100+）

**可能的改进：**
- 添加每个 Server 实际操作的具体示例
- 考虑前后对比

### 8. 安装部分（第 754-798 行）

**当前：** "Three Commands. Zero Configuration." 有 3 个步骤

**审查清单：**
- [ ] Command 准确且有效
- [ ] 步骤 3 显示实际使用示例
- [ ] 时间线视觉（垂直线）正确渲染
- [ ] 代码块上的复制按钮有效

**可能的改进：**
- 如果缺少，添加复制到剪贴板功能
- 考虑添加"您将看到什么"输出示例

### 9. FAQ 部分（第 801-864 行）

**当前：** 手风琴格式的 5 个问题

**审查清单：**
- [ ] 问题解决了真实的反对意见
- [ ] 答案是对话式的（使用"你"）
- [ ] 手风琴展开/折叠有效
- [ ] 答案中没有被动语态

**可能的改进：**
- 审查模糊词汇（"最佳实践建议"）
- 确保答案直接且可操作

### 10. CTA 部分（第 868-886 行）

**当前：** "Install Once. Compound Forever." 带有安装 + GitHub 按钮

**审查清单：**
- [ ] 徽章引人注目（"Free & Open Source"）
- [ ] 标题重申核心价值主张
- [ ] 主 CTA 有箭头图标 ✅
- [ ] 底部有信任线

**可能的改进：**
- 审查信任线文案
- 考虑添加社会证明元素

---

## 新增：社会证明部分（待添加）

**位置：** 在统计部分之后，哲学部分之前

**组件：**
- GitHub 星标计数器（动态或静态）
- "受 X 名开发者信任"指标
- 2-3 条推荐引语（如果有）
- 公司徽标（如适用）

**LaunchKit 模式：**
```html
<section class="social-proof-section">
  <div class="heading centered">
    <p class="paragraph m secondary">Trusted by developers at</p>
  </div>
  <div class="logo-grid">
    <!-- Company logos or GitHub badge -->
  </div>
</section>
```

---

## 实用写作风格清单（应用于所有文案）

### 五大法则
1. **具体先于抽象** - 先故事/示例，然后原则
2. **物理类比** - 导入读者理解的隐喻
3. **对话式语域** - 使用 "你"、缩写、旁白
4. **编号框架** - 创建可引用的结构
5. **作为架构的幽默** - 密集内容的心理锚点

### 需要查找和修复的反模式
- [ ] "It is recommended that..." → "这样做："
- [ ] "Best practices suggest..." → "这是有效的方法："
- [ ] 被动语态 → 主动语态
- [ ] 抽象声明 → 具体示例
- [ ] 大段文字 → 可扫描列表

### 质量清单（每节）
- [ ] 以具体故事或示例开头？
- [ ] 读者能通过浏览标题获得整体脉络吗？
- [ ] 至少使用一次 "你"？
- [ ] 读者可以采取的明确行动？
- [ ] 大声朗读像口语吗？

---

## 实施阶段

### 阶段 1：文案审计（无 HTML 更改）
1. 通读整个页面
2. 标记被动语态实例
3. 标记没有示例的抽象声明
4. 标记缺少 "你" 的语气
5. 记录需要改进的地方

### 阶段 2：文案重写
1. 按照实用风格重写标记的部分
2. 确保每节通过质量清单
3. 保持现有 HTML 结构

### 阶段 3：组件添加
1. 在主 CTA 上添加箭头图标
2. 添加社会证明部分（如果有数据）
3. 考虑视觉演示元素

### 阶段 4：验证
1. 验证所有计数（Agent、Command、Skill）
2. 测试所有链接和按钮
3. 验证移动响应性
4. 检查可访问性

---

## 需要修改的文件

| File | Changes |
|------|---------|
| `docs/index.html` | 文案重写、可能的新部分 |
| `docs/css/style.css` | 社会证明样式（如果添加） |

---

## 成功标准

1. 所有文案通过实用写作质量清单
2. 任何描述中都没有被动语态
3. 每个功能部分都回答"我为什么要关心？"
4. 统计数据与实际文件计数准确
5. 页面在 <3 秒内加载
6. 移动布局完全正常

---

## 参考资料

- LaunchKit Template: https://launchkit.evilmartians.io/
- Pragmatic Writing Skill: `~/.claude/skills/pragmatic-writing-skill/SKILL.md`
- Current Landing Page: `/Users/kieranklaassen/every-marketplace/docs/index.html`
- Style CSS: `/Users/kieranklaassen/every-marketplace/docs/css/style.css`
