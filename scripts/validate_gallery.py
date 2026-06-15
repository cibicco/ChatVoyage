#!/usr/bin/env python3
"""Validate Chat Voyage gallery references and filter metadata."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}


class GalleryParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.figures: list[dict[str, str | None]] = []
        self.filters: dict[str, set[str]] = {
            "style": set(),
            "place": set(),
            "category": set(),
        }
        self.refs: list[str] = []
        self._filter_group: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if tag == "div" and data.get("data-filter-group"):
            self._filter_group = data["data-filter-group"]
        if tag == "button" and self._filter_group and data.get("data-filter"):
            self.filters.setdefault(self._filter_group, set()).add(data["data-filter"])
        if tag == "figure" and data.get("data-style"):
            self.figures.append(
                {
                    "style": data.get("data-style"),
                    "place": data.get("data-place"),
                    "category": data.get("data-category"),
                }
            )
        if tag in {"a", "img", "script", "link"}:
            ref = data.get("href") or data.get("src")
            if ref and not ref.startswith(("http://", "https://", "#", "mailto:")):
                self.refs.append(ref)

    def handle_endtag(self, tag: str) -> None:
        if tag == "div":
            self._filter_group = None


class RefParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.refs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        ref = data.get("href") or data.get("src")
        if ref and not ref.startswith(("http://", "https://", "#", "mailto:")):
            self.refs.append(ref)


def read_index() -> GalleryParser:
    parser = GalleryParser()
    parser.feed((ROOT / "index.html").read_text(encoding="utf-8"))
    return parser


def local_target(base: Path, ref: str) -> Path:
    return (base / ref.split("#", 1)[0]).resolve()


def preset_values(path: Path, pattern: str) -> set[str]:
    text = path.read_text(encoding="utf-8")
    return set(re.findall(pattern, text, flags=re.MULTILINE))


def validate() -> list[str]:
    errors: list[str] = []
    parser = read_index()

    all_daily_images = {
        p.resolve()
        for p in (ROOT / "assets" / "daily").glob("*/*")
        if p.suffix.lower() in IMAGE_SUFFIXES
    }
    daily_images = {
        p
        for p in all_daily_images
        if p.suffix.lower() == ".webp" or p.with_suffix(".webp").resolve() not in all_daily_images
    }
    index_daily_refs = {
        local_target(ROOT, ref)
        for ref in parser.refs
        if ref.startswith("assets/daily/") and Path(ref).suffix.lower() in IMAGE_SUFFIXES
    }

    missing_from_index = sorted(daily_images - index_daily_refs)
    extra_in_index = sorted(index_daily_refs - daily_images)
    if missing_from_index:
        errors.append("daily images missing from index: " + ", ".join(str(p) for p in missing_from_index))
    if extra_in_index:
        errors.append("index references non-daily images: " + ", ".join(str(p) for p in extra_in_index))

    if len(parser.figures) != len(daily_images):
        errors.append(f"figure count mismatch: index={len(parser.figures)} daily={len(daily_images)}")

    for group in ("style", "place", "category"):
        data_values = {f[group] for f in parser.figures if f.get(group)}
        filter_values = parser.filters.get(group, set()) - {"all"}
        missing_filters = sorted(data_values - filter_values)
        if missing_filters:
            errors.append(f"missing {group} filter buttons: {missing_filters}")

    style_presets = preset_values(ROOT / "prompts" / "style-presets.md", r"^## `([^`]+)`")
    category_presets = preset_values(ROOT / "prompts" / "category-presets.md", r"^- `([^`]+)`:")
    index_styles = {f["style"] for f in parser.figures if f.get("style")}
    index_categories = {f["category"] for f in parser.figures if f.get("category")}
    if missing_styles := sorted(index_styles - style_presets):
        errors.append(f"styles missing from prompts/style-presets.md: {missing_styles}")
    if missing_categories := sorted(index_categories - category_presets):
        errors.append(f"categories missing from prompts/category-presets.md: {missing_categories}")

    album_files = sorted((ROOT / "assets").glob("*-album.html"))
    html_files = [ROOT / "index.html", ROOT / "albums.html", *album_files]
    missing_refs: list[str] = []
    non_webp_daily_refs: list[str] = []
    for html in html_files:
        text = html.read_text(encoding="utf-8")
        refs = RefParser()
        refs.feed(text)
        base = html.parent
        for ref in refs.refs:
            if ref.startswith("../"):
                target = local_target(base, ref)
            else:
                target = local_target(ROOT if html.name == "index.html" else base, ref)
            if not target.exists():
                missing_refs.append(f"{html.relative_to(ROOT)} -> {ref}")
            if "daily/" in ref and Path(ref).suffix.lower() in IMAGE_SUFFIXES and Path(ref).suffix.lower() != ".webp":
                non_webp_daily_refs.append(f"{html.relative_to(ROOT)} -> {ref}")
        if html in album_files:
            if "<header" in text:
                errors.append(f"album uses legacy header layout: {html.relative_to(ROOT)}")
            if 'class="open"' in text:
                errors.append(f"album uses legacy open link class: {html.relative_to(ROOT)}")
            if "object-fit: cover" in text:
                errors.append(f"album uses object-fit: cover: {html.relative_to(ROOT)}")
            if "image-link" not in text or "Open image" not in text:
                errors.append(f"album missing direct image links: {html.relative_to(ROOT)}")
            if "../albums.html" not in text:
                errors.append(f"album missing Albums navigation: {html.relative_to(ROOT)}")
    if missing_refs:
        errors.append("missing local refs: " + ", ".join(missing_refs))
    if non_webp_daily_refs:
        errors.append("non-webp daily refs in html: " + ", ".join(non_webp_daily_refs))

    print(f"daily_images: {len(daily_images)}")
    print(f"daily_source_images: {len(all_daily_images)}")
    print(f"index_figures: {len(parser.figures)}")
    print(f"album_index: {(ROOT / 'albums.html').exists()}")
    print(f"album_pages: {len(album_files)}")
    print(f"index_styles: {sorted(index_styles)}")
    print(f"index_categories: {sorted(index_categories)}")
    print(f"errors: {len(errors)}")
    return errors


def main() -> int:
    errors = validate()
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
