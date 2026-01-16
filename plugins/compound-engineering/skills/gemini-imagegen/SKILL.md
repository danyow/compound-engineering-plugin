---
name: gemini-imagegen
description: 使用 Gemini API (Nano Banana Pro) 生成和编辑图像时应使用此技能。适用于从文本提示创建图像、编辑现有图像、应用风格迁移、生成带文字的 Logo、创建贴纸、产品效果图或任何图像生成/处理任务。支持文本生成图像、图像编辑、多轮细化以及多张参考图像的合成。
---

# Gemini 图像生成 (Nano Banana Pro)

使用 Google 的 Gemini API 生成和编辑图像。必须设置环境变量 `GEMINI_API_KEY`。

## 默认模型

| Model | Resolution | 最适合 |
|-------|------------|----------|
| `gemini-3-pro-image-preview` | 1K-4K | 所有图像生成（默认） |

**注意：** 始终使用此 Pro 模型。仅在明确要求时才使用其他模型。

## 快速参考

### 默认设置
- **Model:** `gemini-3-pro-image-preview`
- **Resolution:** 1K（默认，可选：1K、2K、4K）
- **Aspect Ratio:** 1:1（默认）

### 可用的宽高比
`1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`

### 可用的分辨率
`1K`（默认）、`2K`、`4K`

## 核心 API 模式

```python
import os
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# 基础生成（1K，1:1 - 默认值）
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=["Your prompt here"],
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
    ),
)

for part in response.parts:
    if part.text:
        print(part.text)
    elif part.inline_data:
        image = part.as_image()
        image.save("output.png")
```

## 自定义分辨率和宽高比

```python
from google.genai import types

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[prompt],
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio="16:9",  # 宽屏格式
            image_size="2K"       # 更高分辨率
        ),
    )
)
```

### 分辨率示例

```python
# 1K（默认）- 快速，适合预览
image_config=types.ImageConfig(image_size="1K")

# 2K - 质量/速度均衡
image_config=types.ImageConfig(image_size="2K")

# 4K - 最高质量，较慢
image_config=types.ImageConfig(image_size="4K")
```

### 宽高比示例

```python
# 正方形（默认）
image_config=types.ImageConfig(aspect_ratio="1:1")

# 横向宽屏
image_config=types.ImageConfig(aspect_ratio="16:9")

# 超宽全景
image_config=types.ImageConfig(aspect_ratio="21:9")

# 纵向
image_config=types.ImageConfig(aspect_ratio="9:16")

# 照片标准
image_config=types.ImageConfig(aspect_ratio="4:3")
```

## 编辑图像

传递现有图像和文本提示：

```python
from PIL import Image

img = Image.open("input.png")
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=["Add a sunset to this scene", img],
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
    ),
)
```

## 多轮细化

使用聊天进行迭代编辑：

```python
from google.genai import types

chat = client.chats.create(
    model="gemini-3-pro-image-preview",
    config=types.GenerateContentConfig(response_modalities=['TEXT', 'IMAGE'])
)

response = chat.send_message("Create a logo for 'Acme Corp'")
# 保存第一张图像...

response = chat.send_message("Make the text bolder and add a blue gradient")
# 保存细化后的图像...
```

## 提示词最佳实践

### 写实场景
包含相机细节：镜头类型、光照、角度、氛围。
> "一张写实的特写肖像，85mm 镜头，柔和的黄金时段光线，浅景深"

### 风格化艺术
明确指定风格：
> "可爱风格的快乐红熊猫贴纸，粗轮廓，卡通渲染，白色背景"

### 图像中的文字
明确字体样式和位置：
> "创建带有 'Daily Grind' 文字的 Logo，使用简洁的无衬线字体，黑白色，咖啡豆图案"

### 产品效果图
描述光照设置和表面：
> "抛光混凝土上的工作室灯光产品照片，三点柔光箱设置，45 度角"

## 高级功能

### Google Search 搜索增强
基于实时数据生成图像：

```python
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=["Visualize today's weather in Tokyo as an infographic"],
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        tools=[{"google_search": {}}]
    )
)
```

### 多张参考图像（最多 14 张）
从多个来源组合元素：

```python
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[
        "Create a group photo of these people in an office",
        Image.open("person1.png"),
        Image.open("person2.png"),
        Image.open("person3.png"),
    ],
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
    ),
)
```

## 重要：文件格式和媒体类型

**关键：** Gemini API 默认返回 JPEG 格式的图像。保存时始终使用 `.jpg` 扩展名以避免媒体类型不匹配。

```python
# 正确 - 使用 .jpg 扩展名（Gemini 返回 JPEG）
image.save("output.jpg")

# 错误 - 会导致"图像与媒体类型不匹配"错误
image.save("output.png")  # 创建了带 PNG 扩展名的 JPEG！
```

### 转换为 PNG（如需要）

如果特别需要 PNG 格式：

```python
from PIL import Image

# 使用 Gemini 生成
for part in response.parts:
    if part.inline_data:
        img = part.as_image()
        # 通过指定格式保存为 PNG
        img.save("output.png", format="PNG")
```

### 验证图像格式

使用 `file` 命令检查实际格式与扩展名：

```bash
file image.png
# 如果输出显示"JPEG image data" - 重命名为 .jpg！
```

## 注意事项

- 所有生成的图像都包含 SynthID 水印
- Gemini **默认返回 JPEG 格式** - 始终使用 `.jpg` 扩展名
- 仅图像模式（`responseModalities: ["IMAGE"]`）无法与 Google Search 搜索增强一起使用
- 对于编辑，以对话方式描述更改 - 模型理解语义蒙版
- 默认使用 1K 分辨率以提高速度；在质量至关重要时使用 2K/4K
