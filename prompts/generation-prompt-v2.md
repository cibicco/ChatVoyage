# Daily Fashion Generation Prompt V2

Use this when the full parameter checklist makes image generation unstable.
V2 separates detailed planning from the short prompt sent to the image model.

## Principle

Keep the design record detailed, but keep each image-generation prompt compact.
The monthly log is the source of truth for exact parameters, acceptance checks,
and any differences between prompt intent and final image.

Short does not mean generic. Each short prompt must include one distinctive
garment construction, one concrete life action, one reason the outfit belongs
to this person's day, and one anti-repeat instruction so it does not fall back
to a recent familiar template.

Style names do not guarantee visual variety. Before sending the short prompt,
choose the effective rendering target: line language, shading, background
density, texture, color logic, and time/light expression. If two prompts both
look like high-density semi-real editorial rain scenes after generation, they
are repeats even when their `style_preset` slugs differ.

Weather is allowed to repeat when it belongs to the date, city, or chosen
scene. Do not turn a rainy day sunny only for variety. Instead vary time of
day, rain intensity, indoor/outdoor condition, light source, composition,
background density, and medium.

For normal daily exploration, do not make every image a full-outfit fashion
display. Use lifestyle snapshot language for at least two of four prompts when
the set is not explicitly a pure fashion-board set: the woman is doing
something in her life, and the outfit is naturally visible inside that moment.
Back views, partial crops, hands, legs, mirror/reflection views, off-center
framing, and clothes in motion are valid when they make the moment feel lived.

## Before Generation

Fill `prompts/parameter-checklist.md` as usual. Then write a short prompt for
each image with only the visual essentials:

```text
prompt_version: v2-short-generation
image_number: 01-04
place: city and one concrete scene
person: adult Japanese-centered character and age band
persona: selected adult life-and-trait direction, fashion-aware, situated in her own day, not justified only by youth, liveliness, sensuality, or modesty
style: exact style preset in natural language
effective_style_variant: visible rendering target, such as anime-cel-clean, anime-tv-slice-of-life, anime-manga-ink, anime-watercolor-soft, anime-90s-ova, marker-sketch, watercolor-couture, semi-real-editorial, or true 3D
style_execution: line language, shading type, background density, texture, color logic, and time/light expression
snapshot_mode: fashion-editorial, lifestyle-snapshot, work-or-making, relationship-moment, transit-errand, home-life, or partial-detail
pose: one readable pose
movement: one clear intentional action, including chosen risk or balance when the scene involves vehicles, water, stairs, bridges, platforms, or strong motion
composition: how this image avoids the default full-body centered fashion pose; name the crop, viewpoint, off-center placement, mirror/window/reflection use, back/side/partial body choice, or other people's implied presence
attention_target: viewer, near-camera, another person, task/object, place/window, path of movement, mirror, or reflection; across the four-image set avoid both all-camera-contact and all-camera-avoidance
outfit: 4-7 core garments/accessories
fashion_focal_point: one or two distinctive styling details
climate: one sentence about comfort and weather
time_weather_rendering: true weather if relevant, plus time of day, rain/sun/wind intensity, indoor/outdoor condition, and light source
human_context: one phrase about why she chose or can naturally wear this outfit today: work, rest, movement, friends, date, ceremony, errand, travel, hobby, venue, weather, or personal taste
avoid_recent_formula: not the recent repeated formula; name the different silhouette, action, or setting
avoid_recent_screen_grammar: not the recent repeated visual habit; name the different framing or life moment
avoid_recent_effective_style: not the recent visual finish; name the different line, shading, density, texture, color, or light treatment
constraints: no text, no logos, original adult, standalone image
```

Avoid packing every checklist field into the image prompt. Do not include long
lists of internal bookkeeping fields, source links, or repeated guardrail prose.
Do include the anti-repeat line. If it makes the prompt too long, shorten
source mood and internal notes first, not the anti-repeat line.

## After Generation

Inspect each accepted image and record:

```text
prompt_version: v2-short-generation
prompt_shape: short prompt, detailed log
generated_prompt_summary: one sentence describing the prompt actually used
persona_and_focal_point: how the accepted image shows the selected life context, traits, fashion interest, and chosen styling detail
snapshot_mode: whether the accepted result works as fashion-editorial, lifestyle-snapshot, work-or-making, relationship-moment, transit-errand, home-life, or partial-detail
effective_style_variant: the visible rendering target that was intended
style_execution_check: whether line, shading, background density, texture, color, and light match the intended effective style
time_weather_rendering_check: whether true weather was preserved when needed and varied through time, intensity, indoor/outdoor, light, composition, or medium
avoid_recent_formula: the repeated formula that was avoided
avoid_recent_screen_grammar: the repeated visual habit that was avoided
attention_mix_check: whether the set balances viewer-aware, social, task, and place/reflection gazes instead of making everyone look at the viewer or everyone avoid the viewer
avoid_recent_effective_style: the repeated finish that was avoided, or the reason an intentional repeat was accepted
movement_readability: whether the action reads as intentional, physically coherent, and character-driven in the setting
visual_check:
  matches: what the image clearly matches
  deviations: what changed or is weaker than planned
  accepted_reason: why it is still accepted, or why it was regenerated
```

When a prompt needs to be shortened or a category changes to complete the set,
record that in the monthly log. This is not a failure if the final image still
passes the quality gates and the change is documented.

## Acceptance Bias

Prefer stable, natural images over overloaded prompts. If a richly detailed
prompt fails repeatedly, shorten it first. If one scene or category keeps
failing, change the scene/category only when the replacement still fits the
daily direction and the log records the reason.

Do not accept a stable image only because it is clean if it repeats a recent
accepted formula with a new city and lucky color. Regenerate with a targeted
silhouette, action, crop, or background correction, or log the intentional
repeat.

Do not accept an image only because the metadata says the style is different.
If the effective finish looks like the same recent image grammar, regenerate
with a concrete rendering correction such as flatter cel shadows, manga ink,
loose pencil, marker blocks, watercolor wash, sparse background, or a different
time/light condition.
