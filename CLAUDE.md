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

## Where things live (learned from past edits)
- Text that appears in the RSC payloads: `<page>.txt`, `<page>/__next._full.txt`, `__next._index.txt`, `__next.<route>.__PAGE__.txt`, and the inline `self.__next_f.push(...)` strings in each `.html` (escaped as `\"` and `&`). Change all of them, or React throws hydration error #418.
- Header nav and "Book a party" hrefs: `site/_next/static/chunks/1zks_o_wpjea-.js`. Party package data (prices, 2-hour durations): `site/_next/static/chunks/2vmbnu1c4it9u.js`.
- Global CSS: `site/_next/static/chunks/3eyzy37nwwzfh.css`. A rule appended at the end keeps h2 title images full width, so `#packages` jump links land correctly.
- New sections on home must go before the `<!--$--><!--/$-->` marker, or hydration breaks.
- SEO: `site/robots.txt`, `site/sitemap.xml`, canonical and og:url tags, EntertainmentBusiness JSON-LD in `index.html` (hours and phone live there too).

## Current business facts (keep consistent everywhere)
- Store (818) 668-3342 (`tel:+18186683342`, HighLevel tracking number) · Mobile (747) 388-6365 · info@lululandkids.com
- 6600 Topanga Canyon Blvd Suite 70, Canoga Park, CA 91303 (Westfield Topanga, 2nd floor)
- Hours (mall hours): Mon–Thu 10am–8pm, Fri–Sat 10am–9pm, Sun 11am–7pm
- Facebook https://www.facebook.com/profile.php?id=61594077180718 · Instagram https://www.instagram.com/lululand.la/
- All party packages are 2 hours. Prices exclude a 15% service fee. "Book a party" buttons go to `/parties#packages`. Home party cards link to `/parties?package=X#packages`.
- Ad videos and the media dashboard live outside this repo (owner's claude.ai artifact). Don't commit photos or videos of kids' faces beyond what's already on the site.
