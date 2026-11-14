#!/usr/bin/env python3
"""Optional offline format export, NOT image generation. Requires Pillow only when used.

python scripts/export_webp.py source.png assets/stickers/category/id.webp
Rejects small inputs instead of enlarging legacy 192px examples.
"""
import argparse
from pathlib import Path


def export(source: Path, destination: Path):
    from PIL import Image
    with Image.open(source) as image:
        if image.width != image.height or min(image.size) < 1024:
            raise ValueError("Use a square original at least 1024px; do not enlarge old miniatures.")
        if image.mode in {"RGBA", "LA"} or "transparency" in image.info:
            raise ValueError("Export an opaque source with the intended background first.")
        if destination.suffix.lower() != ".webp":
            raise ValueError("Destination must end in .webp")
        destination.parent.mkdir(parents=True, exist_ok=True)
        image.convert("RGB").resize((1024, 1024), Image.Resampling.LANCZOS).save(
            destination, "WEBP", quality=92, method=6)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    if args.destination.exists():
        parser.error("Destination exists; choose a new path to avoid overwriting artwork.")
    export(args.source, args.destination)
