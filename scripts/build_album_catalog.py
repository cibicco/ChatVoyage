#!/usr/bin/env python3
"""Build the Chat Voyage gallery and album pages from JSON album sources."""

from __future__ import annotations

from dataclasses import dataclass, field
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import re

from gallery_metadata import classify_image, labelize_metadata


ROOT = Path(__file__).resolve().parents[1]
ALBUM_DATA_ROOT = ROOT / "data" / "albums"
ASSET_VERSION = "20260706-ux-review-10"
THUMB_CONTAIN_MIN_RATIO = 0.62
THUMB_CONTAIN_MAX_RATIO = 0.72

GALLERY_STYLE = """
    :root {
      color-scheme: light;
      --ink: #202124;
      --muted: #61666d;
      --line: #d8dde3;
      --paper: #fbfaf7;
      --panel: #ffffff;
      --accent: #276f86;
      --active: #1f596a;
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      background: var(--paper);
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.5;
    }

    header,
    main {
      width: min(1120px, calc(100% - 32px));
      margin: 0 auto;
    }

    header {
      padding: 8px 0 6px;
      border-bottom: 1px solid var(--line);
    }

    nav {
      display: flex;
      flex-wrap: wrap;
      gap: 14px;
      margin-bottom: 2px;
      color: var(--muted);
      font-size: 0.88rem;
    }

    h1 {
      margin: 0;
      font-size: 1.25rem;
      line-height: 1.1;
      letter-spacing: 0;
    }

    .intro {
      display: none;
      margin: 0;
      max-width: 680px;
      color: var(--muted);
      font-size: 0.95rem;
    }

    .filters {
      padding: 8px 0 6px;
      display: grid;
      gap: 6px;
      border-bottom: 1px solid var(--line);
    }

    .filter-row {
      display: grid;
      grid-template-columns: 74px minmax(0, 1fr);
      gap: 8px;
      align-items: center;
    }

    .filter-label {
      color: var(--muted);
      font-size: 0.75rem;
      font-weight: 650;
      text-transform: uppercase;
    }

    .filter-buttons {
      display: flex;
      flex-wrap: nowrap;
      gap: 6px;
      overflow-x: auto;
      padding: 0 18px 2px 0;
      scrollbar-width: thin;
      -webkit-mask-image: linear-gradient(90deg, #000 calc(100% - 24px), transparent);
      mask-image: linear-gradient(90deg, #000 calc(100% - 24px), transparent);
    }

    .gallery-controls {
      display: grid;
      grid-template-columns: minmax(160px, 0.28fr) auto;
      gap: 6px;
      align-items: center;
      justify-content: end;
    }

    .gallery-select-field {
      display: grid;
      min-width: 0;
    }

    .gallery-select-field span {
      position: absolute;
      width: 1px;
      height: 1px;
      overflow: hidden;
      clip: rect(0 0 0 0);
      clip-path: inset(50%);
      white-space: nowrap;
    }

    .gallery-select-field select {
      width: 100%;
      min-height: 30px;
      border: 1px solid var(--line);
      border-radius: 7px;
      background: var(--panel);
      color: var(--ink);
      font: inherit;
      font-size: 0.86rem;
      padding: 4px 8px;
    }

    .size-toggle {
      display: flex;
      min-height: 30px;
      border: 1px solid var(--line);
      border-radius: 7px;
      overflow: hidden;
      background: var(--panel);
    }

    .size-toggle button {
      min-height: 28px;
      border: 0;
      border-right: 1px solid var(--line);
      border-radius: 0;
      padding-inline: 10px;
    }

    .size-toggle button:last-child {
      border-right: 0;
    }

    button {
      flex: 0 0 auto;
      min-height: 30px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      color: var(--ink);
      font: inherit;
      font-size: 0.84rem;
      cursor: pointer;
      padding: 5px 9px;
      white-space: nowrap;
    }

    button[aria-pressed="true"] {
      border-color: var(--active);
      background: var(--active);
      color: #fff;
    }

    button.is-zero:not([aria-pressed="true"]) {
      opacity: 0.38;
    }

    button:disabled {
      cursor: default;
    }

    .advanced-filters {
      display: grid;
      gap: 6px;
      min-width: 0;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
    }

    .advanced-filters summary {
      display: flex;
      gap: 10px;
      align-items: center;
      justify-content: space-between;
      min-height: 32px;
      color: var(--ink);
      cursor: pointer;
      font-size: 0.82rem;
      font-weight: 760;
      list-style: none;
      padding: 4px 8px;
    }

    .advanced-filters summary::-webkit-details-marker {
      display: none;
    }

    .advanced-filters summary::after {
      content: "+";
      color: var(--muted);
      font-weight: 760;
    }

    .advanced-filters[open] summary::after {
      content: "-";
    }

    .filter-summary {
      overflow: hidden;
      color: var(--muted);
      font-size: 0.78rem;
      font-weight: 650;
      text-align: right;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    .advanced-filter-body {
      display: grid;
      gap: 8px;
      padding: 0 10px 10px;
    }

    .gallery-collection {
      padding: 10px 0 0;
    }

    .gallery-collection + .gallery-collection {
      border-top: 3px solid var(--line);
      margin-top: 18px;
    }

    .gallery-collection.is-hidden {
      display: none;
    }

    .collection-heading {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: center;
      border-bottom: 1px solid var(--line);
      padding-bottom: 7px;
    }

    .collection-heading h2 {
      margin: 0;
      font-size: 1.05rem;
      line-height: 1.15;
      letter-spacing: 0;
    }

    .collection-count {
      display: inline-flex;
      align-items: center;
      min-height: 22px;
      margin: 0;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: var(--panel);
      color: var(--accent);
      font-size: 0.78rem;
      font-weight: 700;
      padding: 1px 8px;
    }

    section[data-set] {
      padding: 8px 0 14px;
      content-visibility: auto;
      contain-intrinsic-size: 900px;
    }

    section.is-hidden,
    figure.is-hidden,
    .empty.is-hidden {
      display: none;
    }

    h2 {
      margin: 0 0 6px;
      font-size: 1.18rem;
      letter-spacing: 0;
    }

    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
      gap: 16px;
      justify-content: start;
      align-items: start;
    }

    body[data-image-size="large"] .grid {
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    }

    figure {
      margin: 0;
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      overflow: hidden;
    }

    figure:focus-visible {
      outline: 2px solid var(--active);
      outline-offset: 3px;
    }

    figure img {
      cursor: zoom-in;
    }

    img {
      display: block;
      width: 100%;
      height: auto;
      aspect-ratio: 2 / 3;
      object-fit: contain;
      background: #eef1f3;
    }

    body[data-image-size="large"] figcaption {
      font-size: 0.95rem;
    }

    figcaption {
      padding: 10px 11px 12px;
      color: var(--muted);
      font-size: 0.9rem;
    }

    figcaption strong {
      display: block;
      margin-bottom: 2px;
      color: var(--ink);
      font-weight: 650;
    }

    figcaption strong a {
      color: inherit;
      text-decoration: none;
    }

    figcaption strong a:hover {
      color: var(--accent);
      text-decoration: underline;
    }

    .tags {
      display: block;
      color: var(--muted);
      font-size: 0.82rem;
    }

    .empty {
      padding: 26px 0 40px;
      color: var(--muted);
    }

    a {
      color: var(--accent);
      text-decoration-thickness: 1px;
      text-underline-offset: 3px;
    }

    body.is-lightbox-open {
      overflow: hidden;
    }

    .lightbox {
      position: fixed;
      inset: 0;
      z-index: 30;
      display: grid;
      grid-template-columns: minmax(0, 1fr);
      grid-template-rows: minmax(0, 1fr);
      background: #050607;
      color: #fff;
      padding: 10px;
    }

    .lightbox[hidden] {
      display: none;
    }

    .lightbox-bar {
      position: absolute;
      top: 10px;
      left: 10px;
      right: 10px;
      z-index: 2;
      display: flex;
      gap: 12px;
      align-items: center;
      justify-content: space-between;
      pointer-events: none;
    }

    .lightbox-count {
      margin: 0;
      color: rgba(255, 255, 255, 0.76);
      font-size: 0.86rem;
      font-weight: 760;
    }

    .lightbox-actions {
      display: flex;
      gap: 8px;
      align-items: center;
      pointer-events: auto;
    }

    .lightbox-actions a,
    .lightbox-actions button,
    .lightbox-nav {
      min-height: 34px;
      border: 1px solid rgba(255, 255, 255, 0.18);
      border-radius: 8px;
      background: rgba(0, 0, 0, 0.24);
      color: #fff;
      font-size: 0.82rem;
      font-weight: 700;
      padding: 6px 9px;
    }

    .lightbox-actions a {
      display: inline-flex;
      align-items: center;
      text-decoration: none;
    }

    .lightbox-nav {
      position: absolute;
      top: 72px;
      bottom: 72px;
      z-index: 2;
      width: min(14vw, 96px);
      min-width: 44px;
      min-height: 58px;
      border: 0;
      border-radius: 0;
      background: transparent;
      color: rgba(255, 255, 255, 0.32);
      font-size: 1.8rem;
      cursor: pointer;
    }

    .lightbox-nav:hover {
      background: rgba(255, 255, 255, 0.05);
      color: rgba(255, 255, 255, 0.74);
    }

    .lightbox-prev {
      left: 0;
    }

    .lightbox-next {
      right: 0;
    }

    .lightbox img {
      grid-column: 1;
      grid-row: 1;
      align-self: center;
      justify-self: center;
      display: block;
      width: auto;
      max-width: calc(100vw - 20px);
      max-height: calc(100dvh - 20px);
      aspect-ratio: auto;
      object-fit: contain;
      background: transparent;
      cursor: e-resize;
    }

    .lightbox-caption {
      display: none;
      gap: 4px;
      max-width: 760px;
      justify-self: center;
      color: rgba(255, 255, 255, 0.74);
      text-align: center;
    }

    .lightbox-caption strong {
      color: #fff;
    }

    @media (max-width: 640px) {
      header,
      main {
        width: min(100% - 18px, 520px);
      }

      header {
        padding: 7px 0 6px;
      }

      h1 {
        font-size: 1.15rem;
      }

      .filter-row {
        grid-template-columns: 66px minmax(0, 1fr);
      }

      [data-filter-group="collection"] {
        flex-wrap: wrap;
        overflow-x: visible;
        padding-right: 0;
        -webkit-mask-image: none;
        mask-image: none;
      }

      .grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 10px;
      }

      body[data-image-size="large"] .grid {
        grid-template-columns: 1fr;
      }

      .gallery-controls {
        grid-template-columns: minmax(0, 1fr) auto;
      }

      figcaption {
        padding: 8px 9px 10px;
        font-size: 0.82rem;
      }

      .tags {
        font-size: 0.76rem;
      }

      .lightbox {
        padding: 8px;
      }

      .lightbox-actions {
        flex-wrap: wrap;
        justify-content: flex-end;
      }

      .lightbox-nav {
        top: 64px;
        bottom: 64px;
        width: 54px;
      }

      .lightbox img {
        max-width: calc(100vw - 16px);
        max-height: calc(100dvh - 16px);
      }

      .lightbox-caption {
        grid-column: 1 / -1;
        font-size: 0.86rem;
      }
    }
"""

GALLERY_SCRIPT = """
    const filters = {
      collection: "all",
      style: "all",
      place: "all",
      occasion: "all",
      venue: "all",
      activity: "all",
      outfit: "all"
    };

    const figures = Array.from(document.querySelectorAll("figure[data-style]"));
    const sections = Array.from(document.querySelectorAll("section[data-set]"));
    const collectionGroups = Array.from(document.querySelectorAll("[data-gallery-collection]"));
    const filterGroups = Array.from(document.querySelectorAll("[data-filter-group]"));
    const filterSummary = document.querySelector("[data-filter-summary]");
    const gallerySort = document.getElementById("gallery-sort");
    const sizeButtons = Array.from(document.querySelectorAll("[data-size-option]"));
    const empty = document.querySelector(".empty");
    const lightbox = document.querySelector("[data-lightbox]");
    const lightboxImage = document.querySelector("[data-lightbox-image]");
    const lightboxCaption = document.querySelector("[data-lightbox-caption]");
    const lightboxCurrent = document.querySelector("[data-lightbox-current]");
    const lightboxTotal = document.querySelector("[data-lightbox-total]");
    const lightboxOpen = document.querySelector("[data-lightbox-open]");
    const lightboxClose = document.querySelector("[data-lightbox-close]");
    const lightboxPrev = document.querySelector("[data-lightbox-prev]");
    const lightboxNext = document.querySelector("[data-lightbox-next]");
    let activeFigure = -1;
    let lightboxActive = false;

    figures.forEach((figure, index) => {
      figure.tabIndex = 0;
      figure.dataset.originalIndex = String(index);
    });

    function compareDateDesc(a, b) {
      const byDate = (b.dataset.date || "").localeCompare(a.dataset.date || "");
      if (byDate) return byDate;
      return Number(a.dataset.originalIndex || 0) - Number(b.dataset.originalIndex || 0);
    }

    function sortFigures() {
      const value = gallerySort?.value || "newest";
      const sorted = [...figures].sort((a, b) => {
        if (value === "oldest") {
          return (a.dataset.date || "").localeCompare(b.dataset.date || "") || Number(a.dataset.originalIndex || 0) - Number(b.dataset.originalIndex || 0);
        }
        if (value === "title") {
          return (a.dataset.title || "").localeCompare(b.dataset.title || "") || compareDateDesc(a, b);
        }
        if (value === "album") {
          return (a.dataset.albumTitle || "").localeCompare(b.dataset.albumTitle || "") || compareDateDesc(a, b);
        }
        return compareDateDesc(a, b);
      });
      const grid = document.querySelector("[data-gallery-collection] .grid");
      if (grid) sorted.forEach((figure) => grid.appendChild(figure));
    }

    function filterValue(figure, key) {
      if (key === "collection") {
        return figure.dataset.collection || "daily";
      }
      return figure.dataset[key] || "";
    }

    function matches(figure) {
      return Object.entries(filters).every(([key, value]) => {
        return value === "all" || filterValue(figure, key) === value;
      });
    }

    function matchesWith(figure, overrides = {}) {
      return Object.entries({ ...filters, ...overrides }).every(([key, value]) => {
        return value === "all" || filterValue(figure, key) === value;
      });
    }

    function selectedFilterLabel(group, value) {
      const button = document.querySelector(`[data-filter-group="${group}"] button[data-filter="${value}"]`);
      return button?.querySelector(".filter-text")?.textContent || value;
    }

    function renderFilterSummary() {
      if (!filterSummary) return;
      const entries = Object.entries(filters).filter(([group, value]) => group !== "collection" && value !== "all");
      filterSummary.textContent = entries.length
        ? entries.map(([group, value]) => selectedFilterLabel(group, value)).join(", ")
        : "すべて";
    }

    function updateOptionCounts() {
      filterGroups.forEach((group) => {
        const key = group.dataset.filterGroup;
        group.querySelectorAll("button[data-filter]").forEach((button) => {
          const value = button.dataset.filter;
          const count = figures.filter((figure) => matchesWith(figure, { [key]: value })).length;
          const label = button.querySelector(".filter-count");
          if (label) label.textContent = `(${count})`;
          const isZero = count === 0;
          button.classList.toggle("is-zero", isZero);
          button.disabled = isZero && button.getAttribute("aria-pressed") !== "true";
        });
      });
    }

    function applyFilters() {
      let count = 0;
      sortFigures();

      figures.forEach((figure) => {
        const visible = matches(figure);
        figure.classList.toggle("is-hidden", !visible);
        if (visible) count += 1;
      });

      sections.forEach((section) => {
        const hasVisibleFigure = Boolean(section.querySelector("figure:not(.is-hidden)"));
        section.classList.toggle("is-hidden", !hasVisibleFigure);
      });

      collectionGroups.forEach((group) => {
        const collection = group.dataset.galleryCollection;
        const visibleInGroup = figures.filter((figure) => {
          return (collection === "all" || figure.dataset.collection === collection) && !figure.classList.contains("is-hidden");
        }).length;
        const countNode = group.querySelector(`[data-gallery-collection-count="${collection}"]`);
        if (countNode) countNode.textContent = `${visibleInGroup} / ${group.dataset.galleryCollectionTotal || 0} images`;
        group.classList.toggle("is-hidden", visibleInGroup === 0);
      });

      empty.classList.toggle("is-hidden", count !== 0);
      updateOptionCounts();
      renderFilterSummary();
      if (lightboxActive) renderLightbox();
    }

    function visibleFigures() {
      return figures.filter((figure) => !figure.classList.contains("is-hidden"));
    }

    function figureCaption(figure) {
      const strong = figure.querySelector("figcaption strong")?.textContent || "";
      const tags = figure.querySelector(".tags")?.textContent || "";
      return { strong, tags };
    }

    function openLightbox(figure) {
      const visible = visibleFigures();
      activeFigure = visible.indexOf(figure);
      if (activeFigure < 0) activeFigure = figures.indexOf(figure);
      if (activeFigure < 0) return;
      lightboxActive = true;
      lightbox.hidden = false;
      document.body.classList.add("is-lightbox-open");
      renderLightbox();
      lightboxClose.focus();
    }

    function closeLightbox() {
      lightboxActive = false;
      lightbox.hidden = true;
      document.body.classList.remove("is-lightbox-open");
      const figure = visibleFigures()[activeFigure];
      if (figure) figure.focus();
    }

    function moveLightbox(delta) {
      const visible = visibleFigures();
      if (!visible.length) return;
      activeFigure = (activeFigure + delta + visible.length) % visible.length;
      renderLightbox();
    }

    function renderLightbox() {
      const visible = visibleFigures();
      const figure = visible[activeFigure];
      if (!figure) {
        closeLightbox();
        return;
      }
      const image = figure.querySelector("img");
      const caption = figureCaption(figure);
      lightboxImage.src = image.src;
      lightboxImage.alt = image.alt || "";
      lightboxOpen.href = image.src;
      lightboxCurrent.textContent = String(activeFigure + 1);
      lightboxTotal.textContent = String(visible.length);
      lightboxCaption.replaceChildren();
      const title = document.createElement("strong");
      title.textContent = caption.strong || image.alt || "Image";
      const meta = document.createElement("span");
      meta.textContent = caption.tags ? `\\n${caption.tags}` : "";
      lightboxCaption.append(title, meta);
    }

    filterGroups.forEach((group) => {
      group.addEventListener("click", (event) => {
        const button = event.target.closest("button[data-filter]");
        if (!button) return;

        const key = group.dataset.filterGroup;
        filters[key] = button.dataset.filter;

        group.querySelectorAll("button").forEach((candidate) => {
          candidate.setAttribute("aria-pressed", String(candidate === button));
        });

        applyFilters();
      });
    });

    gallerySort?.addEventListener("change", applyFilters);

    sizeButtons.forEach((button) => {
      button.addEventListener("click", () => {
        const size = button.dataset.sizeOption || "small";
        document.body.dataset.imageSize = size;
        sizeButtons.forEach((candidate) => {
          candidate.setAttribute("aria-pressed", String(candidate === button));
        });
      });
    });

    figures.forEach((figure) => {
      figure.addEventListener("click", (event) => {
        if (event.target.closest("a")) return;
        openLightbox(figure);
      });
      figure.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          openLightbox(figure);
        }
      });
    });

    lightboxClose.addEventListener("click", closeLightbox);
    lightboxPrev.addEventListener("click", () => moveLightbox(-1));
    lightboxNext.addEventListener("click", () => moveLightbox(1));
    lightboxImage.addEventListener("click", (event) => {
      event.stopPropagation();
      moveLightbox(1);
    });
    lightbox.addEventListener("click", (event) => {
      if (event.target === lightbox) closeLightbox();
    });

    document.addEventListener("keydown", (event) => {
      if (!lightboxActive) return;
      if (event.key === "Escape") closeLightbox();
      if (event.key === "ArrowLeft") moveLightbox(-1);
      if (event.key === "ArrowRight") moveLightbox(1);
    });

    applyFilters();
"""

SPECIAL_LABEL_PARTS = {
    "3d": "3D",
    "cg": "CG",
    "pbr": "PBR",
    "v2": "V2",
}


@dataclass
class Figure:
    src: str = ""
    width: int = 0
    height: int = 0
    aspect_ratio: str = ""
    alt: str = ""
    style: str = ""
    place: str = ""
    category: str = ""
    occasion: str = ""
    venue: str = ""
    activity: str = ""
    outfit: str = ""
    location_detail: str = ""
    title: str = ""
    tags_text: str = ""
    thumb_fit: str = "cover"


@dataclass
class Album:
    title: str = ""
    notes_href: str = ""
    album_href: str = ""
    meta_text: str = ""
    summary_ja: str = ""
    preferred_aspect_ratio: str = ""
    collection: str = "daily"
    character: str = ""
    sort_order: int = 0
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
            self._current_figure.thumb_fit = thumb_fit_for_src(self._current_figure.src)
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


def read_webp_size(path: Path) -> tuple[int, int] | None:
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if len(data) < 30 or data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        return None
    chunk = data[12:16]
    if chunk == b"VP8X" and len(data) >= 30:
        width = int.from_bytes(data[24:27], "little") + 1
        height = int.from_bytes(data[27:30], "little") + 1
        return width, height
    if chunk == b"VP8 ":
        start = data.find(b"\x9d\x01\x2a", 20)
        if start != -1 and len(data) >= start + 7:
            width = int.from_bytes(data[start + 3 : start + 5], "little") & 0x3FFF
            height = int.from_bytes(data[start + 5 : start + 7], "little") & 0x3FFF
            return width, height
    if chunk == b"VP8L" and len(data) >= 25 and data[20] == 0x2F:
        bits = int.from_bytes(data[21:25], "little")
        width = (bits & 0x3FFF) + 1
        height = ((bits >> 14) & 0x3FFF) + 1
        return width, height
    return None


def thumb_fit_for_src(src: str) -> str:
    size = read_webp_size(ROOT / src)
    if not size:
        return "cover"
    width, height = size
    if width <= 0 or height <= 0:
        return "cover"
    ratio = width / height
    if ratio < THUMB_CONTAIN_MIN_RATIO or ratio > THUMB_CONTAIN_MAX_RATIO:
        return "contain"
    return "cover"


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


def album_collection(album: Album) -> str:
    return album.collection or "daily"


def album_character(album: Album) -> str:
    return album.character or ""


def figure_metadata(fig: Figure):
    inferred = classify_image(fig.category, fig.title, fig.tags_text, fig.alt, fig.src)
    return type(inferred)(
        occasion=fig.occasion or inferred.occasion,
        venue=fig.venue or inferred.venue,
        activity=fig.activity or inferred.activity,
        outfit=fig.outfit or inferred.outfit,
    )


def album_metadata_values(album: Album, key: str) -> list[str]:
    return sorted({getattr(figure_metadata(fig), key) for fig in album.figures})


def figure_title(fig: Figure) -> str:
    if fig.title:
        return fig.title
    return labelize(Path(fig.src).stem)


def figure_display_title(fig: Figure) -> str:
    return re.sub(r"^\d{1,2}\s+", "", figure_title(fig)).strip()


def figure_age(fig: Figure) -> str:
    parts = [part.strip() for part in fig.tags_text.split("/") if part.strip()]
    if parts:
        last = parts[-1]
        if re.search(r"\d|adult", last):
            return last
    return ""


def figure_location_detail(fig: Figure) -> str:
    text = re.sub(r"\s+", " ", fig.alt or "").strip()
    if not text:
        return ""
    text = re.sub(
        r"^(?:Shino,\s*adult\s+(?:\d+|\d+-year-old)(?:\s+recurring character)?|Young Shino,\s*age\s+\d+|Adult\s+(?:\d+(?:-\d+)?|early[-\s]?\d+s|mid[-\s]?\d+s|late[-\s]?\d+s)|Early[-\s]?\d+s|Mid[-\s]?\d+s|Late[-\s]?\d+s)\s*,?\s*",
        "",
        text,
        flags=re.I,
    )
    text = re.sub(r"^Japanese-centered woman\s+", "", text, flags=re.I)
    stop_match = re.search(
        r"(?:\s+while\s+|\s+wearing\s+|,\s+wearing\s+|,\s+checking\s+|,\s+holding\s+|,\s+adjusting\s+|,\s+stepping\s+|,\s+looking\s+|,\s+smiling\s+|,\s+tightening\s+|,\s+fixing\s+|,\s+putting\s+|,\s+carrying\s+|,\s+pulling\s+|,\s+gathering\s+|,\s+seated\s+)",
        text,
        flags=re.I,
    )
    if stop_match:
        text = text[: stop_match.start()]
    match = re.search(
        r"\b(?:at|inside|in|on|near|through|outside|beside|along|by)\s+(?:an|a|the)?\s*([^,]+(?:,\s*[^,]+)?)",
        text,
        flags=re.I,
    )
    if match:
        value = match.group(1)
    else:
        value = text
    value = re.sub(r"\s+(?:with|while)\s+.*$", "", value, flags=re.I)
    value = value.strip(" ,")
    return truncate(value, 110)


def json_text(data: dict[str, object], key: str) -> str:
    value = data.get(key)
    return str(value).strip() if value is not None else ""


def json_int(data: dict[str, object], key: str) -> int:
    value = data.get(key)
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.isdigit():
        return int(value)
    return 0


def load_album_source(path: Path) -> Album:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"album source must be an object: {path.relative_to(ROOT)}")
    slug = json_text(payload, "slug") or path.stem
    album = Album(
        title=json_text(payload, "title") or slug,
        notes_href=json_text(payload, "notesHref") or json_text(payload, "notes_href"),
        album_href=json_text(payload, "href") or f"album.html?set={slug}",
        meta_text=json_text(payload, "summary"),
        summary_ja=json_text(payload, "summaryJa") or json_text(payload, "summary_ja"),
        preferred_aspect_ratio=json_text(payload, "preferredAspectRatio")
        or json_text(payload, "preferred_aspect_ratio"),
        collection=json_text(payload, "collection") or "daily",
        character=json_text(payload, "character"),
        sort_order=json_int(payload, "sortOrder"),
    )
    raw_images = payload.get("images", [])
    if not isinstance(raw_images, list):
        raise ValueError(f"album source images must be a list: {path.relative_to(ROOT)}")
    for raw_image in raw_images:
        if not isinstance(raw_image, dict):
            raise ValueError(f"album source image must be an object: {path.relative_to(ROOT)}")
        album.figures.append(
            Figure(
                src=json_text(raw_image, "src"),
                width=json_int(raw_image, "width"),
                height=json_int(raw_image, "height"),
                aspect_ratio=json_text(raw_image, "aspectRatio") or json_text(raw_image, "aspect_ratio"),
                alt=json_text(raw_image, "alt"),
                style=json_text(raw_image, "style"),
                place=json_text(raw_image, "place"),
                category=json_text(raw_image, "category"),
                occasion=json_text(raw_image, "occasion"),
                venue=json_text(raw_image, "venue"),
                activity=json_text(raw_image, "activity"),
                outfit=json_text(raw_image, "outfit"),
                location_detail=json_text(raw_image, "locationDetail") or json_text(raw_image, "location_detail"),
                title=json_text(raw_image, "title"),
                tags_text=json_text(raw_image, "tags") or json_text(raw_image, "tagsText"),
                thumb_fit=thumb_fit_for_src(json_text(raw_image, "src")),
            )
        )
    return album


def load_albums() -> list[Album]:
    paths = sorted(ALBUM_DATA_ROOT.rglob("*.json"))
    albums = [load_album_source(path) for path in paths]
    albums.sort(key=lambda album: (album_date(album.title), -album.sort_order, album.title), reverse=True)
    return albums


def album_to_dict(album: Album) -> dict[str, object]:
    slug = album_slug(album)
    categories = album_categories(album)
    styles = album_styles(album)
    places = album_places(album)
    images = []
    for index, fig in enumerate(album.figures, start=1):
        metadata = figure_metadata(fig)
        images.append(
            {
                "label": f"{index:02d}",
                "src": fig.src,
                "width": fig.width,
                "height": fig.height,
                "aspectRatio": fig.aspect_ratio,
                "alt": fig.alt,
                "title": figure_title(fig),
                "tags": fig.tags_text,
                "style": fig.style,
                "place": fig.place,
                "category": fig.category,
                "occasion": metadata.occasion,
                "venue": metadata.venue,
                "locationDetail": fig.location_detail or figure_location_detail(fig),
                "activity": metadata.activity,
                "outfit": metadata.outfit,
                "age": figure_age(fig),
            }
        )
    album_data = {
        "slug": slug,
        "href": f"album.html?set={slug}",
        "legacyHref": f"assets/{slug}-album.html",
        "title": album.title,
        "shortTitle": short_title(album.title),
        "date": album_date(album.title),
        "month": album_month(album.title),
        "summary": clean_meta(album),
        "summaryJa": album.summary_ja,
        "notesHref": album.notes_href,
        "places": places,
        "categories": categories,
        "styles": styles,
        "collection": album_collection(album),
        "character": album_character(album),
        "occasions": album_metadata_values(album, "occasion"),
        "venues": album_metadata_values(album, "venue"),
        "activities": album_metadata_values(album, "activity"),
        "outfits": album_metadata_values(album, "outfit"),
        "imageCount": len(album.figures),
        "images": images,
    }
    if album.preferred_aspect_ratio:
        album_data["preferredAspectRatio"] = album.preferred_aspect_ratio
    return album_data


def filter_button(value: str, label: str | None = None, pressed: bool = False, count: int = 0) -> str:
    label = label or labelize_metadata(value)
    return (
        f'          <button type="button" data-filter="{escape(value)}" '
        f'aria-pressed="{str(pressed).lower()}">'
        f'<span class="filter-text">{escape(label)}</span>'
        f'<span class="filter-count">{count}</span></button>'
    )


def gallery_filter_button(value: str, label: str | None = None, pressed: bool = False, count: int = 0) -> str:
    label = label or labelize_metadata(value)
    return (
        f'          <button type="button" data-filter="{escape(value)}" '
        f'aria-pressed="{str(pressed).lower()}">'
        f'<span class="filter-text">{escape(label)}</span> '
        f'<span class="filter-count">({count})</span></button>'
    )


def figure_filter_value(album: Album, fig: Figure, key: str) -> str:
    if key == "collection":
        return album_collection(album)
    if key in {"occasion", "venue", "activity", "outfit"}:
        return getattr(figure_metadata(fig), key)
    return getattr(fig, key) or ""


def gallery_filter_counts(albums: list[Album], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for album in albums:
        for fig in album.figures:
            value = figure_filter_value(album, fig, key)
            if value:
                counts[value] = counts.get(value, 0) + 1
    return counts


def ordered_filter_values(counts: dict[str, int], key: str) -> list[str]:
    if key == "collection":
        preferred = ["daily", "character"]
        return [value for value in preferred if value in counts] + sorted(
            value for value in counts if value not in preferred
        )
    return sorted(counts, key=lambda value: (-counts[value], labelize_metadata(value), value))


def gallery_filter_buttons(albums: list[Album], key: str) -> str:
    counts = gallery_filter_counts(albums, key)
    if key == "collection":
        buttons = [gallery_filter_button("all", "すべて", pressed=True, count=sum(counts.values()))]
        buttons.extend(
            gallery_filter_button(
                value,
                "日常" if value == "daily" else "キャラクター",
                pressed=False,
                count=counts[value],
            )
            for value in ordered_filter_values(counts, key)
        )
        return "\n".join(buttons)
    buttons = [gallery_filter_button("all", "すべて", pressed=True, count=sum(counts.values()))]
    buttons.extend(
        gallery_filter_button(value, count=counts[value])
        for value in ordered_filter_values(counts, key)
    )
    return "\n".join(buttons)


def render_gallery_figure(album: Album, fig: Figure, *, eager: bool, figure_index: int) -> str:
    metadata = figure_metadata(fig)
    title = figure_title(fig)
    city = labelize_metadata(fig.place)
    image_number = image_number_from_title(title, figure_index)
    summary = " / ".join(value for value in [album_date(album.title), city, image_number] if value)
    tags = " / ".join(
        value
        for value in [labelize_metadata(fig.category), specific_gallery_label(title), labelize_metadata(fig.style)]
        if value
    )
    loading = "eager" if eager else "lazy"
    decoding = "sync" if eager else "async"
    href = album_href(album)
    collection = album_collection(album)
    date = album_date(album.title)
    size_attrs = f' width="{fig.width}" height="{fig.height}"' if fig.width and fig.height else ""
    return f"""        <figure data-set="{escape(album_slug(album))}" data-collection="{escape(collection)}" data-date="{escape(date)}" data-title="{escape(title.lower())}" data-album-title="{escape(album.title.lower())}" data-style="{escape(fig.style)}" data-place="{escape(fig.place)}" data-category="{escape(fig.category)}" data-occasion="{escape(metadata.occasion)}" data-venue="{escape(metadata.venue)}" data-activity="{escape(metadata.activity)}" data-outfit="{escape(metadata.outfit)}" data-album-href="{escape(href)}"><img loading="{loading}" decoding="{decoding}" src="{escape(fig.src)}" alt="{escape(fig.alt)}"{size_attrs}><figcaption><strong><a href="{escape(href)}">{escape(summary)}</a></strong><span class="tags">{escape(tags)}</span></figcaption></figure>"""


def image_number_from_title(title: str, fallback_index: int) -> str:
    first = title.split(maxsplit=1)[0] if title else ""
    if first.isdigit():
        return first.zfill(2)
    return f"{fallback_index:02d}"


def specific_gallery_label(title: str) -> str:
    words = title.split()
    if words and words[0].isdigit():
        words = words[1:]
    if words and words[0].lower() in {
        "active",
        "bar",
        "bookstore",
        "ceremony",
        "club",
        "dance",
        "date",
        "disco",
        "formal",
        "gallery",
        "home",
        "lounge",
        "market",
        "mode",
        "music",
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
    }:
        words = words[1:]
    return " ".join(words[:4])


def render_gallery_section(album: Album, *, album_index: int) -> str:
    slug = album_slug(album)
    collection = album_collection(album)
    character = album_character(album)
    figures = "\n".join(
        render_gallery_figure(album, fig, eager=album_index < 2 and index < 4, figure_index=index + 1)
        for index, fig in enumerate(album.figures)
    )
    character_attr = f' data-character="{escape(character)}"' if character else ""
    return f"""    <section data-set="{escape(slug)}" data-collection="{escape(collection)}"{character_attr}>
      <div class="grid">
{figures}
      </div>
    </section>"""


def render_gallery_collection(collection: str, title: str, albums: list[Album]) -> str:
    if not albums:
        return ""
    total_images = sum(len(album.figures) for album in albums)
    figures = "\n".join(
        render_gallery_figure(album, fig, eager=album_index < 2 and index < 4, figure_index=index + 1)
        for album_index, album in enumerate(albums)
        for index, fig in enumerate(album.figures)
    )
    return f"""    <div class="gallery-collection gallery-collection-{escape(collection)}" data-gallery-collection="{escape(collection)}" data-gallery-collection-total="{total_images}" aria-labelledby="{escape(collection)}-images-heading">
      <div class="collection-heading">
        <h2 id="{escape(collection)}-images-heading">{escape(title)}</h2>
        <p class="collection-count" data-gallery-collection-count="{escape(collection)}">{total_images} / {total_images} images</p>
      </div>
      <div class="grid">
{figures}
      </div>
    </div>"""


def build_gallery_index(albums: list[Album]) -> str:
    total_images = sum(len(album.figures) for album in albums)
    sections = render_gallery_collection("all", "画像", albums)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Chat Voyage Gallery</title>
  <style>
{GALLERY_STYLE}
  </style>
</head>
<body>
  <header>
    <nav>
      <a href="albums.html">Albums</a>
    </nav>
    <h1>Chat Voyage</h1>
    <p class="intro">Daily fashion sets and character day albums organized by date, place, style, and scene.</p>
  </header>

  <main>
    <div class="filters" aria-label="Gallery filters">
      <div class="filter-row">
        <div class="filter-label">Album</div>
        <div class="filter-buttons" data-filter-group="collection">
{gallery_filter_buttons(albums, "collection")}
        </div>
      </div>

      <div class="gallery-controls" aria-label="Gallery controls">
        <label class="gallery-select-field" for="gallery-sort">
          <span>並び順</span>
          <select id="gallery-sort">
            <option value="newest">アルバム日付 新しい順</option>
            <option value="oldest">アルバム日付 古い順</option>
            <option value="title">画像タイトル</option>
            <option value="album">アルバムタイトル</option>
          </select>
        </label>
        <div class="size-toggle" data-size-toggle aria-label="画像サイズ">
          <button type="button" data-size-option="small" aria-pressed="true">小</button>
          <button type="button" data-size-option="large" aria-pressed="false">大</button>
        </div>
      </div>

      <details class="advanced-filters">
        <summary><span>詳細フィルタ</span><span class="filter-summary" data-filter-summary>すべて</span></summary>
        <div class="advanced-filter-body">
          <div class="filter-row">
            <div class="filter-label">Style</div>
            <div class="filter-buttons" data-filter-group="style">
{gallery_filter_buttons(albums, "style")}
            </div>
          </div>

          <div class="filter-row">
            <div class="filter-label">Place</div>
            <div class="filter-buttons" data-filter-group="place">
{gallery_filter_buttons(albums, "place")}
            </div>
          </div>

          <div class="filter-row">
            <div class="filter-label">Scene</div>
            <div class="filter-buttons" data-filter-group="occasion">
{gallery_filter_buttons(albums, "occasion")}
            </div>
          </div>

          <div class="filter-row">
            <div class="filter-label">Venue</div>
            <div class="filter-buttons" data-filter-group="venue">
{gallery_filter_buttons(albums, "venue")}
            </div>
          </div>

          <div class="filter-row">
            <div class="filter-label">Action</div>
            <div class="filter-buttons" data-filter-group="activity">
{gallery_filter_buttons(albums, "activity")}
            </div>
          </div>

          <div class="filter-row">
            <div class="filter-label">Outfit</div>
            <div class="filter-buttons" data-filter-group="outfit">
{gallery_filter_buttons(albums, "outfit")}
            </div>
          </div>
        </div>
      </details>
    </div>

    <p class="empty is-hidden">No images match the current filters.</p>
{sections}
  </main>

  <div class="lightbox" data-lightbox hidden role="dialog" aria-modal="true" aria-label="Image preview">
    <div class="lightbox-bar">
      <p class="lightbox-count"><span data-lightbox-current>1</span> / <span data-lightbox-total>0</span></p>
      <div class="lightbox-actions">
        <a data-lightbox-open href="#">Open original</a>
        <button type="button" data-lightbox-close aria-label="Close preview">Close</button>
      </div>
    </div>
    <button class="lightbox-nav lightbox-prev" type="button" data-lightbox-prev aria-label="Previous image">&lt;</button>
    <img data-lightbox-image alt="">
    <button class="lightbox-nav lightbox-next" type="button" data-lightbox-next aria-label="Next image">&gt;</button>
    <div class="lightbox-caption" data-lightbox-caption></div>
  </div>

  <script>
{GALLERY_SCRIPT}
  </script>
</body>
</html>
"""


def build_album_browser(albums: list[Album]) -> str:
    characters = sorted({album_character(album) for album in albums if album_character(album)})
    places = sorted({place for album in albums for place in album_places(album)})
    styles = sorted({style for album in albums for style in album_styles(album)})
    occasions = sorted({value for album in albums for value in album_metadata_values(album, "occasion")})
    venues = sorted({value for album in albums for value in album_metadata_values(album, "venue")})
    activities = sorted({value for album in albums for value in album_metadata_values(album, "activity")})
    outfits = sorted({value for album in albums for value in album_metadata_values(album, "outfit")})
    months = sorted({album_month(album.title) for album in albums if album_month(album.title)}, reverse=True)
    total_images = sum(len(album.figures) for album in albums)
    latest_date = album_date(albums[0].title) if albums else ""

    month_buttons = "\n".join(
        filter_button(month, month, count=sum(1 for album in albums if album_month(album.title) == month))
        for month in months
    )
    character_buttons = "\n".join(
        filter_button(character, count=sum(1 for album in albums if album_character(album) == character))
        for character in characters
    )
    place_buttons = "\n".join(
        filter_button(place, count=sum(1 for album in albums if place in album_places(album)))
        for place in places
    )
    occasion_buttons = "\n".join(
        filter_button(occasion, count=sum(1 for album in albums if occasion in album_metadata_values(album, "occasion")))
        for occasion in occasions
    )
    venue_buttons = "\n".join(
        filter_button(venue, count=sum(1 for album in albums if venue in album_metadata_values(album, "venue")))
        for venue in venues
    )
    activity_buttons = "\n".join(
        filter_button(activity, count=sum(1 for album in albums if activity in album_metadata_values(album, "activity")))
        for activity in activities
    )
    outfit_buttons = "\n".join(
        filter_button(outfit, count=sum(1 for album in albums if outfit in album_metadata_values(album, "outfit")))
        for outfit in outfits
    )
    style_buttons = "\n".join(
        filter_button(style, count=sum(1 for album in albums if style in album_styles(album)))
        for style in styles
    )
    index_lookup = {id(album): index for index, album in enumerate(albums)}
    character_albums = [album for album in albums if album_collection(album) == "character"]
    daily_albums = [album for album in albums if album_collection(album) != "character"]
    sections = "\n".join(
        section
        for section in [
            render_album_all_section(),
            render_album_section("character", "キャラクターアルバム", character_albums, index_lookup),
            render_album_section("daily", "日常アルバム", daily_albums, index_lookup),
        ]
        if section
    )
    date_sections = render_date_image_browser(albums)

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#f4f6f7">
  <title>Chat Voyage Albums</title>
  <link rel="stylesheet" href="assets/album-browser.css?v={ASSET_VERSION}">
</head>
<body>
  <a class="skip-link" href="#albums">アルバムへ</a>
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
        <div><dt>アルバム</dt><dd>{len(albums)}</dd></div>
        <div><dt>画像</dt><dd>{total_images}</dd></div>
        <div><dt>場所</dt><dd>{len(places)}</dd></div>
        <div><dt>最新</dt><dd>{escape(latest_date)}</dd></div>
      </dl>
    </div>
  </header>

		  <main class="album-browser" data-album-app data-view="grid">
		    <div class="collection-mode" data-filter-group="collection" aria-label="Album mode">
		      <a class="gallery-back" href="index.html">画像一覧</a>
{filter_button("all", "すべて", count=len(albums))}
{filter_button("character", "キャラクター", pressed=True, count=len(character_albums))}
{filter_button("daily", "日常", count=len(daily_albums))}
		    </div>

	    <section class="controls" aria-label="Album controls">
      <div class="control-row control-row-main">
        <label class="search-field" for="album-search">
          <span>検索</span>
          <input type="search" id="album-search" placeholder="検索">
        </label>
        <label class="select-field" for="album-sort">
          <span>並び順</span>
          <select id="album-sort">
            <option value="newest">アルバム日付 新しい順</option>
            <option value="oldest">アルバム日付 古い順</option>
            <option value="date-groups">日付ごと</option>
            <option value="city">都市</option>
            <option value="title">タイトル</option>
            <option value="images">画像数</option>
          </select>
        </label>
        <div class="view-toggle" aria-label="View mode">
          <button type="button" data-view-option="grid" aria-pressed="true">グリッド</button>
          <button type="button" data-view-option="list" aria-pressed="false">リスト</button>
        </div>
        <div class="size-toggle" data-size-toggle aria-label="画像サイズ">
          <button type="button" data-size-option="small" aria-pressed="true">小</button>
          <button type="button" data-size-option="large" aria-pressed="false">大</button>
        </div>
        <button class="reset-button" type="button" id="reset-filters">リセット</button>
      </div>

	      <div class="quick-filters" aria-label="Quick album filters">
	        <div class="filter-row" data-filter-group="character">
	          <div class="filter-label">キャラクター</div>
	          <div class="filter-buttons">
{filter_button("all", "すべて", pressed=True, count=len(albums))}
{character_buttons}
          </div>
        </div>
        <div class="filter-row" data-filter-group="month">
          <div class="filter-label">月</div>
          <div class="filter-buttons">
{filter_button("all", "すべて", pressed=True, count=len(albums))}
{month_buttons}
          </div>
        </div>
      </div>

      <details class="filter-drawer" data-filter-drawer>
        <summary>
          <span>詳細フィルタ</span>
          <span data-filter-summary>すべて</span>
        </summary>
        <div class="filter-body">
          <div class="filter-row" data-filter-group="place">
            <div class="filter-label">都市</div>
            <div class="filter-buttons">
{filter_button("all", "すべて", pressed=True, count=len(albums))}
{place_buttons}
            </div>
          </div>
          <div class="filter-row" data-filter-group="occasion">
            <div class="filter-label">場面</div>
            <div class="filter-buttons">
{filter_button("all", "すべて", pressed=True, count=len(albums))}
{occasion_buttons}
            </div>
          </div>
          <div class="filter-row" data-filter-group="venue">
            <div class="filter-label">場所</div>
            <div class="filter-buttons">
{filter_button("all", "すべて", pressed=True, count=len(albums))}
{venue_buttons}
            </div>
          </div>
          <div class="filter-row" data-filter-group="activity">
            <div class="filter-label">行動</div>
            <div class="filter-buttons">
{filter_button("all", "すべて", pressed=True, count=len(albums))}
{activity_buttons}
            </div>
          </div>
          <div class="filter-row" data-filter-group="outfit">
            <div class="filter-label">服装</div>
            <div class="filter-buttons">
{filter_button("all", "すべて", pressed=True, count=len(albums))}
{outfit_buttons}
            </div>
          </div>
          <div class="filter-row" data-filter-group="style">
            <div class="filter-label">絵柄</div>
            <div class="filter-buttons">
{filter_button("all", "すべて", pressed=True, count=len(albums))}
{style_buttons}
            </div>
          </div>
        </div>
      </details>

      <div class="result-bar">
        <p class="count" aria-live="polite"><span id="visible-count">{len(albums)}</span> / <span id="total-count">{len(albums)}</span> <span data-result-unit>件</span></p>
        <div class="active-filters" id="active-filters" aria-label="Active filters"></div>
      </div>
    </section>

    <p class="empty-state" id="empty-state" hidden>条件に合うアルバムがありません。</p>
    <div class="album-sections" id="albums" aria-label="Album results">
{sections}
    </div>
    <div class="date-image-browser" data-date-image-browser aria-label="日付別の画像">
{date_sections}
    </div>
  </main>

  <script src="assets/album-browser.js?v={ASSET_VERSION}"></script>
</body>
</html>
"""


def render_album_all_section() -> str:
    return """    <section class="album-section album-section-all" data-album-section="all" aria-label="すべてのアルバム">
      <div class="albums" data-album-list="all"></div>
    </section>"""


def render_album_section(collection: str, title: str, albums: list[Album], index_lookup: dict[int, int]) -> str:
    if not albums:
        return ""
    cards = "\n".join(
        render_card(
            album,
            is_latest=(index_lookup[id(album)] == 0),
            index=index_lookup[id(album)],
            eager_thumbs=(collection == "character" or position < 3),
        )
        for position, album in enumerate(albums)
    )
    return f"""    <section class="album-section album-section-{escape(collection)}" data-album-section="{escape(collection)}" aria-labelledby="{escape(collection)}-albums-heading">
      <div class="album-section-heading">
        <h2 id="{escape(collection)}-albums-heading">{escape(title)}</h2>
      </div>
      <div class="albums" data-album-list="{escape(collection)}">
{cards}
      </div>
    </section>"""


def render_date_image_browser(albums: list[Album]) -> str:
    grouped: dict[str, list[tuple[Album, Figure, int, int]]] = {}
    for album_index, album in enumerate(albums):
        date = album_date(album.title) or "日付なし"
        grouped.setdefault(date, [])
        for figure_index, fig in enumerate(album.figures, start=1):
            grouped[date].append((album, fig, album_index, figure_index))

    sections: list[str] = []
    for date in sorted(grouped, reverse=True):
        entries = grouped[date]
        album_count = len({album_slug(album) for album, _, _, _ in entries})
        image_count = len(entries)
        tiles = "\n".join(
            render_date_image_tile(album, fig, album_index=album_index, figure_index=figure_index)
            for album, fig, album_index, figure_index in entries
        )
        sections.append(
            f"""      <section class="date-image-section" data-date-image-section data-date="{escape(date)}">
        <div class="date-image-heading">
          <h2>{escape(date)}</h2>
          <span><span data-date-visible-count>{image_count}</span> / {image_count}枚 · {album_count}アルバム</span>
        </div>
        <div class="date-image-grid">
{tiles}
        </div>
      </section>"""
        )
    return "\n".join(sections)


def render_date_image_tile(album: Album, fig: Figure, *, album_index: int, figure_index: int) -> str:
    collection = album_collection(album)
    character = album_character(album)
    metadata = figure_metadata(fig)
    date = album_date(album.title)
    month = album_month(album.title)
    places = [fig.place] if fig.place else album_places(album)
    styles = [fig.style] if fig.style else album_styles(album)
    category = fig.category or ""
    title = figure_title(fig)
    display_title = figure_display_title(fig)
    album_title = short_title(album.title)
    href = f"{album_href(album)}#image-{figure_index}"
    loading = "eager" if album_index < 2 and figure_index <= 4 else "lazy"
    decoding = "sync" if loading == "eager" else "async"
    fit_class = "thumb-contain" if fig.thumb_fit == "contain" else "thumb-cover"
    size_attrs = f' width="{fig.width}" height="{fig.height}"' if fig.width and fig.height else ""
    search = " ".join(
        [
            album.title,
            album_title,
            title,
            fig.alt,
            fig.tags_text,
            collection,
            character,
            *places,
            category,
            metadata.occasion,
            metadata.venue,
            metadata.activity,
            metadata.outfit,
            *styles,
        ]
    ).lower()
    return f"""          <a class="date-image-tile" href="{escape(href)}" data-index="{album_index}-{figure_index:02d}" data-title="{escape(title.lower())}" data-date="{escape(date)}" data-month="{escape(month)}" data-city="{escape(labelize(places[0]).lower())}" data-collection="{escape(collection)}" data-character="{escape(character)}" data-place="{escape(' '.join(places))}" data-category="{escape(category)}" data-occasion="{escape(metadata.occasion)}" data-venue="{escape(metadata.venue)}" data-activity="{escape(metadata.activity)}" data-outfit="{escape(metadata.outfit)}" data-style="{escape(' '.join(styles))}" data-image-count="1" data-search="{escape(search)}">
            <img class="{fit_class}" src="{escape(fig.src)}" alt="{escape(fig.alt or title)}" loading="{loading}" decoding="{decoding}"{size_attrs}>
            <span class="date-image-number">{figure_index:02d}</span>
            <span class="date-image-text">
              <strong>{escape(display_title)}</strong>
              <small>{escape(album_title)}</small>
            </span>
          </a>"""


def render_card(album: Album, *, is_latest: bool, index: int, eager_thumbs: bool) -> str:
    collection = album_collection(album)
    character = album_character(album)
    places = album_places(album)
    categories = album_categories(album)
    styles = album_styles(album)
    occasions = album_metadata_values(album, "occasion")
    venues = album_metadata_values(album, "venue")
    activities = album_metadata_values(album, "activity")
    outfits = album_metadata_values(album, "outfit")
    meta = clean_meta(album)
    date = album_date(album.title)
    month = album_month(album.title)
    city = labelize(places[0])
    image_count = len(album.figures)
    search = " ".join(
        [
            album.title,
            meta,
            collection,
            character,
            *places,
            *categories,
            *styles,
            *occasions,
            *venues,
            *activities,
            *outfits,
            *[fig.alt for fig in album.figures if fig.alt],
            *[fig.tags_text for fig in album.figures if fig.tags_text],
        ]
    ).lower()
    badges = render_badges(album, is_latest=is_latest)
    thumbs = "\n".join(render_thumb(fig, album.title, eager=eager_thumbs) for fig in album.figures[:4])
    title = escape(album.title)
    href = album_href(album)

    return f"""      <article class="album-card" data-index="{index}" data-title="{title.lower()}" data-date="{escape(date)}" data-month="{escape(month)}" data-city="{escape(city.lower())}" data-collection="{escape(collection)}" data-character="{escape(character)}" data-place="{escape(' '.join(places))}" data-category="{escape(' '.join(categories))}" data-occasion="{escape(' '.join(occasions))}" data-venue="{escape(' '.join(venues))}" data-activity="{escape(' '.join(activities))}" data-outfit="{escape(' '.join(outfits))}" data-style="{escape(' '.join(styles))}" data-image-count="{image_count}" data-search="{escape(search)}">
        <a class="thumb-grid" href="{escape(href)}" aria-label="{title} album">
{thumbs}
        </a>
        <div class="album-content">
          <div class="title-row">
            <h2><a href="{escape(href)}">{title}</a></h2>
{badges}
          </div>
        </div>
      </article>"""


def render_thumb(fig: Figure, album_title: str, *, eager: bool = False) -> str:
    alt = fig.alt or f"{album_title} image"
    loading = "eager" if eager else "lazy"
    decoding = "sync" if eager else "async"
    fit_class = "thumb-contain" if fig.thumb_fit == "contain" else "thumb-cover"
    size_attrs = f' width="{fig.width}" height="{fig.height}"' if fig.width and fig.height else ""
    return (
        f'          <img class="{fit_class}" src="{escape(fig.src)}" alt="{escape(alt)}" '
        f'loading="{loading}" decoding="{decoding}"{size_attrs}>'
    )


def render_badges(album: Album, *, is_latest: bool) -> str:
    badges: list[str] = []
    title = album.title.lower()
    if is_latest:
        badges.append("最新")
    if "remake" in title or " v2" in title or "-v2" in title or "regeneration" in title:
        badges.append("再生成")
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
    groups: dict[str, object] = {"daily": [], "character": {}}
    for album in albums:
        slug = album_slug(album)
        if album_collection(album) == "character":
            character = album_character(album) or "unknown"
            character_groups = groups["character"]
            assert isinstance(character_groups, dict)
            character_groups.setdefault(character, []).append(slug)
        else:
            daily_group = groups["daily"]
            assert isinstance(daily_group, list)
            daily_group.append(slug)
    return (
        "window.CHAT_VOYAGE_ALBUMS = "
        + json.dumps(payload, indent=2, sort_keys=True)
        + ";\nwindow.CHAT_VOYAGE_ALBUM_GROUPS = "
        + json.dumps(groups, indent=2, sort_keys=True)
        + ";\n"
    )


def build_album_shell() -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#f4f6f7">
  <title>Chat Voyage Album</title>
  <link rel="stylesheet" href="assets/album-page.css?v={ASSET_VERSION}">
</head>
<body>
  <a class="skip-link" href="#images">画像へ</a>
  <header class="album-header">
    <nav class="site-nav" aria-label="Primary">
      <a href="index.html">Gallery</a>
      <a href="albums.html">Albums</a>
    </nav>
    <p class="not-found-notice" data-not-found-notice hidden></p>
    <div class="album-tools">
      <label class="album-select-field" for="album-select">
        <span>Album</span>
        <select id="album-select"></select>
      </label>
      <div class="album-neighbor-controls" aria-label="前後のアルバム">
        <a class="album-neighbor-button" data-prev-album href="#" aria-label="前のアルバム">&lt;</a>
        <a class="album-neighbor-button" data-next-album href="#" aria-label="次のアルバム">&gt;</a>
      </div>
      <button class="feedback-export" type="button" data-feedback-export>全フィードバックを書き出す</button>
    </div>
    <p class="eyebrow">Chat Voyage Album</p>
    <div class="title-block">
      <h1 id="album-title">Album</h1>
      <dl class="album-stats" aria-label="Album summary">
        <div><dt>日付</dt><dd id="album-date"></dd></div>
        <div><dt>画像</dt><dd id="album-count"></dd></div>
        <div><dt>場所</dt><dd id="album-place"></dd></div>
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
        <div class="viewer-actions">
          <button type="button" data-album-prev aria-label="前の画像">&lt;</button>
          <button type="button" data-album-next aria-label="次の画像">&gt;</button>
          <a class="open-image" data-open-image href="#">画像を開く</a>
          <a class="notes-link" data-notes-link href="#" hidden>メモ</a>
        </div>
        <div class="viewer-caption" data-viewer-caption></div>
        <section class="feedback-panel" data-feedback aria-label="好みフィードバック">
          <div class="feedback-heading">
            <h2>好み</h2>
            <p data-feedback-status>未保存</p>
          </div>
          <div class="feedback-score" role="group" aria-label="画像の好み">
            <button type="button" data-feedback-score="love">好き</button>
            <button type="button" data-feedback-score="neutral">それほどでもない</button>
          </div>
          <fieldset class="feedback-tags">
            <legend>軸</legend>
            <label><input type="checkbox" value="art-style" data-feedback-tag> 絵柄</label>
            <label><input type="checkbox" value="person" data-feedback-tag> 人</label>
            <label><input type="checkbox" value="outfit" data-feedback-tag> 服装</label>
            <label><input type="checkbox" value="color" data-feedback-tag> 色</label>
            <label><input type="checkbox" value="silhouette" data-feedback-tag> シルエット</label>
            <label><input type="checkbox" value="pose" data-feedback-tag> ポーズ</label>
            <label><input type="checkbox" value="place" data-feedback-tag> 場所</label>
            <label><input type="checkbox" value="vibe" data-feedback-tag> 雰囲気</label>
          </fieldset>
          <label class="feedback-note">
            <span>メモ</span>
            <textarea rows="3" data-feedback-note></textarea>
          </label>
          <button class="feedback-reset" type="button" data-feedback-reset>この画像の記録を消す</button>
        </section>
      </aside>
    </section>

    <div class="thumbnail-strip" data-thumbnail-strip role="list" aria-label="画像ナビゲーション"></div>

    <section class="overview" id="images" aria-label="画像">
      <div class="section-heading">
        <h2>画像</h2>
        <p data-image-total></p>
      </div>
      <div class="grid" data-image-grid></div>
    </section>
  </main>
  <div class="lightbox" data-lightbox hidden role="dialog" aria-modal="true" aria-label="画像プレビュー">
    <div class="lightbox-bar">
      <p class="lightbox-count"><span data-lightbox-current>1</span> / <span data-lightbox-total>0</span></p>
      <div class="lightbox-actions">
        <a data-lightbox-open href="#">原寸を開く</a>
        <button type="button" data-lightbox-close aria-label="プレビューを閉じる">閉じる</button>
      </div>
    </div>
    <button class="lightbox-nav lightbox-prev" type="button" data-lightbox-prev aria-label="前の画像">&lt;</button>
    <img data-lightbox-image alt="">
    <button class="lightbox-nav lightbox-next" type="button" data-lightbox-next aria-label="次の画像">&gt;</button>
    <div class="lightbox-caption" data-lightbox-caption></div>
  </div>
  <script src="assets/album-data.js?v={ASSET_VERSION}"></script>
  <script src="assets/album-page.js?v={ASSET_VERSION}"></script>
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
    return load_albums()


def main() -> int:
    albums = load_albums()
    if not albums:
        print("ERROR: no albums found in data/albums")
        return 1

    changed: list[str] = []

    targets = [
        (ROOT / "index.html", build_gallery_index(albums)),
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
