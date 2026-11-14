# Contributing / 贡献指南

欢迎为团斑补充表情和日常场景～

1. 先看 `docs/CHARACTER.md` 与 `docs/STYLE-GUIDE.md`，保持角色可辨识
2. 提交**有权按 MPL-2.0 许可发布**的原创或经充分授权素材；不要上传动漫截图、第三方网络表情包或未经核验的素材
3. 表情包按 192×192、8-bit RGB、非透明 PNG、≤40 KiB 导出，并更新 `stickers/manifest.json`
4. 运行 `python3 scripts/validate.py`；需要新增素材时同时调整校验清单
5. 在 PR 描述中说明创作过程、AI 工具参与情况及来源或许可依据

仓库维护者审核素材质量和许可信息后再合并。新增商标、角色改名、大幅修改外观应单独讨论
