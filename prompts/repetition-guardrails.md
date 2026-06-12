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
- crop and camera formula
- age-band role assignment
- lucky-color placement

If two or more recent sets used the same formula, the next set should either
avoid it or record why the repeat is intentional.

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
wind_or_air_conditioning:
rain_intensity:
walking_or_stationary:
venue_norms:
activity:
```

Then choose fabric weight, sleeve, neckline, hem, footwear, and layering. Warm
humid weather may support open clothing, but it can also support cotton tees,
short-sleeve shirts buttoned normally, airy shirt dresses, sleeveless tailoring,
light jumpsuits, cropped trousers, washable skirts, technical rain pants,
thin cardigans in air-conditioned interiors, or compact outer layers.

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

After a formula appears in two recent sets, put it on cooldown for at least the
next one or two daily sets unless the user explicitly asks for it.

Cooldown examples:

- tank + open short-sleeve shirt + skort or shorts + sandals
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
