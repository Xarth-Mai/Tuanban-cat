# 给团斑添一个小表情

先阅读角色、视觉和贴图规范，保持灰斑方向、圆软形体、暖棕线条和表达边界。
只提交你有权许可的材料；贡献按 MPL-2.0 发布，并说明是否使用 AI 辅助。不要混入第三方角色或网图。

1. 准备不小于 1024px 的独立方形原图，不放大旧 192px 示例。日常修改文档或站点不需要绘图。
2. 导出不透明 1024×1024 WebP，放入 `assets/stickers/{category}/{id}.webp`。
   可选安装 Pillow 后使用 `scripts/export_webp.py source.png target.webp`，这只是格式转换工具。
3. 在 `data/stickers.json` 添加真实描述、关键词、情绪和场景，保持 ID 稳定。
4. 运行 `python3 scripts/build_manifest.py`，提交同步生成的 JS 和 manifest。
5. 运行 `python3 scripts/validate_assets.py` 与 `python3 -m unittest discover -s tests -v`。
6. 双击 index.html 检查图片、筛选、大图和下载；确认 `file://` 下不依赖网络或 fetch。

浏览器开发检查可安装 Python Playwright 并指定本机 Chromium 执行 tests/browser_check.py。
它们不是网站依赖。不要给预览站增加 npm、远程字体、运行时服务或分析统计。

完整三视图目前未齐备。缺少的角度应保持待办，不重复使用正面图冒充侧面。
