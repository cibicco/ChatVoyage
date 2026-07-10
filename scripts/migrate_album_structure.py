#!/usr/bin/env python3
"""Migrate album files to collection/year/month folders and write JSON sources."""

from __future__ import annotations

from dataclasses import dataclass, field
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil


ROOT = Path(__file__).resolve().parents[1]


@dataclass
class Figure:
    src: str = ""
    alt: str = ""
    style: str = ""
    place: str = ""
    category: str = ""
    occasion: str = ""
    venue: str = ""
    activity: str = ""
    outfit: str = ""
    title: str = ""
    tags: str = ""


@dataclass
class Album:
    title: str = ""
    summary: str = ""
    notes_href: str = ""
    album_href: str = ""
    collection: str = "daily"
    character: str = ""
    figures: list[Figure] = field(default_factory=list)


class IndexParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.albums: list[Album] = []
        self._current: Album | None = None
        self._current_figure: Figure | None = None
        self._in_section = False
        self._in_h2 = False
        self._in_meta = False
        self._in_meta_link = False
        self._in_figure = False
        self._in_caption = False
        self._in_caption_title = False
        self._in_caption_tags = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if tag == "section" and "data-set" in data:
            self._in_section = True
            self._current = Album(
                collection=data.get("data-collection") or "daily",
                character=data.get("data-character") or "",
            )
        elif self._in_section and tag == "h2":
            self._in_h2 = True
        elif self._in_section and tag == "p" and data.get("class") == "meta":
            self._in_meta = True
        elif self._in_section and tag == "a" and self._current:
            href = data.get("href") or ""
            if is_album_href(href):
                self._current.album_href = href
            elif href.startswith(("notes/", "logs/")):
                self._current.notes_href = href
            if self._in_meta:
                self._in_meta_link = True
        elif self._in_section and tag == "figure":
            self._in_figure = True
            self._current_figure = Figure(
                style=data.get("data-style") or "",
                place=data.get("data-place") or "",
                category=data.get("data-category") or "",
                occasion=data.get("data-occasion") or "",
                venue=data.get("data-venue") or "",
                activity=data.get("data-activity") or "",
                outfit=data.get("data-outfit") or "",
            )
        elif self._in_figure and tag == "img" and self._current_figure:
            self._current_figure.src = data.get("src") or ""
            self._current_figure.alt = data.get("alt") or ""
        elif self._in_figure and tag == "figcaption":
            self._in_caption = True
        elif self._in_caption and tag == "strong":
            self._in_caption_title = True
        elif self._in_caption and tag == "span" and data.get("class") == "tags":
            self._in_caption_tags = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "section" and self._in_section and self._current:
            if self._current.album_href or self._current.figures:
                self.albums.append(self._current)
            self._current = None
            self._in_section = False
        elif tag == "h2":
            self._in_h2 = False
        elif tag == "p":
            self._in_meta = False
        elif tag == "a":
            self._in_meta_link = False
        elif tag == "strong":
            self._in_caption_title = False
        elif tag == "span":
            self._in_caption_tags = False
        elif tag == "figcaption":
            self._in_caption = False
        elif tag == "figure":
            if self._current and self._current_figure:
                self._current.figures.append(self._current_figure)
            self._current_figure = None
            self._in_figure = False

    def handle_data(self, data: str) -> None:
        text = normalize_text(data)
        if not text:
            return
        if self._current and self._in_h2:
            self._current.title = append_text(self._current.title, text)
        elif self._current and self._in_meta and not self._in_meta_link:
            self._current.summary = append_text(self._current.summary, text)
        elif self._current_figure and self._in_caption_title:
            self._current_figure.title = append_text(self._current_figure.title, text)
        elif self._current_figure and self._in_caption_tags:
            self._current_figure.tags = append_text(self._current_figure.tags, text)


def normalize_text(value: str) -> str:
    return " ".join(value.split())


def append_text(existing: str, value: str) -> str:
    return f"{existing} {value}".strip() if existing else value


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def is_album_href(href: str) -> bool:
    return href.endswith("-album.html") or href.startswith("album.html?set=")


def album_slug(album: Album) -> str:
    if "set=" in album.album_href:
        return album.album_href.split("set=", 1)[1].split("&", 1)[0].split("#", 1)[0]
    if album.album_href.endswith("-album.html"):
        return Path(album.album_href).stem.removesuffix("-album")
    return slugify(album.title)


def album_date(album: Album) -> str:
    match = re.match(r"^(\d{4})-(\d{2})-(\d{2})", album.title)
    return match.group(0) if match else ""


def year_month(album: Album) -> tuple[str, str]:
    date = album_date(album)
    return (date[:4], date[5:7]) if date else ("undated", "unknown")


def album_base(collection: str, character: str) -> Path:
    if collection == "character":
        return Path("assets/albums/characters") / (character or "unknown")
    return Path("assets/albums/daily")


def note_base(collection: str, character: str) -> Path:
    if collection == "character":
        return Path("notes/albums/characters") / (character or "unknown")
    return Path("notes/albums/daily")


def data_base(collection: str, character: str) -> Path:
    if collection == "character":
        return Path("data/albums/characters") / (character or "unknown")
    return Path("data/albums/daily")


def target_album_dir(album: Album) -> Path:
    year, month = year_month(album)
    return album_base(album.collection, album.character) / year / month / album_slug(album)


def target_note_path(album: Album) -> Path:
    year, month = year_month(album)
    return note_base(album.collection, album.character) / year / month / f"{album_slug(album)}.md"


def target_data_path(album: Album) -> Path:
    year, month = year_month(album)
    return data_base(album.collection, album.character) / year / month / f"{album_slug(album)}.json"


def old_album_dir(album: Album) -> Path | None:
    for figure in album.figures:
        parts = Path(figure.src).parts
        if len(parts) >= 3 and parts[0] == "assets" and parts[1] == "daily":
            return Path("assets/daily") / parts[2]
    return None


def move_tree(source: Path, target: Path) -> None:
    source_abs = ROOT / source
    target_abs = ROOT / target
    if source_abs == target_abs:
        return
    if source_abs.exists():
        if target_abs.exists():
            for child in source_abs.iterdir():
                destination = target_abs / child.name
                if destination.exists():
                    continue
                shutil.move(str(child), str(destination))
            try:
                source_abs.rmdir()
            except OSError:
                pass
        else:
            target_abs.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source_abs), str(target_abs))
    elif not target_abs.exists():
        raise FileNotFoundError(f"missing album image folder: {source}")


def move_note(album: Album) -> str:
    if not album.notes_href.startswith("notes/"):
        return album.notes_href
    source = Path(album.notes_href)
    target = target_note_path(album)
    source_abs = ROOT / source
    target_abs = ROOT / target
    if source_abs.exists():
        target_abs.parent.mkdir(parents=True, exist_ok=True)
        if target_abs.exists():
            source_abs.unlink()
        else:
            shutil.move(str(source_abs), str(target_abs))
        return target.as_posix()
    if target_abs.exists():
        return target.as_posix()
    return album.notes_href


def build_payload(album: Album, index: int, notes_href: str) -> dict[str, object]:
    slug = album_slug(album)
    image_dir = target_album_dir(album)
    images = []
    for position, figure in enumerate(album.figures, start=1):
        filename = Path(figure.src).name
        images.append(
            {
                "label": f"{position:02d}",
                "src": (image_dir / filename).as_posix(),
                "alt": figure.alt,
                "title": figure.title,
                "tags": figure.tags,
                "style": figure.style,
                "place": figure.place,
                "category": figure.category,
                "occasion": figure.occasion,
                "venue": figure.venue,
                "activity": figure.activity,
                "outfit": figure.outfit,
            }
        )
    return {
        "slug": slug,
        "title": album.title,
        "summary": album.summary.lstrip("- ").strip(),
        "collection": album.collection,
        "character": album.character,
        "notesHref": notes_href,
        "sortOrder": index,
        "images": images,
    }


def rewrite_text_references(replacements: dict[str, str]) -> list[str]:
    targets = [
        ROOT / "index.html",
        ROOT / "albums.html",
        ROOT / "assets" / "album-data.js",
        *sorted((ROOT / "logs").glob("*.md")),
        *sorted((ROOT / "docs").rglob("*.md")),
        *sorted((ROOT / "prompts").glob("*.md")),
        *sorted((ROOT / "skills").rglob("*.md")),
    ]
    changed: list[str] = []
    for path in targets:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        updated = text
        for old, new in replacements.items():
            updated = updated.replace(old, new)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed.append(path.relative_to(ROOT).as_posix())
    return changed


def parse_index() -> list[Album]:
    parser = IndexParser()
    parser.feed((ROOT / "index.html").read_text(encoding="utf-8"))
    return parser.albums


def main() -> int:
    albums = parse_index()
    if not albums:
        print("ERROR: no albums found in index.html")
        return 1

    replacements: dict[str, str] = {}
    written: list[str] = []
    moved_dirs: list[str] = []
    moved_notes: list[str] = []

    for index, album in enumerate(albums):
        old_dir = old_album_dir(album)
        new_dir = target_album_dir(album)
        if old_dir:
            replacements[old_dir.as_posix()] = new_dir.as_posix()
            move_tree(old_dir, new_dir)
            moved_dirs.append(f"{old_dir.as_posix()} -> {new_dir.as_posix()}")
        old_note = album.notes_href if album.notes_href.startswith("notes/") else ""
        new_note = move_note(album)
        if old_note and new_note != old_note:
            replacements[old_note] = new_note
            moved_notes.append(f"{old_note} -> {new_note}")
        data_path = target_data_path(album)
        data_path_abs = ROOT / data_path
        data_path_abs.parent.mkdir(parents=True, exist_ok=True)
        data_path_abs.write_text(
            json.dumps(build_payload(album, index, new_note), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        written.append(data_path.as_posix())

    ds_store = ROOT / "assets" / "daily" / ".DS_Store"
    if ds_store.exists():
        ds_store.unlink()
    try:
        (ROOT / "assets" / "daily").rmdir()
    except OSError:
        pass

    changed_text = rewrite_text_references(replacements)
    for line in moved_dirs:
        print("moved:", line)
    for line in moved_notes:
        print("moved:", line)
    for line in written:
        print("json:", line)
    for line in changed_text:
        print("rewrote:", line)
    print(f"albums: {len(albums)}")
    print(f"json_files: {len(written)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
