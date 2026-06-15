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
- Use `prompts/persona-presets.md` so each person reads as bright, sociable,
  lively, fashion-aware, interested in clothes, and intentionally stylish.
- Use date seed, weather or seasonal mood, and light current fashion references as inspiration.
- Keep clothing natural for the city, season, weather, temperature, venue, and
  activity; do not force either coverage or openness when it would make the
  person or outfit feel physically uncomfortable.
- Before prompting, compare the last three to five recent sets and avoid
  repeating their category, pose, garment, background, crop, and lucky-color
  placement formulas unless the repeat is intentional and logged.
- Climate-natural clothing must be decided from city, season, time of day,
  weather, temperature band, humidity, indoor/outdoor conditions, wind or air
  conditioning, rain intensity, venue norms, and activity. Do not default to
  tanks, camisoles, open shirts, mesh, and sandals only because the weather is
  warm or humid.
- Do not treat normal warm-weather garments as failed variety. Tanks, open
  shirts, skorts, miniskirts, shorts, sandals, and bare legs can repeat when
  the full styling formula, place, pose, footwear or legwear, and fashion
  attitude are different.
- Treat indoor scenes broadly. Indoor does not mean only rooms, offices,
  meals, cafes, or bars; it can also mean locally specific activity spaces such
  as museums, art museums, galleries, clubs, live houses, theaters, cinemas,
  libraries, ateliers, sports facilities, public halls, stations, markets, or
  covered arcades. Choose places that are characteristic of the city or region
  rather than generic interiors.
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

1. Daily direction: date seed, city, weather, seasonal mood, place language,
   and fashion language. Place language should include concrete local settings,
   including locally specific indoor or activity spaces when they fit the day.
2. Visual style: choose a style family and exact preset from
   `style-presets.md`, such as `anime-editorial`, `pbr-fashion-3d`,
   `marker-sketch`, or `digital-magazine-painting`.
3. Person direction: target age band from `age-presets.md`, hairstyle, build,
   expression, character mood, life scene, silhouette logic, material logic,
   accessory logic, persona direction, and fashion focal point.
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
- persona: bright, sociable, lively, fashion-aware, interested in styling,
  aware of her own charm without erotic framing
- fashion focal point: {color | accessory | fabric | silhouette | shoes | bag | hair accessory | jewelry | layering | fabric movement}
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
- climate and comfort logic: {city, season, time of day, weather, temperature band, humidity, indoor/outdoor, wind or air conditioning, rain intensity, venue norms, movement, and why the outfit would be wearable}
- age-band life scene: {adult life context for this age band}
- age-band silhouette/material/accessory logic: {what differs by age beyond color tone}
- persona direction: {how brightness, sociability, confidence, and fashion interest show up}
- fashion focal point: {one or two distinctive styling details, not everything loud at once}
- avoid recent formula: {recent repeated full formula this image does not use;
  do not ban ordinary garments by themselves}
- outfit focus: {silhouette, garment types, fabric, color accents}
- legwear and footwear: {bare legs | sheer socks | slouch socks | knee socks |
  tights | leggings | bike shorts | sandals | loafers | pumps | sneakers |
  boots; chosen as styling, not only coverage}
- setting: {specific city place; include locally characteristic indoor or
  activity spaces such as museum, art museum, club, theater, library, atelier,
  station, market hall, covered arcade, sports facility, cafe, bar, room,
  workplace, restaurant, terrace, or street when appropriate}

Constraints:
- no logos
- no readable brand text
- no exact commercial product copy
- no celebrity or source-photo reproduction
- no blank mannequin expression; the person should show adult social energy,
  fashion interest, and intentional styling
- no school uniforms, sailor-uniform cues, teen-idol styling, childlike faces,
  or implication that the person is a minor
- realistic youthful Japanese adult features are allowed; the problem is
  underage framing, not looking young
- university settings are allowed for adult characters
- skin visibility is not a problem by itself; judge whether neckline, sleeve,
  hem, fabric, footwear, and layering are natural for the city, venue, weather,
  age band, and activity
- indoor settings should be concrete local places, not only generic rooms,
  offices, meals, cafes, or bars; museums, art museums, clubs, live houses,
  theaters, libraries, ateliers, sports facilities, public halls, stations,
  markets, and covered arcades can be used when characteristic of the city
- do not use high necklines, heavy layers, long sleeves, or closed shoes as a
  default guardrail fix when they do not fit the climate, venue, or activity
- do not use tanks, camisoles, open shirts, mesh, or sandals as a default
  climate fix when the city, time, rain, venue, air conditioning, or activity
  would support another natural silhouette
- do not suppress miniskirts, short skorts, bare legs, socks, tights, sandals,
  or open tops only because they show skin; accept or reject them based on
  adult styling, garment construction, climate, venue, pose, and activity
- do not repeat the recent successful formulas with only a city or lucky-color
  change
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
- place: city and specific local scene type, including any locally distinctive
  indoor/activity space when relevant
- climate context: city, season, time, weather, humidity, venue, and activity
- age-band life scene and silhouette logic
- persona direction and fashion focal point
- avoid recent formula
- fashion language: garment structure, materials, color accents, shoes,
  legwear, and accessories
- person language: age impression, hair, build, pose, and expression
- result: accepted, regenerated, or accepted with note
