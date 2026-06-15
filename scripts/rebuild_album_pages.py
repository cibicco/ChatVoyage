#!/usr/bin/env python3
"""Rebuild all Chat Voyage album pages with the current album template."""

from __future__ import annotations

from dataclasses import dataclass, field
from html import escape, unescape
from html.parser import HTMLParser
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


@dataclass
class Link:
    href: str
    label: str


@dataclass
class Figure:
    src: str
    alt: str
    caption_html: str


@dataclass
class AlbumPage:
    path: Path
    document_title: str = ""
    heading: str = ""
    intro: str = ""
    links: list[Link] = field(default_factory=list)
    figures: list[Figure] = field(default_factory=list)


class AlbumParser(HTMLParser):
    def __init__(self, path: Path) -> None:
        super().__init__(convert_charrefs=False)
        self.page = AlbumPage(path=path)
        self._capture_title = False
        self._capture_h1 = False
        self._capture_intro = False
        self._intro_parts: list[str] = []
        self._in_nav = False
        self._nav_href = ""
        self._nav_parts: list[str] = []
        self._in_figure = False
        self._current_src = ""
        self._current_alt = ""
        self._capture_caption = False
        self._caption_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        rendered = self.get_starttag_text() or ""
        if tag == "title":
            self._capture_title = True
        elif tag == "h1" and not self.page.heading:
            self._capture_h1 = True
        elif tag == "p" and data.get("class") in {"intro", "meta"} and not self.page.intro:
            self._capture_intro = True
            self._intro_parts = []
        elif tag == "nav":
            self._in_nav = True
        elif self._in_nav and tag == "a":
            self._nav_href = data.get("href") or ""
            self._nav_parts = []
        elif tag == "figure":
            self._in_figure = True
            self._current_src = ""
            self._current_alt = ""
            self._caption_parts = []
        elif self._in_figure and tag == "img" and not self._current_src:
            self._current_src = data.get("src") or ""
            self._current_alt = data.get("alt") or ""
        elif self._in_figure and tag == "figcaption":
            self._capture_caption = True
            self._caption_parts = []
            return

        if self._capture_caption:
            self._caption_parts.append(rendered)

    def handle_endtag(self, tag: str) -> None:
        if self._capture_caption and tag != "figcaption":
            self._caption_parts.append(f"</{tag}>")
        if tag == "title":
            self._capture_title = False
        elif tag == "h1":
            self._capture_h1 = False
        elif tag == "p" and self._capture_intro:
            self.page.intro = normalize_text("".join(self._intro_parts))
            self._capture_intro = False
        elif tag == "nav":
            self._in_nav = False
        elif self._in_nav and tag == "a" and self._nav_href:
            label = normalize_text("".join(self._nav_parts))
            self.page.links.append(Link(self._nav_href, label))
            self._nav_href = ""
            self._nav_parts = []
        elif tag == "figcaption":
            self._capture_caption = False
        elif tag == "figure":
            if self._current_src:
                self.page.figures.append(
                    Figure(
                        src=self._current_src,
                        alt=self._current_alt,
                        caption_html=normalize_caption("".join(self._caption_parts), self._current_src),
                    )
                )
            self._in_figure = False

    def handle_data(self, data: str) -> None:
        if self._capture_title:
            self.page.document_title += data
        if self._capture_h1:
            self.page.heading += data
        if self._capture_intro:
            self._intro_parts.append(data)
        if self._in_nav and self._nav_href:
            self._nav_parts.append(data)
        if self._capture_caption:
            self._caption_parts.append(escape(data))

    def handle_entityref(self, name: str) -> None:
        self._append_charref(f"&{name};")

    def handle_charref(self, name: str) -> None:
        self._append_charref(f"&#{name};")

    def _append_charref(self, value: str) -> None:
        if self._capture_title:
            self.page.document_title += value
        if self._capture_h1:
            self.page.heading += value
        if self._capture_intro:
            self._intro_parts.append(value)
        if self._capture_caption:
            self._caption_parts.append(value)


def normalize_text(value: str) -> str:
    return " ".join(value.split())


def unescape_stable(value: str) -> str:
    previous = None
    while value != previous:
        previous = value
        value = unescape(value)
    return value


def normalize_caption(caption: str, src: str) -> str:
    caption = re.sub(
        r"\s*<a\s+class=\"(?:open|open-image)\"\s+href=\"[^\"]+\">Open image</a>\s*",
        "",
        caption,
    ).strip()
    if not caption:
        label = Path(src).stem.replace("-", " ").title()
        caption = f"<h2>{escape(label)}</h2>"
    if not re.search(r"<h2\b", caption):
        text = re.sub(r"<[^>]+>", " ", caption)
        label = normalize_text(text) or Path(src).stem.replace("-", " ").title()
        caption = f"<h2>{escape(label)}</h2>"
    return caption


def normalize_links(page: AlbumPage) -> list[Link]:
    seen: set[str] = set()
    links: list[Link] = []
    for href, label in [
        ("../index.html", "Index"),
        ("../albums.html", "Albums"),
        *[(link.href, link.label) for link in page.links],
    ]:
        if not href or href in seen:
            continue
        seen.add(href)
        links.append(Link(href, label or href))
    return links


def render_page(page: AlbumPage) -> str:
    title = normalize_text(page.document_title) or f"{normalize_text(page.heading)} - Chat Voyage"
    heading = normalize_text(page.heading) or title.replace(" - Chat Voyage", "")
    intro = unescape_stable(page.intro)
    links = "\n".join(
        f'      <a href="{escape(link.href)}">{escape(link.label)}</a>' for link in normalize_links(page)
    )
    figures = "\n".join(render_figure(figure) for figure in page.figures)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #202124;
      --muted: #62666d;
      --line: #d9dde2;
      --paper: #fbfaf7;
      --panel: #ffffff;
      --accent: #276f86;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--paper);
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Hiragino Sans", "Yu Gothic", sans-serif;
      line-height: 1.5;
    }}
    main {{
      width: min(1120px, calc(100% - 32px));
      margin: 0 auto;
      padding: 32px 0 44px;
    }}
    nav {{
      display: flex;
      flex-wrap: wrap;
      gap: 14px;
      margin-bottom: 24px;
      color: var(--muted);
    }}
    a {{
      color: var(--accent);
      text-decoration-thickness: 1px;
      text-underline-offset: 3px;
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: clamp(2rem, 4vw, 3.4rem);
      line-height: 1.05;
      letter-spacing: 0;
    }}
    .intro {{
      max-width: 780px;
      margin: 0 0 24px;
      color: var(--muted);
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 16px;
      align-items: start;
    }}
    figure {{
      margin: 0;
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      overflow: hidden;
    }}
    .image-link {{
      display: block;
      background: #eef1f3;
    }}
    img {{
      display: block;
      width: 100%;
      height: auto;
      max-height: 82vh;
      object-fit: contain;
      background: #eef1f3;
    }}
    figcaption {{ padding: 12px; }}
    h2 {{
      margin: 0 0 6px;
      font-size: 1rem;
      letter-spacing: 0;
    }}
    p {{
      margin: 0;
      color: var(--muted);
      font-size: 0.92rem;
    }}
    dl {{
      display: grid;
      grid-template-columns: max-content 1fr;
      gap: 4px 10px;
      margin: 0;
      color: var(--muted);
      font-size: 0.9rem;
    }}
    dt {{
      color: var(--ink);
      font-weight: 600;
    }}
    dd {{ margin: 0; }}
    .tag {{
      color: var(--accent);
      font-weight: 600;
    }}
    .open-image {{
      display: inline-block;
      margin-top: 10px;
      font-size: 0.9rem;
    }}
    @media (max-width: 720px) {{
      main {{
        width: min(100% - 18px, 480px);
        padding: 18px 0 32px;
      }}
      .grid {{
        grid-template-columns: 1fr;
        gap: 14px;
      }}
      img {{
        max-height: 78vh;
      }}
    }}
  </style>
</head>
<body>
  <main>
    <nav>
{links}
    </nav>
    <h1>{escape(heading)}</h1>
    <p class="intro">{escape(intro)}</p>
    <div class="grid">
{figures}
    </div>
  </main>
</body>
</html>
"""


def render_figure(figure: Figure) -> str:
    src = escape(figure.src)
    alt = escape(figure.alt)
    return f"""      <figure>
        <a class="image-link" href="{src}"><img src="{src}" alt="{alt}" loading="lazy" decoding="async"></a>
        <figcaption>
          {figure.caption_html}
          <a class="open-image" href="{src}">Open image</a>
        </figcaption>
      </figure>"""


def rebuild(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    parser = AlbumParser(path)
    parser.feed(original)
    rendered = render_page(parser.page)
    if rendered == original:
        return False
    path.write_text(rendered, encoding="utf-8")
    return True


def main() -> int:
    changed = []
    for path in sorted((ROOT / "assets").glob("*-album.html")):
        if rebuild(path):
            changed.append(path.relative_to(ROOT))
    for path in changed:
        print(path)
    print(f"changed: {len(changed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
