"""Contact sheets so you can SEE the material before choosing shots.
usage: python3 sheet.py   -> out/sheets/vid*.jpg (3 frames per clip, labelled V<n> <time>) and ph*.jpg (P<n>)"""
import os, subprocess
from lib30 import items, photos, vsrc, psrc, FF, A
from PIL import Image, ImageDraw, ImageFont, ImageOps
D = os.path.dirname(os.path.abspath(__file__)) + '/out/sheets'; os.makedirs(D, exist_ok=True)
f = ImageFont.truetype(A + '/RammettoOne-d182e5.ttf', 22); tw, th = 150, 266
def frame(n, t, out):
    subprocess.run([FF, '-y', '-loglevel', 'error', '-ss', str(t), '-i', vsrc(n), '-frames:v', '1', '-vf', f'scale={tw}:{th}:force_original_aspect_ratio=increase,crop={tw}:{th}', out], check=True)
def sheet(tiles, out, cols):
    rows = (len(tiles) + cols - 1) // cols; im = Image.new('RGB', (cols * tw, rows * (th + 26)), 'white'); d = ImageDraw.Draw(im)
    for j, (lab, p) in enumerate(tiles):
        x, y = (j % cols) * tw, (j // cols) * (th + 26); im.paste(Image.open(p).convert('RGB'), (x, y + 26)); d.text((x + 4, y + 2), lab, font=f, fill='black')
    im.save(out)
vt = []
for n, i in enumerate(items):
    for k, fr in enumerate((0.12, 0.5, 0.88)):
        p = f'{D}/v{n}_{k}.png'; frame(n, i['duration'] * fr, p); vt.append((f'V{n} {i["duration"] * fr:.1f}s', p))
for s in range(0, len(vt), 45): sheet(vt[s:s + 45], f'{D}/vid{s // 45}.jpg', 9)
pt = []
for n in range(len(photos)):
    im = Image.open(psrc(n)).convert('RGB'); im.thumbnail((tw, th)); c = Image.new('RGB', (tw, th), 'gray'); c.paste(im, ((tw - im.width) // 2, (th - im.height) // 2)); p = f'{D}/p{n}.png'; c.save(p); pt.append((f'P{n}', p))
for s in range(0, len(pt), 60): sheet(pt[s:s + 60], f'{D}/ph{s // 60}.jpg', 12)
print('sheets in', D)
