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

- `assets/albums/daily/YYYY/MM/`: normal daily WebP image sets
- `assets/albums/characters/<character>/YYYY/MM/`: character-day WebP image sets
- `data/albums/daily/YYYY/MM/`: canonical JSON metadata for normal daily albums
- `data/albums/characters/<character>/YYYY/MM/`: canonical JSON metadata for character albums
- `assets/album-data.js`: generated album catalog consumed by the album UI
- `notes/albums/`: human-readable direction notes and review notes
- `logs/`: monthly generation logs
- `prompts/`: reusable prompt presets and guardrails
- `scripts/`: gallery build, conversion, and validation scripts
- `docs/`: workflow and handover documentation
- `skills/`: project-tracked copy of the daily generation skill

## Daily Workflow

After adding or regenerating a daily or character set, update its JSON source
under `data/albums/`, then rebuild:

```sh
python3 scripts/build_album_catalog.py
python3 scripts/validate_gallery.py
git status --short --branch
```

Generated display images should be WebP. Generated originals and project-local
PNG copies are project materials: do not delete them automatically. Decide
explicitly whether they should be retained in place, moved to an archive, or
deleted after confirming that the canonical gallery uses the WebP display
copies.

## GitHub Pages

This repository can be published from the `main` branch root. The repository
must be public, or the GitHub account/organization must support private Pages.

See `docs/github-pages-workflow.md` for the current publishing notes.
