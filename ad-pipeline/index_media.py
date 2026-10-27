"""Index a folder of photos/videos (e.g. the unzipped iCloud export) for the ad pipeline.
usage: python3 index_media.py <media_dir> [work_dir]
- HEIC/HEIF photos -> JPEG copies (pillow-heif); every video -> a 1080x1920-friendly H.264 proxy (fast to cut)
- writes <work_dir>/index.json: {"photos": [{path, src, w, h}], "videos": [{path, src, duration}]}
"""
import sys, os, json, subprocess, imageio_ffmpeg
from PIL import Image, ImageOps
FF = imageio_ffmpeg.get_ffmpeg_exe()
src = os.path.abspath(sys.argv[1]); work = os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'work'))
os.makedirs(work + '/photos', exist_ok=True); os.makedirs(work + '/videos', exist_ok=True)
try:
    import pillow_heif; pillow_heif.register_heif_opener()
except ImportError:
    print('pip install pillow-heif  (needed for .HEIC)')
PH = ('.jpg', '.jpeg', '.png', '.heic', '.heif', '.webp'); VI = ('.mov', '.mp4', '.m4v')
files = sorted(os.path.join(r, f) for r, _, fs in os.walk(src) for f in fs if not f.startswith('._'))
photos, videos = [], []
for f in files:
    ext = os.path.splitext(f)[1].lower(); base = os.path.splitext(os.path.basename(f))[0]
    if ext in PH:
        out = f'{work}/photos/{base}.jpg'
        if not os.path.exists(out):
            im = ImageOps.exif_transpose(Image.open(f)).convert('RGB'); im.thumbnail((2400, 2400)); im.save(out, quality=92)
        w, h = Image.open(out).size; photos.append(dict(path=out, src=f, w=w, h=h))
    elif ext in VI:
        out = f'{work}/videos/{base}.mp4'
        if not os.path.exists(out):  # autorotates; long side 1920, 30 fps CFR
            subprocess.run([FF, '-y', '-loglevel', 'error', '-i', f, '-vf', "scale='if(gt(iw,ih),1920,-2)':'if(gt(iw,ih),-2,1920)',fps=30,format=yuv420p",
                            '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-c:a', 'aac', '-b:a', '160k', out], check=True)
        p = subprocess.run([FF, '-i', out], capture_output=True, text=True).stderr
        d = p.split('Duration: ')[1].split(',')[0]; hh, mm, ss = d.split(':'); dur = int(hh) * 3600 + int(mm) * 60 + float(ss)
        videos.append(dict(path=out, src=f, duration=round(dur, 2)))
json.dump(dict(photos=photos, videos=videos), open(work + '/index.json', 'w'), indent=1)
print(len(photos), 'photos,', len(videos), 'videos ->', work + '/index.json')
