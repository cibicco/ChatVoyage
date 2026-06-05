# Chat Voyage Fashion Category Presets

Choose four primary categories for each daily set. Primary categories are
reusable organization labels for filenames, logs, and later search. They are
not a fixed four-part template. Add secondary tags separately.

Daily category selection should be date-seeded or intentionally randomized.
Avoid the old default quartet unless it genuinely fits the day. The selected
four categories should create visible differences in garment structure,
setting, posture, and styling attitude.

## Primary Category Vocabulary

- `street`: practical city styling, layered casual, workwear, or polished everyday wear
- `mode`: sharper editorial styling, sculptural silhouette, gallery or runway language
- `night`: evening, dinner, theater, lounge, or event styling
- `resort`: relaxed holiday, terrace, waterfront, ryokan, or travel styling
- `office`: workday tailoring, smart separates, commute-ready styling
- `weekend`: relaxed off-duty styling, cafe, market, park, or neighborhood walk
- `date`: romantic but wearable styling for a restaurant, cinema, or city outing
- `formal`: ceremony, reception, hotel, or dress-code styling
- `travel`: airport, station, road-trip, or destination-arrival styling
- `active`: sporty, technical, outdoor, dance, or athleisure styling
- `club`: DJ, dance floor, late-night party, or music-event styling
- `lounge`: bar, hotel lounge, cocktail room, listening bar, or quiet night-out styling
- `theater`: theater, concert, fado, live house, opera, or performance-going styling
- `gallery`: museum, art fair, exhibition opening, or design-event styling
- `ceremony`: wedding guest, reception, award dinner, or formal daytime event styling
- `home`: home party, roomwear, studio apartment, balcony, or relaxed indoor styling
- `swim`: pool, beach, spa, or water-side swimwear styling
- `outerwear`: coat, jacket, cape, leather, trench, or outer-layer-focused styling
- `dance`: dance lesson, rehearsal, club movement, or performance-practice styling
- `market`: flea market, food market, bookstore market, or local shopping styling
- `transit`: train, ferry, airport, station, night bus, taxi stand, or arrival/departure styling

## Secondary Tag Vocabulary

Secondary tags add search context without replacing the primary category.

- Weather / season: `rain`, `snow`, `summer`, `winter`, `early-autumn`
- Fashion direction: `retro`, `craft`, `minimal`, `feminine`, `workwear`, `tailoring`
- Place: `gallery`, `harbor`, `theater`, `cafe`, `ryokan`, `waterfront`, `club`, `lounge`, `terminal`, `hotel`, `museum`, `home`, `pool`, `market`
- Materials: `knit`, `velvet`, `satin`, `linen`, `denim`, `technical`
- Visual style: use one preset slug from `style-presets.md`

## Daily Selection Rule

```text
Select four primary categories that fit today's city, season, theme, and
requested outfit. Avoid repeating the same four categories by habit. Use each
selected primary category as the filename prefix:

01-{category}-{look-name}.png
02-{category}-{look-name}.png
03-{category}-{look-name}.png
04-{category}-{look-name}.png
```

Record secondary tags for each image in the monthly generation log. Add a new
stable primary category or secondary tag when a daily theme needs one that is
not covered by the vocabulary above.

## Random Selection Guidance

For ordinary daily generation, choose four categories with this balance:

- 1 practical or daytime anchor: `street`, `office`, `weekend`, `travel`, `market`, or `transit`
- 1 editorial or high-completion anchor: `mode`, `gallery`, `formal`, `ceremony`, or `outerwear`
- 1 social or nightlife anchor: `night`, `date`, `club`, `lounge`, or `theater`
- 1 movement, rest, or destination anchor: `resort`, `active`, `dance`, `home`, or `swim`

This is a balance rule, not a fixed category list. If the user gives a theme
such as nightlife, winter coats, resort, or home party, bias the random draw
toward that theme while still keeping visible variety.
