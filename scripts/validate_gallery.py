#!/usr/bin/env python3
"""Validate Chat Voyage gallery references and filter metadata."""

from __future__ import annotations

from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys

from image_dimensions import aspect_ratio, image_dimensions


ROOT = Path(__file__).resolve().parents[1]
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
ALBUM_IMAGE_ROOT = ROOT / "assets" / "albums"
ALBUM_DATA_ROOT = ROOT / "data" / "albums"
LOCATION_DETAIL_ACTION_WORDS = re.compile(
    r"\b(wearing|holding|checking|adjusting|carrying|putting|pulling|gathering|fixing|tightening|"
    r"smiling|laughing|writing|seated|walking|leaving|stepping|tidying|packing|studying|"
    r"answering|responding|speaking|waiting|entering|watching|playing|measuring|joining|trying|"
    r"jumping|stretching|reading|leaning)\b",
    re.IGNORECASE,
)
LOCATION_DETAIL_WEAK_WORDS = re.compile(
    r"\b(look|fashion illustration|fashion|snapshot|partial snapshot|note|remake|regenerated|motion|crop|reach|sash|dress|floor sit|profile|leaning down)\b|(?<!-)\bstyle\b",
    re.IGNORECASE,
)
LOCATION_DETAIL_CITY_ONLY = {
    "Naha",
    "Mexico City",
    "Reykjavik",
    "Yakushima",
    "Lagos",
    "Vancouver",
    "Buenos Aires",
    "Sao Paulo",
    "Madrid",
    "Istanbul",
    "Hanoi",
    "Copenhagen",
    "Sydney",
    "Kuala Lumpur",
    "Osaka",
    "Hong Kong",
    "Barcelona",
    "Busan",
    "Berlin",
    "Melbourne",
    "Kyoto",
    "Nagoya",
    "Hiroshima",
    "Nagasaki",
    "Fukuoka",
    "Marrakech",
    "Taipei",
    "Kobe",
    "Tokyo",
    "Seoul",
    "Bangkok",
    "Helsinki",
    "Lisbon",
    "Vienna",
    "Sapporo",
    "Yokohama",
    "Kanazawa",
    "Singapore",
    "Fictional Port City",
    "Shino",
    "Unspecified",
}
LOCATION_DETAIL_TIME_ONLY = {
    "sunset",
    "evening",
    "morning",
    "afternoon",
    "night",
    "dusk",
    "dawn",
    "cool july morning",
    "waiting",
    "humid",
    "slow",
}


def invalid_location_detail_reason(value: str) -> str | None:
    location_detail = value.strip()
    if not location_detail:
        return "missing"
    if len(location_detail) > 100:
        return "too long"
    if len(location_detail) < 8:
        return "too short"
    if location_detail in LOCATION_DETAIL_CITY_ONLY:
        return "city only"
    if location_detail.lower() in LOCATION_DETAIL_TIME_ONLY:
        return "time/adjective only"
    if LOCATION_DETAIL_WEAK_WORDS.search(location_detail):
        return "contains display/style filler"
    if LOCATION_DETAIL_ACTION_WORDS.search(location_detail):
        return "contains action prose"
    return None


def invalid_aspect_ratio_reason(value: str) -> str | None:
    ratio = value.strip()
    if not ratio:
        return None
    if not re.fullmatch(r"[1-9]\d*:[1-9]\d*", ratio):
        return "must be a positive width:height ratio"
    return None


def image_shape_error(image: dict[str, object], src: str) -> str | None:
    try:
        width = int(image.get("width", 0) or 0)
        height = int(image.get("height", 0) or 0)
    except (TypeError, ValueError):
        return "width/height must be integers"
    ratio = str(image.get("aspectRatio", "") or "").strip()
    if width <= 0 or height <= 0:
        return "missing width/height"
    if not ratio:
        return "missing aspectRatio"
    target = local_target(ROOT, src)
    if not target.exists():
        return None
    actual_width, actual_height = image_dimensions(target)
    actual_ratio = aspect_ratio(actual_width, actual_height)
    if (width, height) != (actual_width, actual_height):
        return f"dimension mismatch expected {actual_width}x{actual_height}"
    if ratio != actual_ratio:
        return f"aspectRatio mismatch expected {actual_ratio}"
    return None


class GalleryParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.figures: list[dict[str, str | None]] = []
        self.sections: list[dict[str, int | bool | str]] = []
        self.filters: dict[str, set[str]] = {
            "collection": set(),
            "style": set(),
            "place": set(),
            "category": set(),
            "occasion": set(),
            "venue": set(),
            "activity": set(),
            "outfit": set(),
        }
        self.refs: list[str] = []
        self._filter_group: str | None = None
        self._in_section = False
        self._section_collection = "daily"
        self._section_title = ""
        self._section_figures = 0
        self._section_album = False
        self._in_h2 = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if tag == "section" and "data-set" in data:
            self._in_section = True
            self._section_collection = data.get("data-collection") or "daily"
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
                    "set": data.get("data-set"),
                    "collection": data.get("data-collection") or self._section_collection,
                    "style": data.get("data-style"),
                    "place": data.get("data-place"),
                    "category": data.get("data-category"),
                    "occasion": data.get("data-occasion"),
                    "venue": data.get("data-venue"),
                    "activity": data.get("data-activity"),
                    "outfit": data.get("data-outfit"),
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
            self._section_collection = "daily"

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


def parse_js_json_assignment(text: str, name: str):
    prefix = f"window.{name} = "
    start = text.find(prefix)
    if start < 0:
        raise ValueError(f"missing {name}")
    fragment = text[start + len(prefix) :].lstrip()
    value, _ = json.JSONDecoder().raw_decode(fragment)
    return value


def load_album_sources() -> list[dict[str, object]]:
    sources: list[dict[str, object]] = []
    for path in sorted(ALBUM_DATA_ROOT.rglob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError(f"album source must be an object: {path.relative_to(ROOT)}")
        data["_sourcePath"] = str(path.relative_to(ROOT))
        sources.append(data)
    return sources


def source_image_refs(sources: list[dict[str, object]]) -> set[Path]:
    refs: set[Path] = set()
    for album in sources:
        images = album.get("images", [])
        if not isinstance(images, list):
            continue
        for image in images:
            if not isinstance(image, dict):
                continue
            src = str(image.get("src", ""))
            if src and Path(src).suffix.lower() in IMAGE_SUFFIXES:
                refs.add(local_target(ROOT, src))
    return refs


def local_ref_exists(ref: str) -> bool:
    return local_target(ROOT, ref).exists()


def validate() -> list[str]:
    errors: list[str] = []
    parser = read_index()
    try:
        album_sources = load_album_sources()
    except (ValueError, json.JSONDecodeError) as exc:
        album_sources = []
        errors.append(f"album source JSON parse failed: {exc}")

    all_album_images = {
        p.resolve()
        for p in ALBUM_IMAGE_ROOT.rglob("*")
        if p.suffix.lower() in IMAGE_SUFFIXES
    }
    png_files = sorted(p for p in (ROOT / "assets").rglob("*.png") if p.is_file())
    if png_files:
        errors.append(
            "png files remain in assets: "
            + ", ".join(str(p.relative_to(ROOT)) for p in png_files)
        )
    album_images = {
        p
        for p in all_album_images
        if p.suffix.lower() == ".webp" or p.with_suffix(".webp").resolve() not in all_album_images
    }
    source_images = source_image_refs(album_sources)
    if source_images != album_images:
        missing_from_sources = sorted(album_images - source_images)
        missing_from_assets = sorted(source_images - album_images)
        if missing_from_sources:
            errors.append(
                "album images missing from data/albums: "
                + ", ".join(str(p.relative_to(ROOT)) for p in missing_from_sources)
            )
        if missing_from_assets:
            errors.append(
                "data/albums references missing image files: "
                + ", ".join(str(p.relative_to(ROOT)) for p in missing_from_assets)
            )
    old_daily_images = sorted(
        p for p in (ROOT / "assets" / "daily").rglob("*")
        if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES
    ) if (ROOT / "assets" / "daily").exists() else []
    if old_daily_images:
        errors.append(
            "legacy assets/daily images remain: "
            + ", ".join(str(p.relative_to(ROOT)) for p in old_daily_images)
        )
    source_slugs_seen: set[str] = set()
    for album in album_sources:
        source_path = str(album.get("_sourcePath", "data/albums/<unknown>"))
        slug = str(album.get("slug", ""))
        if not slug:
            errors.append(f"album source missing slug: {source_path}")
        elif slug in source_slugs_seen:
            errors.append(f"duplicate album source slug: {slug}")
        source_slugs_seen.add(slug)
        collection = str(album.get("collection", "daily") or "daily")
        character = str(album.get("character", "") or "")
        if collection not in {"daily", "character"}:
            errors.append(f"album source has unknown collection: {source_path} -> {collection}")
        if collection == "character" and not character:
            errors.append(f"character album source missing character: {source_path}")
        summary_ja = str(album.get("summaryJa", "") or "")
        if not summary_ja:
            errors.append(f"album source missing summaryJa: {source_path}")
        elif not re.search(r"[ぁ-んァ-ヶ一-龠]", summary_ja):
            errors.append(f"album source summaryJa is not Japanese: {source_path}")
        preferred_aspect_ratio = str(album.get("preferredAspectRatio", "") or "")
        preferred_aspect_error = invalid_aspect_ratio_reason(preferred_aspect_ratio)
        if preferred_aspect_error:
            errors.append(
                f"album source preferredAspectRatio {preferred_aspect_error}: {source_path} -> {preferred_aspect_ratio}"
            )
        notes_href = str(album.get("notesHref", "") or "")
        if notes_href and notes_href.startswith("notes/") and not local_ref_exists(notes_href):
            errors.append(f"album source references missing note: {source_path} -> {notes_href}")
        images = album.get("images", [])
        if not isinstance(images, list) or not images:
            errors.append(f"album source has no images: {source_path}")
            continue
        expected_prefix = "assets/albums/characters/" if collection == "character" else "assets/albums/daily/"
        for image in images:
            if not isinstance(image, dict):
                errors.append(f"album source image is not an object: {source_path}")
                continue
            src = str(image.get("src", "") or "")
            if not src.startswith(expected_prefix):
                errors.append(f"album source image path outside collection: {source_path} -> {src}")
            shape_error = image_shape_error(image, src)
            if shape_error:
                errors.append(f"album source image {shape_error}: {source_path} -> {src}")
            location_detail = str(image.get("locationDetail", "") or "")
            location_detail_error = invalid_location_detail_reason(location_detail)
            if location_detail_error:
                errors.append(
                    f"album source image locationDetail {location_detail_error}: {source_path} -> {src}"
                )
    index_album_refs = {
        local_target(ROOT, ref)
        for ref in parser.refs
        if ref.startswith("assets/albums/") and Path(ref).suffix.lower() in IMAGE_SUFFIXES
    }

    missing_from_index = sorted(album_images - index_album_refs)
    extra_in_index = sorted(index_album_refs - album_images)
    if missing_from_index:
        errors.append("album images missing from index: " + ", ".join(str(p.relative_to(ROOT)) for p in missing_from_index))
    if extra_in_index:
        errors.append("index references non-album images: " + ", ".join(str(p.relative_to(ROOT)) for p in extra_in_index))

    if len(parser.figures) != len(album_images):
        errors.append(f"figure count mismatch: index={len(parser.figures)} album_images={len(album_images)}")

    missing_album_sections = [
        f"{section['title']} ({section['figures']} figures)"
        for section in parser.sections
        if section["figures"] and not section["album"]
    ]
    if missing_album_sections:
        errors.append("index sections missing album links: " + ", ".join(missing_album_sections))

    for group in ("collection", "style", "place", "occasion", "venue", "activity", "outfit"):
        data_values = {f[group] for f in parser.figures if f.get(group)}
        filter_values = parser.filters.get(group, set()) - {"all"}
        missing_filters = sorted(data_values - filter_values)
        if missing_filters:
            errors.append(f"missing {group} filter buttons: {missing_filters}")
        missing_data = sum(1 for f in parser.figures if not f.get(group))
        if missing_data:
            errors.append(f"figures missing {group} metadata: {missing_data}")

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
    non_webp_album_refs: list[str] = []
    legacy_daily_refs: list[str] = []
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
            if ref.startswith("assets/daily/") or ref.startswith("../assets/daily/"):
                legacy_daily_refs.append(f"{html.relative_to(ROOT)} -> {ref}")
            if "assets/albums/" in ref and Path(ref).suffix.lower() in IMAGE_SUFFIXES and Path(ref).suffix.lower() != ".webp":
                non_webp_album_refs.append(f"{html.relative_to(ROOT)} -> {ref}")
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
                'data-feedback-export',
                'data-feedback-score',
                'data-feedback-tag',
                'data-feedback-note',
            ]
            for feature in required_album_page_features:
                if feature not in text:
                    errors.append(f"album shell missing feature marker: {feature}")
        elif html in album_files:
            if "data-legacy-album" not in text:
                errors.append(f"legacy album missing marker: {html.relative_to(ROOT)}")
            if "../album.html?set=" not in text:
                errors.append(f"legacy album missing canonical viewer redirect: {html.relative_to(ROOT)}")
            if "assets/albums/" in text:
                errors.append(f"legacy album embeds album images: {html.relative_to(ROOT)}")
        elif html.name == "albums.html":
            required_album_browser_features = [
                'data-filter-group="style"',
                'data-filter-group="collection"',
                'data-filter-group="occasion"',
                'data-filter-group="venue"',
                'data-filter-group="activity"',
                'data-filter-group="outfit"',
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
        try:
            album_data = parse_js_json_assignment(data_text, "CHAT_VOYAGE_ALBUMS")
        except (ValueError, json.JSONDecodeError) as exc:
            errors.append(f"album data JSON parse failed: {exc}")
            album_data = []
        try:
            album_groups = parse_js_json_assignment(data_text, "CHAT_VOYAGE_ALBUM_GROUPS")
        except ValueError:
            album_groups = {}
        except json.JSONDecodeError as exc:
            errors.append(f"album group JSON parse failed: {exc}")
            album_groups = {}
        if not isinstance(album_data, list):
            errors.append("album data file has unexpected format")
            album_data = []
        else:
            slugs = [album.get("slug") for album in album_data]
            source_slugs = [album.get("slug") for album in album_sources]
            if len(slugs) != len(set(slugs)):
                errors.append("album data contains duplicate slugs")
            if set(str(slug) for slug in slugs) != set(str(slug) for slug in source_slugs):
                errors.append("album data slugs do not match data/albums sources")
            index_album_sets = {str(figure.get("set")) for figure in parser.figures if figure.get("set")}
            if len(album_data) != len(index_album_sets):
                errors.append(f"album data count mismatch: data={len(album_data)} index_sets={len(index_album_sets)}")
            data_image_count = sum(int(album.get("imageCount", 0)) for album in album_data)
            if data_image_count != len(album_images):
                errors.append(f"album data image count mismatch: data={data_image_count} album_images={len(album_images)}")
            bad_hrefs = [album.get("href") for album in album_data if not str(album.get("href", "")).startswith("album.html?set=")]
            if bad_hrefs:
                errors.append(f"album data has non-canonical hrefs: {bad_hrefs}")
            for album in album_data:
                if not album.get("collection"):
                    errors.append(f"album data missing collection: {album.get('slug')}")
                if not album.get("summaryJa"):
                    errors.append(f"album data missing summaryJa: {album.get('slug')}")
                preferred_aspect_ratio = str(album.get("preferredAspectRatio", "") or "")
                preferred_aspect_error = invalid_aspect_ratio_reason(preferred_aspect_ratio)
                if preferred_aspect_error:
                    errors.append(
                        f"album data preferredAspectRatio {preferred_aspect_error}: {album.get('slug')} -> {preferred_aspect_ratio}"
                    )
                for image in album.get("images", []):
                    for key in ("occasion", "venue", "locationDetail", "activity", "outfit"):
                        if not image.get(key):
                            errors.append(f"album data image missing {key}: {album.get('slug')} / {image.get('src')}")
                    shape_error = image_shape_error(image, str(image.get("src", "") or ""))
                    if shape_error:
                        errors.append(f"album data image {shape_error}: {album.get('slug')} / {image.get('src')}")
                    location_detail = str(image.get("locationDetail", "") or "")
                    location_detail_error = invalid_location_detail_reason(location_detail)
                    if location_detail_error:
                        errors.append(
                            f"album data image locationDetail {location_detail_error}: {album.get('slug')} / {image.get('src')}"
                        )
                    src = str(image.get("src", ""))
                    if not src:
                        errors.append(f"album data image missing src: {album.get('slug')}")
                        continue
                    target = local_target(ROOT, src)
                    if not target.exists():
                        missing_refs.append(f"assets/album-data.js -> {src}")
                    if Path(src).suffix.lower() in IMAGE_SUFFIXES and Path(src).suffix.lower() != ".webp":
                        non_webp_album_refs.append(f"assets/album-data.js -> {src}")
            if album_groups:
                grouped_slugs: set[str] = set()
                daily_group = album_groups.get("daily", []) if isinstance(album_groups, dict) else []
                if isinstance(daily_group, list):
                    grouped_slugs.update(str(slug) for slug in daily_group)
                character_group = album_groups.get("character", {}) if isinstance(album_groups, dict) else {}
                if isinstance(character_group, dict):
                    for values in character_group.values():
                        if isinstance(values, list):
                            grouped_slugs.update(str(slug) for slug in values)
                if grouped_slugs != set(slugs):
                    errors.append("album group slugs do not match album data slugs")
    if missing_refs:
        errors.append("missing local refs: " + ", ".join(missing_refs))
    if legacy_daily_refs:
        errors.append("legacy assets/daily refs in html: " + ", ".join(legacy_daily_refs))
    if non_webp_album_refs:
        errors.append("non-webp album refs in html: " + ", ".join(non_webp_album_refs))

    print(f"album_images: {len(album_images)}")
    print(f"album_source_images: {len(source_images)}")
    print(f"album_source_files: {len(album_sources)}")
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
