# Tuanban · 团斑

A gentle, shy gray-and-white kitten holding everyday feelings in her paws. This standalone
character repository includes her profile, lore, visual guidance, 12 formal stickers, reusable
metadata, and a local preview site. It is separate from Hermes Lively.

Open `index.html` directly, or run `python3 -m http.server 8000`. There is no build step, framework,
node_modules, CDN, runtime API or JSON fetch. Browse categories, search, open large previews and save WebP.

Formal stickers are 1024×1024 opaque WebP. The first four emotions were redrawn, not enlarged from
192px samples. Existing generated outputs were reused for this implementation; no further artwork was
commissioned for the unfinished side view. The existing character sheet includes front/back and
expressions; a complete standalone three-view set is still pending.

`data/stickers.json` is the editable metadata source; `scripts/build_manifest.py` generates
`data/stickers.js` and `data/manifest.json`. Validate with `python3 scripts/validate_assets.py`.
The site itself needs no Python dependencies. See the Chinese README and docs for the full workflow.

Licensed under MPL-2.0 to the extent contributors have licensable rights. AI-assisted artwork; no
copyrightability, exclusivity, or registered trademark is asserted. Preserve ASSET-NOTICE.md when
redistributing separately. Prior v0.1 PNG paths are replaced; history is available through Git.
