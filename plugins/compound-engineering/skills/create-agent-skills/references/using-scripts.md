# 在 Skill 中使用脚本

<purpose>
脚本是 Claude 按原样运行的可执行代码，而不是每次都重新生成。它们确保可靠、无错误地执行重复操作。
</purpose>

<when_to_use>
在以下情况下使用脚本：
- 相同的代码在多次 skill 调用中运行
- 从头重写时操作容易出错
- 涉及复杂的 shell 命令或 API 交互
- 一致性比灵活性更重要

常见的脚本类型：
- **部署** - 部署到 Vercel、发布包、推送发布
- **设置** - 初始化项目、安装依赖项、配置环境
- **API 调用** - 认证请求、webhook 处理程序、数据获取
- **数据处理** - 转换文件、批处理操作、迁移
- **构建过程** - 编译、打包、测试运行器
</when_to_use>

<script_structure>
脚本位于 skill 目录内的 `scripts/` 中：

```
skill-name/
├── SKILL.md
├── workflows/
├── references/
├── templates/
└── scripts/
    ├── deploy.sh
    ├── setup.py
    └── fetch-data.ts
```

结构良好的脚本包括：
1. 顶部的清晰目的注释
2. 输入验证
3. 错误处理
4. 尽可能的幂等操作
5. 清晰的输出/反馈
</script_structure>

<script_example>
```bash
#!/bin/bash
# deploy.sh - 部署项目到 Vercel
# 用法：./deploy.sh [environment]
# 环境：preview（默认）、production

set -euo pipefail

ENVIRONMENT="${1:-preview}"

# 验证环境
if [[ "$ENVIRONMENT" != "preview" && "$ENVIRONMENT" != "production" ]]; then
    echo "Error: Environment must be 'preview' or 'production'"
    exit 1
fi

echo "Deploying to $ENVIRONMENT..."

if [[ "$ENVIRONMENT" == "production" ]]; then
    vercel --prod
else
    vercel
fi

echo "Deployment complete."
```
</script_example>

<workflow_integration>
工作流像这样引用脚本：

```xml
<process>
## Step 5: 部署

1. 确保所有测试通过
2. 运行 `scripts/deploy.sh production`
3. 验证部署成功
4. 使用部署 URL 更新用户
</process>
```

工作流告诉 Claude 何时运行脚本。脚本处理操作如何执行。
</workflow_integration>

<best_practices>
**应该：**
- 使脚本幂等（多次运行安全）
- 包含清晰的用法注释
- 执行前验证输入
- 提供有意义的错误消息
- 在 bash 脚本中使用 `set -euo pipefail`

**不应该：**
- 硬编码秘密或凭证（使用环境变量）
- 为一次性操作创建脚本
- 跳过错误处理
- 使脚本做太多不相关的事情
- 忘记使脚本可执行（`chmod +x`）
</best_practices>

<security_considerations>
- 永远不要在脚本中嵌入 API key、token 或 secret
- 对敏感配置使用环境变量
- 验证和清理任何用户提供的输入
- 对删除或修改数据的脚本要谨慎
- 考虑为破坏性操作添加 `--dry-run` 选项
</security_considerations>
