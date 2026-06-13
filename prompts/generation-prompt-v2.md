# Daily Fashion Generation Prompt V2

Use this when the full parameter checklist makes image generation unstable.
V2 separates detailed planning from the short prompt sent to the image model.

## Principle

Keep the design record detailed, but keep each image-generation prompt compact.
The monthly log is the source of truth for exact parameters, acceptance checks,
and any differences between prompt intent and final image.

Short does not mean generic. Each short prompt must include one distinctive
garment construction, one concrete life action, and one anti-repeat instruction
so it does not fall back to a recent safe template.

## Before Generation

Fill `prompts/parameter-checklist.md` as usual. Then write a short prompt for
each image with only the visual essentials:

```text
prompt_version: v2-short-generation
image_number: 01-04
place: city and one concrete scene
person: adult Japanese-centered character and age band
persona: bright, sociable, lively, fashion-aware, intentionally stylish, aware of her charm without erotic framing
style: exact style preset in natural language
pose: one readable pose
movement: one clear, safe action when the scene involves vehicles, water, stairs, platforms, or strong motion
outfit: 4-7 core garments/accessories
fashion_focal_point: one or two distinctive styling details
climate: one sentence about comfort and weather
avoid_recent_formula: not the recent repeated formula; name the different silhouette, action, or setting
constraints: no text, no logos, original adult, standalone image
```

Avoid packing every checklist field into the image prompt. Do not include long
lists of internal bookkeeping fields, source links, or repeated safety prose.
Do include the anti-repeat line. If it makes the prompt too long, shorten
source mood and internal notes first, not the anti-repeat line.

## After Generation

Inspect each accepted image and record:

```text
prompt_version: v2-short-generation
prompt_shape: short prompt, detailed log
generated_prompt_summary: one sentence describing the prompt actually used
persona_and_focal_point: how the accepted image shows fashion interest and the chosen styling detail
avoid_recent_formula: the repeated formula that was avoided
movement_readability: whether the action reads as normal, safe, and intentional in the setting
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
