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
- screen grammar, such as centered solo subject, polished three-quarter fashion
  view, quiet gallery viewing, cafe/bar sitting, wet city walk, small prop
  gesture, or full-body outfit display
- attention pattern, such as all four women looking at the viewer, all four
  avoiding the viewer, all task-only downward gazes, or all over-shoulder looks
- effective visual style, such as line language, shading, background density,
  texture, color logic, medium, and time/light expression
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
with charcoal utility skort over bike shorts + flat rain sandals + clear tote."
Another skort with different fabric, hem, volume, legwear, footwear, place,
movement, and attitude is a different fashion decision and remains available.

For active, dance, transit, swim, and movement scenes, distinguish a repeated
formula from a useful garment feature. Side slits, vents, curved hems, wrap
openings, drawcords, sport socks, sandals, bike shorts, and safety shorts are
not flaws by themselves. They can be the reason the image reads as active. Put
the overused combination on cooldown only when the full construction repeats or
the layering is unclear. If a cleaner correction removes the action, restore or
regenerate toward the more active version and record why it was accepted.

Separate character day albums from normal daily exploration when checking
novelty. In Chat Voyage, character day albums keep the same date-based album
structure, but their `index.html` section must use
`data-collection="character"` and `data-character="<slug>"`. They are allowed
to repeat the same person because their goal is to show that character moving
through dated days and places. Review them against the character's own recent
route, activity, palette, expression, and object patterns. Do not let those
albums make the normal daily exploration pool look more repetitive than it is.
Conversely, do not use character-album variety as proof that the normal daily
set is novel; check the normal exploration pool on its own.

For character day albums, read `prompts/character-album-policy.md` and the
character prompt profile when one exists. Shino uses
`prompts/character-shino.md`.

## Character Album Drift

Character day albums can accidentally turn one route, color formula, or object
cluster into the character's whole identity. Treat that as a drift risk, not
as a style requirement.

For Shino specifically, black hair, violet eyes, a quietly self-possessed gaze,
fish/lab/aquarium/DJ objects, and quiet behavior are stronger identity anchors
than black or navy clothing. Before generating a Shino album, record:

- `character_album_mode`: `character-day`.
- `shino_story_place_plan`: which main-story city lanes the album uses, such
  as lab district, harbor market, old town, transit detour, aquarium/library,
  night music, home/neighborhood, or seaside spaces.
- `activity_enjoyment_plan`: what Shino does or enjoys in each place, not only
  where she stands.
- `shino_palette_plan`: which non-dark dominant colors will appear.
- `shino_dark_formula_cooldown`: which black/navy/charcoal/graphite formulas
  are being cooled down.
- `palette_role` per image: whether dark colors are dominant, base, accent,
  workwear utility, nightwear, or absent.

Do not ban black, navy, charcoal, or graphite. Use them deliberately. In a
Shino album of four or more images, at least half of the images should have a
non-dark dominant garment unless the story requires a concentrated workwear or
nightwear sequence and the note records why.

Also watch for place drift. Shino should not be trapped in only the lab,
aquarium, bar, and apartment. Use the main-story city over time: harbor market,
old town, tram/station detours, library/bookshop, hill or old wall, seaside
cafe/pool, warehouse lounge, quiet bar, home neighborhood, and the standards
lab district can all be valid Shino places when the scene supports them.

## Effective Art Style And Weather

Check the last three to five sets for the visible finish of the accepted
images, not only the `style_preset` metadata. Different slugs can still produce
the same effective image: glossy fashion-magazine anime, dense semi-real rain
painting, wet pavement reflection, soft cinematic bokeh, or polished
three-quarter city portrait.

For every new image, choose an `effective_style_variant` and state how it
differs in at least three of these axes:

- line language: thick contour, thin contour, manga ink, sketch line, no line,
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
  lamp pools, night neon, rainy reflection, or dry interior with weather hinted
  outside

Weather is not the enemy. If the date, city, or source scan says rain, keep
rain. Do not invent sun just to escape repetition. Instead vary the time of
day, rain intensity, wetness, indoor/outdoor condition, light source, viewing
distance, composition, and rendering medium. A rainy day can still include a
flat cel morning errand, a sparse manga-ink covered arcade, a warm interior
marker sketch with rain outside, and a pale watercolor afternoon drizzle.

Put effective finishes on cooldown when they repeat, for example:

- high-density semi-real wet street painting where reflections do most of the
  place work
- glossy fashion-magazine anime with soft cinematic bokeh
- overcast rain scene with the same three-quarter solo figure and detailed
  urban background
- marker or watercolor treatment used as a label while the final image still
  reads like polished semi-real digital painting

Do not accept an image only because its style slug differs. If the visible
finish repeats, regenerate with a concrete correction: flatter cel shadows,
manga ink, sparse background, looser pencil, marker blocks, watercolor wash,
poster-flat color, or a different time/light condition.

## Lifestyle Snapshot And Screen Grammar

The next novelty frontier is not only clothing or place. Avoid returning to
the same image grammar: a single stylish woman centered in a polished urban
background, usually three-quarter, walking, sitting, looking back, or holding a
small object.

Use action-first planning. Before choosing pose labels, write one concrete life
verb for each image. A set gains real variety when the actions differ, such as
walking while answering someone, floor warm-up, rooftop pause, home dressing,
packing, greeting, carrying, repairing, practicing, waiting, cooking, returning
home, or stepping through weather. Pose families are then chosen to serve
those actions; they are not the main source of novelty by themselves.

For normal daily exploration, make at least two of four images read as
lifestyle snapshots unless the user asks for a pure outfit-board set. In a
lifestyle snapshot, the woman is living a moment and her outfit is naturally
visible inside that moment. Full body, front view, visible face, and centered
composition are optional.

Valid snapshot and partial-detail choices include:

- hands choosing earrings, folding clothes, tying shoes, carrying groceries,
  holding a train strap, or adjusting a wet umbrella
- back, side, mirror, window, reflection, stair, doorway, or over-shoulder
  views where fabric, hem, shoes, bag, or body movement is the fashion signal
- off-center framing, foreground obstruction, cropped legs, cropped torso,
  close-up garment detail, or the subject partly inside a crowd or room
- life actions such as making, repairing, preparing, packing, cleaning,
  waiting, greeting, reacting, commuting, shopping with intent, practicing,
  cooking, carrying, or returning home
- other people implied by hands, shadows, friends just outside the frame,
  shop staff, commuters, classmates, coworkers, or party guests, while the
  main subject remains one adult woman

Do not reject a good image because it is not a full outfit view. Judge whether
the clothing belongs to the woman's moment and whether the set as a whole still
contains enough fashion information.

## Transit And Ferry Composition Cooldown

Transit is useful for local atmosphere, but ferry, tram, cable car, and train
images can easily collapse into the same visual answer: a young woman inside a
vehicle beside a large window, with water or city scenery outside, one hand on
a rail or strap, a small object, and a skirt/skort outfit. After this appears
once in the recent pool, avoid repeating it for the next several normal daily
sets unless the repeat is intentional and logged.

For ferries and boats, rotate the world around the vehicle instead of always
using the cabin window:

- terminal ramp, gangway, pier, quay, ticket gate, covered walkway, waiting
  line, deck edge, stairs, platform, arrival hall, or post-arrival street
- wide exterior movement, back/side view, partial leg/shoe detail, luggage or
  bag handling, wind on clothing, friend or commuter interaction, or water
  visible through the route rather than through a cabin window
- if the cabin is used, change the action and screen grammar decisively:
  seated task, reflection-only crop, hands/feet detail, standing crowd, or a
  non-window-facing composition

Do not treat "different city, different ferry" as enough novelty when the
composition is still a ferry-window fashion pose.

## Gaze And Attention Balance

Viewer contact is a visual rhythm, not a binary rule. A set feels staged when
all four women look straight at the viewer, but it also feels strangely evasive
when all four avoid the viewer.

Before prompting, assign one attention target per image:

- viewer or near-camera acknowledgement
- another person implied in the scene
- task or object
- place, window, rain, stage, street, or path of movement
- mirror or reflection

For normal daily exploration, include at least one viewer-aware or social gaze
and at least one task/place/reflection gaze. Avoid four private downward/task
looks, four over-shoulder looks, or four direct camera looks unless the concept
intentionally depends on that pattern and the log records why.

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
- high-density semi-real rain painting repeated across cities
- glossy cinematic anime where every background becomes the same bokeh city
- style metadata changed, but the final finish still looks like the same
  polished editorial digital painting

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
  thin stockings, back-seam stockings, fishnet or micro-net stockings,
  stirrup tights, leggings, bike shorts, bloomers, or safety shorts when they
  are part of the outfit construction
- sandals, mules, loafers, Mary Janes, slingback pumps, low heels, sneakers,
  short boots, perforated boots, and summer boots according to terrain and
  activity

Use legwear to change the fashion language: playful, club, office, dance,
sporty, retro, polished, rainy, winter, or resort. Do not add legwear only as
a modesty patch, and do not remove it only to signal openness.

Watch for sheer sock drift. Recent Chat Voyage sets have often solved the
ankle-to-knee area with the same transparent sock finish: short sheer ankle
socks, sheer calf socks, or below-knee sheer high socks paired with Mary Janes,
slingbacks, mules, or boots. The user's preferred split is clearer: either
ankle-length socks near the ankle, or thigh-high / over-knee hosiery above the
knee. Avoid the ambiguous below-knee sheer-sock band when it starts repeating.
If recent sets already used that finish repeatedly, put it on cooldown and
choose a clearer alternative: bare legs, opaque or ribbed ankle socks, slouch
socks, sport socks, lace socks, patterned tights, plain sheer stockings,
back-seam stockings, fishnets, over-knee socks, thigh-high stockings, opaque
tights, leggings, or no hosiery with sandals/pumps/boots.

Do not make over-knee or thigh-high styling synonymous with sheer hosiery.
Sheer thigh-highs can be good, but they should not become the default answer
whenever a look needs high legwear. Rotate the material and finish: opaque
knit over-knee socks, ribbed cotton or wool thigh-highs, colored opaque
stockings, matte dance tights, back-seam stockings, lace-top stockings, micro
fishnet, patterned tights, stirrup tights, glossy stage tights, sporty tube
over-knees, or plain bare legs. Choose the finish from the outfit's world:
school-coded innocence is not the goal, and neither is automatic transparency.

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

When a real named place is chosen, do not over-sanitize it into "place-like"
background. Use the real place as the scene anchor and let recognizable public
features, routes, materials, weather, objects, and social use appear. Avoid
trademark/logo reproduction, readable brand marks, exact product copying, and
copying a single source-photo composition, but do not treat specificity itself
as a problem.

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
- same attention pattern across all four images
- same effective finish despite different style preset names
- same action verb under different pose labels, such as four images that are
  all really standing, waiting, or holding a small object

If an image is accepted despite a repeat, record the repeat and the reason in
the visual check.
