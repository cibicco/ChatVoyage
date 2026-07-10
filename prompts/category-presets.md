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
- `music-night`: live music, listening room, concert bar, jazz room, or late music social styling where listening and talking matter more than dancing
- `bar`: wine bar, cocktail bar, standing bar, cafe bar, or night-drink social styling without requiring a dance floor
- `disco`: disco, DJ floor, retro club night, or nightlife styling where dancing, light, and rhythm are the main context
- `theater`: theater, concert, fado, live house, opera, or performance-going styling
- `gallery`: museum, art fair, exhibition opening, or design-event styling
- `ceremony`: wedding guest, reception, award dinner, or formal daytime event styling
- `home`: home party, roomwear, studio apartment, balcony, or relaxed indoor styling
- `swim`: pool, beach, spa, or water-side swimwear styling
- `outerwear`: coat, jacket, cape, leather, trench, or outer-layer-focused styling
- `dance`: dance lesson, rehearsal, club movement, or performance-practice styling
- `market`: flea market, food market, bookstore market, or local shopping styling
- `bookstore`: bookstore, library-shop, reading room, zine fair, or literary retail styling
- `transit`: train, ferry, airport, station, night bus, taxi stand, or arrival/departure styling

## Metadata Axes

The historical `fashion category` slug is kept as a filename and compatibility
label, but it mixes several concepts. For browsing and review, also record
these four independent axes for each image:

- `occasion`: why this outfit exists in the person's day, such as everyday,
  creative-culture, night-out, music-night, bar-night, social-date,
  formal-event, work, travel, movement, leisure, home, or weather-layer.
- `venue`: the type of place, such as city-outdoor, market-retail,
  museum-gallery, dining-bar, music-club, disco-floor, bookstore-library,
  event-venue, workplace, transit-hub, home-interior, waterfront-resort, or
  studio-sports.
- `activity`: what she is doing, such as city-walk, shopping, viewing-design,
  dining-drinks, listening-music, talking, dancing, performance-going,
  attending-event, reading-browsing, working, moving, relaxing, holiday,
  sport-practice, or weather-walk.
- `outfit`: the garment structure, such as casual-separates, tailoring, dress,
  skirt-skort, trousers-shorts, outerwear-layer, swimwear, activewear, or
  eveningwear.

These axes should be inferred from the actual prompt and accepted image, not
copied blindly from the category. For example, `gallery` usually means
creative-culture / museum-gallery / viewing-design, but the outfit can still
be tailoring, dress, skirt-skort, or casual-separates depending on the image.

## Secondary Tag Vocabulary

Secondary tags add search context without replacing the primary category.

- Weather / season: `rain`, `snow`, `summer`, `winter`, `early-autumn`
- Fashion direction: `retro`, `craft`, `minimal`, `feminine`, `workwear`, `tailoring`
- Place: `gallery`, `harbor`, `theater`, `cafe`, `ryokan`, `waterfront`, `club`, `music-night`, `bar`, `disco`, `lounge`, `terminal`, `hotel`, `museum`, `home`, `pool`, `market`, `bookstore`
- Materials: `knit`, `velvet`, `satin`, `linen`, `denim`, `technical`
- Visual style: use one preset slug from `style-presets.md`

## Daily Selection Rule

```text
Select four primary categories that fit today's city, season, theme, and
requested outfit. Avoid repeating the same four categories by habit. Use each
selected primary category as the filename prefix:

01-{category}-{look-name}.webp
02-{category}-{look-name}.webp
03-{category}-{look-name}.webp
04-{category}-{look-name}.webp
```

Record secondary tags for each image in the monthly generation log. Add a new
stable primary category or secondary tag when a daily theme needs one that is
not covered by the vocabulary above.

## Random Selection Guidance

For ordinary daily generation, choose four categories with this balance:

- 1 practical or daytime anchor: `street`, `office`, `weekend`, `travel`, `market`, or `transit`
- 1 editorial or high-completion anchor: `mode`, `gallery`, `formal`, `ceremony`, or `outerwear`
- 1 social or nightlife anchor: `night`, `date`, `club`, `lounge`,
  `music-night`, `bar`, `disco`, or `theater`
- 1 movement, rest, culture, or destination anchor: `resort`, `active`,
  `dance`, `home`, `swim`, or `bookstore`

This is a balance rule, not a fixed category list. If the user gives a theme
such as nightlife, winter coats, resort, or home party, bias the random draw
toward that theme while still keeping visible variety.
