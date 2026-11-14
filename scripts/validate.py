#!/usr/bin/env python3
# SPDX-License-Identifier: MPL-2.0
"""Validate the portable starter sticker pack without external dependencies."""
import json
from pathlib import Path
import struct
import sys

BASE = Path(__file__).resolve().parent.parent
ASSETS = BASE / "stickers"
EXPECTED = {"greeting", "happy", "confused", "comfort"}
SIGNATURE = b"\x89PNG\r\n\x1a\n"


def main():
    data = json.loads((ASSETS / "manifest.json").read_text(encoding="utf-8"))
    assert data["schema_version"] == 1
    assert data["license"] == "MPL-2.0"
    rules = data["format"]
    assert (rules["width"], rules["height"], rules["color_mode"], rules["alpha"]) == (192, 192, "RGB", False)
    ids = [s["id"] for s in data["stickers"]]
    assert len(ids) == len(set(ids)) and set(ids) == EXPECTED, "Unexpected sticker IDs"
    for s in data["stickers"]:
        path = ASSETS / s["file"]
        assert path.parent == ASSETS and path.name == s["id"] + ".png", "Unsafe asset path"
        assert path.is_file() and not path.is_symlink(), f"Missing or linked asset: {path}"
        content = path.read_bytes()
        assert content[:8] == SIGNATURE, f"Not PNG: {path.name}"
        assert len(content) <= rules["max_bytes"], f"Oversized: {path.name}"
        assert content[12:16] == b"IHDR", f"Missing IHDR: {path.name}"
        width, height, bit_depth, color_type, comp, filt, interlace = struct.unpack(">IIBBBBB", content[16:29])
        assert (width, height, bit_depth, color_type, comp, filt, interlace) == (192, 192, 8, 2, 0, 0, 0), f"Not 8-bit non-alpha RGB: {path.name}"
        assert b"tRNS" not in content, f"Unexpected transparency: {path.name}"
        assert "description_zh" in s and "description_en" in s and s["intent"]
        print(f"PASS {path.relative_to(BASE)} {len(content)} bytes RGB 192x192")
    actual = {p.name for p in ASSETS.glob("*.png")}
    assert actual == {s["file"] for s in data["stickers"]}, "Unindexed PNG present"
    print("PASS manifest and starter sticker library")


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, ValueError, OSError, KeyError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
