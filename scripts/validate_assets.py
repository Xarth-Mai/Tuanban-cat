#!/usr/bin/env python3
"""Validate WebP headers, coverage, metadata, hashes and local preview links. Stdlib only."""
from __future__ import annotations
import json
from pathlib import Path
import struct
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
from build_manifest import ROOT, build, load_catalog


def webp_info(path: Path) -> tuple[int, int, bool]:
    data = path.read_bytes()
    if len(data) < 20 or data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        raise ValueError(f"Not WebP: {path.name}")
    if struct.unpack_from("<I", data, 4)[0] + 8 != len(data):
        raise ValueError(f"Wrong RIFF length: {path.name}")
    offset, dimensions, alpha = 12, None, False
    while offset < len(data):
        if offset + 8 > len(data):
            raise ValueError(f"Truncated chunk: {path.name}")
        kind = data[offset:offset + 4]
        size = struct.unpack_from("<I", data, offset + 4)[0]
        body = data[offset + 8:offset + 8 + size]
        if len(body) != size:
            raise ValueError(f"Truncated payload: {path.name}")
        if kind == b"VP8X":
            if len(body) != 10 or body[0] & 0x02:
                raise ValueError("Invalid or animated extended WebP")
            alpha |= bool(body[0] & 0x10)
        elif kind == b"ALPH":
            alpha = True
        elif kind in (b"ANIM", b"ANMF"):
            raise ValueError("Formal stickers are static WebP")
        elif kind == b"VP8 ":
            if len(body) < 10 or body[3:6] != b"\x9d\x01\x2a":
                raise ValueError("Invalid VP8 key frame")
            dimensions = tuple(x & 0x3fff for x in struct.unpack_from("<HH", body, 6))
        elif kind == b"VP8L":
            if len(body) < 5 or body[0] != 0x2f:
                raise ValueError("Invalid lossless WebP")
            bits = int.from_bytes(body[1:5], "little")
            dimensions = ((bits & 0x3fff) + 1, ((bits >> 14) & 0x3fff) + 1)
            alpha |= bool(bits & (1 << 28))
        offset += 8 + size + size % 2
    if offset != len(data) or dimensions is None or min(dimensions) < 1:
        raise ValueError("Missing image or invalid WebP chunk alignment")
    return *dimensions, alpha


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = []

    def handle_starttag(self, tag, attributes):
        for name, value in attributes:
            if name in {"src", "href"} and value:
                self.paths.append(value)


def validate(root: Path = ROOT) -> dict:
    items = load_catalog(root)
    build(root, check=True)
    paths = {item["filename"] for item in items}
    actual = {p.relative_to(root).as_posix() for p in (root / "assets/stickers").rglob("*") if p.is_file()}
    if paths != actual:
        raise ValueError(f"Unindexed or missing stickers: {paths ^ actual}")
    for path in (root / "assets").rglob("*.webp"):
        width, height, alpha = webp_info(path)
        if alpha:
            raise ValueError(f"Transparent master: {path.name}")
        if path.relative_to(root).as_posix() in paths and (width, height) != (1024, 1024):
            raise ValueError(f"Sticker must be 1024x1024: {path.name}")
        if path.stat().st_size > 2 * 1024 * 1024:
            raise ValueError(f"Asset exceeds repository budget of 2 MiB: {path.name}")
    parser = Links()
    parser.feed((root / "index.html").read_text(encoding="utf-8"))
    for link in parser.paths:
        parts = urlsplit(link)
        if parts.scheme or parts.netloc or not parts.path:
            continue
        target = (root / unquote(parts.path)).resolve()
        if not target.is_relative_to(root.resolve()) or not target.is_file():
            raise ValueError(f"Broken local link: {link}")
    return {"stickers": len(items), "categories": len({x["category"] for x in items}),
            "total_sticker_bytes": sum((root / x["filename"]).stat().st_size for x in items)}


if __name__ == "__main__":
    print(json.dumps(validate(), ensure_ascii=False, indent=2))
