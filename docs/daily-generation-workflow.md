# Chat Voyage Daily Generation Workflow

Use this checklist after every daily image generation or reorganization.

## Before Generation

- Choose the Asia/Tokyo date seed unless the user specifies another date.
- Read the relevant prompt presets:
  - `prompts/daily-fashion-template.md`
  - `prompts/style-presets.md`
  - `prompts/category-presets.md`
  - `prompts/age-presets.md`
  - `prompts/pose-presets.md`
- Select four categories from `category-presets.md`; do not default to
  Street / Mode / Night / Resort unless that fits the day.
- Select image style presets from `style-presets.md`.
- Select age bands and pose families before writing image prompts.
- If web/source checks are used, record the sources in the monthly log.

## After Generation

- Save final images under `assets/daily/YYYY-MM-DD-theme/`.
- Keep four separate images; do not make a collage.
- Add or update a human-readable note in `notes/YYYY-MM-DD-theme.md`.
- Add detailed LLM/Codex reuse information to `logs/generation-YYYY-MM.md`.
- Add an album page under `assets/YYYY-MM-DD-theme-album.html` when the set is
  intended to be browsed independently.
- Add the set to `index.html` with:
  - `data-style`
  - `data-place`
  - `data-category`
  - note link
  - album link when available

## Validation

Run:

```sh
python3 scripts/validate_gallery.py
```

The command should report zero errors. It checks:

- every image under `assets/daily/` is represented in `index.html`
- local album/index links and image references exist
- `data-style`, `data-place`, and `data-category` values have filter buttons
- index style/category values exist in the prompt preset files

## Skill Maintenance

When the workflow changes in a way that future agents should repeat, update
`/Users/allegro/.codex/skills/daily-fashion-sketch/SKILL.md` instead of relying
only on project-local notes.
