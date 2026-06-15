#!/usr/bin/env python3
"""Build the Chat Voyage album index from index.html."""

from __future__ import annotations

from dataclasses import dataclass, field
from html import escape
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass
class Figure:
    src: str = ""
    alt: str = ""
    style: str = ""
    place: str = ""
    category: str = ""


@dataclass
class Album:
    title: str = ""
    notes_href: str = ""
    album_href: str = ""
    meta_text: str = ""
    figures: list[Figure] = field(default_factory=list)


class IndexParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.albums: list[Album] = []
        self._current: Album | None = None
        self._in_section = False
        self._in_h2 = False
        self._in_meta = False
        self._in_meta_link = False
        self._in_figure = False
        self._current_figure: Figure | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if tag == "section" and "data-set" in data:
            self._in_section = True
            self._current = Album()
        elif self._in_section and tag == "h2":
            self._in_h2 = True
        elif self._in_section and tag == "p" and data.get("class") == "meta":
            self._in_meta = True
        elif self._in_section and tag == "a":
            href = data.get("href") or ""
            if href.endswith("-album.html"):
                self._current.album_href = href
            elif href.startswith("notes/") or href.startswith("logs/"):
                self._current.notes_href = href
            if self._in_meta:
                self._in_meta_link = True
        elif self._in_section and tag == "figure":
            self._in_figure = True
            self._current_figure = Figure(
                style=data.get("data-style") or "",
                place=data.get("data-place") or "",
                category=data.get("data-category") or "",
            )
        elif self._in_figure and tag == "img" and self._current_figure:
            self._current_figure.src = data.get("src") or ""
            self._current_figure.alt = data.get("alt") or ""

    def handle_endtag(self, tag: str) -> None:
        if tag == "section" and self._in_section and self._current:
            if self._current.album_href:
                self.albums.append(self._current)
            self._current = None
            self._in_section = False
        elif tag == "h2":
            self._in_h2 = False
        elif tag == "p":
            self._in_meta = False
        elif tag == "a":
            self._in_meta_link = False
        elif tag == "figure":
            if self._current and self._current_figure:
                self._current.figures.append(self._current_figure)
            self._current_figure = None
            self._in_figure = False

    def handle_data(self, data: str) -> None:
        if not self._current:
            return
        text = " ".join(data.split())
        if not text:
            return
        if self._in_h2:
            self._current.title += text
        elif self._in_meta and not self._in_meta_link:
            self._current.meta_text += (" " if self._current.meta_text else "") + text


def build_html(albums: list[Album]) -> str:
    places = sorted({fig.place for album in albums for fig in album.figures if fig.place})
    categories = sorted({fig.category for album in albums for fig in album.figures if fig.category})
    cards = "\n".join(render_card(album) for album in albums)
    place_buttons = "\n".join(
        f'          <button type="button" data-filter="{escape(place)}">{escape(place.title())}</button>'
        for place in places
    )
    category_buttons = "\n".join(
        f'          <button type="button" data-filter="{escape(category)}">{escape(category.title())}</button>'
        for category in categories
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Chat Voyage Albums</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #202124;
      --muted: #61666d;
      --line: #d8dde3;
      --paper: #fbfaf7;
      --panel: #ffffff;
      --accent: #276f86;
      --active: #1f596a;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--paper);
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.5;
    }}
    header, main {{
      width: min(1180px, calc(100% - 32px));
      margin: 0 auto;
    }}
    header {{
      padding: 34px 0 22px;
      border-bottom: 1px solid var(--line);
    }}
    nav {{
      display: flex;
      flex-wrap: wrap;
      gap: 14px;
      margin-bottom: 18px;
      color: var(--muted);
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: clamp(2rem, 4vw, 3.4rem);
      line-height: 1.05;
      letter-spacing: 0;
    }}
    .intro {{
      max-width: 760px;
      margin: 0;
      color: var(--muted);
    }}
    .filters {{
      display: grid;
      gap: 12px;
      padding: 18px 0;
      border-bottom: 1px solid var(--line);
    }}
    .filter-row {{
      display: grid;
      grid-template-columns: 86px 1fr;
      gap: 10px;
      align-items: start;
    }}
    .filter-label {{
      padding-top: 7px;
      color: var(--muted);
      font-size: 0.86rem;
      font-weight: 650;
      text-transform: uppercase;
    }}
    .filter-buttons {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}
    button {{
      min-height: 34px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      color: var(--ink);
      font: inherit;
      font-size: 0.9rem;
      cursor: pointer;
      padding: 6px 10px;
    }}
    button[aria-pressed="true"] {{
      border-color: var(--active);
      background: var(--active);
      color: #fff;
    }}
    .count {{
      margin: 0;
      color: var(--muted);
      font-size: 0.9rem;
    }}
    .albums {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 18px;
      padding: 24px 0 44px;
    }}
    .album-card {{
      display: grid;
      grid-template-rows: auto 1fr;
      min-width: 0;
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      overflow: hidden;
    }}
    .strip {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      background: #eef1f3;
    }}
    .strip img {{
      display: block;
      width: 100%;
      aspect-ratio: 3 / 4;
      object-fit: cover;
      background: #eef1f3;
    }}
    .content {{
      display: grid;
      gap: 9px;
      padding: 14px;
    }}
    h2 {{
      margin: 0;
      font-size: 1.02rem;
      line-height: 1.25;
      letter-spacing: 0;
    }}
    .meta {{
      margin: 0;
      color: var(--muted);
      font-size: 0.9rem;
    }}
    .tags {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      color: var(--muted);
      font-size: 0.82rem;
    }}
    .tag {{
      border: 1px solid var(--line);
      border-radius: 999px;
      padding: 2px 8px;
      background: #fafbfc;
    }}
    .links {{
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin-top: 2px;
    }}
    a {{
      color: var(--accent);
      text-decoration-thickness: 1px;
      text-underline-offset: 3px;
    }}
    .is-hidden {{ display: none; }}
    @media (max-width: 640px) {{
      header, main {{
        width: min(100% - 18px, 520px);
      }}
      .filter-row {{
        grid-template-columns: 1fr;
        gap: 6px;
      }}
      .albums {{
        grid-template-columns: 1fr;
        gap: 14px;
      }}
    }}
  </style>
</head>
<body>
  <header>
    <nav>
      <a href="index.html">Gallery</a>
    </nav>
    <h1>Chat Voyage Albums</h1>
    <p class="intro">Album-level browsing for daily fashion sets. Use this page when the gallery has too many individual images and you want to move by set.</p>
  </header>
  <main>
    <div class="filters" aria-label="Album filters">
      <div class="filter-row">
        <div class="filter-label">Place</div>
        <div class="filter-buttons" data-filter-group="place">
          <button type="button" data-filter="all" aria-pressed="true">All</button>
{place_buttons}
        </div>
      </div>
      <div class="filter-row">
        <div class="filter-label">Category</div>
        <div class="filter-buttons" data-filter-group="category">
          <button type="button" data-filter="all" aria-pressed="true">All</button>
{category_buttons}
        </div>
      </div>
      <p class="count" aria-live="polite">Showing <span id="visible-count">{len(albums)}</span> / <span id="total-count">{len(albums)}</span> albums</p>
    </div>
    <div class="albums">
{cards}
    </div>
  </main>
  <script>
    const state = {{ place: "all", category: "all" }};
    const cards = Array.from(document.querySelectorAll(".album-card"));
    const visibleCount = document.getElementById("visible-count");
    const totalCount = document.getElementById("total-count");
    totalCount.textContent = cards.length;
    function matches(card) {{
      return Object.entries(state).every(([key, value]) => {{
        if (value === "all") return true;
        return (card.dataset[key] || "").split(" ").includes(value);
      }});
    }}
    function update() {{
      let visible = 0;
      cards.forEach((card) => {{
        const show = matches(card);
        card.classList.toggle("is-hidden", !show);
        if (show) visible += 1;
      }});
      visibleCount.textContent = visible;
    }}
    document.querySelectorAll("[data-filter-group]").forEach((group) => {{
      const key = group.dataset.filterGroup;
      group.addEventListener("click", (event) => {{
        const button = event.target.closest("button[data-filter]");
        if (!button) return;
        state[key] = button.dataset.filter;
        group.querySelectorAll("button").forEach((item) => {{
          item.setAttribute("aria-pressed", String(item === button));
        }});
        update();
      }});
    }});
  </script>
</body>
</html>
"""


def render_card(album: Album) -> str:
    places = sorted({fig.place for fig in album.figures if fig.place})
    categories = sorted({fig.category for fig in album.figures if fig.category})
    meta = album.meta_text.lstrip("- ").strip()
    thumbs = "\n".join(
        f'        <img src="{escape(fig.src)}" alt="{escape(fig.alt)}" loading="lazy" decoding="async">'
        for fig in album.figures[:4]
    )
    tags = "\n".join(
        f'        <span class="tag">{escape(value)}</span>'
        for value in [*places, *categories]
    )
    notes = f'<a href="{escape(album.notes_href)}">Notes</a>' if album.notes_href else ""
    return f"""      <article class="album-card" data-place="{escape(' '.join(places))}" data-category="{escape(' '.join(categories))}">
        <a class="strip" href="{escape(album.album_href)}" aria-label="{escape(album.title)} album">
{thumbs}
        </a>
        <div class="content">
          <h2>{escape(album.title)}</h2>
          <p class="meta">{escape(meta)}</p>
          <div class="tags">
{tags}
          </div>
          <div class="links">
            <a href="{escape(album.album_href)}">Open album</a>
            {notes}
          </div>
        </div>
      </article>"""


def main() -> int:
    parser = IndexParser()
    parser.feed((ROOT / "index.html").read_text(encoding="utf-8"))
    html = build_html(parser.albums)
    (ROOT / "albums.html").write_text(html, encoding="utf-8")
    print(f"albums: {len(parser.albums)}")
    print("wrote: albums.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
