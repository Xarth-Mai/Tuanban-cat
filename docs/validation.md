# 本地验证记录

日期：2026-11-14。本轮继续工作仅整理既有图像、编写站点/数据/文档，没有继续调用生图工具。

## 已验证

- `python3 scripts/build_manifest.py --check`：浏览器普通 JS、下游 JSON manifest 与唯一数据源同步。
- `python3 scripts/validate_assets.py`：12 张贴图、4 类，均为 1024×1024 不透明静态 WebP；
  贴图合计 889726 字节；校验文件覆盖、元数据、哈希、路径和页面本地链接。
- `python3 -m unittest discover -s tests -v`：6 项检查通过，包含重复 ID、路径逃逸、过期 JS、
  非法 WebP、前四张正式版以及拒绝放大 192px 小图。
- `node --check app.js`：脚本语法通过；Node 仅用于开发检查，不是预览站运行条件。
- `python3 tests/browser_check.py --http-only --screenshots /path/outside/repository`：系统 Chromium
  的本地 HTTP 检查通过。覆盖 12 张图片解码、分类/关键词、空分类/空搜索、大图与方向键/Esc、
  WebP 下载、390px 移动布局和无横向溢出；没有外部网络请求或 JS 错误。
- 桌面与移动截图已目视检查。

## file:// 测试限制

本环境的 Chromium 管理策略阻止 file:// 导航，原始双协议检查返回 ERR_BLOCKED_BY_ADMINISTRATOR，
因此不能把本机 file:// 实测标记为通过，也没有绕过管理策略。

站点按 file:// 使用经典脚本实现：data/character.js、data/lore.js、data/stickers.js 在 app.js 前
按 defer 顺序载入，没有 fetch、ES module、远程字体或服务依赖。在没有该管理策略的浏览器可直接
双击 index.html；如浏览器或组织禁止本地页面，使用 README 中的 Python 静态服务器。
CI 配置运行完整双协议浏览器检查；配置存在不代表 GitHub 已经执行成功。

## 已知未完成项

- 独立正背侧三视参考尚未齐备，尤其侧视图待补充；页面与文档明确说明。
- sleepy、daily、playful、shy、love 尚未收录正式贴图，分类显示零张。
- 本轮未配置线上托管网站；GitHub CI 状态以实际工作流运行结果为准。
