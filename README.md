# 团斑 / Tuanban

> 一只把小情绪捧在爪心里的猫。

![团斑抱着热热的爪印杯](assets/character/cover.webp)

**Tuanban-cat** 是围绕原创小猫「团斑」构建的独立角色与素材仓库：角色设定、故事、视觉规范、
正式贴图库、可复用元数据，以及可在本地直接打开的角色主页。

团斑是温柔、慢热、容易害羞的灰白花小女猫。她喜欢热饮和软垫，也认真对待开心、疑惑和说不出口
的小情绪。正面画面右侧的大块灰斑、圆脸、粉色耳朵和软爪垫，是认出她的线索。

本仓库独立于 [Hermes Lively](https://github.com/Xarth-Mai/Hermes-Plugin-Lively)。其他项目可以消费
manifest 复用素材，但本站不需要 Hermes、Node、模型服务或任何后端。

## 本地预览

最简单：clone 后直接双击 **index.html**。页面使用普通脚本加载数据，不用 `fetch` 读取 JSON，
支持 `file://`，没有构建步骤、外部字体、统计服务或 CDN 依赖。

```bash
git clone https://github.com/Xarth-Mai/Tuanban-cat.git
cd Tuanban-cat
python3 -m http.server 8000
```

也可打开 <http://localhost:8000>。Python 服务器是可选的，不是运行前提。

主页包含角色资料、故事、视觉参考与色板、图库筛选和使用说明。贴图支持按分类、中文关键词、
英文情绪搜索；点击看大图，使用左右方向键切换、Esc 关闭，也可以直接保存 WebP。
页面中的文档链接是源 Markdown 文件；直接打开时可能由浏览器显示原文或下载。

## 角色设定

| 项目 | 设定 |
| --- | --- |
| 名字 | 团斑 / Tuanban |
| 性别 | 女孩子 |
| 物种 / 品种 | 家猫 / 中华田园猫（灰白花），mixed domestic shorthair |
| 形象年龄 | 幼年感的小猫 |
| 生日 | 11 月 14 日，虚构角色设定生日 |
| 性格 | 温柔、慢热、害羞、细腻、偶尔呆萌 |
| 喜欢 | 热饮、软垫、陪伴、被夸、发呆 |
| 不喜欢 | 突然的大动静、被催促、过于严肃的气氛 |

完整资料见 [角色小传](docs/character-profile.md)、[视觉规范](docs/visual-guidelines.md) 和
[贴图创作规范](docs/sticker-guidelines.md)。角色数据在 `data/character.js`，故事在 `data/lore.js`。
灰斑的“右侧”统一指正面画面的右侧，即角色自身左侧，不应为不同姿势随意镜像。

## 正式贴图库 · 第一辑 12 张

| 分类 | 内容 |
| --- | --- |
| greeting · 问候 | 挥爪问好、探头打招呼、小小挥爪 |
| happy · 开心 | 开心举爪、开心小心心、原地蹦蹦 |
| confused · 疑惑 | 歪头问号、小小发愣、思考中 |
| comfort · 安慰 | 递一个抱抱、抱杯陪伴、轻轻拍拍 |

正式贴图均为 **1024×1024、静态、不透明 WebP**，奶油色底、暖棕线条，约 60–90 KiB / 张。
前四种情绪的新正式版为 `greeting-wave`、`happy-cheer`、`confused-tilt`、`comfort-hug`，是重新绘制
的独立图像，并非把旧版 192px 示例放大。本次后续整理只使用已经生成的图片，没有继续生图。

筛选栏也列出 sleepy、daily、playful、shy、love，目前标为零张，留给后续补充；不会显示虚构素材。
现有角色设定图提供正面、背面和表情参考，**独立正背侧三视图尚未齐备，侧视图待补充**。
本轮没有为补齐三视图继续绘画，也没有把其他姿势冒充侧视参考。

## 目录与元数据

```text
index.html / styles.css / app.js        # 无构建预览站
data/
  character.js / lore.js                # 角色与故事，普通浏览器全局变量
  stickers.json                        # 贴图元数据唯一手工编辑源
  stickers.js                          # 生成：window.TUANBAN_STICKERS
  manifest.json                        # 生成：可供其他项目读取的完整清单
assets/
  character/                           # cover、现有角色设定图（WebP）
  stickers/{category}/                  # 12 张正式 WebP
  previews/                            # 社交预览图，复用现有图像
docs/                                  # 设定、视觉、贴图规范、变更记录
scripts/                               # 清单构建、标准库校验、可选 WebP 导出
tests/                                 # 数据与浏览器行为检查
```

`data/stickers.json` 每项包含 `id`、`title`、`filename`、`category`、`mood`、`keywords`、
`description`、`story`、`is_featured`、`version`。`filename` 相对于仓库根目录。
生成的 `data/manifest.json` 另含格式、许可、每张图的尺寸、字节数和 SHA-256；
下游应以 manifest 为入口，不解析网页、不依赖本地绝对路径。

`stickers.js` 与 JSON 使用同一份条目。JS 服务于本地预览，JSON 服务于程序复用；网页不请求 JSON。
从 v0.1 升级时请更新路径：旧 `stickers/*.png` 与旧 manifest 已由上述正式体系替代，历史版本可在 Git 中取得。

## 新增与验证

日常浏览不需要安装任何依赖。数据和文件格式检查只需要 Python 3.10+ 标准库：

```bash
python3 scripts/build_manifest.py          # 修改 stickers.json 后重新生成 JS 与 manifest
python3 scripts/build_manifest.py --check  # 只检查同步，不改文件
python3 scripts/validate_assets.py         # 检查格式、尺寸、透明、路径、清单与链接
python3 -m unittest discover -s tests -v
```

`python3 scripts/validate.py` 保留为新校验器的兼容入口。CI 自动运行上述检查。
需要导出新素材时，可选安装 Pillow，使用 `scripts/export_webp.py`；该脚本仅转换格式，拒绝放大
不足 1024px 的小图。详见 [贡献指南](CONTRIBUTING.md)。
可选的浏览器验证见 `tests/browser_check.py`，仅用于开发，不是预览站依赖。

## 许可与后续计划

角色资料、图像、元数据及代码按 [MPL-2.0](LICENSE) 发布，限于贡献者依法可许可的权利。
允许依许可使用、复制、修改和再分发；分发时保留许可通知，并满足 MPL 适用的源文件提供条件。
商用或再分发时，欢迎保留团斑署名和仓库链接；此建议不替代许可证的具体要求。

名称与图像目前未声明注册商标，MPL 不授予商标权。图像采用 AI 辅助生成并经过筛选、整理，
不承诺每个生成像素具备可版权性或角色名称已完成商标检索。详见 [素材说明](ASSET-NOTICE.md)。

后续按实际需要扩充困困、日常、玩闹、害羞和亲近；独立三视图也是待办，尚未完成的内容不计入当前资产数。
