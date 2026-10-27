"""Second ad batch: beat-timed segments, real transitions (xfade), per-shot looks, music + SFX mix."""
import os, sys, subprocess, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from lib30 import *            # W,H, colors, fonts R/N, text_layer, pill, paint, big, chip, prep_photo, items, vsrc, psrc, FF, O
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import mus
OUT = HERE + '/out'; SEG = OUT + '/seg'; os.makedirs(SEG, exist_ok=True); os.makedirs(OUT + '/sfx', exist_ok=True)
DUR = {n: (i['duration'] or 0) for n, i in enumerate(items)}

# ---------- overlay layers (full-frame RGBA PNGs) ----------
def layer(name, fns):
    im = canvas()
    for f in fns: f(im)
    p = f'{O}/{name}.png'; im.save(p); return name
def scaled(name, s):
    p2 = f'{O}/{name}@{s}.png'
    if not os.path.exists(p2):
        im = Image.open(f'{O}/{name}.png'); w, h = int(W * s), int(H * s)
        big_ = im.resize((w, h), Image.LANCZOS); c = canvas(); c.alpha_composite(big_.crop(((w - W) // 2, (h - H) // 2, (w - W) // 2 + W, (h - H) // 2 + H))); c.save(p2)
    return f'{name}@{s}'
def tbox(txt, size=58, fg=WHITE, bg=(0, 0, 0, 215), y=1180, pad=(34, 20), font=None):
    """TikTok-style caption: text in a rounded box"""
    def f(im):
        t = text_layer(txt, (font or N)(size), fg, pad=0); w, h = t.width + pad[0] * 2, t.height + pad[1] * 2; x = (W - w) // 2
        d = ImageDraw.Draw(im); d.rounded_rectangle([x, y, x + w, y + h], 22, fill=bg); im.alpha_composite(t, (x + pad[0], y + pad[1]))
    return f
def _fit(l, maxw=W - 90):
    if l.width > maxw: l = l.resize((maxw, round(l.height * maxw / l.width)), Image.LANCZOS)
    return l
def center_text(txt, font, fill, y, stroke=0, stroke_fill=INK, spacing=0):
    def f(im):
        if spacing:
            ls = [text_layer(c, font, fill, stroke=stroke, stroke_fill=stroke_fill, pad=4) for c in txt]
            tw = sum(l.width for l in ls) + spacing * (len(ls) - 1); row = Image.new('RGBA', (tw, max(l.height for l in ls)), (0, 0, 0, 0)); x = 0
            for l in ls: row.alpha_composite(l, (x, 0)); x += l.width + spacing
            l = _fit(row)
        else:
            l = _fit(text_layer(txt, font, fill, stroke=stroke, stroke_fill=stroke_fill))
        im.alpha_composite(l, ((W - l.width) // 2, y))
    return f
def solid(c): return lambda im: im.alpha_composite(Image.new('RGBA', (W, H), c))
def letterbox(h=250):
    def f(im):
        d = ImageDraw.Draw(im); d.rectangle([0, 0, W, h], fill=(0, 0, 0, 255)); d.rectangle([0, H - h, W, H], fill=(0, 0, 0, 255))
    return f
def img_at(name, width, x, y, rot=0):
    def f(im):
        t = paint(name, width)
        if rot: t = t.rotate(rot, expand=True, resample=Image.BICUBIC)
        im.alpha_composite(t, (x if x is not None else (W - t.width) // 2, y))
    return f

def pola_photo(n, w, h, fx=0.5, fy=0.5, rot=0):
    im = ImageOps.exif_transpose(Image.open(psrc(n))).convert('RGB')
    if rot: im = im.rotate(rot, expand=True)
    im = wb(im); im = ImageOps.autocontrast(im, cutoff=(0.4, 0.6), preserve_tone=True); im = ImageEnhance.Color(im).enhance(1.1)
    Wd, Hd = im.size; ar = w / h; cw = min(Wd, Hd * ar); ch = cw / ar
    l = max(0, min(Wd - cw, fx * Wd - cw / 2)); t = max(0, min(Hd - ch, fy * Hd - ch / 2))
    return im.crop((round(l), round(t), round(l + cw), round(t + ch))).resize((w, h), Image.LANCZOS)

# ---------- segments ----------
def V(n, ss, beats, ov=(), **fx): return dict(kind='v', n=n, ss=ss, beats=beats, ov=list(ov), fx=fx)
def P(n, beats, ov=(), crop=None, **fx): return dict(kind='p', n=n, beats=beats, ov=list(ov), crop=crop or {}, fx=fx)
def C(color, beats, ov=(), **fx): return dict(kind='c', color=color, beats=beats, ov=list(ov), fx=fx)
def SPLIT(a, b, beats, ov=(), **fx): return dict(kind='split', a=a, b=b, beats=beats, ov=list(ov), fx=fx)
def GRID(srcs, beats, ov=(), **fx): return dict(kind='grid', srcs=srcs, beats=beats, ov=list(ov), fx=fx)
def POLA(n, beats, bg, rot=-4, ov=(), crop=None, **fx): return dict(kind='pola', n=n, beats=beats, bg=bg, rot=rot, ov=list(ov), crop=crop or {}, fx=fx)

def look(fx, L):
    """per-shot look filters appended after scale"""
    f = []
    if fx.get('gray'): f.append('hue=s=0,eq=contrast=0.95:brightness=-0.04')
    if 'colorpop' in fx: t = fx['colorpop']; f.append(f"hue=s='min(1,max(0,(t-{t})/0.35))'")
    if fx.get('warm'): f.append('colorbalance=rs=0.06:gs=0.02:bs=-0.06,eq=saturation=1.05')
    if fx.get('cool'): f.append('colorbalance=rs=-0.04:bs=0.06,eq=contrast=1.08:saturation=0.9')
    if fx.get('film'): f.append('eq=contrast=1.12:saturation=0.85,noise=alls=10:allf=t,vignette=PI/4.5')
    if fx.get('lofi'): f.append('eq=saturation=0.8:contrast=0.92:gamma=1.05,colorbalance=rs=0.05:bs=-0.03,noise=alls=7:allf=t,vignette=PI/5')
    if fx.get('soft'): f.append('gblur=sigma=0.6,eq=saturation=1.08:brightness=0.02')
    if fx.get('shake'): f.append(f"scale=1188:2112,crop={W}:{H}:x='54+30*sin(t*37)':y='96+30*cos(t*29)'")
    for tp in fx.get('punch', []):  # quick zoom punch at time tp
        f.append(f"scale=w='if(between(t,{tp},{tp}+0.25),{W}*(1.12-0.48*(t-{tp})),{W})':h='if(between(t,{tp},{tp}+0.25),{H}*(1.12-0.48*(t-{tp})),{H})':eval=frame,crop={W}:{H}")
    if 'flash' in fx: tf = fx['flash']; f.append(f"eq=brightness='if(between(t,{tf},{tf}+0.12),0.5*(1-(t-{tf})/0.12),0)':eval=frame")
    return (',' + ','.join(f)) if f else ''

def _photo_motion(k, fr, kind):
    if kind == 'in': z = f"1.0+0.10*on/{fr}"; x = "iw/2-(iw/zoom/2)"; y = "ih/2-(ih/zoom/2)"
    elif kind == 'out': z = f"1.10-0.10*on/{fr}"; x = "iw/2-(iw/zoom/2)"; y = "ih/2-(ih/zoom/2)"
    elif kind == 'left': z = "1.12"; x = f"(iw-iw/zoom)*(1-on/{fr})"; y = "ih/2-(ih/zoom/2)"
    elif kind == 'right': z = "1.12"; x = f"(iw-iw/zoom)*on/{fr}"; y = "ih/2-(ih/zoom/2)"
    elif kind == 'up': z = "1.12"; x = "iw/2-(iw/zoom/2)"; y = f"(ih-ih/zoom)*(1-on/{fr})"
    else: z = "1.0"; x = "0"; y = "0"
    return f"zoompan=z='{z}':x='{x}':y='{y}':d=1:s={W}x{H}:fps=30"

def src_chain(sp, L, idx, label):
    """returns (input args, filter producing [label]) for one source spec, used by split/grid"""
    if sp[0] == 'v':
        _, n, ss = sp[:3]; return ['-ss', str(ss), '-t', str(L), '-i', vsrc(n)], f"[{idx}:v]fps=30,scale=1080:1920:flags=lanczos,setsar=1"
    else:
        n = sp[1]; kw = sp[2] if len(sp) > 2 else {}; ph = prep_photo(n, **kw)
        return ['-framerate', '30', '-loop', '1', '-t', str(L), '-i', ph], f"[{idx}:v]scale=1080:1920,setsar=1"

def render_seg(seg, L, name, k):
    out = f'{SEG}/{name}_{k}.mp4'; fx = seg['fx']; fr = int(round(L * 30))
    kind = seg['kind']
    if kind == 'v':
        slow = fx.get('slow', 1.0); rot = fx.get('rot')
        inputs = ['-ss', str(seg['ss']), '-t', str(L / slow + 0.1), '-i', vsrc(seg['n'])]
        pre = {90: 'transpose=1,', -90: 'transpose=2,', 180: 'hflip,vflip,'}.get(rot, '')
        sl = f"setpts={slow}*PTS,minterpolate=fps=30:mi_mode=blend," if slow != 1.0 else ''
        fc = f"[0:v]{pre}{sl}fps=30,scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},setsar=1,eq=saturation=1.1:contrast=1.04,unsharp=5:5:0.5{look(fx, L)}[v0]"
    elif kind == 'p':
        ph = prep_photo(seg['n'], **seg['crop'])
        inputs = ['-framerate', '30', '-loop', '1', '-t', str(L), '-i', ph]
        fc = f"[0:v]{_photo_motion(k, fr, fx.get('move', 'in' if k % 2 else 'out'))},setsar=1{look(fx, L)}[v0]"
    elif kind == 'c':
        inputs = ['-f', 'lavfi', '-t', str(L), '-i', f"color=c={seg['color']}:s={W}x{H}:r=30"]
        fc = f"[0:v]setsar=1{look(fx, L)}[v0]"
    elif kind == 'split':
        ia, fa = src_chain(seg['a'], L, 0, 'a'); ib, fb = src_chain(seg['b'], L, 1, 'b'); inputs = ia + ib
        fc = (f"{fa},crop=1080:960:0:{seg['a'][3] if len(seg['a']) > 3 else 480}[a];{fb},crop=1080:960:0:{seg['b'][3] if len(seg['b']) > 3 else 480}[b];"
              f"[a][b]vstack=2,drawbox=x=0:y=954:w=1080:h=12:color=0x0b0706:t=fill{look(fx, L)}[v0]")
    elif kind == 'grid':
        inputs = []; parts = []
        for i, sp in enumerate(seg['srcs']):
            a, f = src_chain(sp, L, i, 'g'); inputs += a; parts.append(f"{f},scale=540:960,setsar=1[g{i}]")
        fc = ';'.join(parts) + f";[g0][g1]hstack[r0];[g2][g3]hstack[r1];[r0][r1]vstack,drawbox=x=534:y=0:w=12:h=1920:color=0x0b0706:t=fill,drawbox=x=0:y=954:w=1080:h=12:color=0x0b0706:t=fill{look(fx, L)}[v0]"
    elif kind == 'pola':
        im = pola_photo(seg['n'], 780, 1040, **seg['crop'])
        fr_ = Image.new('RGBA', (860, 1240), (255, 255, 255, 255)); fr_.paste(im, (40, 40))
        cap = seg['fx'].get('cap')
        if cap: t = text_layer(cap, R(52), NAVY, pad=0); fr_.alpha_composite(t, ((860 - t.width) // 2, 1110))
        fr_ = fr_.rotate(seg['rot'], expand=True, resample=Image.BICUBIC)
        sh = Image.new('RGBA', fr_.size, (0, 0, 0, 0)); sh.putalpha(fr_.getchannel('A').point(lambda a: int(a * .4))); sh = sh.filter(ImageFilter.GaussianBlur(14))
        bgc = Image.new('RGBA', (W, H), seg['bg']); x0, y0 = (W - fr_.width) // 2, (H - fr_.height) // 2 - 60
        bgc.alpha_composite(sh, (x0 + 10, y0 + 22)); bgc.alpha_composite(fr_, (x0, y0)); pp = f'{SEG}/{name}_{k}_pola.png'; bgc.convert('RGB').save(pp)
        inputs = ['-framerate', '30', '-loop', '1', '-t', str(L), '-i', pp]
        fc = f"[0:v]{_photo_motion(k, fr, 'in')},setsar=1{look(fx, L)}[v0]"
    last = 'v0'; j = inputs.count('-i')
    for o in seg['ov']:
        nm, tin = o[0], o[1]; anim = o[2] if len(o) > 2 else ('none' if nm.endswith(('e0', 'f0')) else 'up'); tout = o[3] if len(o) > 3 else None
        en = f":enable='lt(t,{tout})'" if tout else ''
        if anim == 'pop':
            for s_, a_, b_ in [(1.22, tin, tin + 0.06), (1.09, tin + 0.06, tin + 0.12)]:
                inputs += ['-loop', '1', '-t', str(L), '-i', f'{O}/{scaled(nm, s_)}.png']
                fc += f";[{last}][{j}:v]overlay=0:0:enable='between(t,{a_},{b_})'[v{j}]"; last = f'v{j}'; j += 1
            inputs += ['-loop', '1', '-t', str(L), '-i', f'{O}/{nm}.png']
            fc += f";[{last}][{j}:v]overlay=0:0:enable='gte(t,{tin + 0.12})*{('lt(t,%s)' % tout) if tout else 1}'[v{j}]"; last = f'v{j}'; j += 1
            continue
        inputs += ['-loop', '1', '-t', str(L), '-i', f'{O}/{nm}.png']
        if anim == 'rain':
            fc += f";[{last}][{j}:v]overlay=0:y='mod(t*900\\,160)-160'[v{j}]"
        elif anim == 'none':
            fc += f";[{last}][{j}:v]overlay=0:0:enable='gte(t,{tin})*{('lt(t,%s)' % tout) if tout else 1}'[v{j}]"
        else:
            d = 0.22; xy = {'up': f":y='70*max(0\\,1-(t-{tin})/{d})'", 'down': f":y='-70*max(0\\,1-(t-{tin})/{d})'",
                            'left': f":x='-160*max(0\\,1-(t-{tin})/{d})'", 'right': f":x='160*max(0\\,1-(t-{tin})/{d})'", 'fade': ''}[anim]
            fc += f";[{j}:v]format=rgba,fade=in:st={tin}:d={d}:alpha=1[o{j}];[{last}][o{j}]overlay=0:0{xy}{en}[v{j}]"
        last = f'v{j}'; j += 1
    fc += f";[{last}]tpad=stop_mode=clone:stop_duration=3,setsar=1,settb=AVTB,format=yuv420p[v]"
    subprocess.run([FF, '-y', '-loglevel', 'error'] + inputs + ['-filter_complex', fc, '-map', '[v]', '-t', f'{L:.4f}', '-r', '30',
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-an', out], check=True)
    return out

def build(name, song, bpm, SC, total, sfx=(), title=''):
    """SC: list of segments; each seg may carry 'tr': (xfade_type, beats) for the transition INTO the next segment."""
    spb = 60 / bpm
    for s in SC:
        if 'tr' in s['fx']: s['tr'] = s['fx'].pop('tr')
    T = [0]
    for s in SC: T.append(T[-1] + s['beats'] * spb)
    T[-1] = total
    d = [0] + [s.get('tr', (None, 0))[1] * spb if s.get('tr') else 0 for s in SC[:-1]] + [0]
    segs = []
    for k, s in enumerate(SC):
        L = (T[k + 1] + d[k + 1] / 2) - (T[k] - d[k] / 2)
        segs.append(render_seg(s, L, name, k))
    # assemble with xfade / hard cuts
    inputs = []; [inputs.extend(['-i', p]) for p in segs]
    fc = ''.join(f"[{k}:v]setsar=1,fps=30,settb=AVTB,format=yuv420p[i{k}];" for k in range(len(segs))); last = 'i0'
    for k in range(1, len(segs)):
        tr = SC[k - 1].get('tr')
        if tr and tr[0]:
            off = T[k] - d[k] / 2
            fc += f"[{last}][i{k}]xfade=transition={tr[0]}:duration={d[k]:.4f}:offset={off:.4f}[x{k}];"
        else:
            fc += f"[{last}][i{k}]concat=n=2:v=1:a=0[x{k}];"
        last = f'x{k}'
    vf = fc + f"[{last}]trim=duration={total},setpts=PTS-STARTPTS,format=yuv420p[v]"
    # audio: music + sfx
    ai = len(segs); inputs += ['-i', song]; amix = [f"[{ai}:a]atrim=0:{total},asetpts=PTS-STARTPTS[m]"]; labels = ['[m]']
    for i, (t, kind, gain) in enumerate(sfx):
        p = f'{OUT}/sfx/{kind}.wav'
        if not os.path.exists(p): mus.sfx(kind, p)
        inputs += ['-i', p]; amix.append(f"[{ai + 1 + i}:a]volume={gain},adelay={int(t * 1000)}|{int(t * 1000)}[s{i}]"); labels.append(f'[s{i}]')
    af = ';'.join(amix) + f";{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=first,alimiter=limit=0.93:level=false,afade=out:st={total - 0.03}:d=0.03[a]"
    final = f'{OUT}/{name}.mp4'
    subprocess.run([FF, '-y', '-loglevel', 'error'] + inputs + ['-filter_complex', vf + ';' + af, '-map', '[v]', '-map', '[a]', '-t', str(total),
                    '-c:v', 'libx264', '-preset', 'slow', '-crf', '20', '-maxrate', '4.5M', '-bufsize', '9M', '-pix_fmt', 'yuv420p', '-r', '30',
                    '-c:a', 'aac', '-b:a', '192k', '-ar', '44100', '-movflags', '+faststart'] + (['-metadata', f'title={title}'] if title else []) + [final], check=True)
    print(name, 'segments', len(segs), 'MB', round(os.path.getsize(final) / 1e6, 1)); return final, T
