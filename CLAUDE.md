# Lulu Land — lululandkids.com

## What this repo is
- `site/` = the exact files served from Namecheap cPanel `public_html` (Next.js static export).
- Pushing to `main` (changes under `site/`) auto-deploys via `.github/workflows/deploy.yml` (FTPS, changed files only).
- The original Next.js source is not in this repo; edit the exported files directly.

## Pages
- `site/index.html` (home), `create.html`, `parties.html`, `gallery.html`, `visit.html`, `404.html`
- Images: `site/images/`  ·  Next assets: `site/_next/` (do not hand-edit minified chunks unless necessary)

## Editing rules
- Change visible text/links/images in the page's `.html` file.
- Each page also has a matching `.txt` RSC payload (e.g. `create.txt`, `__next.*.txt`). Next.js uses it for in-site navigation.
  After editing an `.html`, make the same text change in the matching `.txt`, or delete that `.txt` so Next falls back to a full page load.
- Keep changes minimal; don't reformat whole files.
- Never commit secrets. FTP credentials live only in GitHub Secrets: `FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD`.
- Server-only paths never deployed from here: `cgi-bin/`, `nc_assets/`, `.well-known/`, `.htaccess`.
- The inquiry form backend runs separately on the server (`~/party-inquiry`, Node app) and is not in this repo.

## Verify
After the Deploy action finishes (~1–2 min), check https://lululandkids.com with a hard refresh.
