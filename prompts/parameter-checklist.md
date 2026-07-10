# Daily Fashion Parameter Checklist

Use this before writing image prompts and again when recording the final set.
It is the compact parameter map for Chat Voyage daily fashion generation.

## Required Before Generation

```text
date_seed: YYYY-MM-DD, usually Asia/Tokyo
theme: daily theme or short concept
city: primary city
place_language: four concrete scene/place directions, one per image when possible; choose places where local atmosphere is visible, whether indoor or outdoor; include cafes, workshops, night bars, pools, beaches, mountains, cultural facilities, markets, stations, terraces, studios, streets, and locally specific indoor or activity spaces when relevant, not generic rooms with a city name attached
common_mood: one subtle shared mood
lucky_color: one shared color, varied by placement and intensity
lucky_color_age_tone: how the same lucky color shifts by age band
climate_fit: weather, temperature, humidity, venue, and activity comfort notes
local_activity_space_plan: how the set uses city- or region-specific places whose atmosphere can be seen, including cafes, workshops, night bars, pools, beaches, mountains, cultural facilities, museums, galleries, clubs, live houses, theaters, cinemas, libraries, ateliers, sports facilities, public halls, stations, markets, covered arcades, workspaces, restaurants, terraces, or streets as appropriate
lifestyle_snapshot_plan: which images are fashion-editorial views and which are candid life snapshots; for normal daily exploration, make at least two of four images feel like a woman's lived moment where the outfit is naturally visible, not a pose staged only to show the full outfit
character_album_mode: `normal-daily` or `character-day`; character day albums show a specific recurring character going to places and enjoying a dated story day
character_slug: recurring character slug; leave blank for normal daily exploration
character_profile: character prompt profile read before generation; leave blank for normal daily exploration
character_age_plan: for character day albums, chosen adult age or adult age band; age may vary by album/date, but face/body continuity must stay stable
character_identity_continuity_plan: for character day albums, what keeps the face, body proportions, posture, gaze, hair, and objects recognizably the same character
character_visual_style_anchor: for character day albums, the visual style or reference look that keeps the image in that character's illustration language
story_day_summary: for character day albums, one sentence for what kind of day this is for the character
character_route_plan: for character day albums, ordered route across places or story beats
exact_place_plan: for character day albums, city and specific named places; use real names when the album is in a real city, not vague "something-style" placeholders
activity_enjoyment_plan: for character day albums, what the character does, enjoys, notices, or shares in each place
palette_role_plan: for character day albums, per-image role of dark colors such as dominant, base, accent, workwear utility, nightwear, or absent
fashion_category: four slugs from prompts/category-presets.md
style_preset: one shared slug or four slugs from prompts/style-presets.md
style_family: family for each selected style preset
effective_style_variant: visible rendering target per image, such as anime-cel-clean, anime-tv-slice-of-life, anime-manga-ink, anime-watercolor-soft, anime-90s-ova, marker-sketch, watercolor-couture, semi-real-editorial, or true 3D
style_execution_plan: how line language, shading, background density, texture, color logic, and time/light expression differ across the four images
time_weather_rendering_plan: if weather repeats or belongs to the day, how time of day, rain intensity, indoor/outdoor condition, light source, composition, and medium keep the set varied without changing the weather unrealistically
effective_style_recent_scan: last three to five sets checked for repeated visual finish, not only style_preset slugs
effective_style_cooldowns: recent finishes to avoid, such as high-density semi-real rain painting, glossy fashion-magazine anime, wet-reflection street default, or dense cinematic bokeh
target_age_band: four values from prompts/age-presets.md
persona_direction: selected adult life-and-trait direction from prompts/persona-presets.md, anchored in agency, fashion awareness, comfort, context, and presentation
persona_traits: two to five traits per image, such as personable, sociable, sensual, bright, quiet, practical, daring, relaxed, elegant, playful, reserved, or self-possessed
action_first_pose_plan: one concrete life-action verb phrase per image before selecting pose labels, such as walking while responding, floor warm-up, rooftop pause, home dressing, packing, greeting, carrying, repairing, practicing, waiting, or returning home
pose_family: four values from prompts/pose-presets.md
face_direction: one per image
attention_target: one per image, such as viewer, near-camera, another person, task/object, place/window, path of movement, mirror, or reflection
attention_mix_plan: how the four-image set avoids both all-camera-contact and all-camera-avoidance; include at least one viewer-aware or social gaze unless the concept intentionally needs solitude
body_direction: one per image
camera_angle: one per image
hand_placement: one per image
crop: one per image
movement_readability: for dynamic, vehicle, waterside, stair, bridge, or platform scenes, what the person is doing, where her weight is, and whether any risk is intentional
person_language: adult character notes, varied across all four images
fashion_language: garment structure, silhouette, material, shoes, legwear, accessories
fashion_focal_point: one or two distinctive styling details per image
skin_coverage_comfort_plan: how neckline, sleeve, hem, skin visibility, airflow, fabric weight, and layering fit the scene without forcing either coverage or openness
hem_legwear_footwear_plan: how hem length, bare legs or legwear, and shoes vary as fashion styling rather than as a modesty correction
short_sheer_sock_drift_check: whether short transparent ankle socks or short sheer socks have appeared too often in recent sets; if yes, rotate to bare legs, opaque/ribbed/slouch/sport/lace socks, knee-highs, stockings, tights, fishnets, mesh knee-highs, leggings, or no hosiery
comfort_naturalness: why the outfit is plausible for the weather, place, and activity
variation_axes: what differs across the four images beyond color
composition_variation_axes: how framing and screen grammar differ, such as centered versus off-center subject, full body versus partial body, face-visible versus face-optional, front view versus back/side/mirror/reflection, single-person portrait versus other people implied, and posed fashion view versus candid life action
avoid_rules: no logos, readable brand text, exact product/source-photo copy, celebrity copy, school-uniform cues, teen-idol styling, childlike framing
source_notes: local references read, missing references, and web/source links when used
recent_set_scan: last three to five sets checked for repeated category, pose, garment, background, and crop formulas
cooldown_formulas: recent formulas that should be avoided or explicitly justified
category_rotation_reason: why the selected categories are not repeating the recent default pattern
prompt_version: prompt workflow version, such as v1-full-detail or v2-short-generation
prompt_shape: how much detail went into the image prompt versus the log
save_path: assets/albums/daily/YYYY/MM/YYYY-MM-DD-theme/ or assets/albums/characters/<character>/YYYY/MM/YYYY-MM-DD-theme/
```

## Per-Image Prompt Parameters

Each of the four image prompts should make these explicit:

```text
image_number: 01-04
primary_category: category slug
target_age_band: age band
character_age: for character day albums, chosen adult age or age band for this image; it may vary, but should not break face/body continuity
style_family: broad style family
style_preset: exact style preset slug
effective_style_variant: the visible style execution target, especially for anime substyles
style_execution: line language, shading type, background density, texture, color logic, and time/light expression
time_weather_rendering: true weather if relevant, plus time of day, rain/sun/wind intensity, indoor/outdoor condition, light source, and medium
person_language: age impression, hairstyle, build, expression, adult context
persona_direction: how the selected traits, agency, self-awareness, comfort, boundaries, social context, and fashion interest appear
persona_traits: the selected trait mix for this image
life_action: the concrete action she is doing before pose labels are chosen; the action should belong to her day and make the outfit naturally visible
pose_language: pose family, face direction, body direction, camera angle, hand placement, crop
attention_target: whether she is looking at the viewer, near camera, another person, task/object, place/window, path of movement, mirror, or reflection
movement_readability: clear action, weight, intention, and optional chosen risk, especially for boats, ferries, trains, buses, stations, stairs, platforms, piers, bridges, and water edges
scene_language: city, specific named place, time/weather, and background support; choose a place where local atmosphere is legible through architecture, light, weather, landscape, materials, objects, or social activity, not a generic room or cafe with the city name attached, and not vague "something-style" language when a real place is intended
snapshot_mode: fashion-editorial, lifestyle-snapshot, work-or-making, relationship-moment, transit-errand, home-life, or partial-detail; when using lifestyle-snapshot or partial-detail, full outfit, face, front view, and centered composition are not required if the clothing appears naturally in the moment
fashion_language: garment list, construction, materials, texture, proportion, hem length, shoes, legwear, accessories
fashion_focal_point: chosen styling point such as color, accessory, fabric, silhouette, shoes, bag, jewelry, hair accessory, layering, or fabric movement
lucky_color_use: where the daily lucky color appears
lucky_color_tone_for_age: brightness, saturation, material, and placement for the selected age band
skin_coverage_comfort: how skin visibility, sheer layers, hem length, neckline, sleeve, or cutout choices feel natural for the category, climate, venue, and action; do not use skin amount as a pass/fail proxy
hem_legwear_footwear: mini, midi, trousers, shorts, skort, bare legs, sheer or opaque socks, ribbed/slouch/sport/lace socks, knee-highs, stockings, patterned or opaque tights, fishnets, mesh knee-highs, leggings, bike shorts, sandals, pumps, sneakers, boots, or other leg styling chosen for fashion language and activity
comfort_naturalness: breathable fabric, seasonal weight, movement, footwear, and layering logic
climate_context: city, season, weather, temperature band, humidity, time of day, indoor/outdoor, wind or air conditioning, rain intensity, venue norms, local activity space, and activity
age_band_life_scene: what this age band is doing in adult life, not only how old she looks
age_band_silhouette: how the silhouette differs from the other age bands and recent sets
age_band_material_logic: why the material choice fits this age band, scene, and climate
age_band_accessory_logic: how shoes, bag, jewelry, eyewear, umbrella, or object use differs by age band
avoid_recent_formula: one recent successful formula this image intentionally does not repeat
avoid_recent_screen_grammar: one recent composition habit this image avoids, such as centered three-quarter standing, quiet solo gallery viewing, cafe/bar sitting, small object pose, wet city walk, or full-body outfit display
avoid_recent_effective_style: one recent visual finish this image avoids, such as glossy editorial anime, dense semi-real wet street painting, or marker/watercolor treatment if recently repeated
source_mood_tags: broad influence tags, never exact copying
constraints: originality, no text/logo, adult character, coherent action, one standalone image, not a collage
generated_prompt_summary: compact summary of the prompt actually sent
```

## Required After Generation

Record these in `logs/generation-YYYY-MM.md`:

```text
generated_on
image_count
saved_in
album
note
city_place_language
local_activity_space_plan
common_mood
lucky_color
lucky_color_age_tone
climate_fit
categories
age_bands
persona_direction
skin_coverage_comfort_plan
action_first_pose_plan
pose_families
attention_mix_plan
style_presets
effective_style_variant
style_execution_plan
time_weather_rendering_plan
source_scan_or_missing_reference_note
recent_set_scan
effective_style_recent_scan
character_album_mode
character_slug
character_profile
character_age_plan
character_identity_continuity_plan
character_visual_style_anchor
story_day_summary
character_route_plan
exact_place_plan
activity_enjoyment_plan
palette_role_plan
cooldown_formulas
effective_style_cooldowns
screen_grammar_cooldowns
hem_legwear_footwear_plan
composition_variation_axes
lifestyle_snapshot_plan
category_rotation_reason
prompt_version
prompt_shape
final_files:
  filename
  source_file
  primary_category
  target_age_band
  style_family
  style_preset
  effective_style_variant
  style_execution_check
  time_weather_rendering_check
  secondary_tags
  place
  person_language
  persona_direction
  persona_traits
  life_action
  fashion_language
  fashion_focal_point
  lucky_color_tone_for_age
  skin_coverage_comfort
  hem_legwear_footwear
  comfort_naturalness
  climate_context
  age_band_life_scene
  age_band_silhouette
  avoid_recent_formula
  avoid_recent_screen_grammar
  avoid_recent_effective_style
  action_first_pose_check
  pose_family
  attention_target
  attention_mix_check
  snapshot_mode
  movement_readability
  generated_prompt_summary
  visual_check
  result_note
```

Record these in the album JSON under `data/albums/**/*.json`:

```text
collection: `character` for character day albums, otherwise `daily`
character: recurring character slug such as `shino`; omit for normal daily exploration
notesHref
summaryJa
preferredAspectRatio: intended album generation ratio, usually `2:3` portrait or `3:2` landscape
image_src
alt_text
caption_title
caption_tags
style: exact style preset slug
place: existing place filter slug
category: exact category slug from prompts/category-presets.md
occasion
venue
locationDetail: concrete place/detail for UI display, not city-only or action prose
activity
outfit
```

Do not hand-write `width`, `height`, or image-level `aspectRatio`; run
`python3 scripts/enrich_album_source_metadata.py` after image files and JSON
paths are in place.

Record these in the human note under `notes/albums/.../YYYY-MM-DD-theme.md`:

```text
date_seed
city
theme
common_mood
lucky_color
lucky_color_age_tone
climate_fit
selected_categories
character_album_mode
character_slug
character_profile
story_day_summary
character_route_plan
activity_enjoyment_plan
palette_role_plan
age_bands
persona_direction
skin_coverage_comfort_plan
action_first_pose_plan
pose_families
attention_mix_plan
movement_readability_notes
style_presets
effective_style_variant
style_execution_plan
time_weather_rendering_plan
saved_path
one-line result for each final image
quality or exception notes
prompt_version and any generation stability notes
recent-set repetition notes and any intentional repeats
```

## Acceptance Check

- Four separate images exist under the project save path, unless the fixed
  character story explicitly uses a different count and records it.
- Normal daily exploration sets have visibly different adults. Character day
  albums intentionally keep the same adult character and instead check
  face/body/style continuity, adult age fit, dated route, exact place use,
  activity/enjoyment variety, palette drift, and scene variety.
- Each person reads as fashion-aware, interested in clothes, and intentionally
  stylish, with a selected adult trait mix such as personable, sociable,
  sensual, bright, quiet, practical, daring, relaxed, elegant, playful,
  reserved, or self-possessed. Adult presentation is expressed through
  posture, expression, gesture, outfit completion, color, fabric, silhouette,
  accessories, context, or scene behavior rather than automatic erotic framing
  or automatic sanitizing.
- Each image has one or two clear fashion focal points, such as accessory,
  fabric, silhouette, color placement, shoes, bag, jewelry, hair accessory,
  layering, or fabric movement.
- Hem, legwear, and footwear are active styling choices. The set should not
  accidentally suppress miniskirts, skorts, bare legs, socks, tights, sandals,
  pumps, boots, or other leg styling because of skin-visibility caution.
- Category, style, age, pose, and crop choices match preset vocabulary.
- Style variety is visible in the image, not only in metadata. When two images
  share a family, they should differ through line language, shading, background
  density, texture, color logic, time/light expression, or medium.
- Same weather is acceptable when it fits the date or city, but the set should
  avoid four copies of the same wet-street or overcast visual finish. Vary time
  of day, rain intensity, indoor/outdoor condition, light source, composition,
  background density, or rendering medium.
- The set varies silhouette, garment construction, material, shoes or legwear,
  exposure balance, setting, pose, and camera direction.
- The set varies screen grammar as well as clothing. For normal daily
  exploration, at least two images should be lifestyle snapshots or
  lived-moment compositions rather than full-outfit fashion displays, unless
  the user asks for a pure fashion-board set.
- The set uses action-first pose planning. Each image should have a clear life
  action before the pose label is chosen, and the four actions should not all
  collapse into the same underlying verb such as standing, waiting, holding a
  small object, or simply posing.
- The set balances gaze and attention direction. Avoid both all four people
  looking at the viewer and all four people avoiding the viewer. Use a mix of
  viewer-aware, social, task/object, place/window, mirror, path-of-movement, or
  reflection attention.
- Full body, front view, visible face, and centered composition are not quality
  requirements by themselves. Back views, partial body crops, hands, legs,
  mirrors, reflections, windows, off-center framing, and clothes in motion can
  all be accepted when they support the woman's life moment and the outfit is
  naturally visible.
- At least one image should show a life action beyond posing or simply holding
  a small prop: making, repairing, preparing, carrying, folding, waiting,
  greeting, reacting, moving through weather, working, practicing, shopping
  with intent, or interacting with another person's presence.
- The lucky color appears in all four images without becoming a simple color
  swap.
- The lucky color tone changes by target age band, not only by placement. For
  example, younger adult looks may use fresher or clearer tones, while late-20s
  looks may use deeper, dustier, glossier, or more restrained tones when the
  category calls for it.
- The age bands differ by life scene, silhouette, materials, accessories, and
  styling attitude, not only by color tone or face age.
- Places are concrete and locally characteristic. Indoor or outdoor is
  secondary; cafes, workspaces, night bars, pools, beaches, mountains, cultural
  facilities, markets, stations, terraces, studios, and streets are all valid
  when the local atmosphere is visible. Indoor scenes are not limited to
  ordinary rooms, work, meals, cafes, or bars; they can include museums, art
  museums, galleries, clubs, live houses, theaters, cinemas, libraries,
  ateliers, sports facilities, public halls, stations, markets, or covered
  arcades when those spaces fit the city, time, and category.
- Dynamic actions are readable and intentional for the setting. Risky or
  balancing actions are allowed when they are clearly chosen by the character:
  the image should show what she is doing, where her weight is, and why the
  action fits the scene. Avoid only unintended ambiguity such as accidental
  falling, unexplained leaping away from a vehicle, or unclear body mechanics.
- Skin visibility and coverage are intentionally varied across the set because
  garment construction, climate, and activity vary. Do not let rainy, outerwear,
  or low-key themes collapse all looks into long, covered layers, and do not
  force openness where the venue or activity would make it unnatural.
- Clothing openness or coverage is not justified by youth, liveliness,
  sensuality, or modesty alone. Judge it as part of human life: weather,
  comfort, movement, place, social context, taste, work, rest, play, travel,
  ceremony, and the person's own presentation.
- Outfit coverage must feel natural for the climate and activity. Do not force
  high necklines, heavy layers, long sleeves, or closed shoes just to reduce
  visible skin; choose breathable adult fashion that fits the city, season,
  temperature, venue, and movement.
- Climate naturalness is specific to city, season, time of day, weather,
  temperature band, humidity, rain intensity, indoor/outdoor conditions, wind
  or air conditioning, venue norms, and activity. It must not default to the
  same warm-weather tank/camisole/open-shirt/mesh/sandal formula.
- Recent successful full formulas from the last three to five sets are not
  repeated without a logged reason. Check category sequence, pose sequence,
  garment stack, shoes and legwear, background formula, crop, and lucky-color
  placement. Do not ban a normal garment category by itself.
- Recent effective visual finishes from the last three to five sets are not
  repeated without a logged reason. Check whether the final image looks like
  the same anime gloss, semi-real rain painting, marker sketch, watercolor wash,
  dense background, or night bokeh pattern despite different metadata.
- Recent-set novelty checks separate character day albums from normal daily
  exploration. Character albums should be reviewed against the same character's
  recent route, activity, place, wardrobe, object, and expression patterns; they
  should not inflate or distort the novelty analysis for unrelated daily
  exploration sets.
- Screen-grammar repeats are checked separately from metadata. Even when city,
  category, and outfit differ, reject or document repeats of the same visual
  pattern such as a centered solo woman in a polished urban background, quiet
  gallery viewing, seated lounge pose, cafe/bar moment, or full-body
  three-quarter fashion display.
- No image depends on a copied source look, readable logo, brand mark, or
  celebrity likeness.
- The log records the prompt workflow version. If using
  `v2-short-generation`, the log also records the prompt summary and visual
  check for each final image, including the anti-repeat instruction.
- `python3 scripts/validate_gallery.py` reports `errors: 0`.
