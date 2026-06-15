#!/usr/bin/env python3
"""Normalize Chat Voyage album pages for mobile viewing and direct image access."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
IMG_TAG = re.compile(r"(?P<indent>\s*)<img(?P<attrs>[^>]*?\bsrc=\"(?P<src>daily/[^\"]+)\"[^>]*)>", re.DOTALL)
FIGURE_BLOCK = re.compile(r"<figure>(?P<body>.*?)</figure>", re.DOTALL)


def ensure_css(text: str) -> str:
    text = re.sub(r"object-fit:\s*cover;", "object-fit: contain;", text)
    text = re.sub(r"aspect-ratio:\s*9\s*/\s*(?:16|18);", "", text)
    text = re.sub(r"height:\s*auto;\s*;", "height: auto;", text)
    if "max-height:" not in text:
        text = text.replace(
            "      object-fit: contain;",
            "      max-height: 82vh;\n      object-fit: contain;",
        )
    if ".image-link" not in text:
        insert = """\n    .image-link {\n      display: block;\n      background: #eef1f3;\n    }\n    .open-image,\n    .open {\n      display: inline-block;\n      margin-top: 10px;\n      font-size: 0.9rem;\n    }\n"""
        text = text.replace("    figcaption", insert + "\n    figcaption", 1)
    if "@media (max-width: 720px)" not in text and "</style>" in text:
        media = """\n    @media (max-width: 720px) {\n      main {\n        width: min(100% - 18px, 480px);\n        padding: 18px 0 32px;\n      }\n      .grid {\n        grid-template-columns: 1fr;\n        gap: 14px;\n      }\n      img {\n        max-height: 78vh;\n      }\n    }\n"""
        text = text.replace("  </style>", media + "  </style>")
    return text


def ensure_nav(text: str) -> str:
    if '../albums.html">Albums</a>' in text:
        return text
    if '<a href="../index.html">Index</a>' in text:
        return text.replace('<a href="../index.html">Index</a>', '<a href="../index.html">Index</a>\n      <a href="../albums.html">Albums</a>')
    if '<a href="../index.html">Main Gallery</a>' in text:
        return text.replace('<a href="../index.html">Main Gallery</a>', '<a href="../index.html">Main Gallery</a>\n      <a href="../albums.html">Albums</a>')
    return text


def add_loading(attrs: str) -> str:
    if "loading=" not in attrs:
        attrs += ' loading="lazy"'
    if "decoding=" not in attrs:
        attrs += ' decoding="async"'
    return attrs


def normalize_figure(match: re.Match[str]) -> str:
    body = match.group("body")
    if "image-link" not in body:
        def wrap_img(img_match: re.Match[str]) -> str:
            indent = img_match.group("indent")
            attrs = add_loading(img_match.group("attrs"))
            src = img_match.group("src")
            return f'{indent}<a class="image-link" href="{src}"><img{attrs}></a>'
        body = IMG_TAG.sub(wrap_img, body, count=1)
    else:
        body = IMG_TAG.sub(
            lambda m: f'{m.group("indent")}<img{add_loading(m.group("attrs"))}>',
            body,
        )

    src_match = re.search(r"(?:href|src)=\"(daily/[^\"]+\.(?:png|jpg|jpeg|webp))\"", body)
    if src_match and "Open image" not in body:
        open_link = f'          <a class="open-image" href="{src_match.group(1)}">Open image</a>\n'
        if "</figcaption>" in body:
            body = body.replace("</figcaption>", open_link + "        </figcaption>", 1)
        else:
            body += "\n        <figcaption>\n" + open_link + "        </figcaption>"
    return "<figure>" + body + "</figure>"


def normalize_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    text = ensure_nav(ensure_css(original))
    text = FIGURE_BLOCK.sub(normalize_figure, text)
    if text == original:
        return False
    path.write_text(text, encoding="utf-8")
    return True


def main() -> int:
    changed = []
    for path in sorted((ROOT / "assets").glob("*-album.html")):
        if normalize_file(path):
            changed.append(path.relative_to(ROOT))
    for path in changed:
        print(path)
    print(f"changed: {len(changed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
