#!/usr/bin/env python3
"""Entrypoint: copy bundled entry.png to output dir (deterministic, no network)."""
from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

MAX_BYTES = 1048576  # 1 MiB


def main() -> int:
    parser = argparse.ArgumentParser(description="Copy entry.png to output dir or check it.")
    parser.add_argument("--check", action="store_true", help="Verify image is 1024x1024 and report bytes without copying.")
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent
    src = base_dir / "entry.png"
    out_dir_env = os.environ.get("MAKEFUN_OUTPUT_DIR")
    out_dir = Path(out_dir_env) if out_dir_env else Path("/output")

    if not src.is_file():
        print(f"ERROR: missing source image: {src}", file=sys.stderr)
        return 1

    size = src.stat().st_size
    if size <= 0 or size > MAX_BYTES:
        print(f"ERROR: entry.png invalid size: {size} bytes (limit {MAX_BYTES})", file=sys.stderr)
        return 1

    if args.check:
        try:
            from PIL import Image
        except Exception as exc:
            print(f"ERROR: cannot import PIL: {exc}", file=sys.stderr)
            return 1
        try:
            with Image.open(src) as im:
                w, h = im.size
        except Exception as exc:
            print(f"ERROR: cannot open image: {exc}", file=sys.stderr)
            return 1
        if w != 1024 or h != 1024:
            print(f"ERROR: image size {w}x{h} != 1024x1024", file=sys.stderr)
            return 1
        print(f"OK: 1024x1024, {size} bytes")
        return 0

    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print(f"ERROR: cannot create output dir {out_dir}: {exc}", file=sys.stderr)
        return 1

    dst = out_dir / "entry.png"
    shutil.copyfile(src, dst)
    print(f"copied {src.name} -> {dst} ({dst.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
