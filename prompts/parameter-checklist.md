# Daily Fashion Parameter Checklist

Use this before writing image prompts and again when recording the final set.
It is the compact parameter map for Chat Voyage daily fashion generation.

## Required Before Generation

```text
date_seed: YYYY-MM-DD, usually Asia/Tokyo
theme: daily theme or short concept
city: primary city
place_language: four scene/place directions, one per image when possible
common_mood: one subtle shared mood
lucky_color: one shared color, varied by placement and intensity
lucky_color_age_tone: how the same lucky color shifts by age band
climate_fit: weather, temperature, humidity, venue, and activity comfort notes
fashion_category: four slugs from prompts/category-presets.md
style_preset: one shared slug or four slugs from prompts/style-presets.md
style_family: family for each selected style preset
target_age_band: four values from prompts/age-presets.md
persona_direction: bright, sociable, lively, fashion-aware, fashion-interested adult charm direction from prompts/persona-presets.md
pose_family: four values from prompts/pose-presets.md
face_direction: one per image
body_direction: one per image
camera_angle: one per image
hand_placement: one per image
crop: one per image
movement_readability: for dynamic, vehicle, waterside, stair, or platform scenes, what the person is doing and why it reads as safe and normal
person_language: adult character notes, varied across all four images
fashion_language: garment structure, silhouette, material, shoes, legwear, accessories
fashion_focal_point: one or two distinctive styling details per image
exposure_plan: covered, moderate, open, or layered exposure balance for each image
comfort_naturalness: why the outfit is plausible for the weather, place, and activity
variation_axes: what differs across the four images beyond color
avoid_rules: no logos, readable brand text, exact product/source-photo copy, celebrity copy, school-uniform cues, teen-idol styling, childlike framing
source_notes: local references read, missing references, and web/source links when used
recent_set_scan: last three to five sets checked for repeated category, pose, garment, background, and crop formulas
cooldown_formulas: recent formulas that should be avoided or explicitly justified
category_rotation_reason: why the selected categories are not repeating the recent default pattern
prompt_version: prompt workflow version, such as v1-full-detail or v2-short-generation
prompt_shape: how much detail went into the image prompt versus the log
save_path: assets/daily/YYYY-MM-DD-theme/
```

## Per-Image Prompt Parameters

Each of the four image prompts should make these explicit:

```text
image_number: 01-04
primary_category: category slug
target_age_band: age band
style_family: broad style family
style_preset: exact style preset slug
person_language: age impression, hairstyle, build, expression, adult context
persona_direction: how brightness, sociability, self-awareness, and fashion interest appear
pose_language: pose family, face direction, body direction, camera angle, hand placement, crop
movement_readability: clear action and safety logic, especially for boats, ferries, trains, buses, stations, stairs, platforms, piers, bridges, and water edges
scene_language: city, place, time/weather, background support
fashion_language: garment list, construction, materials, texture, proportion, shoes, legwear, accessories
fashion_focal_point: chosen styling point such as color, accessory, fabric, silhouette, shoes, bag, jewelry, hair accessory, layering, or fabric movement
lucky_color_use: where the daily lucky color appears
lucky_color_tone_for_age: brightness, saturation, material, and placement for the selected age band
exposure_balance: how skin, sheer layers, hem length, neckline, sleeve, or cutout choices support the category without erotic framing
comfort_naturalness: breathable fabric, seasonal weight, movement, footwear, and layering logic
climate_context: city, season, weather, temperature band, humidity, time of day, indoor/outdoor, wind or air conditioning, rain intensity, venue norms, and activity
age_band_life_scene: what this age band is doing in adult life, not only how old she looks
age_band_silhouette: how the silhouette differs from the other age bands and recent sets
age_band_material_logic: why the material choice fits this age band, scene, and climate
age_band_accessory_logic: how shoes, bag, jewelry, eyewear, umbrella, or object use differs by age band
avoid_recent_formula: one recent successful formula this image intentionally does not repeat
source_mood_tags: broad influence tags, never exact copying
constraints: safety, originality, no text/logo, one standalone image, not a collage
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
common_mood
lucky_color
lucky_color_age_tone
climate_fit
categories
age_bands
persona_direction
exposure_plan
pose_families
style_presets
source_scan_or_missing_reference_note
recent_set_scan
cooldown_formulas
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
  secondary_tags
  place
  person_language
  persona_direction
  fashion_language
  fashion_focal_point
  lucky_color_tone_for_age
  exposure_balance
  comfort_naturalness
  climate_context
  age_band_life_scene
  age_band_silhouette
  avoid_recent_formula
  pose_family
  movement_readability
  generated_prompt_summary
  visual_check
  result_note
```

Record these in `index.html`:

```text
data-style: exact style preset slug
data-place: existing place filter slug, or add a filter button first
data-category: exact category slug from prompts/category-presets.md
image_src
alt_text
caption_title
caption_tags
notes_link
album_link
```

Record these in `notes/YYYY-MM-DD-theme.md`:

```text
date_seed
city
theme
common_mood
lucky_color
lucky_color_age_tone
climate_fit
selected_categories
age_bands
persona_direction
exposure_plan
pose_families
movement_readability_notes
style_presets
saved_path
one-line result for each final image
quality or exception notes
prompt_version and any generation stability notes
recent-set repetition notes and any intentional repeats
```

## Acceptance Check

- Four separate images exist under the project save path.
- The four people are visibly different adults.
- Each person reads as bright, sociable, lively, fashion-aware, interested in
  clothes, and intentionally stylish, with adult charm expressed through
  posture, expression, gesture, outfit completion, color, fabric, silhouette,
  accessories, or scene behavior rather than erotic framing.
- Each image has one or two clear fashion focal points, such as accessory,
  fabric, silhouette, color placement, shoes, bag, jewelry, hair accessory,
  layering, or fabric movement.
- Category, style, age, pose, and crop choices match preset vocabulary.
- The set varies silhouette, garment construction, material, shoes or legwear,
  exposure balance, setting, pose, and camera direction.
- The lucky color appears in all four images without becoming a simple color
  swap.
- The lucky color tone changes by target age band, not only by placement. For
  example, younger adult looks may use fresher or clearer tones, while late-20s
  looks may use deeper, dustier, glossier, or more restrained tones when the
  category calls for it.
- The age bands differ by life scene, silhouette, materials, accessories, and
  styling attitude, not only by color tone or face age.
- Dynamic actions are readable and safe for the setting. Vehicle, ferry,
  waterside, stair, platform, pier, bridge, and station scenes must not look
  like jumping off, falling, running out of a vehicle, or leaving a safe
  surface.
- Exposure balance is intentionally varied across the set. Do not let rainy,
  outerwear, or low-key themes collapse all looks into long, covered layers;
  use tasteful adult fashion exposure such as sleeveless cuts, open backs,
  sheer layering, shorter hems, waist detail, sandals, or dance/resort/night
  construction when appropriate.
- Outfit coverage must feel natural for the climate and activity. Do not force
  high necklines, heavy layers, long sleeves, or closed shoes just to reduce
  exposure; choose breathable adult fashion that fits the city, season,
  temperature, venue, and movement.
- Climate naturalness is specific to city, season, time of day, weather,
  temperature band, humidity, rain intensity, indoor/outdoor conditions, wind
  or air conditioning, venue norms, and activity. It must not default to the
  same warm-weather tank/camisole/open-shirt/mesh/sandal formula.
- Recent successful formulas from the last three to five sets are not repeated
  without a logged reason. Check category sequence, pose sequence, garment
  formula, background formula, crop, and lucky-color placement.
- No image depends on a copied source look, readable logo, brand mark, or
  celebrity likeness.
- The log records the prompt workflow version. If using
  `v2-short-generation`, the log also records the prompt summary and visual
  check for each final image, including the anti-repeat instruction.
- `python3 scripts/validate_gallery.py` reports `errors: 0`.
