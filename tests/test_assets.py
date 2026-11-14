"""Regression checks for asset constraints and a synchronized, extensible catalog."""
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_manifest import build, load_catalog
from validate_assets import validate, webp_info


class AssetsTest(unittest.TestCase):
    def test_formal_collection(self):
        result = validate()
        self.assertEqual(result["stickers"], 12)
        self.assertEqual(result["categories"], 4)
        for item in load_catalog():
            self.assertEqual(webp_info(ROOT / item["filename"]), (1024, 1024, False))

    def test_new_first_four_have_distinct_ids(self):
        items = load_catalog()
        featured = {x["id"] for x in items if x["is_featured"]}
        self.assertEqual(featured, {"greeting-wave", "happy-cheer", "confused-tilt", "comfort-hug"})
        self.assertEqual(len({x["filename"] for x in items}), 12)

    def test_duplicate_and_escape_are_rejected(self):
        for mutate in (lambda items: items.append(items[0].copy()),
                       lambda items: items[0].update(filename="../../private.webp")):
            with tempfile.TemporaryDirectory() as tmp:
                copy = Path(tmp)
                shutil.copytree(ROOT / "data", copy / "data")
                shutil.copytree(ROOT / "assets", copy / "assets")
                items = json.loads((copy / "data/stickers.json").read_text())
                mutate(items)
                (copy / "data/stickers.json").write_text(json.dumps(items))
                with self.assertRaises(ValueError):
                    load_catalog(copy)

    def test_stale_js_fails_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp)
            shutil.copytree(ROOT / "data", copy / "data")
            shutil.copytree(ROOT / "assets", copy / "assets")
            (copy / "data/stickers.js").write_text("window.TUANBAN_STICKERS = [];")
            with self.assertRaisesRegex(ValueError, "Stale"):
                build(copy, check=True)

    def test_malformed_webp_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "broken.webp"
            path.write_bytes(b"RIFF\x00\x00\x00\x00WEBP")
            with self.assertRaises(ValueError):
                webp_info(path)

    def test_exporter_rejects_old_small_sources(self):
        if importlib.util.find_spec("PIL") is None:
            self.skipTest("Pillow is optional; normal validation has no dependencies")
        from PIL import Image
        from export_webp import export
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "small.png"
            Image.new("RGB", (192, 192)).save(source)
            with self.assertRaisesRegex(ValueError, "do not enlarge"):
                export(source, Path(tmp) / "not-created.webp")
            self.assertFalse((Path(tmp) / "not-created.webp").exists())


if __name__ == "__main__":
    unittest.main()
