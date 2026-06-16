# Notion Gallery Import

This workflow uploads a small Chat Voyage sample to a private Notion database.
It was a trial and is no longer the primary Chat Voyage publishing path.

## Current Decision

Notion is not the main Chat Voyage viewing or review surface. Keep this document
as a record of the trial and as a reference only if Notion is revisited later.
Use the static album site, preferably published through GitHub Pages, as the
primary browsing surface.

## Scope

- First trial: latest 40 images.
- Grain: one Notion row per image.
- Use: private browsing and preference notes.
- Database name: `Chat Voyage Images`.
- Primary view: Gallery with image covers. Notion is used for review,
  selection, and metadata browsing, not as the only source archive.

## Database Design

Keep one Notion record per image. Store the actual uploaded image in the
`Image` files property and use that property or the page cover for gallery card
previews. Keep page body content short so the database stays useful as a fast
review surface.

The importer currently creates these properties:

| Property | Type | Purpose |
| --- | --- | --- |
| `Name` | title | Stable display name: date, variant, city, image title. |
| `Image` | files | Uploaded WebP image used for visual browsing. |
| `Date` | date | Date seed. |
| `Status` | select | Review workflow: `Generated`, `Keep`, `Reject`, `Favorite`, `Posted`. |
| `Set` | rich text | Album/set title. |
| `Batch ID` | rich text | Set slug for grouping a four-image run. |
| `Image No` | number | Existing Chat Voyage image index. |
| `Variant` | number | Stable variant number for the image within the batch. |
| `City` | rich text | City label from the set. |
| `Place` | rich text | Place label from the image metadata. |
| `Category` | select | Fashion category. |
| `Art style` | select | Style preset. |
| `Age band` | select | Target adult age band. |
| `Theme` | rich text | Set summary or short theme. |
| `Scene` | rich text | Compact scene/image description. |
| `Prompt Short` | rich text | Short prompt/search text derived from metadata. |
| `Model` | select | Generation model, blank until reliably tracked. |
| `Aspect Ratio` | select | `1:1`, `portrait`, or `landscape`. |
| `File Size MB` | number | Uploaded local file size. |
| `Width` | number | Pixel width, when Pillow can read it. |
| `Height` | number | Pixel height, when Pillow can read it. |
| `Rating` | select | Personal rating. Supports `1`-`5` plus legacy `Love`/`Good`/`Pass`. |
| `Preference` | multi-select | What worked: art style, person, outfit, color, silhouette, pose, place, vibe. |
| `Note` | rich text | Short review note. |
| `Source path` | rich text | Local project path. |
| `Album URL` | url | Local album route/path reference. |
| `Set slug` | rich text | Stable project set slug. |

## Recommended Views

Notion database views are partly UI-managed. Configure the active database as:

| View | Type | Filter / Sort | Card setup | Purpose |
| --- | --- | --- | --- | --- |
| `Images Only` | Gallery | Sort `Date` desc, `Batch ID` desc, `Variant` asc | Preview `Image` or page cover, medium/large cards, hide properties | Fast visual scan. |
| `Latest` | Gallery | Current month or last 7 days; same sort | Show `Status`, `Rating` only if useful | Daily review. |
| `Keep / Favorite` | Gallery | `Status` is `Keep` or `Favorite` | Image preview | Selection shortlist. |
| `Rejected` | Gallery or table | `Status` is `Reject` | Image preview plus `Note` | Failure pattern review. |
| `Metadata Table` | Table | Sort `Date` desc, `Variant` asc | Show editable metadata | Bulk cleanup and notes. |
| `By Date` | Gallery or board | Group by date if available | Image preview | Set-level review. |

## Page Body Template

Each image page should stay light:

```md
## Prompt

Short prompt/search text. Add the full generation prompt only when it is
available and useful for reuse.

## Scene

Compact scene, movement, place, time, and mood description.

## Review Notes

Post-review comments and next-generation instructions.
```

## Naming Rules

- Name: `YYYY-MM-DD / vNN / City - Image title`
- Batch ID: existing Chat Voyage set slug, e.g.
  `2026-06-16-busan-seaglass-coastal-motion`
- Image file: keep the existing Chat Voyage WebP filename under
  `assets/daily/YYYY-MM-DD-slug/`.

The generated filenames are more descriptive than the generic
`YYYY-MM-DD-fashion-01-v01.webp` pattern, so the repo filenames remain the
source of truth.

## Notion Setup

1. Open Notion developer connections.
2. Create a connection named `Chat Voyage Importer`.
3. Give it content insert/read/update capability.
4. Copy the internal integration token.
5. Create or choose a private Notion page to contain the database.
6. Invite/connect `Chat Voyage Importer` to that page.
7. Copy the parent page ID from the page URL.

Do not commit the real token. Put it in `.notion.env`, which is ignored by git:

```sh
NOTION_TOKEN=secret_xxx
NOTION_PARENT_PAGE_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_DATABASE_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_DATA_SOURCE_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_VERSION=2022-06-28
NOTION_DATA_SOURCE_VERSION=2026-03-11
```

## Dry Run

```sh
python3 scripts/notion_upload_gallery.py --limit 40
```

The dry run prints the selected image rows and total upload size without
sending data to Notion.

## Upload

Uploading sends the selected local WebP images and metadata to Notion:

```sh
python3 scripts/notion_upload_gallery.py --limit 40 --confirm-upload
```

The script creates a Notion database under the parent page and uploads each
image to the database's `Image` property.

The script is intentionally dry-run by default. Without `--sync-existing`, it
creates a new database when `--confirm-upload` is used. With
`--sync-existing`, it updates existing rows matched by `Source path`; add
`--append-missing` only when missing rows should be uploaded into the existing
data source.

## Existing Database Sync

For the current `Chat Voyage Images` trial database, use the image data source
directly. This avoids Notion's multi-data-source dashboard surface.

Current IDs:

- Database ID: `381ecca2-7ba4-81b5-b327-fc2e5a8a55ac`
- Image data source ID: `381ecca2-7ba4-8124-965d-000b2171071a`
- Empty table data source ID created during UI exploration:
  `381ecca2-7ba4-8047-a3d2-000bb4298c01`

Dry-run matching existing rows:

```sh
python3 scripts/notion_upload_gallery.py \
  --limit 40 \
  --sync-existing \
  --data-source-id 381ecca2-7ba4-8124-965d-000b2171071a
```

Apply metadata updates to existing rows:

```sh
python3 scripts/notion_upload_gallery.py \
  --limit 40 \
  --sync-existing \
  --data-source-id 381ecca2-7ba4-8124-965d-000b2171071a \
  --confirm-upload
```

This mode updates matched pages by `Source path` and does not reupload images.
Use `--append-missing` only when adding new generated images to the existing
Notion data source.

## 2026-06-16 Trial Result

- Parent page: `Chat Voyage`
- Database: `Chat Voyage Images`
- Database ID: `381ecca2-7ba4-81b5-b327-fc2e5a8a55ac`
- Uploaded rows: 40
- Uploaded image bytes: about 8.1 MB
- Source range: latest 10 album sets, 2026-06-16 through 2026-06-09
- UI update: the gallery view was restored from the accidental dashboard
  surface, renamed `Images Only`, set to page-cover card previews, medium
  cards, media fit on, popup page opening, sorted by `Date` descending and
  `Image No` ascending.
- Data source dry-run after the dashboard incident matched 40 existing rows and
  found 0 missing rows.

The token used for upload was shared in the chat during setup. Rotate or
regenerate the Notion connection token after the trial if continuing the
workflow.
