#!/usr/bin/env python3
"""Create album pages for index sections that do not have one yet."""

from __future__ import annotations

from dataclasses import dataclass, field
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import re

from rebuild_album_pages import AlbumPage, Figure as AlbumFigure, Link, render_page


ROOT = Path(__file__).resolve().parents[1]


@dataclass
class IndexFigure:
    src: str = ""
    alt: str = ""
    caption_html: str = ""


@dataclass
class IndexSection:
    title: str = ""
    meta_html: str = ""
    notes_href: str = ""
    album_href: str = ""
    image_folder_href: str = ""
    figures: list[IndexFigure] = field(default_factory=list)


class SectionParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.sections: list[IndexSection] = []
        self._section: IndexSection | None = None
        self._in_h2 = False
        self._in_meta = False
        self._meta_parts: list[str] = []
        self._in_figure = False
        self._figure: IndexFigure | None = None
        self._in_caption = False
        self._caption_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        rendered = self.get_starttag_text() or ""
        if tag == "section" and "data-set" in data:
            self._section = IndexSection()
        elif self._section and tag == "h2":
            self._in_h2 = True
        elif self._section and tag == "p" and data.get("class") == "meta":
            self._in_meta = True
            self._meta_parts = []
        elif self._section and self._in_meta and tag == "a":
            href = data.get("href") or ""
            if href.endswith("-album.html"):
                self._section.album_href = href
            elif href.startswith("notes/") or href.startswith("logs/"):
                self._section.notes_href = href
            self._meta_parts.append(rendered)
        elif self._section and tag == "figure":
            self._in_figure = True
            self._figure = IndexFigure()
        elif self._section and self._in_figure and tag == "img" and self._figure:
            self._figure.src = data.get("src") or ""
            self._figure.alt = data.get("alt") or ""
        elif self._section and self._in_figure and tag == "figcaption":
            self._in_caption = True
            self._caption_parts = []
            return

        if self._in_caption:
            self._caption_parts.append(rendered)
        elif self._in_meta and not (tag == "p" and data.get("class") == "meta"):
            self._meta_parts.append(rendered)

    def handle_endtag(self, tag: str) -> None:
        if self._in_caption and tag != "figcaption":
            self._caption_parts.append(f"</{tag}>")
        if self._in_meta and tag != "p":
            self._meta_parts.append(f"</{tag}>")

        if tag == "h2":
            self._in_h2 = False
        elif tag == "p" and self._in_meta:
            if self._section:
                self._section.meta_html = "".join(self._meta_parts).strip()
            self._in_meta = False
        elif tag == "figcaption":
            self._in_caption = False
        elif tag == "figure":
            if self._section and self._figure:
                self._figure.caption_html = "".join(self._caption_parts).strip()
                self._section.figures.append(self._figure)
            self._figure = None
            self._in_figure = False
        elif tag == "section" and self._section:
            self._section.image_folder_href = image_folder_href(self._section)
            self.sections.append(self._section)
            self._section = None

    def handle_data(self, data: str) -> None:
        if self._section and self._in_h2:
            self._section.title += data
        if self._in_meta:
            self._meta_parts.append(escape(data))
        if self._in_caption:
            self._caption_parts.append(escape(data))

    def handle_entityref(self, name: str) -> None:
        self._append_ref(f"&{name};")

    def handle_charref(self, name: str) -> None:
        self._append_ref(f"&#{name};")

    def _append_ref(self, value: str) -> None:
        if self._in_meta:
            self._meta_parts.append(value)
        if self._in_caption:
            self._caption_parts.append(value)


def slugify(title: str) -> str:
    value = title.lower()
    value = value.replace("/", " ")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def image_folder_href(section: IndexSection) -> str:
    if not section.figures:
        return ""
    src = section.figures[0].src
    if not src.startswith("assets/daily/"):
        return ""
    parts = src.split("/")
    if len(parts) < 4:
        return ""
    return f"daily/{parts[2]}/"


def intro_text(meta_html: str) -> str:
    text = re.sub(r"<[^>]+>", " ", meta_html)
    return " ".join(text.split()).lstrip("- ").strip()


def album_page(section: IndexSection, album_href: str) -> str:
    path = ROOT / album_href
    figures = [
        AlbumFigure(
            src=figure.src.removeprefix("assets/"),
            alt=figure.alt,
            caption_html=figure.caption_html,
        )
        for figure in section.figures
    ]
    links = []
    if section.notes_href:
        links.append(Link(f"../{section.notes_href}", "Notes"))
    if section.image_folder_href:
        links.append(Link(section.image_folder_href, "Image Folder"))
    page = AlbumPage(
        path=path,
        document_title=f"{section.title} - Chat Voyage",
        heading=section.title,
        intro=intro_text(section.meta_html),
        links=links,
        figures=figures,
    )
    return render_page(page)


def add_album_links(index_html: str, sections: list[IndexSection]) -> tuple[str, list[str]]:
    updated = index_html
    created_hrefs: list[str] = []
    for section in sections:
        if section.album_href or not section.figures:
            continue
        href = f"assets/{slugify(section.title)}-album.html"
        pattern = re.compile(
            r"(<section data-set>\s*<h2>"
            + re.escape(section.title)
            + r"</h2>\s*<p class=\"meta\">)(.*?)(</p>)",
            flags=re.DOTALL,
        )
        match = pattern.search(updated)
        if not match:
            raise RuntimeError(f"could not find section meta for {section.title}")
        meta = match.group(2)
        if "Album</a>" not in meta:
            meta = f'{meta} <a href="{href}">Album</a>'
        updated = updated[: match.start()] + match.group(1) + meta + match.group(3) + updated[match.end() :]
        section.album_href = href
        created_hrefs.append(href)
    return updated, created_hrefs


def main() -> int:
    index_path = ROOT / "index.html"
    index_html = index_path.read_text(encoding="utf-8")
    parser = SectionParser()
    parser.feed(index_html)

    updated_index, created_hrefs = add_album_links(index_html, parser.sections)
    for section in parser.sections:
        if section.album_href and section.album_href in created_hrefs:
            output = ROOT / section.album_href
            output.write_text(album_page(section, section.album_href), encoding="utf-8")
            print(f"created: {output.relative_to(ROOT)}")

    if created_hrefs:
        index_path.write_text(updated_index, encoding="utf-8")
        print(f"updated: index.html ({len(created_hrefs)} links)")
    else:
        print("missing albums: 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
