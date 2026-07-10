# Chat Voyage Pose Presets

Use one pose family per image. Choose poses before writing the outfit prompt so
the set does not collapse into four similar standing three-quarter views.

## Action-First Pose Planning

Do not start from pose labels alone. First decide what she is doing in her
day, then choose the pose family that makes that action visible. The strongest
sets feel varied because each image has a different life verb: walking through
a corridor while responding to someone, warming up on a studio floor, pausing
on a rooftop to look over the city, adjusting clothing at home, carrying
groceries, greeting a friend, packing a bag, checking fabric, practicing,
waiting, returning home, or stepping through weather.

Record the action as a short verb phrase before assigning `pose_family`.
`standing-front`, `seated-side`, `back-three-quarter`, and similar labels are
implementation details. They should not become the creative starting point.
When the action is clear, full body, face visibility, direct camera contact,
and centered composition become optional rather than default requirements.

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

Also specify the attention target:

- toward viewer: camera contact, near-camera glance, or a look that openly
  acknowledges being seen
- toward person: looking at a friend, coworker, staff member, dance partner, or
  someone implied just outside the frame
- toward task: looking at hands, shoes, object, fabric, phone, book, ticket, or
  the path of movement
- toward place: looking out a window, across water, through a venue, at a
  stage, into rain, or along a street

For a four-image set, avoid both extremes: do not make all four women look at
the viewer, and do not make all four avoid the viewer. A good default is one
direct or near-camera acknowledgement, one person-to-person/social gaze, one
task gaze, and one place or reflection gaze. If the set intentionally breaks
that balance, record why.

Default four-image mix:

```text
01: using-object or close-crop-upper / face left / knee-up or waist-up
02: walking-stride or jump-motion / face camera / wide-action or full-body
03: seated-side, floor-sit, or leaning-wall / face down or side / knee-up
04: dance-motion, stretching-reach, or back-three-quarter / face over-shoulder or down / dynamic angle
```

## Movement Readability And Intentional Risk

Dynamic motion must be immediately readable as a normal action in the chosen
place, or as an intentional risky/balancing action. The question is not whether
the action is safe. The question is whether the image makes clear what she is
doing, where her weight is, and why that action belongs to her character and
scene.

For boats, ferries, trains, buses, stations, stairs, platforms, piers, bridges,
and water edges, balance and risk can be part of the image: walking along a
boat edge, balancing on a narrow bridge, stepping over a gap, or turning on a
wet pier can work when the body language and setting are legible. Avoid only
unintended ambiguity: accidental falling, unexplained leaping away from a
vehicle, or a pose where the viewer cannot tell what she is trying to do.
Useful action patterns:

- stepping onto a gangway, deck, platform, pier, or stair with one foot planted
- walking along a pier or deck while holding a rail, strap, ticket, hat, or bag
- balancing along a boat edge or narrow bridge with arms, gaze, and foot
  placement clearly showing control
- leaning on a railing, adjusting a jacket or bag strap, checking a map, or
  turning on deck
- using `jump-motion` only when the takeoff, landing, and intention are clear

## Avoid Rules

- Do not let all four images face the same direction.
- Do not let all four images make direct camera contact.
- Do not let all four images avoid the viewer completely.
- Do not make every gaze private/task-only; include at least one social or
  viewer-aware attention direction unless the daily concept explicitly needs
  solitude.
- Do not use four standing three-quarter poses in one set.
- Do not hide shoes or hands in every image.
- Do not sacrifice garment readability for extreme action.
- Do not accept dynamic travel, vehicle, or waterside poses that are
  unintentionally ambiguous, even if the outfit itself is successful.
- Full-body is useful but not required. Use knee-up, waist-up, close-up detail,
  or wide-action crops when that better serves pose variety and fashion detail.
- If a pose fails, regenerate only that image with a targeted pose correction.
