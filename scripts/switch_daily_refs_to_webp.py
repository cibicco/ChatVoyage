#!/usr/bin/env python3
"""Switch Chat Voyage daily image references to WebP when the WebP exists."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
REF_PATTERN = re.compile(r"((?:\.\./)?assets/daily/[^\"')\s]+?|daily/[^\"')\s]+?)\.(png|jpg|jpeg)")


def webp_exists(ref: str, base: Path) -> bool:
    candidate = ref + ".webp"
    if candidate.startswith("../"):
        path = (base / candidate).resolve()
    elif candidate.startswith("assets/"):
        path = ROOT / candidate
    elif candidate.startswith("daily/"):
        path = ROOT / "assets" / candidate
    else:
        return False
    return path.exists()


def switch_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")

    def replace(match: re.Match[str]) -> str:
        stem = match.group(1)
        return stem + ".webp" if webp_exists(stem, path.parent) else match.group(0)

    updated = REF_PATTERN.sub(replace, original)
    if updated == original:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def main() -> int:
    targets = [
        ROOT / "index.html",
        ROOT / "albums.html",
        ROOT / "album.html",
        ROOT / "assets" / "album-data.js",
        *sorted((ROOT / "notes").glob("*.md")),
        *sorted((ROOT / "logs").glob("generation-*.md")),
    ]
    changed = [p.relative_to(ROOT) for p in targets if p.exists() and switch_file(p)]
    for path in changed:
        print(path)
    print(f"changed: {len(changed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
