# Chat Voyage

Chat Voyage is a static gallery archive for daily fashion-image explorations:
four-image sets, city-specific styling notes, prompt presets, and lightweight
album review UI.

The current gallery is built from plain HTML, CSS, JavaScript, and WebP image
assets. It is intended to run directly on GitHub Pages or any static file host.

## Browse

- `index.html`: chronological image gallery with filters
- `albums.html`: album browser
- `album.html?set=2026-06-17-barcelona-citrus-coral-city-day`: single-album viewer

The album viewer stores preference feedback in browser `localStorage`. Feedback
is local to the browser and is not synced to a server.

## Structure

- `assets/daily/`: generated WebP daily image sets
- `assets/album-data.js`: generated album catalog consumed by the album UI
- `notes/`: daily direction notes and review notes
- `logs/`: monthly generation logs
- `prompts/`: reusable prompt presets and guardrails
- `scripts/`: gallery build, conversion, and validation scripts
- `docs/`: workflow and handover documentation
- `skills/`: project-tracked copy of the daily generation skill

## Daily Workflow

After adding or regenerating a daily set:

```sh
python3 scripts/build_album_catalog.py
python3 scripts/validate_gallery.py
git status --short --branch
```

Generated display images should be WebP. Project PNG copies are intentionally
not kept.

## GitHub Pages

This repository can be published from the `main` branch root. The repository
must be public, or the GitHub account/organization must support private Pages.

See `docs/github-pages-workflow.md` for the current publishing notes.
