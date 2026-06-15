#!/usr/bin/env python3
"""Validate Chat Voyage gallery references and filter metadata."""

from __future__ import annotations

from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}


class GalleryParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.figures: list[dict[str, str | None]] = []
        self.sections: list[dict[str, int | bool | str]] = []
        self.filters: dict[str, set[str]] = {
            "style": set(),
            "place": set(),
            "category": set(),
        }
        self.refs: list[str] = []
        self._filter_group: str | None = None
        self._in_section = False
        self._section_title = ""
        self._section_figures = 0
        self._section_album = False
        self._in_h2 = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if tag == "section" and "data-set" in data:
            self._in_section = True
            self._section_title = ""
            self._section_figures = 0
            self._section_album = False
        elif self._in_section and tag == "h2":
            self._in_h2 = True
        if tag == "div" and data.get("data-filter-group"):
            self._filter_group = data["data-filter-group"]
        if tag == "button" and self._filter_group and data.get("data-filter"):
            self.filters.setdefault(self._filter_group, set()).add(data["data-filter"])
        if tag == "figure" and data.get("data-style"):
            if self._in_section:
                self._section_figures += 1
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
            if self._in_section and ref and is_album_ref(ref):
                self._section_album = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "div":
            self._filter_group = None
        elif tag == "h2":
            self._in_h2 = False
        elif tag == "section" and self._in_section:
            self.sections.append(
                {
                    "title": self._section_title,
                    "figures": self._section_figures,
                    "album": self._section_album,
                }
            )
            self._in_section = False

    def handle_data(self, data: str) -> None:
        if self._in_h2:
            self._section_title += data


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
    clean_ref = ref.split("#", 1)[0].split("?", 1)[0]
    return (base / clean_ref).resolve()


def is_album_ref(ref: str) -> bool:
    return ref.endswith("-album.html") or ref.startswith("album.html?set=")


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
    png_files = sorted(p for p in (ROOT / "assets").rglob("*.png") if p.is_file())
    if png_files:
        errors.append(
            "png files remain in assets: "
            + ", ".join(str(p.relative_to(ROOT)) for p in png_files)
        )
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

    missing_album_sections = [
        f"{section['title']} ({section['figures']} figures)"
        for section in parser.sections
        if section["figures"] and not section["album"]
    ]
    if missing_album_sections:
        errors.append("index sections missing album links: " + ", ".join(missing_album_sections))

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
    album_shell = ROOT / "album.html"
    html_files = [ROOT / "index.html", ROOT / "albums.html", album_shell, *album_files]
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
        if html == album_shell:
            required_album_page_features = [
                'assets/album-page.css',
                'assets/album-data.js',
                'assets/album-page.js',
                'data-album-viewer',
                'id="album-select"',
                'data-stage-image',
                'data-thumbnail-strip',
                'data-image-grid',
            ]
            for feature in required_album_page_features:
                if feature not in text:
                    errors.append(f"album shell missing feature marker: {feature}")
        elif html in album_files:
            if "data-legacy-album" not in text:
                errors.append(f"legacy album missing marker: {html.relative_to(ROOT)}")
            if "../album.html?set=" not in text:
                errors.append(f"legacy album missing canonical viewer redirect: {html.relative_to(ROOT)}")
            if "daily/" in text:
                errors.append(f"legacy album embeds daily images: {html.relative_to(ROOT)}")
        elif html.name == "albums.html":
            required_album_browser_features = [
                'data-filter-group="style"',
                'id="album-sort"',
                'data-view-option="grid"',
                'id="active-filters"',
                'assets/album-browser.css',
                'assets/album-browser.js',
                'album.html?set=',
            ]
            for feature in required_album_browser_features:
                if feature not in text:
                    errors.append(f"album browser missing feature marker: {feature}")
            if re.search(r'href="assets/[^"]+-album\.html"', text):
                errors.append("album browser links to legacy album html")
        elif html.name == "index.html":
            if re.search(r'href="assets/[^"]+-album\.html"', text):
                errors.append("index links to legacy album html")

    data_path = ROOT / "assets" / "album-data.js"
    if not data_path.exists():
        errors.append("missing album data file: assets/album-data.js")
    else:
        data_text = data_path.read_text(encoding="utf-8")
        match = re.match(r"window\.CHAT_VOYAGE_ALBUMS = (.*);\s*$", data_text, flags=re.DOTALL)
        if not match:
            errors.append("album data file has unexpected format")
        else:
            try:
                album_data = json.loads(match.group(1))
            except json.JSONDecodeError as exc:
                errors.append(f"album data JSON parse failed: {exc}")
                album_data = []
            slugs = [album.get("slug") for album in album_data]
            if len(slugs) != len(set(slugs)):
                errors.append("album data contains duplicate slugs")
            if len(album_data) != len([section for section in parser.sections if section["figures"]]):
                errors.append(f"album data count mismatch: data={len(album_data)} index_sections={len(parser.sections)}")
            data_image_count = sum(int(album.get("imageCount", 0)) for album in album_data)
            if data_image_count != len(daily_images):
                errors.append(f"album data image count mismatch: data={data_image_count} daily={len(daily_images)}")
            bad_hrefs = [album.get("href") for album in album_data if not str(album.get("href", "")).startswith("album.html?set=")]
            if bad_hrefs:
                errors.append(f"album data has non-canonical hrefs: {bad_hrefs}")
            for album in album_data:
                for image in album.get("images", []):
                    src = str(image.get("src", ""))
                    if not src:
                        errors.append(f"album data image missing src: {album.get('slug')}")
                        continue
                    target = local_target(ROOT, src)
                    if not target.exists():
                        missing_refs.append(f"assets/album-data.js -> {src}")
                    if Path(src).suffix.lower() in IMAGE_SUFFIXES and Path(src).suffix.lower() != ".webp":
                        non_webp_daily_refs.append(f"assets/album-data.js -> {src}")
    if missing_refs:
        errors.append("missing local refs: " + ", ".join(missing_refs))
    if non_webp_daily_refs:
        errors.append("non-webp daily refs in html: " + ", ".join(non_webp_daily_refs))

    print(f"daily_images: {len(daily_images)}")
    print(f"daily_source_images: {len(all_daily_images)}")
    print(f"index_figures: {len(parser.figures)}")
    print(f"album_index: {(ROOT / 'albums.html').exists()}")
    print(f"album_shell: {album_shell.exists()}")
    print(f"legacy_album_pages: {len(album_files)}")
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
