# Chat Voyage Daily Generation Workflow

Use this checklist after every daily image generation or reorganization.

## Before Generation

- Choose the Asia/Tokyo date seed unless the user specifies another date.
- Read the relevant prompt presets:
  - `prompts/daily-fashion-template.md`
  - `prompts/parameter-checklist.md`
  - `prompts/repetition-guardrails.md`
  - `prompts/persona-presets.md`
  - `prompts/generation-prompt-v2.md`
  - `prompts/style-presets.md`
  - `prompts/category-presets.md`
  - `prompts/age-presets.md`
  - `prompts/pose-presets.md`
- Fill the required generation parameters from
  `prompts/parameter-checklist.md` before prompting.
- Scan the last three to five daily notes or monthly log entries and write down
  repeated category, pose, garment, background, crop, and lucky-color placement
  formulas before choosing the new set.
- Decide climate fit from city, season, time of day, weather, temperature band,
  humidity, indoor/outdoor conditions, wind or air conditioning, rain intensity,
  venue norms, and activity. Do not default to one warm-weather formula.
- Include locally specific indoor or activity spaces when they fit the set.
  Indoor is not limited to rooms, work, meals, cafes, or bars; use museums, art
  museums, galleries, clubs, live houses, theaters, cinemas, libraries,
  ateliers, sports facilities, public halls, stations, markets, covered
  arcades, or similar local places when they are characteristic of the city.
- Vary age bands by life scene, silhouette, material, and accessories, not only
  by color tone or face age.
- Define how the core persona appears in each image: bright, sociable, lively,
  fashion-aware, intentionally stylish, and aware of her charm without erotic
  framing.
- Choose one or two fashion focal points per image, such as color, accessory,
  fabric, silhouette, shoes, bag, jewelry, hair accessory, layering, or fabric
  movement.
- If full-detail prompts are unstable, switch to
  `prompts/generation-prompt-v2.md`: keep the image prompt short, include one
  anti-repeat instruction per image, and record the detailed design plus visual
  check in the monthly log.
- Select four categories from `category-presets.md`; do not default to
  Street / Mode / Night / Resort unless that fits the day.
- Do not repeat `market` / `gallery` / `lounge` / `transit` or another recent
  category quartet by habit. If repeated, log why the repeat is necessary.
- Select image style presets from `style-presets.md`.
- Select age bands and pose families before writing image prompts.
- If web/source checks are used, record the sources in the monthly log.

## After Generation

- Save final display images under `assets/daily/YYYY-MM-DD-theme/` as WebP
  by default. Use `python3 scripts/convert_daily_images_to_webp.py <folder>`
  after generation when the image tool produced PNG files. Keep generated PNG
  originals only when they are needed as source material; do not delete
  originals unless the user explicitly asks.
- Keep four separate images; do not make a collage.
- Add or update a human-readable note in `notes/YYYY-MM-DD-theme.md`.
- Add detailed LLM/Codex reuse information to `logs/generation-YYYY-MM.md`.
  Use the after-generation fields in `prompts/parameter-checklist.md`.
- Record `prompt_version`, prompt summary, visual check, and any prompt
  shortening or category changes when using prompt v2.
- Record recent-set repetition notes, cooldown formulas, category rotation
  reason, climate context, age-band life scene, age-band silhouette, and the
  anti-repeat instruction for each accepted image.
- Record the persona direction and fashion focal point for each accepted image.
- Add an album page under `assets/YYYY-MM-DD-theme-album.html` when the set is
  intended to be browsed independently.
- Use album markup that works on mobile: `object-fit: contain`, direct image
  links, `loading` / `decoding` attributes, and an `Open image` link for each
  image.
- Rebuild existing or newly edited album pages with the current shared
  template when needed:
  `python3 scripts/rebuild_album_pages.py`
- For a small compatibility cleanup without full template rebuild, run:
  `python3 scripts/normalize_album_pages.py`
- Add the set to `index.html` with:
  - `data-style`
  - `data-place`
  - `data-category`
  - note link
- album link when available
- Rebuild the album-level browser when album links change:
  `python3 scripts/build_album_index.py`
- If references were bulk-edited or old PNG references remain, switch display
  references to WebP where matching files exist:
  `python3 scripts/switch_daily_refs_to_webp.py`

## Validation

Run:

```sh
python3 scripts/validate_gallery.py
```

The command should report zero errors. It checks:

- every image under `assets/daily/` is represented in `index.html`
- local album/index links and image references exist
- HTML display references use WebP when a WebP display copy exists
- album pages use non-cropping image display and direct image links
- `data-style`, `data-place`, and `data-category` values have filter buttons
- index style/category values exist in the prompt preset files

## Skill Maintenance

When the workflow changes in a way that future agents should repeat, update the
project-tracked copy first:

- `skills/daily-fashion-sketch/SKILL.md`
- `skills/daily-fashion-sketch/agents/openai.yaml`

Then sync the same content to the installed Codex skill location:

- `/Users/allegro/.codex/skills/daily-fashion-sketch/SKILL.md`
- `/Users/allegro/.codex/skills/daily-fashion-sketch/agents/openai.yaml`
