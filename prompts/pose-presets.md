# Chat Voyage Pose Presets

Use one pose family per image. Choose poses before writing the outfit prompt so
the set does not collapse into four similar standing three-quarter views.

## Pose Families

- `standing-front`: front-facing standing pose, garment front readable
- `walking-stride`: walking or stepping pose, one foot forward, movement in hem or outerwear
- `seated-side`: seated side or three-quarter pose, legs and shoes or garment drape visible, hands readable
- `leaning-wall`: leaning against wall, railing, counter, or doorway, asymmetrical weight
- `crouching-market`: crouching or low bend to inspect an object, still adult and composed
- `dance-motion`: mid-turn or dance motion, dynamic limbs, garment movement readable
- `jump-motion`: small jump, hop, stair step, or lifted-heel motion, dynamic but garment-readable
- `close-crop-upper`: waist-up or knee-up crop focused on top, jacket, hair, bag, and hand gesture
- `floor-sit`: sitting on floor, steps, curb, or studio floor with garment layers visible
- `stretching-reach`: reaching overhead, stretching, pulling strap, or adjusting hair with torso twist
- `back-three-quarter`: back or rear three-quarter view, looking over shoulder, back details visible
- `over-shoulder`: torso angled away, face looking back, useful for jackets, backs, and bags
- `using-object`: interacting with a phone, hanger, ticket, book, cup, umbrella, bag, or garment rack
- `hands-in-pocket`: relaxed standing or walking pose with one or both hands in pockets
- `adjusting-jacket`: hands adjusting collar, sleeve, belt, strap, or outer layer
- `looking-down`: face angled down toward shoes, fabric, table, book, or bag

## Direction Mix Rule

For a four-image set, specify all of these independently:

- face direction: `left`, `right`, `camera`, `down`, or `over-shoulder`
- body direction: `front`, `left-profile`, `right-profile`, `three-quarter`, `back-three-quarter`
- camera angle: `eye-level`, `low`, `high`, `side`, or `diagonal`
- hand placement: object interaction, pocket, collar, bag strap, table, railing, or free motion
- crop: `full-body`, `knee-up`, `waist-up`, `close-up-detail`, or `wide-action`

Default four-image mix:

```text
01: using-object or close-crop-upper / face left / knee-up or waist-up
02: walking-stride or jump-motion / face camera / wide-action or full-body
03: seated-side, floor-sit, or leaning-wall / face down or side / knee-up
04: dance-motion, stretching-reach, or back-three-quarter / face over-shoulder or down / dynamic angle
```

## Movement Safety And Readability

Dynamic motion must be immediately readable as a normal action in the chosen
place. If the viewer would ask "what is she doing?", the pose needs a clearer
action description or a regeneration.

For boats, ferries, trains, buses, stations, stairs, platforms, piers, bridges,
and water edges, avoid poses that can read as jumping off, falling, running out
of a vehicle, or leaving a safe surface. Prefer a clear, grounded action:

- stepping onto a gangway, deck, platform, pier, or stair with one foot planted
- walking along a pier or deck while holding a rail, strap, ticket, hat, or bag
- leaning on a railing, adjusting a jacket or bag strap, checking a map, or
  turning safely on deck
- using a compact `jump-motion` only when the surface and direction are clear,
  such as a small hop on a dry plaza or a stair step away from edges

## Avoid Rules

- Do not let all four images face the same direction.
- Do not use four standing three-quarter poses in one set.
- Do not hide shoes or hands in every image.
- Do not sacrifice garment readability for extreme action.
- Do not accept dynamic travel, vehicle, or waterside poses that look unsafe or
  ambiguous, even if the outfit itself is successful.
- Full-body is useful but not required. Use knee-up, waist-up, close-up detail,
  or wide-action crops when that better serves pose variety and fashion detail.
- If a pose fails, regenerate only that image with a targeted pose correction.
