# Lulu Land — lululandkids.com

## What this repo is
- `site/` = the exact files served from Namecheap cPanel `public_html` (Next.js static export).
- Deploy is automatic: the server pulls `main` every 5 minutes (cPanel cron) and copies `site/` into `public_html`. Nothing on the server is ever deleted by this; it only adds/overwrites files.
- The original Next.js source is not in this repo; edit the exported files directly.
- Repo is public. Never commit secrets, credentials, or private data.

## Pages
- `site/index.html` (home), `create.html`, `parties.html`, `gallery.html`, `visit.html`, `404.html`
- Images: `site/images/` · Next assets: `site/_next/` (do not hand-edit minified chunks unless necessary)

## Editing rules
- Change visible text/links/images in the page's `.html` file.
- Each page also has a matching `.txt` RSC payload (e.g. `create.txt`, `__next.*.txt`). Next.js uses it for in-site navigation. After editing an `.html`, make the same text change in the matching `.txt`, or delete that `.txt` so Next falls back to a full page load.
- Keep changes minimal; don't reformat whole files.
- Server-only paths that are not in this repo and must stay untouched: `cgi-bin/`, `nc_assets/`, `.well-known/`, `.htaccess`.
- The inquiry form backend runs separately on the server (`~/party-inquiry`, Node app) and is not in this repo.

## Verify
Within ~5 minutes of a commit to `main`, check https://lululandkids.com with a hard refresh.
