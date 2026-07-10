# Prompts

Reusable prompt notes for Chat Voyage daily image sets.

Keep prompts specific enough to force visible fashion variation, but avoid exact brand product copies, logos, or source-photo reproduction.

## Files

- `daily-fashion-template.md`: shared scaffold for four-image daily sets.
- `age-presets.md`: adult age-band vocabulary and guardrails, including 18-19 adult handling.
- `persona-presets.md`: default character persona for bright, sociable, fashion-aware daily subjects.
- `repetition-guardrails.md`: recent-set comparison and anti-template rules.
- `generation-prompt-v2.md`: short-prompt workflow with detailed logging and anti-repeat fields.
- `category-presets.md`: reusable category vocabulary; select four categories for each daily set.
- `pose-presets.md`: pose, face direction, body direction, camera angle, and hand-placement vocabulary.
- `style-presets.md`: reusable visual style switches, separate from daily theme and outfit instructions.
- `character-album-policy.md`: shared policy for date-based albums where a
  recurring character goes to places and enjoys a story day.
- `character-shino.md`: Shino identity, route, place, gaze, and palette
  guardrails for albums marked with `data-character="shino"`.

## Sync Check

After adding a new style or category to `index.html`, also add it to the
corresponding preset file, then run:

```sh
python3 scripts/validate_gallery.py
```
