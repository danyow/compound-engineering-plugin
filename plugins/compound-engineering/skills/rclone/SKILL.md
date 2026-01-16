---
name: rclone
description: 使用 rclone 在云存储提供商之间上传、同步和管理文件。用于上传文件（图像、视频、文档）到 S3、Cloudflare R2、Backblaze B2、Google Drive、Dropbox 或任何 S3 兼容存储。触发词："上传到 S3"、"同步到云端"、"rclone"、"备份文件"、"上传视频/图像到存储桶"，或请求传输文件到远程存储。
---

# rclone 文件传输 Skill

## 设置检查（总是先运行）

在任何 rclone 操作之前，验证安装和配置：

```bash
# 检查 rclone 是否已安装
command -v rclone >/dev/null 2>&1 && echo "rclone installed: $(rclone version | head -1)" || echo "NOT INSTALLED"

# 列出已配置的远程
rclone listremotes 2>/dev/null || echo "NO REMOTES CONFIGURED"
```

### 如果 rclone 未安装

指导用户安装：

```bash
# macOS
brew install rclone

# Linux (脚本安装)
curl https://rclone.org/install.sh | sudo bash

# 或通过包管理器
sudo apt install rclone  # Debian/Ubuntu
sudo dnf install rclone  # Fedora
```

### 如果没有配置远程

引导用户完成交互式配置：

```bash
rclone config
```

**常见提供商设置快速参考：**

| 提供商 | 类型 | 关键设置 |
|----------|------|--------------|
| AWS S3 | `s3` | access_key_id, secret_access_key, region |
| Cloudflare R2 | `s3` | access_key_id, secret_access_key, endpoint (account_id.r2.cloudflarestorage.com) |
| Backblaze B2 | `b2` | account (keyID), key (applicationKey) |
| DigitalOcean Spaces | `s3` | access_key_id, secret_access_key, endpoint (region.digitaloceanspaces.com) |
| Google Drive | `drive` | OAuth 流程（打开浏览器） |
| Dropbox | `dropbox` | OAuth 流程（打开浏览器） |

**示例：配置 Cloudflare R2**
```bash
rclone config create r2 s3 \
  provider=Cloudflare \
  access_key_id=YOUR_ACCESS_KEY \
  secret_access_key=YOUR_SECRET_KEY \
  endpoint=ACCOUNT_ID.r2.cloudflarestorage.com \
  acl=private
```

**示例：配置 AWS S3**
```bash
rclone config create aws s3 \
  provider=AWS \
  access_key_id=YOUR_ACCESS_KEY \
  secret_access_key=YOUR_SECRET_KEY \
  region=us-east-1
```

## 常见操作

### 上传单个文件
```bash
rclone copy /path/to/file.mp4 remote:bucket/path/ --progress
```

### 上传目录
```bash
rclone copy /path/to/folder remote:bucket/folder/ --progress
```

### 同步目录（镜像，删除已移除的文件）
```bash
rclone sync /local/path remote:bucket/path/ --progress
```

### 列出远程内容
```bash
rclone ls remote:bucket/
rclone lsd remote:bucket/  # 仅目录
```

### 检查将要传输的内容（试运行）
```bash
rclone copy /path remote:bucket/ --dry-run
```

## 有用的标志

| 标志 | 用途 |
|------|---------|
| `--progress` | 显示传输进度 |
| `--dry-run` | 预览而不传输 |
| `-v` | 详细输出 |
| `--transfers=N` | 并行传输（默认 4） |
| `--bwlimit=RATE` | 带宽限制（例如 `10M`） |
| `--checksum` | 按校验和比较，而非大小/时间 |
| `--exclude="*.tmp"` | 排除模式 |
| `--include="*.mp4"` | 仅包含匹配的 |
| `--min-size=SIZE` | 跳过小于 SIZE 的文件 |
| `--max-size=SIZE` | 跳过大于 SIZE 的文件 |

## 大文件上传

对于视频和大文件，使用分块上传：

```bash
# S3 分段上传（>200MB 自动）
rclone copy large_video.mp4 remote:bucket/ --s3-chunk-size=64M --progress

# 恢复中断的传输
rclone copy /path remote:bucket/ --progress --retries=5
```

## 验证上传

```bash
# 检查文件是否存在并匹配
rclone check /local/file remote:bucket/file

# 获取文件信息
rclone lsl remote:bucket/path/to/file
```

## 故障排除

```bash
# 测试连接
rclone lsd remote:

# 调试连接问题
rclone lsd remote: -vv

# 检查配置
rclone config show remote
```
