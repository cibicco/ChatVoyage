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
fashion_category: four slugs from prompts/category-presets.md
style_preset: one shared slug or four slugs from prompts/style-presets.md
style_family: family for each selected style preset
target_age_band: four values from prompts/age-presets.md
pose_family: four values from prompts/pose-presets.md
face_direction: one per image
body_direction: one per image
camera_angle: one per image
hand_placement: one per image
crop: one per image
person_language: adult character notes, varied across all four images
fashion_language: garment structure, silhouette, material, shoes, legwear, accessories
variation_axes: what differs across the four images beyond color
avoid_rules: no logos, readable brand text, exact product/source-photo copy, celebrity copy, school-uniform cues, teen-idol styling, childlike framing
source_notes: local references read, missing references, and web/source links when used
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
pose_language: pose family, face direction, body direction, camera angle, hand placement, crop
scene_language: city, place, time/weather, background support
fashion_language: garment list, construction, materials, texture, proportion, shoes, legwear, accessories
lucky_color_use: where the daily lucky color appears
source_mood_tags: broad influence tags, never exact copying
constraints: safety, originality, no text/logo, one standalone image, not a collage
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
categories
age_bands
pose_families
style_presets
source_scan_or_missing_reference_note
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
  fashion_language
  pose_family
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
selected_categories
age_bands
pose_families
style_presets
saved_path
one-line result for each final image
quality or exception notes
```

## Acceptance Check

- Four separate images exist under the project save path.
- The four people are visibly different adults.
- Category, style, age, pose, and crop choices match preset vocabulary.
- The set varies silhouette, garment construction, material, shoes or legwear,
  exposure balance, setting, pose, and camera direction.
- The lucky color appears in all four images without becoming a simple color
  swap.
- No image depends on a copied source look, readable logo, brand mark, or
  celebrity likeness.
- `python3 scripts/validate_gallery.py` reports `errors: 0`.
