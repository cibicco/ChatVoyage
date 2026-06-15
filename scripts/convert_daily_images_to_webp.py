#!/usr/bin/env python3
"""Create WebP display copies for Chat Voyage daily image folders."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUFFIXES = {".png", ".jpg", ".jpeg"}


def convert_image(path: Path, quality: int, overwrite: bool) -> tuple[Path, int, int] | None:
    out = path.with_suffix(".webp")
    if out.exists() and not overwrite:
        return None

    with Image.open(path) as image:
        image = image.convert("RGB")
        image.save(out, "WEBP", quality=quality, method=6)

    return out, path.stat().st_size, out.stat().st_size


def iter_sources(target: Path) -> list[Path]:
    if target.is_file():
        paths = [target]
    else:
        paths = sorted(
            p
            for p in target.rglob("*")
            if p.is_file() and p.suffix.lower() in DEFAULT_SUFFIXES
        )
    return paths


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", help="Image file or folder, relative to project root unless absolute")
    parser.add_argument("--quality", type=int, default=82, help="WebP quality, default: 82")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing WebP files")
    args = parser.parse_args()

    target = Path(args.target)
    if not target.is_absolute():
        target = ROOT / target
    if not target.exists():
        print(f"missing target: {target}", file=sys.stderr)
        return 1

    converted: list[tuple[Path, int, int]] = []
    for path in iter_sources(target):
        result = convert_image(path, args.quality, args.overwrite)
        if result:
            converted.append(result)

    before = sum(item[1] for item in converted)
    after = sum(item[2] for item in converted)
    for out, src_size, out_size in converted:
        rel = out.relative_to(ROOT)
        ratio = out_size / src_size if src_size else 0
        print(f"{rel}: {src_size:,} -> {out_size:,} ({ratio:.1%})")
    print(f"converted: {len(converted)}")
    if converted:
        print(f"total: {before:,} -> {after:,} ({after / before:.1%})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
