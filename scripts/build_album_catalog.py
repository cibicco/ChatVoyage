#!/usr/bin/env python3
"""Build the Chat Voyage album product from index.html."""

from __future__ import annotations

from dataclasses import dataclass, field
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]

SPECIAL_LABEL_PARTS = {
    "3d": "3D",
    "cg": "CG",
    "pbr": "PBR",
    "v2": "V2",
}


@dataclass
class Figure:
    src: str = ""
    alt: str = ""
    style: str = ""
    place: str = ""
    category: str = ""
    title: str = ""
    tags_text: str = ""


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
            self._current = Album()
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
            self._current.meta_text = append_text(self._current.meta_text, text)
        elif self._current_figure and self._in_caption_title:
            self._current_figure.title = append_text(self._current_figure.title, text)
        elif self._current_figure and self._in_caption_tags:
            self._current_figure.tags_text = append_text(self._current_figure.tags_text, text)


def normalize_text(value: str) -> str:
    return " ".join(value.split())


def append_text(existing: str, value: str) -> str:
    return f"{existing} {value}".strip() if existing else value


def labelize(value: str) -> str:
    return " ".join(SPECIAL_LABEL_PARTS.get(part, part.capitalize()) for part in value.split("-"))


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def is_album_href(href: str) -> bool:
    return href.endswith("-album.html") or href.startswith("album.html?set=")


def album_date(title: str) -> str:
    match = re.match(r"^(\d{4}-\d{2}-\d{2})", title)
    return match.group(1) if match else ""


def album_month(title: str) -> str:
    date = album_date(title)
    return date[:7] if date else ""


def album_slug(album: Album) -> str:
    href = album.album_href
    if "set=" in href:
        return href.split("set=", 1)[1].split("&", 1)[0].split("#", 1)[0]
    if href.endswith("-album.html"):
        return Path(href).stem.removesuffix("-album")
    return slugify(album.title)


def album_href(album: Album) -> str:
    return f"album.html?set={album_slug(album)}"


def legacy_album_href(album: Album) -> str:
    return f"assets/{album_slug(album)}-album.html"


def short_title(title: str) -> str:
    date = album_date(title)
    return title[len(date) :].strip(" -") if date else title


def clean_meta(album: Album) -> str:
    return album.meta_text.lstrip("- ").strip()


def album_places(album: Album) -> list[str]:
    values = sorted({fig.place for fig in album.figures if fig.place})
    return values or ["unspecified"]


def album_categories(album: Album) -> list[str]:
    return sorted({fig.category for fig in album.figures if fig.category})


def album_styles(album: Album) -> list[str]:
    return sorted({fig.style for fig in album.figures if fig.style})


def figure_title(fig: Figure) -> str:
    if fig.title:
        return fig.title
    return labelize(Path(fig.src).stem)


def figure_age(fig: Figure) -> str:
    parts = [part.strip() for part in fig.tags_text.split("/") if part.strip()]
    if parts:
        last = parts[-1]
        if re.search(r"\d|adult", last):
            return last
    return ""


def album_to_dict(album: Album) -> dict[str, object]:
    slug = album_slug(album)
    categories = album_categories(album)
    styles = album_styles(album)
    places = album_places(album)
    images = []
    for index, fig in enumerate(album.figures, start=1):
        images.append(
            {
                "label": f"{index:02d}",
                "src": fig.src,
                "alt": fig.alt,
                "title": figure_title(fig),
                "tags": fig.tags_text,
                "style": fig.style,
                "place": fig.place,
                "category": fig.category,
                "age": figure_age(fig),
            }
        )
    return {
        "slug": slug,
        "href": f"album.html?set={slug}",
        "legacyHref": f"assets/{slug}-album.html",
        "title": album.title,
        "shortTitle": short_title(album.title),
        "date": album_date(album.title),
        "month": album_month(album.title),
        "summary": clean_meta(album),
        "notesHref": album.notes_href,
        "places": places,
        "categories": categories,
        "styles": styles,
        "imageCount": len(album.figures),
        "images": images,
    }


def filter_button(value: str, label: str | None = None, pressed: bool = False, count: int = 0) -> str:
    label = label or labelize(value)
    return (
        f'          <button type="button" data-filter="{escape(value)}" '
        f'aria-pressed="{str(pressed).lower()}">'
        f'<span class="filter-text">{escape(label)}</span>'
        f'<span class="filter-count">{count}</span></button>'
    )


def build_album_browser(albums: list[Album]) -> str:
    places = sorted({place for album in albums for place in album_places(album)})
    categories = sorted({category for album in albums for category in album_categories(album)})
    styles = sorted({style for album in albums for style in album_styles(album)})
    months = sorted({album_month(album.title) for album in albums if album_month(album.title)}, reverse=True)
    total_images = sum(len(album.figures) for album in albums)
    latest_date = album_date(albums[0].title) if albums else ""

    month_buttons = "\n".join(
        filter_button(month, month, count=sum(1 for album in albums if album_month(album.title) == month))
        for month in months
    )
    place_buttons = "\n".join(
        filter_button(place, count=sum(1 for album in albums if place in album_places(album)))
        for place in places
    )
    category_buttons = "\n".join(
        filter_button(category, count=sum(1 for album in albums if category in album_categories(album)))
        for category in categories
    )
    style_buttons = "\n".join(
        filter_button(style, count=sum(1 for album in albums if style in album_styles(album)))
        for style in styles
    )
    cards = "\n".join(render_card(album, is_latest=(index == 0), index=index) for index, album in enumerate(albums))

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#f4f6f7">
  <title>Chat Voyage Albums</title>
  <link rel="stylesheet" href="assets/album-browser.css">
</head>
<body>
  <a class="skip-link" href="#albums">Skip to albums</a>
  <header class="page-header">
    <nav class="site-nav" aria-label="Primary">
      <a href="index.html">Gallery</a>
      <a href="albums.html" aria-current="page">Albums</a>
    </nav>
    <div class="masthead">
      <div>
        <p class="eyebrow">Chat Voyage</p>
        <h1>Albums</h1>
      </div>
      <dl class="stats" aria-label="Album summary">
        <div><dt>Albums</dt><dd>{len(albums)}</dd></div>
        <div><dt>Images</dt><dd>{total_images}</dd></div>
        <div><dt>Places</dt><dd>{len(places)}</dd></div>
        <div><dt>Latest</dt><dd>{escape(latest_date)}</dd></div>
      </dl>
    </div>
  </header>

  <main class="album-browser" data-album-app data-view="grid">
    <section class="controls" aria-label="Album controls">
      <div class="control-row control-row-main">
        <label class="search-field" for="album-search">
          <span>Search</span>
          <input type="search" id="album-search" placeholder="City, theme, style, category">
        </label>
        <label class="select-field" for="album-sort">
          <span>Sort</span>
          <select id="album-sort">
            <option value="newest">Newest first</option>
            <option value="oldest">Oldest first</option>
            <option value="city">City</option>
            <option value="title">Title</option>
            <option value="images">Image count</option>
          </select>
        </label>
        <div class="view-toggle" aria-label="View mode">
          <button type="button" data-view-option="grid" aria-pressed="true">Grid</button>
          <button type="button" data-view-option="list" aria-pressed="false">List</button>
        </div>
        <button class="reset-button" type="button" id="reset-filters">Reset</button>
      </div>

      <div class="filter-row" data-filter-group="month">
        <div class="filter-label">Month</div>
        <div class="filter-buttons">
{filter_button("all", "All", pressed=True, count=len(albums))}
{month_buttons}
        </div>
      </div>
      <div class="filter-row" data-filter-group="place">
        <div class="filter-label">Place</div>
        <div class="filter-buttons">
{filter_button("all", "All", pressed=True, count=len(albums))}
{place_buttons}
        </div>
      </div>
      <div class="filter-row" data-filter-group="category">
        <div class="filter-label">Category</div>
        <div class="filter-buttons">
{filter_button("all", "All", pressed=True, count=len(albums))}
{category_buttons}
        </div>
      </div>
      <div class="filter-row" data-filter-group="style">
        <div class="filter-label">Style</div>
        <div class="filter-buttons">
{filter_button("all", "All", pressed=True, count=len(albums))}
{style_buttons}
        </div>
      </div>

      <div class="result-bar">
        <p class="count" aria-live="polite"><span id="visible-count">{len(albums)}</span> / <span id="total-count">{len(albums)}</span> albums</p>
        <div class="active-filters" id="active-filters" aria-label="Active filters"></div>
      </div>
    </section>

    <p class="empty-state" id="empty-state" hidden>No albums match the current filters.</p>
    <section class="albums" id="albums" aria-label="Album results">
{cards}
    </section>
  </main>

  <script src="assets/album-browser.js"></script>
</body>
</html>
"""


def render_card(album: Album, *, is_latest: bool, index: int) -> str:
    places = album_places(album)
    categories = album_categories(album)
    styles = album_styles(album)
    meta = clean_meta(album)
    date = album_date(album.title)
    month = album_month(album.title)
    city = labelize(places[0])
    image_count = len(album.figures)
    search = " ".join(
        [
            album.title,
            meta,
            *places,
            *categories,
            *styles,
            *[fig.alt for fig in album.figures if fig.alt],
            *[fig.tags_text for fig in album.figures if fig.tags_text],
        ]
    ).lower()
    badges = render_badges(album, is_latest=is_latest)
    thumbs = "\n".join(render_thumb(fig, album.title) for fig in album.figures[:4])
    place_tags = "\n".join(render_tag(place, "place") for place in places[:2])
    category_tags = "\n".join(render_tag(category, "category") for category in categories[:4])
    notes = f'<a class="secondary-link" href="{escape(album.notes_href)}">Notes</a>' if album.notes_href else ""
    title = escape(album.title)
    href = album_href(album)
    summary = truncate(meta, 150)
    meta_html = f'<p class="summary">{escape(summary)}</p>' if summary else ""

    return f"""      <article class="album-card" data-index="{index}" data-title="{title.lower()}" data-date="{escape(date)}" data-month="{escape(month)}" data-city="{escape(city.lower())}" data-place="{escape(' '.join(places))}" data-category="{escape(' '.join(categories))}" data-style="{escape(' '.join(styles))}" data-image-count="{image_count}" data-search="{escape(search)}">
        <a class="thumb-grid" href="{escape(href)}" aria-label="{title} album">
{thumbs}
        </a>
        <div class="album-content">
          <div class="album-kicker">
            <span>{escape(date)}</span>
            <span>{escape(city)}</span>
            <span>{image_count} images</span>
          </div>
          <div class="title-row">
            <h2><a href="{escape(href)}">{title}</a></h2>
{badges}
          </div>
{meta_html}
          <div class="tag-groups" aria-label="Album metadata">
            <div class="tag-group">{place_tags}</div>
            <div class="tag-group">{category_tags}</div>
          </div>
          <div class="album-actions">
            <a class="primary-link" href="{escape(href)}">Open</a>
            {notes}
          </div>
        </div>
      </article>"""


def render_thumb(fig: Figure, album_title: str) -> str:
    alt = fig.alt or f"{album_title} image"
    return (
        f'          <img src="{escape(fig.src)}" alt="{escape(alt)}" '
        'loading="lazy" decoding="async">'
    )


def render_tag(value: str, kind: str) -> str:
    return f'<span class="tag tag-{kind}">{escape(labelize(value))}</span>'


def render_badges(album: Album, *, is_latest: bool) -> str:
    badges: list[str] = []
    title = album.title.lower()
    if is_latest:
        badges.append("Latest")
    if "remake" in title or " v2" in title or "-v2" in title or "regeneration" in title:
        badges.append("Remake")
    if len(album.figures) != 4:
        badges.append(f"{len(album.figures)} images")
    if not badges:
        return ""
    return '<div class="badges">' + "".join(f'<span class="badge">{escape(badge)}</span>' for badge in badges) + "</div>"


def truncate(value: str, limit: int) -> str:
    if len(value) <= limit:
        return value
    shortened = value[: limit - 3].rstrip()
    if " " in shortened:
        shortened = shortened.rsplit(" ", 1)[0]
    return shortened + "..."


def build_album_data(albums: list[Album]) -> str:
    payload = [album_to_dict(album) for album in albums]
    return "window.CHAT_VOYAGE_ALBUMS = " + json.dumps(payload, indent=2, sort_keys=True) + ";\n"


def build_album_shell() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#f4f6f7">
  <title>Chat Voyage Album</title>
  <link rel="stylesheet" href="assets/album-page.css">
</head>
<body>
  <a class="skip-link" href="#images">Skip to images</a>
  <header class="album-header">
    <nav class="site-nav" aria-label="Primary">
      <a href="index.html">Gallery</a>
      <a href="albums.html">Albums</a>
    </nav>
    <div class="album-tools">
      <label class="album-select-field" for="album-select">
        <span>Album</span>
        <select id="album-select"></select>
      </label>
    </div>
    <p class="eyebrow">Chat Voyage Album</p>
    <div class="title-block">
      <h1 id="album-title">Album</h1>
      <dl class="album-stats" aria-label="Album summary">
        <div><dt>Date</dt><dd id="album-date"></dd></div>
        <div><dt>Images</dt><dd id="album-count"></dd></div>
        <div><dt>Place</dt><dd id="album-place"></dd></div>
      </dl>
    </div>
    <p class="intro" id="album-summary"></p>
  </header>

  <main class="album-viewer" data-album-viewer>
    <section class="viewer" aria-label="Selected image">
      <div class="stage">
        <a class="stage-link" data-stage-link href="#">
          <img class="stage-image" data-stage-image alt="" loading="eager" decoding="async">
        </a>
      </div>
      <aside class="viewer-panel">
        <p class="viewer-count"><span data-current-image>1</span> / <span data-total-images>0</span></p>
        <div class="viewer-caption" data-viewer-caption></div>
        <div class="viewer-actions">
          <button type="button" data-album-prev aria-label="Previous image">&lt;</button>
          <button type="button" data-album-next aria-label="Next image">&gt;</button>
          <a class="open-image" data-open-image href="#">Open image</a>
          <a class="notes-link" data-notes-link href="#" hidden>Notes</a>
        </div>
        <div class="album-neighbors" aria-label="Nearby albums">
          <a data-prev-album href="#"></a>
          <a data-next-album href="#"></a>
        </div>
      </aside>
    </section>

    <div class="thumbnail-strip" data-thumbnail-strip role="list" aria-label="Album thumbnails"></div>

    <section class="overview" id="images" aria-label="Images">
      <div class="section-heading">
        <h2>Images</h2>
        <p data-image-total></p>
      </div>
      <div class="grid" data-image-grid></div>
    </section>
  </main>
  <script src="assets/album-data.js"></script>
  <script src="assets/album-page.js"></script>
</body>
</html>
"""


def build_legacy_album(album: Album) -> str:
    title = escape(album.title)
    href = f"../album.html?set={escape(album_slug(album))}"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="refresh" content="0; url={href}">
  <link rel="canonical" href="{href}">
  <title>{title} - Chat Voyage</title>
</head>
<body data-legacy-album>
  <main>
    <p>This album moved to the unified viewer.</p>
    <p><a href="{href}">Open {title}</a></p>
  </main>
  <script>
    location.replace("{href}" + location.hash);
  </script>
</body>
</html>
"""


def rewrite_index_album_links(albums: list[Album]) -> bool:
    path = ROOT / "index.html"
    text = path.read_text(encoding="utf-8")
    updated = text
    for album in albums:
        hrefs = {album.album_href, legacy_album_href(album)}
        for href in hrefs:
            if href and href != album_href(album):
                updated = updated.replace(f'href="{href}"', f'href="{album_href(album)}"')
    if updated == text:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def write_if_changed(path: Path, content: str) -> bool:
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def parse_index() -> list[Album]:
    parser = IndexParser()
    parser.feed((ROOT / "index.html").read_text(encoding="utf-8"))
    return parser.albums


def main() -> int:
    albums = parse_index()
    if not albums:
        print("ERROR: no albums found in index.html")
        return 1

    changed: list[str] = []
    if rewrite_index_album_links(albums):
        changed.append("index.html")
        albums = parse_index()

    targets = [
        (ROOT / "albums.html", build_album_browser(albums)),
        (ROOT / "album.html", build_album_shell()),
        (ROOT / "assets" / "album-data.js", build_album_data(albums)),
    ]
    for path, content in targets:
        if write_if_changed(path, content):
            changed.append(str(path.relative_to(ROOT)))

    for album in albums:
        path = ROOT / legacy_album_href(album)
        if write_if_changed(path, build_legacy_album(album)):
            changed.append(str(path.relative_to(ROOT)))

    for item in changed:
        print(item)
    print(f"albums: {len(albums)}")
    print(f"changed: {len(changed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
