# Lulu Land ad pipeline (for Claude on the VPS)

These are the tools that made the Oct 20 batch of 10 ads (`ads-delivery/`). Use them to make the **next 10 ads from the new shoot**.

## 0. Setup (once)
```bash
cd ~/projects/lululand && git fetch origin claude/zen-lamport-a254jk && git checkout origin/claude/zen-lamport-a254jk -- ad-pipeline ads-delivery
cd ad-pipeline
python3 -m pip install pillow numpy imageio-ffmpeg mido pillow-heif gdown
python3 -m pip download tinysoundfont --no-deps -d /tmp/tsf && python3 -m pip install --no-deps /tmp/tsf/tinysoundfont-*.whl   # its pyaudio dependency won't build; it isn't needed
mkdir -p sf && curl -L -o sf/GeneralUser-GS.sf2 https://raw.githubusercontent.com/mrbumpy409/GeneralUser-GS/main/GeneralUser-GS.sf2   # SoundFont, commercial use allowed
```
The repo must be at `~/projects/lululand`. If it's somewhere else, set `LULULAND_REPO`, because the brand art comes from `site/images/paint/`.

## 1. Get the new shoot
- Drive folder: https://drive.google.com/drive/folders/1isHmyLfd9b3h6Xm1GzpU-srtD4UZIrv_
- It holds one file: `iCloud Photos from Fariza James.zip` (648 MB), file id `1ehfxotI0-xnztmyQxpsalDbsJRFEX9Dz`.
```bash
mkdir -p ~/lululand-media/shoot2 && cd ~/lululand-media
gdown 1ehfxotI0-xnztmyQxpsalDbsJRFEX9Dz -O shoot2.zip    # if gdown is refused, ask the owner to set the file to "Anyone with the link" for an hour
unzip -q shoot2.zip -d shoot2
cd ~/projects/lululand/ad-pipeline && python3 index_media.py ~/lululand-media/shoot2 ./work
python3 sheet.py       # out/sheets/vid*.jpg and ph*.jpg — LOOK at every sheet before picking shots
```
`index_media.py` converts HEIC to JPEG and makes 30 fps H.264 proxies of every video, then numbers them: `V(n, ...)` are videos and `P(n, ...)` are photos, in sheet order.

## 2. Make 10 NEW ads (5 × 30 s, 5 × 15 s)
- Copy `example_ads_oct20.py` to `ads3.py`. Its clip and photo numbers point at the OLD shoot, so replace every shot after looking at the sheets.
- Each ad needs its own concept, music and transitions, different from all 20 earlier ads. The concepts already used:
  - Original batch: general walk-in, $59 birthday, parents party, pour art, slime, grand-opening tour.
  - Oct 20 batch: movie trailer, Top 5 game, before/after, birthday in 5 scenes, rainy weekend, oddly satisfying, slime beat, grand-opening ticket, shopping break, POV first visit.
- Music: write 10 new cues in `songs.py` (genres not used yet, e.g. bossa nova, K-pop dance, surf rock, gospel claps, cumbia, sea shanty, ska, bluegrass, synthwave, steel drums). Or make vocal kids-pop on the 5090 the way the earlier vocal versions were made. Each cue's length must be the ad length, with cuts timed to the beat (`build(..., bpm, ...)`). Set `s.mix` levels so the melody sits clearly above the drums.
- Tools in `lib2.py`:
  - Shot types: `V`, `P`, `C` (color card), `SPLIT`, `GRID`, `POLA`.
  - Looks via `fx`: `film`, `lofi`, `gray`, `colorpop`, `warm`, `shake`, `punch`, `flash`, `slow`.
  - Overlay animations: `pop`, `up`, `left`, `right`, `fade`, `none`, `rain`.
  - Transitions: any ffmpeg xfade type, set with `tr=(type, beats)`.
- Facts (keep them exact):
  - Store phone (818) 668-3342.
  - Offer: Grand Opening · first 10 new families · Lulu Party $65 → **$59 per kid** · min. 8 kids · 15% service fee not included.
  - Hours: Mon–Thu 10am–8pm, Fri–Sat 10am–9pm, Sun 11am–7pm.
  - Address: Westfield Topanga 2nd Floor · lululandkids.com.
  - Every party is 2 hours.
- Keep text between y≈160 and y≈1450 (phone UI covers the rest). `center_text` auto-shrinks text that is too wide.

## 3. Check every ad before delivering
`./tile.sh out/<ad>.mp4 out/tile.jpg` shows one frame every 0.5 s. Look at each one for:
- overlapping or cut-off text, and title art covering the hours box;
- sideways clips (use `rot=90` in `crop=` for photos, or `rot=` in fx for videos);
- squashed photos;
- other stores' logos;
- empty or black frames.

## 4. Deliver
1. Claude.ai dashboard https://claude.ai/artifact/G7q5h8zGQG63xni12gF7W8:
   - Upload the MP4s as assets (`Artifact` publish, `asset: true`, `file_paths`).
   - Add posters `ads/<name>.jpg` (540×960).
   - Put the new entries first in `ads.json`, with `"isNew": true`, `"added": "<YYYY-MM-DD>"` and `"style": "<music genre>"`, then republish `ads.json` and the posters. Read the live `ads.json` first and keep every other entry.
   - The page then shows a "🆕 Added <date>" banner and "NEW · <date>" tags on its own.
2. Staff site https://lululand.chcking.com/media-picks/:
   - Copy the MP4s and posters into its `ads/` folder and add the same entries.
   - Set the banner and date tags as in `ads-delivery/README.md`.
   - Use plain `<a href download>` links so phones can save the files.
3. Tell the owner in Korean, in a few lines: the 10 titles, the date tag, and both links.
