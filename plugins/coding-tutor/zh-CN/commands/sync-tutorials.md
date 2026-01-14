# 同步 Coding Tutor 教程

将您的教程提交并推送到 GitHub 仓库以进行备份和移动阅读。

## 说明

1. **前往教程仓库**：`cd ~/coding-tutor-tutorials`

2. **检查更改**：运行 `git status` 查看新增或修改的内容

3. **如果有更改**：
   - 暂存所有更改：`git add -A`
   - 创建一个总结添加/更新内容的提交消息（例如，"Add tutorial on React hooks" 或 "Update quiz scores"）
   - 推送到远程：`git push`

4. **如果不存在 GitHub 远程仓库**：
   - 创建仓库：`gh repo create coding-tutor-tutorials --private --source=. --push`

5. **报告结果**：告诉用户同步了什么或一切都已是最新状态

## 注意事项

- 教程仓库位于：`~/coding-tutor-tutorials/`
- 创建 GitHub 仓库时始终使用 `--private`
- 这是您个人的学习旅程 - 保持备份！
