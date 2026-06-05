# Chat Voyage Logs

This directory stores Codex / LLM oriented generation records.

## Rotation

Use one Markdown file per month:

- `generation-YYYY-MM.md`

Monthly files are compact enough for an LLM to read when planning the next daily set, while avoiding one ever-growing project log.

## What Belongs Here

Record operational details that help future generation:

- date seed and generated image count
- city, place, season, common mood, lucky color
- image save paths and source generation paths
- person design, role, outfit construction, materials, styling
- target age band, using `prompts/age-presets.md`
- pose family, face direction, body direction, camera angle, and hand placement, using `prompts/pose-presets.md`
- illustration style and quality/result notes
- fashion language and reusable variation ideas
- selected primary category for each image
- secondary tags for each image: weather, season, fashion direction, place, materials, and visual style
- missing reference files or source-scan notes

Keep human-facing theme summaries in `notes/`. Keep detailed implementation and reuse records here.

## Per-Image Category Format

```text
- Primary category: {one slug from prompts/category-presets.md}
- Target age band: {18-19-adult | 20-24 | 25-29}
- Style preset: {one slug from prompts/style-presets.md}
- Pose family: {one slug from prompts/pose-presets.md}
- Secondary tags: {weather}, {season}, {fashion direction}, {place}, {materials}, {visual style preset}
```
