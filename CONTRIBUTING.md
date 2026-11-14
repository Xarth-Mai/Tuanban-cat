# 参与创作

欢迎为团斑补充贴图、改进网站或完善角色资料。开始前请阅读 [角色设定](docs/character-profile.md)、[视觉规范](docs/visual-guidelines.md) 和 [贴图规范](docs/sticker-guidelines.md)。

提交的材料应由你拥有相应许可权，并说明是否使用 AI 辅助。贡献内容按仓库的 [MPL-2.0](LICENSE) 发布；不要混入未经许可的第三方角色或图片。

## 添加贴图

1. 准备至少 1024×1024 的独立方形原图，保持团斑的形象和灰斑位置一致
2. 导出不透明的 1024×1024 WebP，保存到 `assets/stickers/{category}/{id}.webp`
3. 在唯一的手工数据源 `data/stickers.json` 中添加条目，保持 ID 稳定
4. 重新生成浏览器数据和外部清单，并运行校验

```bash
python3 scripts/build_manifest.py
python3 scripts/build_manifest.py --check
python3 scripts/validate_assets.py
python3 -m unittest discover -s tests -v
```

转换图片时可选用 `scripts/export_webp.py`（需要 Pillow）；普通网站使用和元数据验证仅需 Python 3.10+ 标准库。

## 网站维护

网站由 `index.html`、`styles.css` 和 `app.js` 构成，不需要构建步骤。请保持 `file://` 直接打开可用，不引入远程字体、CDN、统计服务或运行时请求。浏览器回归测试位于 `tests/browser_check.py`（可选 Playwright）。

`data/stickers.js` 与 `data/manifest.json` 是生成文件，请修改 `data/stickers.json` 后由脚本更新。提交前确认页面能正常筛选、搜索、放大和下载。
