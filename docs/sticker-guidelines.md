# 贴图创作规范

正式贴图统一为 **1024×1024、静态、不透明的 RGB WebP**，使用奶油色背景，一张图片表达一个主要情绪。

主体建议占画面约 65–75%，给耳朵、尾巴、动作符号留出空间。线条与现有系列协调，可以使用少量爱心、问号、星光或动作线，不依赖大段文字。

## 分类与命名

图片路径为 `assets/stickers/{category}/{id}.webp`，例如 `assets/stickers/greeting/greeting-wave.webp`。ID 使用稳定的小写短横线格式，已有作品修改时递增 `version`。

当前已有四类：`greeting`、`happy`、`confused`、`comfort`。更多分类随实际作品加入；新增分类时同步更新网页标签、构建校验与相关测试。

图片建议小于 512 KiB，校验硬上限为 2 MiB；不要为了压缩牺牲清晰度。

## 元数据

只编辑 `data/stickers.json`。每个条目包含 `id`、`title`、`filename`、`category`、`mood`、`keywords`、`description`、`story`、`is_featured` 和 `version`。

- `description`：客观描述画面中的动作、表情与道具
- `story`：适合在怎样的对话或日常情境使用
- `keywords`：自然中文检索词
- `mood`：供程序复用的英文情绪词

运行 `python3 scripts/build_manifest.py` 生成供网页使用的 `stickers.js` 和供外部项目使用的 `manifest.json`。CI 会检查生成文件与资源哈希的一致性。

## 表达原则

表情是表达素材，不替下游 Agent 定义人格。安慰先尊重真实情绪，亲近与拥抱应考虑对方意愿，疑惑不等于嘲讽。没有合适图片时，使用文字即可。

下游使用时也应如实处理发送结果：图片路径存在或上传成功，不代表最终消息已送达。
