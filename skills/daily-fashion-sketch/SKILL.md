---
name: daily-fashion-sketch
description: Chat Voyage repo-specific daily/theme fashion generation skill. Use only when working in /Users/allegro/Applications/ChatVoyage, or when the user explicitly asks for Chat Voyage daily images. Generates and organizes date-seeded non-recurring daily/theme fashion image sets with canonical album JSON, WebP display handling, notes/logs, catalog rebuilds, and validation. Do not use for generic fashion generation outside Chat Voyage. Do not use for Shino/紫乃 fixed-character albums; use shino-album-generation for those.
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
   - `prompts/character-album-policy.md` only when the user explicitly asks
     for a non-Shino character day album
   - for Shino/紫乃 fixed-character albums, switch to
     `$shino-album-generation` instead of continuing with this general daily
     workflow
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
   - four browsing metadata axes per image: `occasion`, `venue`, `activity`,
     and `outfit`, inferred from the actual person, place, action, and garment
     structure rather than copied blindly from the legacy category
   - one shared visual style or two to four mixed styles from `style-presets.md`
   - an effective style plan for each image, especially for anime: line
     language, shading, background density, texture, color logic, and
     time/light expression. Do not rely on `style_preset` slugs alone; if two
     generated images both read as the same glossy anime or semi-real rain
     finish, treat them as repeats.
   - four target age bands and pose families
   - a persona direction from `prompts/persona-presets.md`
   - age-based tone choices for the lucky color
   - a garment openness, hem, legwear, and footwear plan that varies airflow,
     fabric, neckline, hem length, shoes, socks/tights/bare legs, and layering
     according to scene needs
   - climate and comfort logic so the outfit is natural for the weather,
     venue, temperature, and activity
   - a time/weather rendering plan. If the date, city, or source scan calls
     for rain or another repeated weather condition, keep it and vary time of
     day, rain intensity, indoor/outdoor condition, light source, composition,
     background density, and medium instead of inventing different weather only
     for novelty.
   - a local place plan that prioritizes visible local atmosphere over the
     indoor/outdoor distinction. Cafes, workshops, night bars, pools, beaches,
     mountains, cultural facilities, markets, stations, terraces, studios,
     and streets are all valid when the image can show the city's light,
     architecture, materials, weather, landscape, objects, or social rhythm.
     Indoor scenes should still be broad: not only rooms, work, meals, cafes,
     or bars, but also city-specific activity spaces such as museums, art
     museums, galleries, clubs, live houses, theaters, cinemas, libraries,
     ateliers, sports facilities, public halls, stations, markets, and covered
     arcades when they fit the set.
   - a lifestyle snapshot plan for normal daily exploration. Unless the user
     asks for a pure fashion-board set, make at least two of four images lived
     moments where the outfit is naturally visible rather than a full-outfit
     display staged only for fashion review.
   - an action-first pose plan. Before assigning pose-family labels, decide the
     concrete life action for each image, such as walking while responding to
     someone, floor warm-up, rooftop pause, home dressing, packing, greeting,
     carrying, repairing, practicing, waiting, or returning home. Pose labels
     are implementation details, not the main source of variety.
   - a screen-grammar variation plan that may include off-center framing,
     back/side views, mirror/window/reflection views, hands/legs/partial-body
     crops, clothes in motion, or another person's implied presence.
   - a gaze and attention mix plan. Avoid both all four women looking at the
     viewer and all four women avoiding the viewer; mix viewer-aware, social,
     task/object, place/window, mirror, reflection, or path-of-movement
     attention.
   - for non-Shino character work, a character album mode note. In Chat Voyage,
     character day albums should
     be marked with `data-collection="character"` and
     `data-character="<slug>"`; they show a recurring character going to places
     and enjoying a dated story day, and they are evaluated as their own pool.
     They may reinterpret a normal daily city/date set as that character's
     album, so preserve face, body continuity, gaze, and visual style while
     allowing the adult age band, city, outfit, and activity to change.
     Real-city character albums should use exact named places, not
     "something-style" placeholders.
   - exported album preference feedback when available, using `art-style`,
     `person`, and `outfit` as primary preference dimensions, and `color`,
     `silhouette`, `pose`, `place`, and `vibe` as supporting evidence
   - Open-Meteo weather capture when the city/date is known:
     resolve the city with
     `https://geocoding-api.open-meteo.com/v1/search?name=<city>&count=5&language=en&format=json`,
     then use `https://archive-api.open-meteo.com/v1/archive` for past dates
     or `https://api.open-meteo.com/v1/forecast` for today/future dates.
     Request daily
     `weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,rain_sum,sunshine_duration,wind_speed_10m_max`
     and hourly
     `temperature_2m,relative_humidity_2m,precipitation,rain,weather_code,wind_speed_10m,is_day`
     with the selected city's timezone. Record the selected geocode result,
     endpoint type, requested variables, daily summary, and any design
     consequence in the monthly log and album note. Treat Open-Meteo as a
     gridded/model archive or forecast source, not exact street-level weather.
   - the variation axes across all four images
   - a recent-set repetition check using `prompts/repetition-guardrails.md`
   - a recent effective-style check using `prompts/style-presets.md` and
     `prompts/repetition-guardrails.md`, including cooldowns for repeated
     visual finishes such as high-density semi-real rain painting, glossy
     fashion-magazine anime, wet-reflection city default, or cinematic bokeh
   - the required parameter map from `prompts/parameter-checklist.md`
8. Build four separate prompts from the Chat Voyage presets. Mix at least three influence systems in every look: garment structure, mood/source tags, and visual expression.
9. If the full prompt is likely to be unstable, use
   `prompts/generation-prompt-v2.md`: keep the image-generation prompt short,
   include one anti-repeat instruction per image, and record the full parameter
   map plus visual check in the monthly log.
10. Before generation, briefly show the common mood, lucky color, city theme, selected categories, selected styles, pose plan, and source links if web was used. Then generate the four images.
11. Inspect each result against the quality gates. Regenerate only the failing image with a targeted correction if needed. When using prompt v2, record prompt summaries and visual checks for accepted images.
12. Save accepted display images as WebP by default:
    - normal daily albums:
      `assets/albums/daily/YYYY/MM/YYYY-MM-DD-theme/`
    - character day albums:
      `assets/albums/characters/<character>/YYYY/MM/YYYY-MM-DD-theme/`
    If the image tool produced PNG files, use
    `python3 scripts/convert_daily_images_to_webp.py <folder>` and point the
    album JSON at the WebP files. Treat generated originals and intermediate
    PNG files as project materials: do not delete or destructively rewrite them
    unless the user explicitly approves that scope. If project-local PNG display
    copies are no longer wanted, first verify matching WebP files and gallery
    references, then ask whether to archive, move, or delete those PNG copies.
13. Update the monthly log, note, canonical album JSON, and generated catalog.
    Album JSON lives under `data/albums/daily/YYYY/MM/` for normal daily sets
    and `data/albums/characters/<character>/YYYY/MM/` for non-Shino character
    sets.
    Use `album.html?set=YYYY-MM-DD-theme` as the stable album link.
    Choose and record album-level `preferredAspectRatio` before generation.
    Use `2:3` for standard portrait albums and `3:2` for standard landscape
    albums unless the concept needs a different crop.
    Keep the historical `category` slug for filenames and compatibility, but
    also add `occasion`, `venue`, `activity`, and `outfit` for browsing and
    review. Add `summaryJa` and concrete `locationDetail`; then run
    `python3 scripts/enrich_album_source_metadata.py` so measured `width`,
    `height`, and image-level `aspectRatio` are populated from the files.
    The product-facing album view is the unified `album.html` shell backed by
    generated `assets/album-data.js`; legacy
    `assets/YYYY-MM-DD-theme-album.html` files are compatibility redirects only.
    If album preference feedback influenced the set, record the dimensions
    used and whether the result was meant to preserve, vary, or avoid them.
14. When old pages or bulk edits are involved, run
    `python3 scripts/switch_daily_refs_to_webp.py` and
    `python3 scripts/build_album_catalog.py`.
15. Rebuild the album catalog with `python3 scripts/build_album_catalog.py`
    whenever album JSON, set metadata, or image references change.
16. Run `python3 scripts/validate_gallery.py` from the Chat Voyage root when that script exists.

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

Do not treat Asian adult youthful appearance as an underage signal by itself.
Judge only concrete underage cues such as child body proportions,
school-uniform or student-minor context, explicitly childish styling,
infantilized presentation, or sexualized minor-coded framing. `18-19-adult` is
an adult age band. A crouching, seated, kneeling, low-angle, or partial-body
pose is not a problem by itself; these poses can be valuable because sets
otherwise drift toward standing fashion views. If rejecting a low pose, record
the concrete issue rather than using vague youth or pose-risk language.

The persona should be selected per image, not forced into one fixed type.
Every character should have ordinary human agency: a day, a place to be, a
body, preferences, comfort, boundaries, mood, social context, and reasons for
what she wears. She should be fashion-aware and capable of choosing
distinctive styling details without being reduced to erotic display or
sanitized coverage. Then choose two to five traits such as bright, quiet,
sociable, personable, sensual, practical, self-possessed, playful, curious,
daring, relaxed, elegant, reserved, sharp, or quietly confident. Express the
selected traits through posture, expression, gesture, outfit completion,
color, fabric, silhouette, accessories, context, and scene behavior. Prefer
light, mobile, fashionable styling over heavy clothing used only as a
guardrail.

Vary more than color. Across the four prompts, explicitly vary:

- silhouette and garment construction
- life scene and activity by age band
- personality expression and fashion focal point
- length and proportion
- material and texture
- shoes and legwear
- garment openness and skin/coverage comfort
- lucky-color tone by age band
- lucky-color placement by garment type, not only color of a repeated garment
- styling attitude
- time of day and background
- local place type, including city-specific indoor or activity spaces when
  relevant rather than only generic rooms, offices, cafes, bars, or restaurants
- visual style preset when the user asks for mixed style exploration
- effective visual style even when style metadata changes: line language,
  shading, background density, texture, color logic, medium, and time/light
  expression should not collapse into the same recent finish
- weather rendering when weather is shared: keep true rain or overcast
  conditions when they fit, but vary time of day, rain intensity,
  indoor/outdoor condition, light source, composition, background density, or
  medium
- pose family, face direction, body direction, camera angle, hand placement,
  and crop
- screen grammar: centered versus off-center subject, full body versus partial
  crop, face-visible versus face-optional, front view versus back/side/mirror
  view, solo portrait versus other people implied, and fashion-editorial view
  versus candid life action
- attention direction: direct or near-camera acknowledgement, another person,
  task/object, place/window, mirror, reflection, or path of movement. Avoid
  both all-camera-contact and all-camera-avoidance across the four images.

Keep sensual, night, resort, or swimwear elements tasteful and editorial. Skin
visibility is not a problem by itself, and low skin visibility is not a quality
goal by itself. Judge whether the garment construction, neckline, sleeves, hem,
fabric weight, footwear, and layering feel natural for the city, season,
weather, temperature, venue, time of day, and activity.

Do not treat ordinary warm-weather pieces as a problem by themselves. Tanks,
open shirts, camisoles, mesh, sandals, miniskirts, short skorts, shorts, bare
legs, socks, tights, bike shorts, and visible leg styling are all valid adult
fashion choices when the full outfit, pose, scene, age band, and activity make
them natural. Cool down repeated full formulas, not garment categories.

Do not justify clothing openness or coverage only through youth, liveliness,
sensuality, or modesty. Ground it in human life: weather, comfort, movement,
venue, social context, taste, work, rest, play, travel, ceremony, and the
person's own presentation for that day.

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

Do not treat anime as one style. Anime outputs can be clean cel, slice-of-life
TV, manga ink, retro OVA, watercolor-soft, pop graphic, low-fidelity sketch,
cinematic night, or comic-panel. If the final result looks like the same recent
glossy editorial anime despite a different slug, regenerate with concrete
instructions for line, shading, background density, texture, color, or light.

Use legwear deliberately as fashion language: bare legs, sheer or opaque
socks, ribbed socks, slouch socks, sport socks, lace socks, knee socks, sheer
or mesh knee-highs, thin stockings, back-seam stockings, patterned or opaque
tights, fishnets, leggings, bike shorts, bloomers, and safety shorts can all
be correct. They should not be added only as modesty patches or removed only to
signal openness. If recent sets repeatedly use the same short transparent
ankle-sock or below-knee sheer-sock finish, put that specific finish on
cooldown. Prefer a clearer length decision: ankle-length socks, bare legs, or
over-knee / thigh-high hosiery above the knee when hosiery is part of the
fashion language.

Also check for repeated short outer bottoms over black bike shorts, safety
shorts, dance shorts, or fitted city shorts. That construction can be valid for
sport, dance, transit, and swim contexts, but if it appears repeatedly, put the
exact layering formula on cooldown and use a different lower-body structure
such as single-layer joggers, wide trousers, capri pants, opaque tights, a
dress, or a skirt/skort without visible black under-shorts.

When reviewing an active look, record why the accepted garment works. Side
slits, wrap hems, vents, drawcords, curved hems, open wind layers, visible
socks, sandals, bike shorts, and safety shorts can all be valid fashion and
movement details when they serve the activity, climate, pose energy, or styling
attitude. Do not reject a detail merely because it could be conservatively
misread. Reject or revise tired formulas and unclear layering, not active
construction details by themselves. If a user points out that a previous
version better preserves the action or movement, compare the concrete tradeoff
and record the accepted reason in the note and monthly log rather than
defaulting to the safest-looking correction.

Do not make high legwear automatically sheer. Over-knee or thigh-high styling
can be opaque knit, ribbed cotton or wool, colored opaque stocking, matte
dance tight, back-seam stocking, lace-top stocking, micro fishnet, patterned
tight, stirrup tight, glossy stage tight, sporty tube sock, bare-leg
contrast, or sheer hosiery. Choose the material from the person, venue,
season, movement, and outfit construction rather than treating transparency as
the default.

Age bands must differ by more than color tone. For each target age band, vary
the life scene, silhouette, material logic, accessory logic, and styling
attitude. Do not repeatedly assign the same role such as young market casual,
early-20s open-back gallery, late-20s seated camisole lounge, and early-20s
mesh transit unless that repeat is intentional and logged.

Places should make local atmosphere visible. Indoor or outdoor is secondary:
cafes, workshops, night bars, pools, beaches, mountains, cultural facilities,
markets, stations, terraces, studios, and streets can all work when the image
shows the city's light, architecture, materials, weather, landscape, objects,
or social rhythm. Indoor and activity scenes should still be locally specific.
Indoor does not mean only ordinary rooms, work, meals, cafes, or bars. Use
city- or region-specific activity spaces such as museums, art museums,
galleries, clubs, live houses, theaters, cinemas, libraries, ateliers, sports
facilities, public halls, stations, markets, covered arcades, baths, or
performance foyers when they fit the date and category. The place should
affect outfit construction, footwear, layering, pose, object interaction, and
time-of-day behavior.

When a real named place is selected, keep it concrete. The user often wants to
see the world's actual scenes, not a generic "inspired by" version. Use the
place name in planning, notes, and logs, and show public architecture,
materials, routes, light, landscape, objects, activity, and social rhythm.
Avoid logos, readable trademarks, exact product copies, and single-source
photo copying; do not treat real-place specificity as a problem.

Full-body is allowed but not required. Use knee-up, waist-up, close-up detail,
wide-action, seated, back three-quarter, jumping, reaching, leaning, or object
interaction crops when they better express pose variety and fashion detail.
For normal daily exploration, at least two images should be lifestyle snapshots:
the woman is doing something in her life and the outfit is naturally visible
inside that moment. Full body, front view, visible face, and centered
composition are not quality requirements for those images. Back views,
partial-body crops, hands, legs, mirror or window reflections, foreground
obstruction, clothes in motion, and other people's implied presence can all be
valid when they make the scene feel lived rather than staged.
Plan those actions before choosing the pose family. Good pose variety comes
from different life verbs, not from changing pose labels while the image still
feels like a person standing, waiting, or holding a small object. Record the
action-first pose plan in notes or logs when generating a reusable set.
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
- Character day albums use `data-collection="character"` and
  `data-character="<slug>"`. They keep the same recurring adult character and
  are checked for face/body/style continuity, dated route, exact place,
  activity/enjoyment, wardrobe, palette, and expression variety. Adult age may
  vary by album or image when the character profile allows it.
- At least two images in a normal daily exploration set should avoid the
  default polished full-outfit display by using lifestyle snapshot or
  partial-detail composition, unless the user asked for a pure fashion-board
  set.
- Each image should have a clear life action before the pose label is chosen,
  and the four actions should not collapse into the same underlying verb such
  as standing, waiting, holding a small object, or simply posing.
- Four primary categories were selected intentionally. Do not default to
  Street / Mode / Night / Resort unless they genuinely fit the day.
- Recent category, garment, pose, crop, and background formulas were checked
  and any repeated formula was avoided or explicitly justified.
- Recent screen grammar was checked separately from metadata: centered solo
  subject, polished three-quarter urban pose, quiet gallery viewing, cafe/bar
  sitting, wet city walk, small prop gesture, and full-body outfit display
  should not become the default visual answer.
- Gaze and attention are balanced. The set should not make all four women look
  at the viewer, and it should not make all four avoid the viewer. Include a
  mix of viewer-aware, social, task/object, place/window, mirror, reflection,
  or path-of-movement attention unless the concept intentionally needs a single
  attention pattern and the log records why.
- Selected `data-style` and `data-category` values exist in the Chat Voyage
  prompt presets when working in that project.
- Effective style variety is visible in the images, not only in metadata.
  Check whether line language, shading, background density, texture, color
  logic, medium, and time/light expression actually differ.
- Shared weather is handled honestly. Rain, overcast, humidity, or heat can
  repeat when they fit the day, but the set should not become four copies of
  the same wet-reflection or overcast cinematic finish.
- Browsing metadata is present and conceptually separated: `data-category`
  remains the legacy slug, while `data-occasion`, `data-venue`,
  `data-activity`, and `data-outfit` describe why the outfit exists, where it
  is, what she is doing, and the garment structure.
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
- Places are concrete and locally characteristic, not generic interiors or
  generic streets with city names attached. Indoor or outdoor both work when
  local atmosphere is visible through light, architecture, materials, weather,
  landscape, objects, or social rhythm.
- No single source, brand look, celebrity outfit, or reference image is reproduced.
- Backgrounds support the outfit context without overpowering the figure.
- No visible text, watermark, logo imitation, or brand mark is requested.
- Poses do not all face the same direction, and the set does not collapse into
  four standing three-quarter views.
- Dynamic travel, vehicle, waterside, stair, pier, bridge, or platform actions
  read as intentional and physically coherent for the place. Risky or balancing
  actions are allowed when they read as the character's choice.
- Logs, notes, album/index references, album-level browsing, and validation are updated when the user
  asks for a reusable Chat Voyage set.

## Final Response Shape

If using `image_gen`, provide the daily header before the image calls:

```text
共通ムード: ...
ラッキーカラー: ...
都市テーマ: ...
カテゴリ: ...
スタイル: ...
実効スタイル: ...
ポーズ方針: ...
```

If web sources were used, include a compact `確認ソース:` line with links before generation. After the image calls, follow the active `imagegen` tool rules for post-generation text.
