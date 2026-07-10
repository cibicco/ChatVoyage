# Chat Voyage Style Presets

Choose one or more visual styles for each daily set. Keep the style choice
separate from the daily theme, person, and outfit instructions.

Daily style selection should be date-seeded, not habitual. A daily set may use
one shared style for all four images or mix two to four styles when the user
asks for comparison, album diversity, or style exploration.

Record both the broad family and the exact preset in logs and albums:

```text
style_family: anime | 3d-cg | fashion-illustration | semi-real-digital
style_preset: anime-editorial | pbr-fashion-3d | ...
```

## Selection Pools

Use these pools for random or date-seeded selection. Avoid repeating the same
family more than two daily sets in a row unless the user requests it.

- Anime family: `anime-editorial`, `anime-cel-polished`, `anime-soft-cinematic`, `anime-fashion-magazine`, `anime-cel-clean`, `anime-tv-slice-of-life`, `anime-manga-ink`, `anime-90s-ova`, `anime-watercolor-soft`, `anime-pop-graphic`, `anime-lofi-sketch`, `anime-cinematic-night`, `anime-comic-panel`
- 3D CG family: `3d-cg-fashion`, `pbr-fashion-3d`, `game-cinematic-3d`, `doll-like-3d`
- Fashion illustration family: `fashion-illustration`, `runway-board-illustration`, `marker-sketch`, `watercolor-couture`
- Semi-real digital family: `semi-real-editorial`, `digital-magazine-painting`, `soft-real-fashion-art`

## Effective Style Controls

Do not rely on `style_preset` names alone. Before generation, choose an
`effective_style_variant` and make the visible rendering differences explicit:

- line language: thick contour, thin contour, sketch line, manga ink, no line,
  construction line, or painterly edge
- shading: flat cel, two-step cel, soft gradient, marker blocks, watercolor
  wash, graphite value, or digital paint
- background density: blank paper, minimal props, simplified local setting,
  detailed local setting, cinematic scene, or full environmental painting
- texture: clean digital, paper grain, marker bleed, watercolor bloom, screen
  tone, pencil, or PBR material
- color logic: flat poster color, muted slice-of-life palette, high-contrast
  night color, limited monochrome, soft wash, or glossy editorial color
- time/light expression: morning flat light, overcast diffuse light, indoor
  lamp pools, night neon, rainy reflection, or dry interior with weather
  hinted outside

Weather can stay the same across a daily set. If the day is rainy, do not
invent sun only for variety. Instead vary the time of day, rain intensity,
indoor/outdoor condition, light source, background density, and rendering
medium. A rainy set can include morning after-rain cel anime, pale afternoon
watercolor drizzle, a dry indoor marker sketch with rain hinted outside, and a
semi-real wet street threshold without feeling repetitive.

If two images use the same family, their effective styles must still differ in
at least three visible axes, such as line language, shading, background
density, texture, and time/light expression.

## Anime Effective Variants

Use these when selecting anime styles. They are stable style slugs and can be
recorded as `style_preset` when the image should be browsed by that exact
anime look. If compatibility needs an older preset, record the older preset in
`data-style` and record this value as `effective_style_variant` in logs.

## `3d-cg-fashion`

Use when the user asks for 3D. This means a finished 3D CG render, not
"3D-like" illustration.

```text
True stylized 3D CG fashion render. High-end CG character, physically based
fabric shaders, visible garment thickness, detailed knit and textile materials,
ray-traced reflections, cinematic depth of field, polished fashion-editorial
lighting. Not a drawing, not a watercolor, not a sketch, not flat anime line
art, and not a real photo.
```

## `pbr-fashion-3d`

```text
True 3D CG fashion render with physically based materials, realistic fabric
roughness, stitched seams, garment thickness, accurate reflections, and
high-end product-editorial lighting. Keep the character stylized and original;
do not make it look like a real photograph.
```

## `game-cinematic-3d`

```text
Stylized 3D game-cinematic fashion character. Strong silhouette, dramatic
scene lighting, detailed accessories, readable garment layers, and dynamic
camera angle. Not flat anime art, not watercolor, and not a real photo.
```

## `doll-like-3d`

```text
Polished doll-like 3D fashion character with smooth stylized features,
carefully modeled hair, tactile fabric surfaces, and boutique lookbook
lighting. Keep adult proportions and fashion readability.
```

## `anime-editorial`

```text
High-definition anime fashion illustration. Crisp refined linework, controlled
cel shading, detailed garment textures, polished character design, and
fashion-editorial composition. Not a 3D render and not a real photo.
```

## `anime-cel-clean`

```text
Clean flat cel-anime fashion image. Strong readable contour lines, flat color
blocks, simple two-step shadows, minimal gradients, simplified but local
background, and clear outfit shapes. Avoid semi-real skin, painterly hair,
cinematic bokeh, and dense digital rain rendering.
```

## `anime-cel-polished`

```text
Polished cel-shaded anime fashion image. Clean contour lines, bold but refined
shadow shapes, crisp color blocks, and precise garment details. Mature
character design; not school-uniform coded, not chibi, not a 3D render.
```

## `anime-tv-slice-of-life`

```text
Adult slice-of-life TV anime look. Natural everyday expressions, modest
background detail, soft but still line-based character art, readable local
props, and restrained color. Use for lived moments, errands, work breaks,
home, transit, or quiet social scenes. Avoid glossy fashion-magazine polish.
```

## `anime-soft-cinematic`

```text
Soft cinematic anime fashion image with atmospheric lighting, gentle gradients,
refined adult character design, and detailed fabrics. Keep the outfit fully
readable and avoid overly dreamy blur.
```

## `anime-manga-ink`

```text
Manga-ink fashion image. Black ink linework, selective spot color or limited
palette, screen-tone or hatch shadows, strong composition, and garment folds
read through line rather than full rendering. Background can be sparse and
graphic. No full-color semi-real painting.
```

## `anime-90s-ova`

```text
Retro 1990s OVA-inspired anime fashion frame. Strong cel shadows, slightly
grainy analog texture, dramatic but readable lighting, mature adult character
design, and bolder color separation. Use for night, club, theater, rain, or
city movement when a stronger mood is needed. Avoid modern glossy digital
fashion-magazine finish.
```

## `anime-watercolor-soft`

```text
Anime character design with soft watercolor-like background and gentle wash.
Character remains line-based and outfit-readable, while the setting uses pale
bleeds, paper grain, and loose local shapes. Use for rain, lake, weekend, home,
or reflective scenes. Avoid dense semi-real rendering.
```

## `anime-pop-graphic`

```text
Graphic pop anime fashion image. Poster-like flat shapes, bold color blocking,
clean silhouettes, minimal shadows, simplified background, and playful
composition. Use when color, accessories, or silhouette should feel fresh and
visibly different from painterly editorial work.
```

## `anime-lofi-sketch`

```text
Loose low-fidelity anime sketch. Visible rough pencil or digital sketch lines,
light wash, imperfect but intentional strokes, and airy background. Use for
daily life, preparation, home, or partial-body snapshots. Avoid polished
magazine lighting and highly finished hair/skin.
```

## `anime-cinematic-night`

```text
Anime night-scene fashion image with controlled cinematic lighting, clear line
art, limited glow, and readable garment shapes. Use sparingly; do not let
every rainy or night image become a dark glossy semi-real street scene.
```

## `anime-comic-panel`

```text
Anime comic-panel fashion image. Strong cropped composition, graphic panel-like
framing, motion lines or sparse environmental cues, and outfit details carried
by line, pose, and silhouette. No text balloons, captions, readable text, or
mock manga page layout unless explicitly requested.
```

## `anime-fashion-magazine`

```text
Anime fashion magazine editorial. Clean full-body composition, sophisticated
posing, elegant typography-free magazine lighting, and strong styling clarity.
No readable text, logos, or mock magazine cover elements.
```

## `fashion-illustration`

```text
Traditional fashion illustration. Elegant elongated proportions, visible
garment construction, expressive ink or pencil line, and controlled marker or
watercolor wash. Runway-board clarity rather than a finished anime scene.
```

## `runway-board-illustration`

```text
Runway-board fashion illustration. Long proportions, front or three-quarter
pose, construction lines, precise garment silhouette, and minimal background
so the outfit can be studied.
```

## `marker-sketch`

```text
Expressive fashion marker sketch with confident ink lines, controlled marker
blocks, visible paper texture, and quick but accurate garment rendering.
```

## `watercolor-couture`

```text
Watercolor couture fashion illustration. Soft wash, elegant line economy,
fabric movement, delicate transparency control, and refined adult styling.
```

## `semi-real-editorial`

```text
Semi-realistic digital fashion editorial. Natural adult proportions, detailed
fabric rendering, soft cinematic light, and a refined magazine-image finish.
Keep a visibly authored digital-art quality; do not present it as a real photo.
```

## `digital-magazine-painting`

```text
Digital fashion magazine painting. Semi-real adult proportions, painterly
finish, controlled editorial lighting, rich fabric rendering, and original
character design. Do not present as a real photo.
```

## `soft-real-fashion-art`

```text
Soft-real fashion artwork with natural proportions, gentle skin rendering,
subtle painterly edges, and detailed textile surfaces. Keep it visibly
illustrated rather than photographic.
```

## Shared Pose Rule

```text
Give each image a clearly different pose, camera angle, face direction, and
hand placement. Choose poses that make the garment construction readable.
```
