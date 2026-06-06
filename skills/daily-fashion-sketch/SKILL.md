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
   - age-based tone choices for the lucky color
   - an exposure plan that varies covered, moderate, open, and layered styling
   - climate and comfort logic so the outfit is natural for the weather,
     venue, temperature, and activity
   - the variation axes across all four images
   - the required parameter map from `prompts/parameter-checklist.md`
8. Build four separate prompts using [prompt-architecture.md](references/prompt-architecture.md) and the Chat Voyage presets. Mix at least three influence systems in every look: garment structure, mood/source tags, and visual expression.
9. Before generation, briefly show the common mood, lucky color, city theme, selected categories, selected styles, pose plan, and source links if web was used. Then generate the four images.
10. Inspect each result against the quality gates. Regenerate only the failing image with a targeted correction if needed.
11. Save accepted images under `assets/daily/YYYY-MM-DD-theme/`, then update the monthly log, notes, album, and `index.html`.
12. Run `python3 scripts/validate_gallery.py` from the Chat Voyage root when that script exists.

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

Vary more than color. Across the four prompts, explicitly vary:

- silhouette and garment construction
- length and proportion
- material and texture
- shoes and legwear
- exposure balance
- lucky-color tone by age band
- styling attitude
- time of day and background
- visual style preset when the user asks for mixed style exploration
- pose family, face direction, body direction, camera angle, hand placement,
  and crop

Keep sensual, night, resort, or swimwear elements tasteful and editorial.
Exposure is allowed when it is clearly fashion styling, runway, club, resort,
swim, dance, sheer layering, cutouts, lingerie-inspired layering, or evening
wear. Treat it as garment-focused styling, not erotic display.

Do not overcorrect into consistently covered looks. If the daily theme is rain,
outerwear, transit, or low-key city walking, still consider adult fashion
constructions such as sleeveless inner layers, sheer shells, open backs,
shorter hems with legwear, carried jackets, sandals, or dance/resort/night
details where the category supports them.

Do not solve adult/age guardrails by forcing unnatural coverage. Necklines,
sleeves, fabric weight, footwear, and layering should be plausible for the
city, season, temperature, humidity, venue, and activity. In warm or humid
weather, prefer breathable adult fashion choices over default high-neck tops,
heavy layers, long sleeves, or closed shoes when those would make the person
look physically uncomfortable.

Full-body is allowed but not required. Use knee-up, waist-up, close-up detail,
wide-action, seated, back three-quarter, jumping, reaching, leaning, or object
interaction crops when they better express pose variety and fashion detail.

## Quality Gates

Before accepting the set, check:

- Four separate images were generated.
- The four women are visibly different people.
- The four looks are not color swaps of the same outfit.
- Four primary categories were selected intentionally. Do not default to
  Street / Mode / Night / Resort unless they genuinely fit the day.
- Selected `data-style` and `data-category` values exist in the Chat Voyage
  prompt presets when working in that project.
- The shared daily mood is present but subtle.
- The lucky color appears in each image, with different intensity or placement.
- The lucky color tone reflects the target age band, not only the shared daily
  color name.
- Exposure balance is intentionally varied and does not collapse into four
  similarly covered long-layer looks unless the user asks for that.
- The outfit feels natural for the weather, temperature, venue, and movement;
  the person is not being forced into coverage that fights the scene.
- No single source, brand look, celebrity outfit, or reference image is reproduced.
- Backgrounds support the outfit context without overpowering the figure.
- No visible text, watermark, logo imitation, or brand mark is requested.
- Poses do not all face the same direction, and the set does not collapse into
  four standing three-quarter views.
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
