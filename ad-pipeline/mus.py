"""Tiny arranger: hand-written parts rendered with the GeneralUser GS SoundFont (commercial use allowed)."""
import os, subprocess, numpy as np, tinysoundfont as tsf, wave
HERE = os.path.dirname(os.path.abspath(__file__))
SF = HERE + '/sf/GeneralUser-GS.sf2'
import imageio_ffmpeg; FF = imageio_ffmpeg.get_ffmpeg_exe()
SR = 44100
NOTE = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}

def midi(n):
    """'C4', 'F#5', 'Bb3' -> midi number"""
    if isinstance(n, int): return n
    k = NOTE[n[0]]; i = 1
    while i < len(n) and n[i] in '#b': k += 1 if n[i] == '#' else -1; i += 1
    return k + 12 * (int(n[i:]) + 1)

CH = {'': [0, 4, 7], 'm': [0, 3, 7], '7': [0, 4, 7, 10], 'maj7': [0, 4, 7, 11], 'm7': [0, 3, 7, 10],
      'sus4': [0, 5, 7], 'sus2': [0, 2, 7], 'add9': [0, 4, 7, 14], '6': [0, 4, 7, 9], 'dim': [0, 3, 6], '9': [0, 4, 7, 10, 14], 'm9': [0, 3, 7, 10, 14]}
def chord(name, octave=4):
    r = name[0]; i = 1
    if len(name) > 1 and name[1] in '#b': r += name[1]; i = 2
    q = name[i:]; root = midi(r + str(octave))
    return [root + x for x in CH[q]]

class Song:
    def __init__(s, bpm, swing=0.0):
        s.bpm = bpm; s.swing = swing; s.ev = []; s.prog = {}
    def b2s(s, b):
        # swing: delay off-beat 8ths
        if s.swing:
            whole = np.floor(b * 2) / 2; frac = b * 2 - np.floor(b * 2)
            if abs((whole * 2) % 2 - 1) < 1e-6 and frac < 1e-6: b = b + s.swing * 0.5
        return b * 60.0 / s.bpm
    def inst(s, ch, prog, bank=0, drums=False, vol=100, pan=64, rev=40):
        s.prog[ch] = (bank, prog, drums, vol, pan, rev)
    def n(s, ch, beat, note, dur, vel=90):
        s.ev.append((s.b2s(beat), 1, ch, midi(note), vel)); s.ev.append((s.b2s(beat + dur) - 0.005, 0, ch, midi(note), 0))
    def notes(s, ch, beat, notes, dur, vel=90):
        for x in notes: s.n(ch, beat, x, dur, vel)
    def seq(s, ch, beat, text, vel=90, octave_shift=0):
        """'C5:1 E5:.5 r:.5 [C4,E4,G4]:2' durations in beats; returns end beat"""
        b = beat
        for tok in text.split():
            nm, d = tok.rsplit(':', 1); d = float(d)
            v = vel
            if nm.endswith('!'): nm = nm[:-1]; v = min(127, vel + 22)
            if nm != 'r':
                ns = nm.strip('[]').split(',') if nm.startswith('[') else [nm]
                for x in ns: s.n(ch, b, midi(x) + 12 * octave_shift, d * 0.95, v)
            b += d
        return b
    def drums(s, beat, bars, pat, steps=16, vel=95, ch=9, beats_per_bar=4):
        """pat: {note: 'x.x.X...'} X accent, x normal, o soft"""
        st = beats_per_bar / steps
        for bar in range(bars):
            for note, p in pat.items():
                for i, c in enumerate(p):
                    if c in 'xXo':
                        v = {'X': min(127, vel + 25), 'x': vel, 'o': int(vel * 0.55)}[c]
                        s.n(ch, beat + bar * beats_per_bar + i * st, note, st * 0.9, v)
    def _stem(s, ch, total):
        syn = tsf.Synth(samplerate=SR, gain=-6); sf = syn.sfload(SF)
        bank, prog, dr, vol, pan, rev = s.prog[ch]
        syn.program_select(ch, sf, 128 if dr else bank, prog, dr); syn.control_change(ch, 7, 110); syn.control_change(ch, 10, pan)
        ev = sorted([e for e in s.ev if e[2] == ch], key=lambda e: (e[0], e[1]))
        out = np.zeros((total, 2), np.float32); pos = 0
        for t, on, c, note, vel in ev:
            k = int(t * SR)
            if k >= total: break
            if k > pos: out[pos:k] = np.frombuffer(syn.generate(k - pos), np.float32).reshape(-1, 2); pos = k
            if on: syn.noteon(c, note, vel)
            else: syn.noteoff(c, note)
        if pos < total: out[pos:] = np.frombuffer(syn.generate(total - pos), np.float32).reshape(-1, 2)
        return out
    def render(s, length, path, tail=0.0, reverb=0.18, gain_db=0, fade_end=False):
        """Each channel is rendered alone, set to its target loudness (s.mix: dBFS RMS while playing), then summed."""
        total = int((length + tail) * SR); mixd = getattr(s, 'mix', {})
        out = np.zeros((total, 2), np.float32); s.levels = {}
        for ch in sorted(s.prog):
            x = s._stem(ch, total)
            e = np.sqrt(np.convolve((x ** 2).mean(1), np.ones(2048) / 2048, 'same'))
            act = e > 10 ** (-50 / 20)
            if not act.any(): continue
            rms = np.sqrt((x[act] ** 2).mean()); target = mixd.get(ch, -20)
            g = 10 ** (target / 20) / max(rms, 1e-9); s.levels[ch] = round(20 * np.log10(rms), 1)
            out += x * g
        out = out[:int(length * SR)]
        if getattr(s, 'env', None):
            tb = np.array([s.b2s(b) for b, _ in s.env]); g = np.array([d for _, d in s.env], float)
            out *= (10 ** (np.interp(np.arange(len(out)) / SR, tb, g) / 20))[:, None].astype(np.float32)
        if reverb: out = add_reverb(out, reverb)
        n = int(0.012 * SR); out[-n:] *= np.linspace(1, 0, n)[:, None]
        raw = path + '.raw.wav'; write_wav(raw, out)
        pre = f'acompressor=threshold=-18dB:ratio=2.5:attack=8:release=120:makeup=2,volume={gain_db}dB'
        m = subprocess.run([FF, '-hide_banner', '-i', raw, '-af', pre + ',loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
        import json as _j; j = _j.loads(m[m.rindex('{'):m.rindex('}') + 1])
        ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}"
              f":measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
        subprocess.run([FF, '-y', '-loglevel', 'error', '-i', raw, '-af', pre + ',' + ln, '-ar', str(SR), path], check=True)
        os.remove(raw)
        return path

def add_reverb(x, wet):
    rng = np.random.default_rng(7); L = int(1.6 * SR); t = np.arange(L) / SR
    ir = np.stack([rng.standard_normal(L) * np.exp(-t / 0.42), rng.standard_normal(L) * np.exp(-t / 0.42)], 1).astype(np.float32)
    ir[: int(0.012 * SR)] = 0; ir /= np.sqrt((ir ** 2).sum(0))
    from numpy.fft import rfft, irfft
    N = 1 << int(np.ceil(np.log2(len(x) + L)))
    y = np.stack([irfft(rfft(x[:, c], N) * rfft(ir[:, c], N), N)[:len(x)] for c in range(2)], 1)
    return (x + wet * y).astype(np.float32)

def write_wav(path, x):
    x = np.clip(x / max(1e-6, np.abs(x).max()) * 0.89, -1, 1)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype('<i2').tobytes())

# ---------------- SFX ----------------
def sfx(kind, path, dur=None):
    rng = np.random.default_rng(3)
    if kind == 'whoosh':
        d = dur or 0.45; t = np.arange(int(d * SR)) / SR; nz = rng.standard_normal(len(t))
        env = np.sin(np.pi * t / d) ** 2
        # moving one-pole lowpass sweep
        f = 300 + 5000 * np.sin(np.pi * t / d); y = np.zeros_like(nz); a = 0
        for i in range(len(t)):
            c = 1 - np.exp(-2 * np.pi * f[i] / SR); a += c * (nz[i] - a); y[i] = a
        y *= env; x = np.stack([y * (1 - t / d * 0.6), y * (0.4 + t / d * 0.6)], 1)
    elif kind == 'pop':
        d = dur or 0.18; t = np.arange(int(d * SR)) / SR; f = 900 * np.exp(-t * 18) + 180
        y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 22); x = np.stack([y, y], 1)
    elif kind == 'shutter':
        d = dur or 0.25; t = np.arange(int(d * SR)) / SR; y = rng.standard_normal(len(t)) * (np.exp(-t * 90) + 0.8 * np.exp(-np.maximum(0, t - 0.09) * 120) * (t > 0.09))
        x = np.stack([y, y], 1)
    elif kind == 'riser':
        d = dur or 1.5; t = np.arange(int(d * SR)) / SR; nz = rng.standard_normal(len(t)); y = np.zeros_like(nz); a = 0
        f = 200 + 7000 * (t / d) ** 2
        for i in range(len(t)):
            c = 1 - np.exp(-2 * np.pi * f[i] / SR); a += c * (nz[i] - a); y[i] = a
        y *= (t / d) ** 1.5; x = np.stack([y, y], 1)
    elif kind == 'boom':
        d = dur or 1.6; t = np.arange(int(d * SR)) / SR; f = 40 + 80 * np.exp(-t * 6)
        y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.2) + 0.3 * rng.standard_normal(len(t)) * np.exp(-t * 14)
        x = np.stack([y, y], 1)
    elif kind == 'coin':
        d = 0.32; t = np.arange(int(d * SR)) / SR; f = np.where(t < 0.07, 988, 1319)
        y = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.5 * np.exp(-np.maximum(0, t - 0.07) * 9); x = np.stack([y, y], 1)
    elif kind == 'scratch':
        d = 0.5; t = np.arange(int(d * SR)) / SR; f = 600 + 500 * np.sin(2 * np.pi * 7 * t)
        y = rng.standard_normal(len(t)) * 0.5 * np.abs(np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-t * 3); x = np.stack([y, y], 1)
    elif kind == 'sparkle':
        d = 0.9; t = np.arange(int(d * SR)) / SR; y = np.zeros(len(t))
        for k, fr in enumerate([2093, 2637, 3136, 4186]):
            s0 = int(k * 0.07 * SR); tt = t[: len(t) - s0]; y[s0:] += np.sin(2 * np.pi * fr * tt) * np.exp(-tt * 6) * 0.4
        x = np.stack([y, y], 1)
    if kind == 'rain':
        d = dur or 7.0; n = int(d * SR); t = np.arange(n) / SR; nz = rng.standard_normal((n, 2))
        from numpy.fft import rfft, irfft
        f = np.fft.rfftfreq(n, 1 / SR); shape = 1 / (1 + (f / 2500) ** 2) * (f > 150)
        y = np.stack([irfft(rfft(nz[:, c]) * shape, n) for c in range(2)], 1)
        for _ in range(int(d * 14)):
            k = rng.integers(0, n - 2000); dd = np.exp(-np.arange(2000) / 120) * np.sin(2 * np.pi * rng.uniform(1800, 4200) * np.arange(2000) / SR)
            y[k:k + 2000, rng.integers(0, 2)] += dd * rng.uniform(0.05, 0.2) * np.abs(y).max()
        env = np.minimum(1, t / 0.3) * np.minimum(1, (d - t) / 0.4); x = y * env[:, None]
    x = x.astype(np.float32); x /= max(1e-6, np.abs(x).max()); x *= 0.8
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype('<i2').tobytes())
    return path
