# Album JSON Contract

This project treats `data/albums/**/*.json` as the source of truth for album and
image metadata. Generated files such as `assets/album-data.js`, `index.html`,
`albums.html`, and `album.html` must be rebuilt from this source.

## Album Object

Required fields:

- `slug`: stable album id. It must match the filename stem.
- `title`: display title, usually starting with the date.
- `summary`: English source summary. Keep for generation notes and search.
- `summaryJa`: short Japanese UI summary. Do not include the date if the date is already shown elsewhere.
- `preferredAspectRatio`: optional intended generation ratio for the album, usually `2:3` for portrait or `3:2` for landscape.
- `collection`: `daily` or `character`.
- `character`: character id for character albums, otherwise an empty string.
- `notesHref`: path to the album note.
- `sortOrder`: numeric tie-breaker within the same date.
- `images`: ordered list of image objects.

Collection rules:

- Character albums live under `data/albums/characters/<character>/yyyy/mm/`.
- Daily/theme albums live under `data/albums/daily/yyyy/mm/`.
- Character albums must not be mixed into daily/theme albums.

## Image Object

Required fields:

- `label`: two-digit display number.
- `src`: image path under `assets/albums/...`.
- `width`: measured pixel width of `src`.
- `height`: measured pixel height of `src`.
- `aspectRatio`: normalized display/generation ratio from `width:height`, such as `2:3`, `3:2`, `3:4`, `9:16`, or `1:1`.
- `alt`: full generation/content description.
- `title`: short image title.
- `tags`: legacy display/search text.
- `style`: controlled style id.
- `place`: controlled city/place id.
- `category`: old broad category retained for migration/search.
- `occasion`: normalized scene category.
- `venue`: normalized location category.
- `locationDetail`: concrete place/detail for UI display.
- `activity`: normalized action category.
- `outfit`: normalized outfit category.

`width`, `height`, and image-level `aspectRatio` are derived from the actual
image file by `scripts/enrich_album_source_metadata.py`. `width` and `height`
are exact pixels. `aspectRatio` is normalized to a common ratio when the
measured file is close enough; otherwise it falls back to the exact reduced
ratio. Do not hand-edit these fields unless the image file itself changed and
the enrich script is rerun immediately after.

`preferredAspectRatio` is different: it records the intended generation/layout
policy for the album before images are created or regenerated. It is human
authored and must not be inferred from a finished image unless that is an
explicit migration decision.

## Location Detail

`locationDetail` is the human-readable place shown in album detail pages.

Good examples:

- `Kokusai-dori / Heiwa-dori covered arcade in Naha`
- `Okinawa Prefectural Museum and Art Museum-style entrance courtyard in Naha`
- `Naminoue Beach / Naminoue seawall`
- `Unspecified gallery setting`

Avoid:

- city only: `Naha`
- time only: `evening`
- action prose: `walking through...`, `checking...`
- display/style filler: `look`, `fashion illustration`, `motion`, `crop`
- outfit-only text: `black floral dress`

If the old source lacks a real place, use `Unspecified <venue> setting` instead
of inventing a location.

## Aspect Ratio Policy

Store aspect ratio in JSON because it affects both generation consistency and
gallery layout.

- Use image-level `aspectRatio` for the measured ratio of each finished image.
- Use album-level `preferredAspectRatio` for the intended ratio to request in
  future image generation.

Recommended generation defaults:

- Character continuity albums: prefer one consistent ratio for the album, usually portrait `2:3`.
- Daily/theme four-image sets: prefer one consistent standard ratio, usually portrait `2:3` or landscape `3:2`, unless the set explicitly explores crops.
- `3:4`, square, ultratall, or other ratios are allowed only when the album concept calls for it, and the differing ratio should be intentional.

Validation enforces that image-level `aspectRatio` matches `width` and
`height`, that both match the actual image file, and that
`preferredAspectRatio` uses a valid ratio format when present.

## Update Flow

1. Edit or add source JSON under `data/albums/...`.
2. Run `python3 scripts/enrich_album_source_metadata.py`.
3. Run `python3 scripts/build_album_catalog.py`.
4. Run `python3 scripts/validate_gallery.py`.

The validator checks source JSON, generated album data, image references,
location detail quality, and image dimensions.

By default, `scripts/enrich_album_source_metadata.py` preserves existing
`summaryJa` and `locationDetail` because these are human-facing editorial
fields. Use `python3 scripts/enrich_album_source_metadata.py --refresh-text`
only when deliberately regenerating those text fields from heuristics.
