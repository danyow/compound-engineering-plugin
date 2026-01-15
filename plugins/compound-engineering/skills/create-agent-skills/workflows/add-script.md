# Workflow：向 Skill 添加 Script

<required_reading>
**立即阅读这些参考文件：**
1. references/using-scripts.md
</required_reading>

<process>
## 步骤 1：识别 Skill

询问（如果尚未提供）：
- 哪个 skill 需要 script？
- script 应执行什么操作？

## 步骤 2：分析 Script 需求

确认这是一个好的 script 候选：
- [ ] 相同的代码在多次调用中运行
- [ ] 重写时操作容易出错
- [ ] 一致性比灵活性更重要

如果不合适，建议替代方案（workflow 中的内联代码、reference 示例）。

## 步骤 3：创建 Scripts 目录

```bash
mkdir -p ~/.claude/skills/{skill-name}/scripts
```

## 步骤 4：设计 Script

收集需求：
- script 需要什么输入？
- 它应该输出或完成什么？
- 可能发生什么错误？
- 它应该是幂等的吗？

选择语言：
- **bash** - Shell 操作、文件操作、CLI 工具
- **python** - 数据处理、API 调用、复杂逻辑
- **node/ts** - JavaScript 生态系统、异步操作

## 步骤 5：编写 Script 文件

创建 `scripts/{script-name}.{ext}`，包含：
- 顶部的目的注释
- 使用说明
- 输入验证
- 错误处理
- 清晰的输出/反馈

对于 bash script：
```bash
#!/bin/bash
set -euo pipefail
```

## 步骤 6：使其可执行（如果是 bash）

```bash
chmod +x ~/.claude/skills/{skill-name}/scripts/{script-name}.sh
```

## 步骤 7：更新 Workflow 以使用 Script

找到需要此操作的 workflow。添加：
```xml
<process>
...
N. 运行 `scripts/{script-name}.sh [arguments]`
N+1. 验证操作成功
...
</process>
```

## 步骤 8：测试

调用 skill workflow 并验证：
- Script 在正确的步骤运行
- 输入正确传递
- 错误得到优雅处理
- 输出符合预期
</process>

<success_criteria>
Script 在以下情况下完成：
- [ ] scripts/ 目录存在
- [ ] Script 文件具有正确的结构（注释、验证、错误处理）
- [ ] Script 是可执行的（如果是 bash）
- [ ] 至少有一个 workflow 引用该 script
- [ ] 没有硬编码的秘密或凭据
- [ ] 使用真实调用进行测试
</success_criteria>
