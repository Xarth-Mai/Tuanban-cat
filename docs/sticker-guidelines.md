# 贴图规范与扩展约定

正式主资产：单张 **1024×1024 静态 WebP**，RGB、不透明、奶油色背景，单一明确情绪。
主体约占画面 65–75% 为创作目标，留出耳朵、尾巴和动作符号的安全边距；不机械裁切以追求占比。
线条粗细与已有系列协调，可用少量爱心、问号、蒸汽、星光或动作线，不依赖大段文字。

## 命名与目录

`assets/stickers/{category}/{id}.webp`，例如 `assets/stickers/greeting/greeting-wave.webp`。
ID 用稳定的小写短横线格式，不使用中文路径或临时序号。同一 ID 的修改递增 `version`。
图片建议小于 512 KiB，校验器当前硬上限为 2 MiB；清晰度优先于极限压缩。

已有分类：greeting、happy、confused、comfort。
预留分类：sleepy、daily、playful、shy、love。尚未有图片的分类显示真实空态，不填占位图。
未来 work、weather、holiday 等新增分类需同步更新前端筛选、清单校验与文档。

## 数据源

手工编辑 `data/stickers.json`，包含 id、title、filename、category、mood、keywords、description、
story、is_featured、version。description 描述实际画面，story 记录适合的社交使用场景，不能虚构不存在的道具。
关键词使用自然中文，mood 使用便于机器复用的英文情绪词。

运行 `python3 scripts/build_manifest.py` 生成普通 JS 数据和完整 manifest。不得只改生成文件；
CI 通过 `--check` 检查它们与源 JSON、文件哈希同步。

## 使用节奏

一张图表达一个主要情绪。通常每回合一张足够，连续贴图应跟随用户的互动意愿。
安慰先尊重真实情绪，不把拥抱强加给别人；表示疑惑时不讽刺。图库是表达材料，不替下游 Agent 定义人格。
没有合适贴图时文字也很好。路径或接口成功不等于图片实际送达，下游应如实处理投递状态。
