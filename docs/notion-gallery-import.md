# Notion Gallery Import

This workflow uploads a small Chat Voyage sample to a private Notion database.

## Scope

- First trial: latest 40 images.
- Grain: one Notion row per image.
- Use: private browsing and preference notes.
- Database name: `Chat Voyage Images`.

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
NOTION_VERSION=2022-06-28
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

## 2026-06-16 Trial Result

- Parent page: `Chat Voyage`
- Database: `Chat Voyage Images`
- Database ID: `381ecca2-7ba4-81b5-b327-fc2e5a8a55ac`
- Uploaded rows: 40
- Uploaded image bytes: about 8.1 MB
- Source range: latest 10 album sets, 2026-06-16 through 2026-06-09

The token used for upload was shared in the chat during setup. Rotate or
regenerate the Notion connection token after the trial if continuing the
workflow.
