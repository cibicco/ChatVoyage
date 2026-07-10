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
  - `prompts/character-album-policy.md` when the set is a character day album
- Fill the required generation parameters from
  `prompts/parameter-checklist.md` before prompting.
- Scan the last three to five daily notes or monthly log entries and write down
  repeated category, pose, garment, background, crop, and lucky-color placement
  formulas before choosing the new set.
- Choose whether the set is normal daily exploration or a character day album.
  In Chat Voyage, character day albums use the same date-based structure, but
  their `index.html` section is marked with `data-collection="character"` and
  `data-character="<slug>"`.
- For Shino/紫乃 fixed-character albums, use `skills/shino-album-generation/`
  instead of the general daily workflow. Shino work has its own identity,
  reference, palette drift, and catalog aftercare requirements.
- For non-Shino character day albums, read `prompts/character-album-policy.md`
  and the relevant character prompt profile before generation.
- A character day album may reinterpret a normal daily city/date set as that
  character's album. It does not need to match the character's main story beat
  exactly, but it must keep face, body continuity, gaze, and visual style strong
  enough that the images read as that character.
- When the album uses a real city, use exact named places rather than
  "something-style" settings. Keep the public place concrete while avoiding
  readable logos, brand marks, exact commercial products, and single-source
  photo copying.
- Check exported album preference feedback when available. Treat `art-style`,
  `person`, and `outfit` as the primary preference dimensions, with `color`,
  `silhouette`, `pose`, `place`, and `vibe` as supporting evidence.
- Capture weather with Open-Meteo when the city/date is known:
  - Resolve the city with
    `https://geocoding-api.open-meteo.com/v1/search?name=<city>&count=5&language=en&format=json`
    and record the selected result's name, country, timezone, latitude, and
    longitude.
  - For past dates, use
    `https://archive-api.open-meteo.com/v1/archive`.
  - For today or future dates, use
    `https://api.open-meteo.com/v1/forecast`.
  - Request at least daily
    `weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,rain_sum,sunshine_duration,wind_speed_10m_max`
    and hourly
    `temperature_2m,relative_humidity_2m,precipitation,rain,weather_code,wind_speed_10m,is_day`
    with the selected city's timezone.
  - Record that Open-Meteo is a gridded/model archive or forecast source, not a
    hand-confirmed station observation. Do not overstate it as exact street
    weather.
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
- Define how the person appears in each image: her adult life context, mood,
  comfort, boundaries, social situation, fashion awareness, and reason for
  wearing the outfit that day. Do not justify openness or coverage only by
  youth, liveliness, sensuality, or modesty.
- Do not treat Asian adult youthful appearance as an underage signal by
  itself. Judge only concrete underage cues such as child body proportions,
  school-uniform or student-minor context, explicitly childish styling,
  infantilized presentation, or sexualized minor-coded framing. `18-19-adult`
  is an adult age band.
- Decide the set's lifestyle snapshot plan. For normal daily exploration, make
  at least two of four images lived moments where the outfit is naturally
  visible: work, making, preparation, errands, waiting, moving through weather,
  home life, carrying, greeting, or reacting. Full body, front view, visible
  face, and centered composition are not required for those images.
- Use action-first pose planning. Before assigning `pose_family`, write the
  concrete life action for each image: for example walking while responding to
  someone, floor warm-up, rooftop pause, home dressing, packing, greeting,
  carrying, repairing, practicing, waiting, or returning home. Pose labels are
  implementation details, not the main source of variety.
- Vary screen grammar as well as outfit: include off-center framing, back or
  side views, mirror/window/reflection views, hands/legs/partial-body crops,
  clothes in motion, or another person's implied presence when it suits the
  moment.
- Plan gaze and attention direction separately from face direction. Avoid both
  all four people looking at the viewer and all four people avoiding the
  viewer; mix viewer-aware, social, task/object, place/window, mirror,
  reflection, or path-of-movement attention.
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
- Select an `effective_style_variant` for each image, especially when using
  anime. Record the intended line language, shading, background density,
  texture, color logic, and time/light expression; do not rely on style slug
  differences alone.
- If the date or city calls for repeated weather, preserve it. Vary time of
  day, rain intensity, indoor/outdoor condition, light source, composition,
  background density, and rendering medium rather than changing the weather
  unrealistically for variety.
- Check recent effective visual finishes separately from category, garment,
  and screen grammar. Cool down repeated finishes such as dense semi-real rain
  painting, glossy fashion-magazine anime, wet-reflection city default, or
  polished cinematic bokeh when they have become familiar.
- Select age bands and pose families before writing image prompts.
- If web/source checks are used, record the sources in the monthly log.
- If Open-Meteo weather was used, record the API method and the resulting
  weather summary in both the monthly log and the album note. Include the
  chosen geocode result, endpoint type (`archive` or `forecast`), requested
  variables, daily values, and any design consequence such as heat, rain,
  humidity, strong wind, or overcast light.

## After Generation

- Save final display images as WebP by default:
  - normal daily albums: `assets/albums/daily/YYYY/MM/YYYY-MM-DD-theme/`
  - character day albums:
    `assets/albums/characters/<character>/YYYY/MM/YYYY-MM-DD-theme/`
  Use `python3 scripts/convert_daily_images_to_webp.py <folder>` after
  generation when the image tool produced PNG files. WebP is the display format
  for the gallery, but generated originals and intermediate PNG files are still
  project materials. Do not delete or destructively rewrite them unless the
  user explicitly approves that scope. If project-local PNG display copies are
  no longer wanted, first verify matching WebP files and gallery references,
  then ask whether to archive, move, or delete those PNG copies.
- Keep four separate images; do not make a collage.
- Add or update a human-readable note:
  - normal daily albums: `notes/albums/daily/YYYY/MM/YYYY-MM-DD-theme.md`
  - character day albums:
    `notes/albums/characters/<character>/YYYY/MM/YYYY-MM-DD-theme.md`
- Add or update the canonical JSON metadata:
  - normal daily albums: `data/albums/daily/YYYY/MM/YYYY-MM-DD-theme.json`
  - character day albums:
    `data/albums/characters/<character>/YYYY/MM/YYYY-MM-DD-theme.json`
- Add detailed LLM/Codex reuse information to `logs/generation-YYYY-MM.md`.
  Use the after-generation fields in `prompts/parameter-checklist.md`.
- Record `prompt_version`, prompt summary, visual check, and any prompt
  shortening or category changes when using prompt v2.
- Record recent-set repetition notes, cooldown formulas, category rotation
  reason, climate context, age-band life scene, age-band silhouette, and the
  anti-repeat instruction for each accepted image.
- Record `effective_style_variant`, `style_execution_check`,
  `time_weather_rendering_check`, and `avoid_recent_effective_style` for each
  accepted image when the set is meant to reduce sameness.
- Record `snapshot_mode`, `composition_variation_axes`, and
  `avoid_recent_screen_grammar` when the set uses lifestyle snapshots or
  partial-detail images. Also record `attention_mix_plan` or
  `attention_mix_check` when gaze balance was part of the correction.
- Record the action-first pose plan and the final action check: what each
  woman is doing before the pose label, and whether the accepted image kept
  those actions distinct.
- If a low, crouching, seated, kneeling, or partial-body pose is rejected,
  record the concrete reason. Do not reject it merely because it looks younger,
  less upright, or less like a standard standing fashion pose. Low poses can be
  valuable because daily sets otherwise drift toward standing views.
- When reviewing recent outfit formulas, explicitly check for repeated
  short outer bottoms over black bike shorts, safety shorts, dance shorts, or
  fitted city shorts. This can be valid for sport, dance, transit, and swim
  contexts, but if it appears repeatedly, put that exact layering formula on
  cooldown and use a different lower-body structure such as single-layer
  joggers, wide trousers, capri pants, opaque tights, a dress, or a skirt/skort
  without visible black under-shorts.
- Record why an active garment is accepted, not only why a safer-looking
  correction was made. Side slits, wrap hems, vents, drawcords, curved hems,
  open wind layers, visible socks, sandals, bike shorts, or safety shorts can
  all be valid when they clearly serve movement, climate, activity, or styling
  attitude. Do not reject those details merely because they could be
  conservatively misread. The rejection target is a tired or unclear repeated
  formula, not an active construction detail by itself.
- When the user indicates that a prior version has the better action,
  silhouette, or character of movement, treat that as design evidence. Compare
  the concrete visual tradeoff before replacing it: active read, garment
  function, pose energy, local place cue, and repetition risk. If restoring the
  prior version, record the accepted reason plainly in the note and monthly log.
- Record the persona direction and fashion focal point for each accepted image.
- For non-Shino character day albums, record the character profile used, chosen adult age
  or age band, identity/style continuity plan, exact place plan, dated route and
  enjoyment plan, and any character-specific drift check.
- Record the four browsing metadata axes for each accepted image: `occasion`,
  `venue`, `activity`, and `outfit`. Keep `data-category` as the historical
  filename/category slug, but do not rely on it as the only browsing axis.
- If album feedback influenced the set, record which preference dimensions were
  used and whether the result was meant to preserve, vary, or avoid them.
- Do not hand-edit `index.html`, `albums.html`, `album.html`, or
  `assets/album-data.js` for album content. They are generated from
  `data/albums/**/*.json`.
- Use `album.html?set=YYYY-MM-DD-theme` as the stable product-facing album
  link. The product-facing album view is the unified `album.html` shell backed
  by `assets/album-data.js`, not a separate full HTML page per set.
- For character day albums, keep the same `YYYY-MM-DD-theme` slug, but set
  `"collection": "character"` and `"character": "<slug>"` in the album JSON.
- Choose album-level `"preferredAspectRatio"` before generation. The default
  standard ratios are `"2:3"` for portrait albums and `"3:2"` for landscape
  albums. Use `"3:4"`, square, or other ratios only when the concept
  deliberately needs a different crop.
- Rebuild the album catalog after every JSON, note, or image reference change:
  `python3 scripts/build_album_catalog.py`
- The legacy `assets/YYYY-MM-DD-theme-album.html` files are compatibility
  redirects only. Do not hand-edit them as album content.
- Add each image to the album JSON with:
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
  - `label`
- Then run `python3 scripts/enrich_album_source_metadata.py` to populate
  measured `width`, `height`, and image-level `aspectRatio`. Do not hand-edit
  those measured fields. Existing `summaryJa` and `locationDetail` are
  preserved unless `--refresh-text` is used deliberately.
- If old sections are missing album links, run the unified catalog builder:
  `python3 scripts/build_album_catalog.py`
- If references were bulk-edited or old PNG references remain, switch display
  references to WebP where matching files exist:
  `python3 scripts/switch_daily_refs_to_webp.py`

## Validation

Run:

```sh
python3 scripts/validate_gallery.py
```

The command should report zero errors. It checks:

- every image under `assets/albums/` is represented in `data/albums/**/*.json`
  and `index.html`
- local album/index links, image references, and the album data file exist
- HTML display references use WebP when a WebP display copy exists
- the unified album shell has data-driven image viewing, thumbnail navigation,
  and direct image links
- every `index.html` set has an album link
- the album browser exposes style filtering, sorting, view switching, active
  filters, and linked CSS/JS assets
- `data-style`, `data-place`, `data-category`, `data-occasion`,
  `data-venue`, `data-activity`, and `data-outfit` values have filter buttons
- index style/category values exist in the prompt preset files

## Skill Maintenance

When the workflow changes in a way that future agents should repeat, update the
project-tracked copy first:

- `skills/daily-fashion-sketch/SKILL.md`
- `skills/daily-fashion-sketch/agents/openai.yaml`

Then sync the same content to the installed Codex skill location:

- `/Users/allegro/.codex/skills/daily-fashion-sketch/SKILL.md`
- `/Users/allegro/.codex/skills/daily-fashion-sketch/agents/openai.yaml`
