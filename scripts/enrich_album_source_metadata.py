#!/usr/bin/env python3
"""Populate structured display metadata in data/albums JSON sources."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

from image_dimensions import aspect_ratio, image_dimensions


ROOT = Path(__file__).resolve().parents[1]
ALBUM_DATA_ROOT = ROOT / "data" / "albums"

ACTION_CLAUSES = (
    "adjusting",
    "answering",
    "balancing",
    "carrying",
    "checking",
    "choosing",
    "comparing",
    "entering",
    "fixing",
    "gathering",
    "holding",
    "laughing",
    "leaning",
    "looking",
    "moving",
    "packing",
    "putting",
    "pulling",
    "reading",
    "responding",
    "seated",
    "sitting",
    "smiling",
    "speaking",
    "stepping",
    "studying",
    "tidying",
    "tightening",
    "turning",
    "walking",
    "writing",
)

OUTFIT_HINTS = (
    "blouse",
    "cardigan",
    "dress",
    "jacket",
    "knit",
    "pants",
    "shirt",
    "shorts",
    "skirt",
    "skort",
    "socks",
    "stockings",
    "suit",
    "swimsuit",
    "tee",
    "top",
    "trousers",
    "vest",
)

LOCATION_WEAK_WORDS = re.compile(
    r"\b(look|fashion illustration|fashion|snapshot|partial snapshot|note|remake|regenerated|motion|crop|reach|sash|dress|floor sit|profile|leaning down)\b|(?<!-)\bstyle\b",
    re.IGNORECASE,
)
LOCATION_ACTION_WORDS = re.compile(
    r"\b(wearing|holding|checking|adjusting|carrying|putting|pulling|gathering|fixing|tightening|"
    r"smiling|laughing|writing|seated|walking|leaving|stepping|tidying|packing|studying|"
    r"answering|responding|speaking|waiting|entering|watching|playing|measuring|joining|trying|jumping|stretching|reading|leaning)\b",
    re.IGNORECASE,
)
TITLE_PREFIX_WORDS = {
    "active",
    "ceremony",
    "club",
    "dance",
    "date",
    "formal",
    "gallery",
    "home",
    "lounge",
    "market",
    "mode",
    "night",
    "office",
    "outerwear",
    "resort",
    "street",
    "swim",
    "theater",
    "transit",
    "travel",
    "weekend",
}
VENUE_DETAIL_LABEL = {
    "beach-waterfront": "waterfront",
    "city-outdoor": "street",
    "dining-bar": "bar",
    "event-venue": "event venue",
    "garden-park": "park",
    "home-interior": "interior",
    "library-bookstore": "library or bookstore",
    "market-retail": "market",
    "museum-gallery": "gallery",
    "music-club": "music venue",
    "studio": "studio",
    "transit-hub": "transit hub",
    "waterfront-resort": "waterfront",
    "workplace": "workplace",
}

PLACE_JA = {
    "bangkok": "バンコク",
    "barcelona": "バルセロナ",
    "berlin": "ベルリン",
    "buenos-aires": "ブエノスアイレス",
    "busan": "釜山",
    "copenhagen": "コペンハーゲン",
    "fictional-port-city": "架空の港町",
    "fukuoka": "福岡",
    "hanoi": "ハノイ",
    "helsinki": "ヘルシンキ",
    "hiroshima": "広島",
    "hong-kong": "香港",
    "istanbul": "イスタンブール",
    "kanazawa": "金沢",
    "kobe": "神戸",
    "kyoto": "京都",
    "lagos": "ラゴス",
    "lisbon": "リスボン",
    "madrid": "マドリード",
    "marrakech": "マラケシュ",
    "melbourne": "メルボルン",
    "mexico-city": "メキシコシティ",
    "nagano": "長野",
    "nagasaki": "長崎",
    "nagoya": "名古屋",
    "naha": "那覇",
    "osaka": "大阪",
    "reykjavik": "レイキャビク",
    "sapporo": "札幌",
    "sao-paulo": "サンパウロ",
    "seoul": "ソウル",
    "singapore": "シンガポール",
    "sydney": "シドニー",
    "taipei": "台北",
    "tokyo": "東京",
    "unspecified": "場所未指定",
    "vancouver": "バンクーバー",
    "vienna": "ウィーン",
    "yakushima": "屋久島",
    "yokohama": "横浜",
}

THEME_JA = {
    "adire indigo": "色の軸はアディレインディゴ。",
    "azulejo": "色の軸はアズレージョブルー。",
    "burgundy": "色の軸はバーガンディ。",
    "cempaka": "色の軸はチェンパカイエロー。",
    "celadon": "色の軸はセラドン。",
    "citrus coral": "色の軸はシトラスコーラル。",
    "cloudberry": "色の軸はクラウドベリーアンバー。",
    "coral": "色の軸はコーラル。",
    "gardenia": "色の軸はガーデニアホワイト。",
    "glass blue": "色の軸はグラスブルー。",
    "guava": "色の軸はグアバピンク。",
    "hydrangea": "色の軸はハイドランジアブルー。",
    "indigo": "色の軸はインディゴ。",
    "jabuticaba": "色の軸はジャブチカバパープル。",
    "lilac": "色の軸はライラック。",
    "lotus": "色の軸はロータスピンク。",
    "malbec": "色の軸はマルベックプラム。",
    "mamey coral": "色の軸はマメイコーラル。",
    "mango-lime": "色の軸はマンゴーライム。",
    "milky blue": "色の軸はミルキーブルー。",
    "momiji": "色の軸はもみじバーミリオン。",
    "moss": "色の軸はモスグリーン。",
    "orchid": "色の軸はオーキッドクローム。",
    "pearl apricot": "色の軸はパールアプリコット。",
    "rhubarb": "色の軸はルバーブレッド。",
    "saffron": "色の軸はサフラン。",
    "seaglass": "色の軸はシーグラスグリーン。",
    "sea glass": "色の軸はシーグラスグリーン。",
    "shikuwasa lime": "色の軸はシークワーサーライム。",
    "sumac": "色の軸はスマックレッド。",
    "tezontle coral": "色の軸はテソントレコーラル。",
    "verdigris": "色の軸はヴェルディグリ。",
    "wattle": "色の軸はワトルイエロー。",
    "yuzu": "色の軸は柚子イエロー。",
}

VENUE_JA = {
    "beach-waterfront": "海辺",
    "city-outdoor": "街歩き",
    "dining-bar": "飲食店",
    "event-venue": "イベント会場",
    "garden-park": "公園",
    "home-interior": "室内",
    "library-bookstore": "本と資料",
    "market-retail": "マーケット",
    "museum-gallery": "ミュージアム",
    "music-club": "音楽の場",
    "studio": "スタジオ",
    "transit-hub": "移動",
    "waterfront-resort": "水辺",
    "workplace": "仕事場",
}

ACTIVITY_JA = {
    "attending-event": "イベント",
    "city-walk": "街歩き",
    "commuting": "移動",
    "dancing": "ダンス",
    "dining-drinks": "食事",
    "holiday": "休日",
    "moving": "移動",
    "performance-going": "鑑賞",
    "reading": "読書",
    "relaxing": "休憩",
    "shopping": "買い物",
    "swimming": "水辺",
    "viewing-design": "鑑賞",
    "working": "仕事",
}


def clean_prefix(value: str) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    value = re.sub(
        r"^(?:Shino,\s*adult\s+(?:\d+|\d+-year-old)(?:\s+recurring character)?|Young Shino,\s*age\s+\d+|Adult\s+(?:\d+(?:-\d+)?|early[-\s]?\d+s|mid[-\s]?\d+s|late[-\s]?\d+s)|Early[-\s]?\d+s|Mid[-\s]?\d+s|Late[-\s]?\d+s)\s*,?\s*",
        "",
        value,
        flags=re.I,
    )
    value = re.sub(r"^Japanese-centered woman\s+", "", value, flags=re.I)
    return re.sub(r"^Shino\s+", "", value, flags=re.I)


def before_outfit(value: str) -> str:
    match = re.search(r"\bwhile\s+wearing\b|\bwearing\b", value, flags=re.I)
    return value[: match.start()].strip(" ,") if match else value


def strip_action_clauses(value: str) -> str:
    action_pattern = "|".join(re.escape(word) for word in ACTION_CLAUSES)
    value = re.sub(rf",\s+(?:{action_pattern})\b.*$", "", value, flags=re.I)
    value = re.sub(rf"\s+look\s+(?:{action_pattern})\b.*$", " look", value, flags=re.I)
    value = re.sub(
        rf"\b(?:{action_pattern})\b(?:\s+with\s+[^,]+?)?(?:\s+[^,]+?)?\s+(at|outside|inside|in|on|near|by|along|through)\s+",
        r"\1 ",
        value,
        flags=re.I,
    )
    value = re.sub(
        rf"\b(?:{action_pattern})\s+(through|into|out of|inside|at|on|near|along)\s+",
        r"\1 ",
        value,
        flags=re.I,
    )
    value = re.sub(r"^leaving\s+", "", value, flags=re.I)
    value = re.sub(r"^walking\s+out\s+of\s+", "", value, flags=re.I)
    value = re.sub(r"^stepping\s+into\s+", "", value, flags=re.I)
    value = re.sub(r"^sitting\s+sideways\s+on\s+", "", value, flags=re.I)
    value = re.sub(r"^seated\s+on\s+", "", value, flags=re.I)
    value = re.sub(r"^riding\s+", "", value, flags=re.I)
    value = re.sub(r"^entering\s+(?:the\s+)?", "", value, flags=re.I)
    return value.strip(" ,")


def trim_outfit_tail(value: str) -> str:
    lowered = value.lower()
    for hint in OUTFIT_HINTS:
        marker = f" in a "
        index = lowered.find(marker)
        if index > 0 and hint in lowered[index:]:
            return value[:index].strip(" ,")
    return value.strip(" ,")


def truncate_words(value: str, limit: int = 96) -> str:
    value = value.strip(" ,")
    if len(value) <= limit:
        return value
    shortened = value[: limit - 1].rstrip()
    boundary = max(shortened.rfind(","), shortened.rfind(" "))
    return shortened[: boundary if boundary > 40 else len(shortened)].rstrip() + "…"


def compact_location_text(value: str) -> str:
    value = re.sub(r"\s+", " ", value).strip(" ,")
    action_pattern = "|".join(re.escape(word) for word in ACTION_CLAUSES)
    value = re.sub(rf",\s+(?:{action_pattern})\b.*$", "", value, flags=re.I)
    value = re.sub(r"\s+\b(?:anime|marker|watercolor|digital|semi-real|soft-real|pbr|3d|cg|runway|board|cel|manga|editorial|cinematic)\b.*$", "", value, flags=re.I)
    value = re.sub(r"\s+\b(?:with|wearing)\b.*$", "", value, flags=re.I)
    value = re.sub(r"\s+\b(?:after|before|while)\b.*$", "", value, flags=re.I)
    value = re.sub(r"\b(?:fashion\s+)?(?:illustration|look|snapshot|remake|regenerated|note)\b|(?<!-)\bstyle\b", "", value, flags=re.I)
    value = re.sub(r"\s+(?:in|at|on|near|by|inside|outside|through|along)$", "", value, flags=re.I)
    value = re.sub(r"\s+", " ", value).strip(" ,-")
    return truncate_words(value)


def is_weak_location(value: str) -> bool:
    normalized = value.strip()
    if not normalized or len(normalized) < 8:
        return True
    if LOCATION_WEAK_WORDS.search(normalized):
        return True
    if LOCATION_ACTION_WORDS.search(normalized):
        return True
    if re.fullmatch(r"(?:\d{4}-\d{2}-\d{2}|morning|afternoon|evening|night|dusk|dawn|humid|slow|waiting)", normalized, flags=re.I):
        return True
    if normalized.lower() in {"shino", "tokyo", "seoul", "naha", "istanbul", "vancouver", "yokohama"}:
        return True
    return False


def location_detail_from_alt(alt: str) -> str:
    text = trim_outfit_tail(before_outfit(clean_prefix(alt)))
    text = re.sub(r"\s+(?:with|while)\b.*$", "", text, flags=re.I).strip(" ,")
    look_match = re.search(r"\blook\s+(?:at|in|on|inside|outside|near|by)\s+(?:an|a|the)?\s*([^,]+)", text, flags=re.I)
    if look_match:
        return compact_location_text(look_match.group(1))
    match = re.search(
        r"\b(?:at|inside|in|on|near|through|outside|beside|along|by|under)\s+(?:an|a|the)?\s*([^,]+(?:,\s*[^,]+)?)",
        text,
        flags=re.I,
    )
    value = match.group(1) if match else strip_action_clauses(text)
    value = re.sub(r"\s+(?:after|before|with|while|after visiting)\b.*$", "", value, flags=re.I)
    value = re.sub(r"\s+in\s+the\s+(?:evening|morning|afternoon|night)\b.*$", "", value, flags=re.I)
    return compact_location_text(value)


def title_location_candidate(title: str, image: dict[str, object]) -> str:
    if str(image.get("place", "")) == "unspecified":
        return fallback_location_detail(image)
    value = re.sub(r"^\s*\d+\s+", "", title).strip()
    parts = value.split()
    if parts and parts[0].lower() in TITLE_PREFIX_WORDS:
        parts = parts[1:]
    value = " ".join(parts).strip()
    value = compact_location_text(value)
    words = value.split()
    if len(words) == 1:
        venue = VENUE_DETAIL_LABEL.get(str(image.get("venue", "")), "")
        if venue and words[0].lower() not in venue:
            value = f"{value} {venue}"
    return value


def fallback_location_detail(image: dict[str, object]) -> str:
    place = str(image.get("place", "") or "").replace("-", " ").title() or "Unspecified"
    venue = VENUE_DETAIL_LABEL.get(str(image.get("venue", "")), "setting")
    if place.lower() == "unspecified":
        return f"Unspecified {venue} setting"
    return f"{place} {venue}"


def location_detail_for_image(image: dict[str, object]) -> str:
    if str(image.get("place", "")) == "unspecified":
        return fallback_location_detail(image)
    alt = str(image.get("alt", ""))
    title_candidate = title_location_candidate(str(image.get("title", "")), image)
    alt_candidate = location_detail_from_alt(alt)
    candidates = [title_candidate, alt_candidate, fallback_location_detail(image)] if LOCATION_WEAK_WORDS.search(alt) else [alt_candidate, title_candidate, fallback_location_detail(image)]
    for candidate in candidates:
        candidate = compact_location_text(candidate)
        if not is_weak_location(candidate):
            return candidate
    return fallback_location_detail(image)


def place_ja(album: dict[str, object]) -> str:
    places = [str(image.get("place", "")) for image in album.get("images", []) if isinstance(image, dict)]
    for place in places:
        if place in PLACE_JA:
            return PLACE_JA[place]
    title = str(album.get("title", ""))
    for key, label in PLACE_JA.items():
        if key.replace("-", " ").lower() in title.lower():
            return label
    return "各地"


def theme_ja(album: dict[str, object]) -> str:
    haystack = " ".join([str(album.get("title", "")), str(album.get("summary", ""))]).lower()
    for key, label in THEME_JA.items():
        if key in haystack:
            return label
    return ""


def scene_label(image: dict[str, object]) -> str:
    venue = str(image.get("venue", ""))
    activity = str(image.get("activity", ""))
    return VENUE_JA.get(venue) or ACTIVITY_JA.get(activity) or venue or activity or "画像"


def unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def summary_ja(album: dict[str, object]) -> str:
    images = [image for image in album.get("images", []) if isinstance(image, dict)]
    scenes = "、".join(unique([scene_label(image) for image in images])[:4])
    scene_text = f"構成は{scenes}。" if scenes else ""
    return f"{place_ja(album)}のアルバム。{theme_ja(album)}{scene_text}".strip()


def ordered_album(album: dict[str, object]) -> dict[str, object]:
    top_keys = [
        "slug",
        "title",
        "summary",
        "summaryJa",
        "preferredAspectRatio",
        "collection",
        "character",
        "notesHref",
        "sortOrder",
        "images",
    ]
    ordered = {key: album[key] for key in top_keys if key in album}
    for key, value in album.items():
        if key not in ordered:
            ordered[key] = value
    return ordered


def ordered_image(image: dict[str, object]) -> dict[str, object]:
    image_keys = [
        "label",
        "src",
        "width",
        "height",
        "aspectRatio",
        "alt",
        "title",
        "tags",
        "style",
        "place",
        "category",
        "occasion",
        "venue",
        "locationDetail",
        "activity",
        "outfit",
    ]
    ordered = {key: image[key] for key in image_keys if key in image}
    for key, value in image.items():
        if key not in ordered:
            ordered[key] = value
    return ordered


def has_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def enrich(path: Path, refresh_text: bool = False) -> bool:
    album = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(album, dict):
        raise ValueError(f"album JSON must be object: {path}")
    if refresh_text or not has_text(album.get("summaryJa")):
        album["summaryJa"] = summary_ja(album)
    images = album.get("images", [])
    if not isinstance(images, list):
        raise ValueError(f"album images must be list: {path}")
    enriched_images = []
    for image in images:
        if not isinstance(image, dict):
            raise ValueError(f"album image must be object: {path}")
        src = str(image.get("src", ""))
        if src:
            width, height = image_dimensions(ROOT / src)
            image["width"] = width
            image["height"] = height
            image["aspectRatio"] = aspect_ratio(width, height)
        if refresh_text or not has_text(image.get("locationDetail")):
            image["locationDetail"] = location_detail_for_image(image)
        enriched_images.append(ordered_image(image))
    album["images"] = enriched_images
    next_text = json.dumps(ordered_album(album), ensure_ascii=False, indent=2) + "\n"
    old_text = path.read_text(encoding="utf-8")
    if next_text == old_text:
        return False
    path.write_text(next_text, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--refresh-text",
        action="store_true",
        help="also regenerate summaryJa and locationDetail; by default existing human-edited text is preserved",
    )
    args = parser.parse_args()
    changed = 0
    for path in sorted(ALBUM_DATA_ROOT.rglob("*.json")):
        if enrich(path, refresh_text=args.refresh_text):
            changed += 1
            print(path.relative_to(ROOT))
    print(f"changed: {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
