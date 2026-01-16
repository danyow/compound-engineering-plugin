<overview>
在构建需要凭证（API key、token、secret）的 API 调用的 skill 时，遵循此协议以防止凭证出现在聊天中。
</overview>

<the_problem>
原始的 curl 命令会暴露环境变量中的凭证：

```bash
# ❌ 错误 - API key 在聊天中可见
curl -H "Authorization: Bearer $API_KEY" https://api.example.com/data
```

当 Claude 执行此命令时，展开 `$API_KEY` 后的完整命令会出现在对话中。
</the_problem>

<the_solution>
使用 `~/.claude/scripts/secure-api.sh` - 一个在内部加载凭证的包装器。

<for_supported_services>
```bash
# ✅ 正确 - 凭证不可见
~/.claude/scripts/secure-api.sh <service> <operation> [args]

# 示例：
~/.claude/scripts/secure-api.sh facebook list-campaigns
~/.claude/scripts/secure-api.sh ghl search-contact "email@example.com"
```
</for_supported_services>

<adding_new_services>
当构建需要 API 调用的新 skill 时：

1. **将操作添加到包装器** (`~/.claude/scripts/secure-api.sh`)：

```bash
case "$SERVICE" in
    yourservice)
        case "$OPERATION" in
            list-items)
                curl -s -G \
                    -H "Authorization: Bearer $YOUR_API_KEY" \
                    "https://api.yourservice.com/items"
                ;;
            get-item)
                ITEM_ID=$1
                curl -s -G \
                    -H "Authorization: Bearer $YOUR_API_KEY" \
                    "https://api.yourservice.com/items/$ITEM_ID"
                ;;
            *)
                echo "Unknown operation: $OPERATION" >&2
                exit 1
                ;;
        esac
        ;;
esac
```

2. **将配置文件支持添加到包装器**（如果服务需要多个账户）：

```bash
# In secure-api.sh, add to profile remapping section:
yourservice)
    SERVICE_UPPER="YOURSERVICE"
    YOURSERVICE_API_KEY=$(eval echo \$${SERVICE_UPPER}_${PROFILE_UPPER}_API_KEY)
    YOURSERVICE_ACCOUNT_ID=$(eval echo \$${SERVICE_UPPER}_${PROFILE_UPPER}_ACCOUNT_ID)
    ;;
```

3. **使用配置文件命名将凭证占位符添加到 `~/.claude/.env`**：

```bash
# Check if entries already exist
grep -q "YOURSERVICE_MAIN_API_KEY=" ~/.claude/.env 2>/dev/null || \
  echo -e "\n# Your Service - Main profile\nYOURSERVICE_MAIN_API_KEY=\nYOURSERVICE_MAIN_ACCOUNT_ID=" >> ~/.claude/.env

echo "Added credential placeholders to ~/.claude/.env - user needs to fill them in"
```

4. **在你的 SKILL.md 中记录配置文件工作流**：

```markdown
## 配置文件选择工作流

**关键：** 始终使用配置文件选择以防止使用错误的账户凭证。

### 当用户请求 YourService 操作时：

1. **检查已保存的配置文件：**
   ```bash
   ~/.claude/scripts/profile-state get yourservice
   ```

2. **如果没有保存的配置文件，发现可用的配置文件：**
   ```bash
   ~/.claude/scripts/list-profiles yourservice
   ```

3. **如果只有一个配置文件：** 自动使用它并宣布：
   ```
   "使用 YourService 配置文件 'main' 列出项目..."
   ```

4. **如果有多个配置文件：** 询问用户使用哪一个：
   ```
   "使用哪个 YourService 配置文件：main、clienta 或 clientb？"
   ```

5. **保存用户的选择：**
   ```bash
   ~/.claude/scripts/profile-state set yourservice <selected_profile>
   ```

6. **在调用 API 前始终宣布使用哪个配置文件：**
   ```
   "使用 YourService 配置文件 'main' 列出项目..."
   ```

7. **使用配置文件进行 API 调用：**
   ```bash
   ~/.claude/scripts/secure-api.sh yourservice:<profile> list-items
   ```

## 安全的 API 调用

所有 API 调用使用配置文件语法：

```bash
~/.claude/scripts/secure-api.sh yourservice:<profile> <operation> [args]

# 示例：
~/.claude/scripts/secure-api.sh yourservice:main list-items
~/.claude/scripts/secure-api.sh yourservice:main get-item <ITEM_ID>
```

**配置文件在会话中持久：** 一旦选择，在后续操作中使用相同的配置文件，除非用户明确更改它。
```
</adding_new_services>
</the_solution>

<pattern_guidelines>
<simple_get_requests>
```bash
curl -s -G \
    -H "Authorization: Bearer $API_KEY" \
    "https://api.example.com/endpoint"
```
</simple_get_requests>

<post_with_json_body>
```bash
ITEM_ID=$1
curl -s -X POST \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d @- \
    "https://api.example.com/items/$ITEM_ID"
```

用法：
```bash
echo '{"name":"value"}' | ~/.claude/scripts/secure-api.sh service create-item
```
</post_with_json_body>

<post_with_form_data>
```bash
curl -s -X POST \
    -F "field1=value1" \
    -F "field2=value2" \
    -F "access_token=$API_TOKEN" \
    "https://api.example.com/endpoint"
```
</post_with_form_data>
</pattern_guidelines>

<credential_storage>
**位置：** `~/.claude/.env`（对所有 skill 全局，可从任何目录访问）

**格式：**
```bash
# Service credentials
SERVICE_API_KEY=your-key-here
SERVICE_ACCOUNT_ID=account-id-here

# Another service
OTHER_API_TOKEN=token-here
OTHER_BASE_URL=https://api.other.com
```

**在脚本中加载：**
```bash
set -a
source ~/.claude/.env 2>/dev/null || { echo "Error: ~/.claude/.env not found" >&2; exit 1; }
set +a
```
</credential_storage>

<best_practices>
1. **永远不要在 skill 示例中使用带 `$VARIABLE` 的原始 curl** - 始终使用包装器
2. **将所有操作添加到包装器** - 不要让用户弄清楚 curl 语法
3. **自动创建凭证占位符** - 在创建 skill 时立即向 `~/.claude/.env` 添加空字段
4. **将凭证保存在 `~/.claude/.env` 中** - 一个中心位置，处处可用
5. **记录每个操作** - 在 SKILL.md 中展示示例
6. **优雅地处理错误** - 检查缺失的环境变量，显示有用的错误消息
</best_practices>

<testing>
测试包装器而不暴露凭证：

```bash
# 此命令会出现在聊天中
~/.claude/scripts/secure-api.sh facebook list-campaigns

# 但 API key 永远不会出现 - 它们在脚本内部加载
```

验证凭证已加载：
```bash
# 检查 .env 是否存在
ls -la ~/.claude/.env

# 检查特定变量（不显示值）
grep -q "YOUR_API_KEY=" ~/.claude/.env && echo "API key configured" || echo "API key missing"
```
</testing>
