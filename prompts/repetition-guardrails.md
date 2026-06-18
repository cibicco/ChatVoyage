# Daily Fashion Repetition Guardrails

Use this before every daily generation after reading the normal presets. The
goal is not novelty for its own sake; it is to avoid producing the same fashion
grammar with a different city and lucky color.

## Recent-Set Comparison

Before writing prompts, scan the last three to five daily notes or monthly log
entries and list the repeated patterns. Check at least:

- primary category sequence
- pose-family sequence
- garment formula
- outer-layer formula
- shoe formula
- background formula
- generic interior formula versus locally specific activity space
- crop and camera formula
- age-band role assignment
- lucky-color placement

If two or more recent sets used the same full styling formula, the next set
should either change the composition or record why the repeat is intentional.
Do not put a normal garment type on cooldown by itself. Cooldown applies to the
combined formula: garment stack, category, pose, shoes or legwear, place, crop,
and styling attitude together.

When recording the repeated formula, do not shorten it to a broad garment
category such as "skort + sandals" or "tank + open shirt." That loses the
fashion information. Name the actual construction and styling relationship:
for example, "covered-market crouch + rib tank + loose short-sleeve open shirt
+ charcoal utility skort over bike shorts + flat rain sandals + clear tote."
Another skort with different fabric, hem, volume, legwear, footwear, place,
movement, and attitude is a different fashion decision and remains available.

## Climate Specificity

Do not reduce climate naturalness to "warm and humid means tank, camisole,
open shirt, mesh, and sandals." Decide clothing from the full context:

```text
city:
season:
actual_or_expected_weather:
temperature_band:
humidity:
time_of_day:
indoor_or_outdoor:
local_activity_space:
wind_or_air_conditioning:
rain_intensity:
walking_or_stationary:
venue_norms:
activity:
```

Then choose fabric weight, sleeve, neckline, hem, footwear, and layering. The
goal is natural dress for the situation, not reducing or increasing visible
skin. Warm humid weather may support open clothing, but it can also support
cotton tees, short-sleeve shirts buttoned normally, airy shirt dresses,
sleeveless tailoring, light jumpsuits, cropped trousers, washable skirts,
technical rain pants, thin cardigans in air-conditioned interiors, or compact
outer layers.

## Age-Band Differentiation

Age bands must differ by more than lucky-color tone.

- `18-19-adult`: adult young casual, campus or first-job adjacent, practical
  movement, playful proportions, simple accessories, no school cues.
- `20-24`: experimental street, gallery, music, active, cafe, travel, or early
  career scenes; more trend risk and mixed materials.
- `25-29`: polished daily, work-adjacent, design-event, restaurant, theater,
  travel, hotel, or quiet night scenes; sharper editing, better tailoring,
  richer fabrics, or restrained detail.

For every image, record:

```text
age_band_life_scene:
age_band_silhouette:
age_band_material_logic:
age_band_accessory_logic:
```

## Formula Cooldowns

After a full formula appears in two recent sets, put that full combination on
cooldown for at least the next one or two daily sets unless the user explicitly
asks for it. Do not treat tanks, open shirts, miniskirts, skorts, shorts,
sandals, bare legs, or visible skin as the problem. They remain valid fashion
choices when the city, weather, venue, activity, age band, and styling attitude
support them.

Cooldown examples:

- young covered-market crouch + rib tank + loose short-sleeve open shirt +
  charcoal utility skort over bike shorts + flat rain sandals + clear tote
- open-back halter + carried mesh bolero + culotte shorts
- satin camisole + draped blazer + sheer-over-opaque midi skirt
- black tank + mesh/rain shell + wide pants + sneakers
- market crouch + snack/object inspection
- gallery over-shoulder open-back crop
- lounge seated-side looking down
- rain set made entirely of wet pavement reflections

## Category Rotation

Do not keep returning to `market`, `gallery`, `lounge`, and `transit` as the
default warm-weather quartet. Prefer a new balance when recent sets used those
labels:

- workday: `office`, `outerwear`, `date`, `home`
- culture: `theater`, `formal`, `gallery`, `travel`
- movement: `active`, `dance`, `street`, `weekend`
- destination: `resort`, `swim`, `travel`, `lounge`
- local day: `weekend`, `date`, `market`, `home`

The category choice should change garment construction and life scene, not
only the background.

## Hem, Legwear, And Footwear Variety

Do not let age or skin-visibility caution erase shorter hems or leg styling.
Mini skirts, micro-to-mini skorts, short wrap skirts, cargo minis, pleated
minis, bias minis, city shorts, hot-weather half pants, and dance or active
skorts are all available adult fashion options when the scene supports them.

Legwear should be an active styling axis, not an afterthought. Consider:

- bare legs when weather and venue make that natural
- sheer ankle socks, ribbed socks, slouch socks, sport socks, lace-trim socks,
  or color-pop socks
- knee socks, sheer knee-highs, mesh socks, patterned tights, opaque tights,
  leggings, bike shorts, bloomers, or safety shorts when they are part of the
  outfit construction
- sandals, mules, loafers, Mary Janes, slingback pumps, low heels, sneakers,
  short boots, perforated boots, and summer boots according to terrain and
  activity

Use legwear to change the fashion language: playful, club, office, dance,
sporty, retro, polished, rainy, winter, or resort. Do not add legwear only as
a modesty patch, and do not remove it only to signal openness.

## Local Atmosphere And Place Specificity

Do not treat indoor variety as only ordinary rooms, work, meals, cafes, or
bars. Use local activity spaces when they fit the date and category:

- museums, art museums, galleries, design centers, public halls, libraries, and
  archives
- clubs, live houses, listening rooms, theaters, cinemas, rehearsal studios,
  and performance foyers
- sports facilities, dance studios, climbing gyms, pools, baths, stations,
  markets, covered arcades, and transit halls

Outdoor or semi-outdoor places are equally useful: beaches, harbors, mountain
paths, pools, terraces, night streets, markets, shrine or temple approaches,
arcades, parks, and transit edges can all work when they reveal the local
atmosphere.

The place should feel characteristic of the city or region, not a generic
interior or generic street with the city name attached. Prefer locations where
the image can show local light, architecture, landscape, materials, objects,
weather, or social rhythm. The local place choice should also affect outfit
construction, footwear, layer logic, pose, object interaction, and time-of-day
behavior.

## Prompt V2 Anti-Template Rule

When using `v2-short-generation`, keep the prompt short but include one
specific anti-repeat instruction per image:

```text
avoid_recent_formula: not the recent {formula}; use {new silhouette/action}
```

The prompt should name one distinctive garment construction or life action
that makes the image different from recent accepted sets.

## Acceptance Check

Reject or regenerate an image when it passes basic quality but visually repeats
a recent accepted formula without a documented reason. Examples:

- same silhouette with only a color change
- same open-back gallery pose as the previous city
- same seated camisole lounge composition as the previous city
- same wet-reflection background doing most of the place work
- same age-band role assignment across the four images

If an image is accepted despite a repeat, record the repeat and the reason in
the visual check.
