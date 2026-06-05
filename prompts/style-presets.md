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

- Anime family: `anime-editorial`, `anime-cel-polished`, `anime-soft-cinematic`, `anime-fashion-magazine`
- 3D CG family: `3d-cg-fashion`, `pbr-fashion-3d`, `game-cinematic-3d`, `doll-like-3d`
- Fashion illustration family: `fashion-illustration`, `runway-board-illustration`, `marker-sketch`, `watercolor-couture`
- Semi-real digital family: `semi-real-editorial`, `digital-magazine-painting`, `soft-real-fashion-art`

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

## `anime-cel-polished`

```text
Polished cel-shaded anime fashion image. Clean contour lines, bold but refined
shadow shapes, crisp color blocks, and precise garment details. Mature
character design; not school-uniform coded, not chibi, not a 3D render.
```

## `anime-soft-cinematic`

```text
Soft cinematic anime fashion image with atmospheric lighting, gentle gradients,
refined adult character design, and detailed fabrics. Keep the outfit fully
readable and avoid overly dreamy blur.
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
