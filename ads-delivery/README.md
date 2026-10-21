# Lulu Land ads — delivery folder for the VPS staff page

These are the finished ad videos for the staff page at https://lululand.chcking.com/media-picks/ (access code on the server). This folder is outside `site/`, so the lululandkids.com cron never serves it.

## Added 2026-10-20 (10 new ads)
- `ads/*.mp4` and `ads/*.jpg`: the 10 videos and their posters.
- `new-ads-2026-10-20.json`: their list entries, with `url` already pointing to `ads/<file>`. Each entry has `"isNew": true`, `"added": "2026-10-20"` and `"style"` (the music genre).
- `dashboard-index.html`: the claude.ai dashboard page. Copy the Ads-tab UI from it: `renderAds()` plus the `.ads-group`, `.date-tag` and `.ad.is-new` CSS.

## Deploy on the VPS (Claude on the VPS does this)
1. `git clone` (first time) or `git pull` this repo into `/root/projects/lululand-ads`.
2. Copy `ads/*` into the server's `ads/` folder, next to the 10 vocal ads already there.
3. Put the 10 new entries first in the server's ads list, and keep the existing 10.
4. Add the Ads-tab UI to the server page:
   - A rose banner "🆕 Added October 20, 2026 · 10 ads" above the new ads, then an "Earlier ads" banner.
   - A "NEW · OCT 20" tag and a rose outline on each new card.
   - Filter chips "🆕 New · Oct 20" and "🎂 Birthday parties".
   - "♪ style" in front of each file name.
5. Downloads on the server are plain `<a href="ads/<file>" download>` links, so staff can save them on any phone or computer. Keep the access-code login.
6. Check: log in. Ads shows 20 ads with the new 10 on top under the Oct 20 banner. Each new MP4 plays and downloads, and the phone layout has no sideways scroll.
