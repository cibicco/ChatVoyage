# GitHub Pages Workflow

GitHub Pages is the preferred publishing path for Chat Voyage browsing.

## Scope

- Publish the existing static site: `index.html`, `albums.html`, `album.html`,
  `assets/`, CSS, JS, and WebP images.
- Keep generated images and album metadata in this repository as the source of
  truth.
- Use browser `localStorage` feedback in the album UI for lightweight personal
  review. This feedback is device/browser-local and is not a shared database.
- Do not use Notion as the main review or gallery surface unless the workflow is
  explicitly reopened.

## Why Pages

- The current site is already static.
- Current image assets are small enough for Pages: `assets/` is about 30 MB and
  `assets/daily/` is about 29 MB as of 2026-06-17.
- The existing album UI and localStorage feedback can run without an application
  server.

## Publication Shape

Recommended setup:

1. Push the repository to GitHub.
2. Enable GitHub Pages for the repository.
3. Publish from the `main` branch root if the repository is dedicated to Chat
   Voyage.
4. Confirm these URLs load:
   - `/index.html`
   - `/albums.html`
   - `/album.html?set=2026-06-16-busan-seaglass-coastal-motion`
5. After each daily generation, run:

```sh
python3 scripts/validate_gallery.py
git status --short --branch
```

## Notes

- GitHub Pages is a viewing surface, not a private image database.
- If the repository or Pages site is public, generated images are public.
- If private publishing is required, confirm GitHub account/organization plan
  support before depending on Pages.
- Notion trial artifacts can stay in the repo as historical tooling, but they
  are not part of the daily path.
