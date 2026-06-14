---
name: daily-fashion-sketch
description: Generate and organize a date-seeded Chat Voyage set of four separate fashion images, including style/category/pose variation, adult Japanese-centered character guardrails, logs, notes, albums, and gallery validation. Use when the user asks for today's/daily fashion images, 今日の画像, 今日らしいファッション, city/theme-based Japanese women fashion looks, 3D/anime/fashion-illustration style exploration, or a four-image editorial fashion workflow that should use the imagegen skill.
---

# Daily Fashion Sketch

## Core Workflow

Use this skill with the `imagegen` skill. The output should be four separate
raster images, generated with one `image_gen` call per image. Do not make a
single four-panel collage.

1. Establish the date seed from the current date in the user's locale unless the user specifies a date.
2. If working in Chat Voyage, use the project root one level above `assets/`:
   `/Users/allegro/Applications/ChatVoyage`.
3. Read Chat Voyage prompt presets when present:
   - `prompts/daily-fashion-template.md`
   - `prompts/parameter-checklist.md`
   - `prompts/generation-prompt-v2.md`
   - `prompts/repetition-guardrails.md`
   - `prompts/persona-presets.md`
   - `prompts/style-presets.md`
   - `prompts/category-presets.md`
   - `prompts/age-presets.md`
   - `prompts/pose-presets.md`
4. Read the project references when present in the current workspace:
   - `fashion_reference_chatgpt_simple.xlsx`
   - `source_list_chatgpt_complete.md`
   - `fashion_reference_image_guardrails.md`
   - `project_reference_image_plan.md`
5. If a reference file is missing, state that fact briefly and continue with the available files and web/source scan. Do not imply that missing files were read.
6. Lightly scan current sources when web access is available, prioritizing a broader young-adult source mix rather than relying only on Vogue:
   - street/holiday: FASHIONSNAP, FUDGE, GINZA
   - young culture: NYLON JAPAN, i-D, Dazed, Hypebeast/Hypebae, local street snaps, university-age street style sources
   - runway/completion: Vogue Runway and brand lookbooks
   - night/events/gloss: NYLON JAPAN, Dazed, i-D
   - resort/swim: Vogue Runway Resort, ALEXIA STAM, San-ai Resort, Hunza G, Calzedonia
7. Synthesize a daily direction before prompting:
   - one common mood
   - one lucky color
   - one city theme
   - four selected fashion categories from `category-presets.md`
   - one shared visual style or two to four mixed styles from `style-presets.md`
   - four target age bands and pose families
   - a persona direction from `prompts/persona-presets.md`
   - age-based tone choices for the lucky color
   - a skin/coverage comfort plan that varies garment openness, airflow,
     coverage, and layering according to scene needs
   - climate and comfort logic so the outfit is natural for the weather,
     venue, temperature, and activity
   - a local place plan that treats indoor scenes broadly: not only rooms,
     work, meals, cafes, or bars, but also city-specific activity spaces such
     as museums, art museums, galleries, clubs, live houses, theaters, cinemas,
     libraries, ateliers, sports facilities, public halls, stations, markets,
     and covered arcades when they fit the set
   - the variation axes across all four images
   - a recent-set repetition check using `prompts/repetition-guardrails.md`
   - the required parameter map from `prompts/parameter-checklist.md`
8. Build four separate prompts using [prompt-architecture.md](references/prompt-architecture.md) and the Chat Voyage presets. Mix at least three influence systems in every look: garment structure, mood/source tags, and visual expression.
9. If the full prompt is likely to be unstable, use
   `prompts/generation-prompt-v2.md`: keep the image-generation prompt short,
   include one anti-repeat instruction per image, and record the full parameter
   map plus visual check in the monthly log.
10. Before generation, briefly show the common mood, lucky color, city theme, selected categories, selected styles, pose plan, and source links if web was used. Then generate the four images.
11. Inspect each result against the quality gates. Regenerate only the failing image with a targeted correction if needed. When using prompt v2, record prompt summaries and visual checks for accepted images.
12. Save accepted images under `assets/daily/YYYY-MM-DD-theme/`, then update the monthly log, notes, album, and `index.html`.
13. Run `python3 scripts/validate_gallery.py` from the Chat Voyage root when that script exists.

## Reference Reading

Prefer source cards, tags, prompt memos, guardrails, and planning notes over copying any one visual example.

For the spreadsheet, inspect workbook sheet names and header rows first. Load only the relevant rows/columns needed for source cards, tags, mood, color, season, category, prompt memo, silhouettes, materials, and avoid rules. Use spreadsheet tooling or a structured parser; do not rely on raw string scraping for `.xlsx`.

For Markdown references, search for sections about:

- source cards / tags / prompt memo
- image guardrails
- outfit construction
- diversity across people and looks
- forbidden copying / single-source reproduction
- resort, swim, night, and sensuality constraints

## Image Requirements

Each image must show a different adult Japanese woman or Japanese-centered
model. Current Chat Voyage age bands are `18-19-adult`, `20-24`, and `25-29`
unless the user explicitly asks otherwise. Realistic youthful Japanese adult
features are acceptable; the problem is underage framing. Avoid childlike
styling, school-uniform cues, sailor-uniform cues, teen-idol styling, and
identical face/body/hair patterns. University settings are allowed for adult
characters.

The persona should be selected per image, not forced into one fixed type.
Every character should be fashion-aware, interested in clothes, good at
choosing distinctive styling details, and aware of her own charm without being
reduced to erotic display. Then choose two to five traits such as bright,
sociable, personable, sensual, lively, self-possessed, playful, curious,
daring, relaxed, elegant, sharp, or quietly confident. Express the selected
traits through posture, expression, gesture, outfit completion, color, fabric,
silhouette, accessories, and scene behavior. Prefer light, mobile, fashionable
styling over heavy clothing used only as a guardrail.

Vary more than color. Across the four prompts, explicitly vary:

- silhouette and garment construction
- life scene and activity by age band
- personality expression and fashion focal point
- length and proportion
- material and texture
- shoes and legwear
- skin/coverage comfort
- lucky-color tone by age band
- lucky-color placement by garment type, not only color of a repeated garment
- styling attitude
- time of day and background
- local place type, including city-specific indoor or activity spaces when
  relevant rather than only generic rooms, offices, cafes, bars, or restaurants
- visual style preset when the user asks for mixed style exploration
- pose family, face direction, body direction, camera angle, hand placement,
  and crop

Keep sensual, night, resort, or swimwear elements tasteful and editorial. Skin
visibility is not a problem by itself, and low skin visibility is not a quality
goal by itself. Judge whether the garment construction, neckline, sleeves, hem,
fabric weight, footwear, and layering feel natural for the city, season,
weather, temperature, venue, time of day, and activity.

Do not overcorrect into consistently covered looks, and do not force openness
where it fights the scene. If the daily theme is rain, outerwear, transit, or
low-key city walking, still consider adult fashion constructions such as
sleeveless inner layers, sheer shells, open backs, shorter hems with legwear,
carried jackets, sandals, or dance/resort/night details where the category
supports them.

Do not solve adult/age guardrails by forcing unnatural coverage. Necklines,
sleeves, fabric weight, footwear, and layering should be plausible for the
city, season, temperature, humidity, venue, time of day, weather intensity,
wind or air conditioning, and activity. Do not reduce climate naturalness to a
single warm-weather formula. In warm or humid weather, breathable adult fashion
choices may include tanks, camisoles, open shirts, mesh, and sandals, but also
cotton tees, buttoned short-sleeve shirts, airy shirt dresses, sleeveless
tailoring, light jumpsuits, cropped trousers, washable skirts, technical rain
pants, sneakers, mules, thin cardigans for air-conditioned interiors, or
compact outer layers.

Age bands must differ by more than color tone. For each target age band, vary
the life scene, silhouette, material logic, accessory logic, and styling
attitude. Do not repeatedly assign the same role such as young market casual,
early-20s open-back gallery, late-20s seated camisole lounge, and early-20s
mesh transit unless that repeat is intentional and logged.

Indoor and activity scenes should be locally specific. Indoor does not mean
only ordinary rooms, work, meals, cafes, or bars. Use city- or region-specific
activity spaces such as museums, art museums, galleries, clubs, live houses,
theaters, cinemas, libraries, ateliers, sports facilities, public halls,
stations, markets, covered arcades, baths, or performance foyers when they fit
the date and category. The place should affect outfit construction, footwear,
layering, pose, object interaction, and time-of-day behavior.

Full-body is allowed but not required. Use knee-up, waist-up, close-up detail,
wide-action, seated, back three-quarter, jumping, reaching, leaning, or object
interaction crops when they better express pose variety and fashion detail.
For boats, ferries, trains, buses, stations, piers, bridges, water edges,
stairs, or platforms, dynamic motion must read as a clear intentional action.
Risk and balance are allowed when chosen by the character: walking along a boat
edge, balancing on a narrow bridge, stepping over a gap, or turning on a wet
pier can work when body language, weight, gaze, and foot placement are legible.
Do not accept an image that looks like accidental falling, unexplained leaping
away from a vehicle, or unclear body mechanics just because the outfit itself
is successful.

## Quality Gates

Before accepting the set, check:

- Four separate images were generated.
- The four women are visibly different people.
- Each woman reads as a fashion-aware adult with selected personality traits
  and a chosen styling focal point, not a neutral mannequin wearing clothes.
- The four looks are not color swaps of the same outfit.
- The set is not a repeat of the last three to five accepted daily sets with
  only the city and lucky color changed.
- Four primary categories were selected intentionally. Do not default to
  Street / Mode / Night / Resort unless they genuinely fit the day.
- Recent category, garment, pose, crop, and background formulas were checked
  and any repeated formula was avoided or explicitly justified.
- Selected `data-style` and `data-category` values exist in the Chat Voyage
  prompt presets when working in that project.
- The shared daily mood is present but subtle.
- The lucky color appears in each image, with different intensity or placement.
- The lucky color tone reflects the target age band, not only the shared daily
  color name.
- Skin visibility, airflow, and coverage are intentionally varied because
  garment construction, climate, venue, and activity vary. Do not collapse into
  four similarly covered long-layer looks unless the user asks for that, and do
  not force openness where it would be unnatural.
- The outfit feels natural for the weather, temperature, venue, and movement;
  the person is not being forced into coverage that fights the scene.
- Climate fit reflects city, season, time of day, rain intensity, indoor or
  outdoor setting, wind or air conditioning, venue norms, and activity instead
  of defaulting to tanks, camisoles, mesh, open shirts, and sandals.
- Indoor or activity places are concrete and locally characteristic, not only
  generic rooms, work, meals, cafes, bars, or interchangeable interiors.
- No single source, brand look, celebrity outfit, or reference image is reproduced.
- Backgrounds support the outfit context without overpowering the figure.
- No visible text, watermark, logo imitation, or brand mark is requested.
- Poses do not all face the same direction, and the set does not collapse into
  four standing three-quarter views.
- Dynamic travel, vehicle, waterside, stair, pier, bridge, or platform actions
  read as intentional and physically coherent for the place. Risky or balancing
  actions are allowed when they read as the character's choice.
- Logs, notes, album/index references, and validation are updated when the user
  asks for a reusable Chat Voyage set.

## Final Response Shape

If using `image_gen`, provide the daily header before the image calls:

```text
共通ムード: ...
ラッキーカラー: ...
都市テーマ: ...
カテゴリ: ...
スタイル: ...
ポーズ方針: ...
```

If web sources were used, include a compact `確認ソース:` line with links before generation. After the image calls, follow the active `imagegen` tool rules for post-generation text.
