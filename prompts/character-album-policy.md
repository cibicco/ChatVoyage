# Character Day Album Policy

Use this for Chat Voyage albums where a specific original character, such as
Shino, spends a dated day in a specific city, visits concrete places, enjoys
the city, works, rests, meets people, gets lost, listens to music, or follows a
small personal thread.

This is a direction change from treating `collection="character"` as only a
continuity quarantine. Character albums are now first-class date-based albums.
They still use the normal `YYYY-MM-DD-theme` slug, notes, logs, and unified
`album.html?set=...` viewer, but their images and JSON live under the
character collection path.

## Data Shape

- In `data/albums/characters/<character>/YYYY/MM/YYYY-MM-DD-theme.json`,
  `"collection": "character"` marks a character day album.
- `"character": "<slug>"` names the recurring character, for example
  `"character": "shino"`.
- Character album images live under
  `assets/albums/characters/<character>/YYYY/MM/YYYY-MM-DD-theme/`.
- Normal exploratory fashion sets use `"collection": "daily"` and live under
  `assets/albums/daily/YYYY/MM/YYYY-MM-DD-theme/`.
- Character albums should still carry image-level `style`, `place`,
  `category`, `occasion`, `venue`, `activity`, and `outfit` so they remain
  browsable by place, activity, and clothing.

## Album Purpose

A character day album should answer:

- Who is this character today?
- What date or story moment is this?
- Which city and exact places does she visit?
- What does she do or enjoy there?
- Who or what changes her mood?
- What small object, route, mistake, errand, hobby, or plan ties the images
  together?

Fashion still matters, but it is not the only reason the album exists. Clothes
should belong to the character's day: work, commute, market, aquarium,
library, cafe, bar, ferry, tram, home, event, detour, weather, or rest.

Character day albums do not have to reproduce the main story beat for beat.
They can reinterpret a normal daily city/date set as "what this character did
there" while preserving the character's face, body language, visual style, and
objects strongly enough that the result reads as that character's album, not a
generic fashion set.

For a recurring character such as Shino, the character's own visual style wins
over the normal daily album style. The daily album may provide the city,
specific places, actions, key color, weather, and outfit ideas. It should not
provide a different art style, different face grammar, different age-model
look, or different body grammar. Use the character's current reference images
for i2i/reference continuity whenever they are available.

Character consistency does not mean repeating one neutral expression. A
character album should allow the character to feel the day: joy, pleasure,
delight, amusement, pride, relaxation, anticipation, embarrassment, surprise,
or quiet afterglow can all belong when the scene supports them. For Shino in
particular, "quiet" means self-possessed and observant, not expressionless.
Her gaze may carry confidence, small pleasure, absorbed delight, or warmth
with a familiar person; morning slowness or late-night softness are situational
states, not the default face.

When the album uses a real city, use specific named places rather than
"something-style" placeholders. For example, prefer "Biblioteca Vasconcelos",
"San Angel courtyard reception", "Roma Norte dance studio", or "Coyoacan
rooftop textile corner" over "Biblioteca Vasconcelos-style library". Avoid
prominent advertising, readable trademarks, exact product copying, and
single-source photo copying, but keep the place concrete. Ordinary readable
street-name signs are acceptable place context. Do not remove them merely
because they are legible. Incidental everyday labels or product details do not
need to be rejected when they are not the visual focus and do not read as a
real brand promotion.

## Required Planning Fields

Before generating a character album, record:

```text
character_album_mode: character-day
character_slug:
character_profile:
character_age_plan:
character_identity_continuity:
character_visual_style_anchor:
character_expression_plan:
character_i2i_reference_plan:
date_seed:
story_day_summary:
character_route_plan:
exact_place_plan:
place_lane_plan:
activity_enjoyment_plan:
wardrobe_palette_plan:
source_daily_outfit_plan:
continuity_anchors:
signage_policy:
```

`exact_place_plan` should name the city and specific places. `place_lane_plan`
should use more than one place type unless the story is deliberately confined.
`activity_enjoyment_plan` should name what the character is doing or enjoying,
not only where she stands.
`character_expression_plan` should name the emotional range for the set, not
only a default gaze. Use scene-specific expressions that fit the character and
moment, such as focused observation, quiet pleasure, absorbed delight, a small
proud smile, a warm familiar laugh, or relaxed afterglow.

## Acceptance Check

- The same character identity is intentional and stable.
- Face, body proportions, visual style, and character-specific presence remain
  stable even when age, city, outfit, or activity changes.
- The album has a dated story arc, even if it is quiet.
- The images show the character going to or inhabiting multiple places over
  the day.
- Real-city albums use specific named places instead of vague "style" places.
- Each image has a concrete life action or moment of enjoyment.
- The expression mix supports the character's lived day instead of collapsing
  into the same neutral, sleepy, or blank face across the album.
- Wardrobe, palette, objects, and mood vary without breaking identity.
- Repeated garments, colors, or poses are acceptable when they belong to the
  character and the date. Do not apply generic cooldown rules to a character
  album unless the user specifically asks for that kind of novelty control.
- Character albums are compared against that character's recent albums for
  route, palette, expression, and object drift.
- Normal daily exploration sets are compared separately, so character albums
  do not distort the novelty check for unrelated daily fashion work.
