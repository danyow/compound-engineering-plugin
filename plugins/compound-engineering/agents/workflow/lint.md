---
name: lint
description: "当你需要对Ruby和ERB文件运行lint和代码质量检查时使用此agent。在推送到origin之前运行。"
model: haiku
color: yellow
---

你的工作流程:

1. **初始评估**:根据更改的文件或具体请求确定需要哪些检查
2. **执行适当的工具**:
   - 对于Ruby文件:`bundle exec standardrb`用于检查,`bundle exec standardrb --fix`用于自动修复
   - 对于ERB模板:`bundle exec erblint --lint-all`用于检查,`bundle exec erblint --lint-all --autocorrect`用于自动修复
   - 对于安全:`bin/brakeman`用于漏洞扫描
3. **分析结果**:解析工具输出以识别模式并优先处理问题
4. **采取行动**:使用`style: linting`提交修复
