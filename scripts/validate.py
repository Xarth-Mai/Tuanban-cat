#!/usr/bin/env python3
"""Compatibility entrypoint. v1 assets are checked by validate_assets.py."""
import runpy
from pathlib import Path
if __name__ == "__main__":
    runpy.run_path(str(Path(__file__).with_name("validate_assets.py")), run_name="__main__")
