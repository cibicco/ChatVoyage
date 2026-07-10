---
name: shino-album-generation
description: Chat Voyage repo-specific Shino/紫乃 fixed-character album skill. Use only when working in /Users/allegro/Applications/ChatVoyage, or when the user explicitly asks for Chat Voyage Shino albums. Generate, review, organize, and catalog Shino character-day albums with i2i/reference continuity planning, Shino-specific palette and identity drift checks, WebP conversion, canonical JSON metadata, notes/log updates, album catalog rebuilds, and validation. Do not use for generic character generation or normal daily fashion sets.
---

# Shino Album Generation

## Scope

Use this skill only in `/Users/allegro/Applications/ChatVoyage` for Shino
character albums. It is repo-specific. Keep `daily-fashion-sketch` for normal
daily/theme albums; use this skill when the recurring character herself is the
work product.

This skill covers generation through aftercare:

- Shino identity, age, palette, and story continuity.
- i2i/reference planning when references are available.
- Shino visual-style lock: normal daily sets supply place, action, color, and
  clothing ideas, not a different art style or body grammar.
- Image acceptance/regeneration decisions.
- WebP display files and original-file handling.
- Canonical album JSON under `data/albums/characters/shino/YYYY/MM/`.
- Notes, monthly logs, generated `assets/album-data.js`, and validation.

## Required Reading

Before generating or reorganizing a Shino album, read:

1. `AGENTS.md`
2. `prompts/character-shino.md`
3. `prompts/character-album-policy.md`
4. `docs/album-json-contract.md`
5. `docs/daily-generation-workflow.md`
6. Recent Shino notes under `notes/albums/characters/shino/`
7. Recent Shino source JSON under `data/albums/characters/shino/`

If the task is review-only, also use the installed `shino-image-review` skill
when available.

## Planning

Plan the album before prompting. Record the plan in the note or log.

- `collection`: `character`
- `character`: `shino`
- `preferredAspectRatio`: choose before generation. Usually use portrait
  `2:3` for Shino continuity albums; use landscape `3:2` when the story
  deliberately wants a wider scene.
- `story_day_summary`: what kind of day this is for Shino.
- `shino_story_place_plan` or `shino_travel_place_plan`: concrete route and
  place details.
- `shino_palette_plan`: how the daily key color and outfit palette translate
  into Shino's own visual style.
- `source_daily_outfit_plan`: which normal daily-set clothing ideas should be
  preserved.
- `identity_continuity_plan`: face, gaze, hair, body proportion, posture,
  objects, and visual language.
- `reference_plan`: which i2i/reference images are used. For current Shino in
  Chat Voyage, default to the 2026-06-21 Shino albums when possible,
  especially `2026-06-21-shino-coastal-lab-aquarium/04-home-old-building-lobby-headphones.webp`
  for face, body, and style continuity.
- `signage_policy`: street-name signs are allowed as place context; avoid
  brand promotion, real company logos/names, and prominent advertising.

Do not make Shino a generic daily fashion model with her name attached. The
city, clothing, and activity may change, but the image should still read as
Shino living through a dated day.

## Prompting

Generate separate images, never a collage. A Shino prompt should be short
enough for image stability and should include:

- one adult woman, Shino, with the chosen adult age band;
- same Shino character illustration language, face/body continuity, long black
  hair with restrained lavender reflection, violet eyes, and quiet confident
  gaze;
- the Shino visual style should match the current Shino reference images,
  especially the 2026-06-21 Shino set; do not inherit the normal daily album's
  art style;
- concrete place and activity;
- specific outfit construction, usually preserving the source daily outfit idea
  unless it conflicts with Shino or the action;
- scene-specific expression or attention target;
- no prominent brand/logo/real company name, no infographic. Ordinary readable
  street names are acceptable and should not be filtered out.

For real cities, use exact named places. For the fictional port city, use the
place lanes in `prompts/character-shino.md` rather than vague placeholders.

## Acceptance Check

Inspect each image before saving it as accepted.

Accept only if:

- Shino is recognizably the same recurring adult character.
- The image uses Shino's unified visual style and body continuity, not the
  normal daily set's style preset or a different model.
- The image is not school-coded, childlike, idol-costume framed, or generic.
- The place/action is legible enough to support `locationDetail`, `venue`, and
  `activity` metadata.
- The outfit follows the source daily clothing idea when it fits Shino, the
  weather, and the action. Do not reject a Shino image merely because a color,
  garment, or silhouette appeared recently.
- The image is a standalone asset, not a collage or diagram.
- Major anatomy, hands, face, and clothing structure are usable.

Regenerate only the failing image with a targeted correction. If identity
drift is severe across multiple images, stop and re-plan the reference/identity
prompt instead of continuing to catalog weak images.

## Storage

Save display images as WebP under:

```text
assets/albums/characters/shino/YYYY/MM/YYYY-MM-DD-theme/
```

Use:

```text
python3 scripts/convert_daily_images_to_webp.py <folder>
```

Treat generated originals and intermediate PNGs as project materials. Do not
delete, destructively rewrite, or discard originals unless the user explicitly
approves that exact scope.

## Canonical JSON

Create or update:

```text
data/albums/characters/shino/YYYY/MM/YYYY-MM-DD-theme.json
```

Album fields:

- `slug`
- `title`
- `summary`
- `summaryJa`
- `preferredAspectRatio`
- `collection`: `character`
- `character`: `shino`
- `notesHref`
- `sortOrder`
- `images`

Per image, write the human-authored fields first:

- `label`
- `src`
- `alt`
- `title`
- `tags`
- `style`
- `place`
- `category`
- `occasion`
- `venue`
- `locationDetail`
- `activity`
- `outfit`

Then run the enrich script to populate measured fields:

```text
python3 scripts/enrich_album_source_metadata.py
```

Do not hand-edit `width`, `height`, or image-level `aspectRatio`; they are
measured from the image file. Do not run `--refresh-text` unless deliberately
regenerating `summaryJa` and `locationDetail` from heuristics.

## Notes And Logs

Create or update:

```text
notes/albums/characters/shino/YYYY/MM/YYYY-MM-DD-theme.md
logs/generation-YYYY-MM.md
```

Record:

- prompt summaries and accepted/regenerated decisions;
- `preferredAspectRatio`;
- reference plan and identity continuity notes;
- route/place/activity plan;
- palette plan and source-daily outfit translation;
- final Shino identity and palette check;
- PNG/original handling decision if relevant.

## Build And Validate

After JSON, note, or image changes:

```text
python3 scripts/build_album_catalog.py
python3 scripts/validate_gallery.py
git diff --check
```

The product album URL is:

```text
album.html?set=YYYY-MM-DD-theme
```

Legacy `assets/YYYY-MM-DD-theme-album.html` files are compatibility redirects
only. Do not hand-edit them as album content.
