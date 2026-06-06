# Daily Fashion Image Template

Use this as the shared prompt scaffold for Chat Voyage daily sets.

## Set Rules

- Generate four separate images, not a collage.
- Subject: adult Japanese woman, original character.
- Select one visual style from `style-presets.md` for the set, or select mixed
  styles when the user asks for style exploration.
- Select style and category candidates with date-seeded randomness unless the
  user explicitly fixes them.
- Select a target age band from `age-presets.md` for each image.
- Select a pose family from `pose-presets.md` for each image before writing
  the outfit prompt.
- Keep visible outfit variety across silhouette, fabric, color, setting, and styling.
- Use date seed, weather or seasonal mood, and light current fashion references as inspiration.
- Keep clothing natural for the city, season, weather, temperature, venue, and
  activity; do not force coverage that makes the person look physically
  uncomfortable.
- Brand names may be used only as loose mood references; do not reproduce logos, readable marks, exact products, or source-photo compositions.

## Category Selection

Select four categories for the daily set from `category-presets.md`. Do not
automatically repeat the same four categories every day.

Use a date-seeded random draw, then adjust for the user's theme. The ordinary
balance is:

- one practical or daytime anchor
- one editorial or high-completion anchor
- one social or nightlife anchor
- one movement, rest, or destination anchor

When the user gives a strong theme, bias the random draw toward that theme but
still preserve visible differences in garment structure, setting, and pose.

Use the selected category slug as each filename prefix. Existing sets using
`street`, `mode`, `night`, and `resort` remain valid historical sets.

## Input Layers

1. Daily direction: date seed, city, weather, seasonal mood, and fashion language.
2. Visual style: choose a style family and exact preset from
   `style-presets.md`, such as `anime-editorial`, `pbr-fashion-3d`,
   `marker-sketch`, or `digital-magazine-painting`.
3. Person direction: target age band from `age-presets.md`, hairstyle, build,
   expression, and character mood.
4. Pose direction: pose family, face direction, body direction, camera angle,
   and hand placement from `pose-presets.md`.
5. Optional person detail: age impression, hairstyle, build, expression, and
   character mood.
6. Optional outfit direction: user image reference, garment list, fabric,
   silhouette, color, or an outfit that must appear in one selected image.

## Prompt Skeleton

```text
Chat Voyage daily fashion set for {YYYY-MM-DD}, Asia/Tokyo date seed.

Today's four selected categories: {choose four slugs from category-presets.md}.
Today's style selection: {one preset for all images, or one preset per image}.
Today's age-band selection: {one target_age_band per image from age-presets.md}.
Today's pose selection: {one pose_family plus face/body/camera direction per image from pose-presets.md}.

Create one image for look {01-04}: {selected category slug}.
Adult Japanese woman, original character, outfit and styling readable, refined styling, expressive but not childish. Full-body is allowed but not required.

Visual style:
- family: {anime | 3d-cg | fashion-illustration | semi-real-digital}
- preset: {exact preset slug from style-presets.md}
- style prompt: {paste the chosen preset text}

Optional person direction:
- target_age_band: {18-19-adult | 20-24 | 25-29}
- {age impression, hairstyle, build, expression, character mood}

Pose direction:
- pose_family: {standing-front | walking-stride | seated-side | leaning-wall | crouching-market | dance-motion | back-three-quarter | over-shoulder | using-object | hands-in-pocket | adjusting-jacket | looking-down}
- face direction: {left | right | camera | down | over-shoulder}
- body direction: {front | left-profile | right-profile | three-quarter | back-three-quarter}
- camera angle: {eye-level | low | high | side | diagonal}
- hand placement: {object interaction, pocket, collar, bag strap, table, railing, free motion}
- crop: {full-body | knee-up | waist-up | close-up-detail | wide-action}

Optional outfit direction:
- {user reference image or garment instructions, or leave open}
- required placement: {which one image must use it, or apply loosely across the set}

Fashion direction:
- mood references: {brand-or-editorial-mood, not exact products}
- season/weather cue: {seasonal cue}
- climate and comfort logic: {temperature, humidity, venue, movement, and why the outfit would be wearable}
- outfit focus: {silhouette, garment types, fabric, color accents}
- setting: {city/gallery/night waterfront/resort terrace/etc.}

Constraints:
- no logos
- no readable brand text
- no exact commercial product copy
- no celebrity or source-photo reproduction
- no school uniforms, sailor-uniform cues, teen-idol styling, childlike faces,
  or implication that the person is a minor
- realistic youthful Japanese adult features are allowed; the problem is
  underage framing, not looking young
- university settings are allowed for adult characters
- exposure is allowed when it is clearly fashion styling, runway, club,
  resort, swim, dance, sheer layering, cutouts, lingerie-inspired layering, or
  evening wear; keep it adult, tasteful, garment-focused, and non-erotic
- do not use high necklines, heavy layers, long sleeves, or closed shoes as a
  default safety fix when they do not fit the climate, venue, or activity
- one complete standalone image, not a collage
- full-body is not mandatory; use knee-up, waist-up, close-up-detail, or
  wide-action crops when they better express pose, garment detail, or mood
- vary pose family, camera angle, face direction, body direction, and hand
  placement across the set; do not let all four images face the same direction
```

## Log / Album Fields

For every final image, record:

- fashion category: selected category slug
- target age band: selected age band from `age-presets.md`
- style family: broad family from `style-presets.md`
- style preset: exact style preset slug
- pose family: selected pose family from `pose-presets.md`
- place: city and scene type
- fashion language: garment structure, materials, color accents, shoes, and accessories
- person language: age impression, hair, build, pose, and expression
- result: accepted, regenerated, or accepted with note
