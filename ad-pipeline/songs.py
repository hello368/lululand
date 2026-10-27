"""10 original cues, one per new ad. Lengths match the ads exactly."""
import sys
from mus import Song, chord, midi

def strum(s, ch, beat, notes, dur, vel=80, spread=0.03, down=True):
    ns = notes if down else list(reversed(notes))
    for i, n in enumerate(ns):
        s.n(ch, beat + i * spread * s.bpm / 60, n, max(0.05, dur - i * spread * s.bpm / 60), vel - i * 2)

# 1 -------- Cinematic trailer, D minor -> D major (30 s @ 100) --------
def trailer():
    s = Song(100)
    s.inst(0, 48, vol=110); s.inst(1, 48, vol=100); s.inst(2, 52, vol=80); s.inst(3, 61, vol=105)
    s.inst(4, 47, vol=120); s.inst(5, 116, vol=110); s.inst(6, 55, vol=100); s.inst(7, 60, vol=100); s.inst(9, 48, drums=True, vol=110)
    roots = ['D', 'D', 'Bb', 'C'] * 2
    for bar in range(8):
        r = roots[bar]; b = bar * 4; hi = bar >= 4
        for i in range(8):
            acc = i in (0, 3, 6)
            s.n(1, b + i * .5, f'{r}3', .4, 100 if acc else 70)
            if acc: s.n(1, b + i * .5, f'{r}2', .4, 95)
            if hi: s.n(1, b + i * .5, f'{r}4', .3, 60)
    s.n(4, 0, 'D2', 3, 120); s.n(4, 8, 'D2', 3, 115)
    for b, c in [(0, ['D4', 'F4', 'A4']), (8, ['D4', 'F4', 'Bb4']), (12, ['E4', 'G4', 'C5'])]:
        s.notes(2, b, c, 4 if b else 8, 55)
    # build
    for bar in range(4, 8):
        b = bar * 4; s.n(4, b, f'{roots[bar]}2', 1.5, 120)
        for i, c in enumerate('X..x..x.X...x.x.'):
            if c != '.': s.n(5, b + i * .25, 'C3', .25, 120 if c == 'X' else 90)
    for b, c in [(16, ['D3', 'A3', 'D4', 'F4']), (20, ['D3', 'A3', 'D4', 'F4']), (24, ['Bb2', 'F3', 'Bb3', 'D4']), (28, ['C3', 'G3', 'C4', 'E4'])]:
        s.notes(3, b, c, 3.4, 95); s.notes(2, b, [x + 12 for x in map(midi, c[1:])], 3.5, 70)
    s.seq(7, 16, 'D4:2 F4:2 A4:4 Bb4:2 A4:1 G4:1 A4:3.5', vel=95)
    for i in range(32):  # snare roll 28 -> 31.5
        s.n(9, 28 + i * 0.109, 38, .1, 50 + i * 2)
    # 32: D major, triumphant
    s.notes(6, 32, ['D4', 'F#4', 'A4', 'D5'], 1, 120); s.n(9, 32, 49, 2, 127); s.n(9, 32, 36, 1, 127)
    prog = [('D', ['D3', 'A3', 'D4', 'F#4']), ('G', ['G2', 'D3', 'G3', 'B3']), ('A', ['A2', 'E3', 'A3', 'C#4']), ('D', ['D3', 'A3', 'D4', 'F#4'])]
    for k, (r, c) in enumerate(prog):
        b = 32 + k * 4
        for i in range(8): s.notes(1, b + i * .5, [f'{r}2', f'{r}3'], .4, 105 if i % 2 == 0 else 85)
        s.notes(0, b, [x + 12 for x in map(midi, c)], 4, 90); s.notes(2, b, [x + 12 for x in map(midi, c[1:])], 4, 80)
        s.n(4, b, f'{r}2', 1, 120); s.n(4, b + 2, f'{r}2', 1, 110); s.n(9, b, 49 if k else 57, 2, 115)
        for i in range(8): s.n(5, b + i * .5, 'C3', .4, 115 if i % 2 == 0 else 85)
    s.seq(3, 32, 'D4:1.5 A4:.5 A4:2 B4:1 A4:1 G4:1 B4:1 C#5:1.5 B4:.5 A4:1 E5:1 D5:4', vel=118)
    s.seq(7, 32, 'F#3:1.5 F#3:.5 F#3:2 G3:2 D4:2 E4:2 C#4:2 D4:4', vel=100)
    # 48 final tutti
    s.notes(6, 48, ['D3', 'D4', 'F#4', 'A4', 'D5'], 2, 127); s.notes(3, 48, ['D3', 'A3', 'D4', 'F#4', 'A4'], 2, 120)
    s.notes(0, 48, ['D4', 'F#4', 'A4', 'D5', 'F#5'], 2, 110); s.n(4, 48, 'D2', 2, 127); s.n(9, 48, 57, 2, 127); s.n(5, 48, 'C3', 1, 127)
    s.env = [(0,-8),(16,-5),(31.4,-1),(31.55,-30),(31.97,-30),(32,0),(50,0)]
    s.mix = {0: -22, 1: -20, 2: -26, 3: -17, 4: -20, 5: -19, 6: -18, 7: -19, 9: -24}
    return s, 30.0

# 2 -------- Chiptune, C major (30 s @ 132) --------
def chip():
    s = Song(132)
    s.inst(0, 80, vol=88); s.inst(1, 38, vol=105); s.inst(2, 80, vol=52, pan=40); s.inst(9, 24, drums=True, vol=100)
    prog = ['C', 'G', 'Am', 'F']
    A = ['E5:.5 G5:.5 C6:.5 G5:.5 E5:.5 G5:.5 C6:1', 'D6:.5 B5:.5 G5:.5 B5:.5 D6:1 r:1',
         'C6:.5 A5:.5 E5:.5 A5:.5 C6:.5 E6:.5 D6:1', 'C6:.5 A5:.5 F5:.5 A5:.5 G5:2']
    B = ['E6:.5 D6:.5 C6:.5 G5:.5 A5:.5 G5:.5 E5:1', 'D5:.5 G5:.5 B5:.5 D6:.5 G6:1 r:1',
         'E6:.5 C6:.5 A5:.5 C6:.5 E6:.5 G6:.5 E6:1', 'F6:.5 E6:.5 D6:.5 C6:.5 D6:2']
    s.seq(0, 0, 'C5:.25 E5:.25 G5:.25 C6:.25 E6:.5 r:.5 G6:1 r:1 G5:.5 A5:.5 B5:.5 C6:.5 D6:.5 E6:.5 F#6:.5 G6:.5', vel=95)
    for bar in range(18):
        b = bar * 4
        if b >= 66: break
        c = 'C' if bar < 2 else (prog[(bar - 2) % 4] if bar < 12 else ['F', 'G', 'C', 'C', 'C', 'C'][bar - 12])
        notes = chord(c, 4)
        for i in range(16):
            if b + i * .25 < 64: s.n(2, b + i * .25, notes[i % 3] + 12 * ((i // 3) % 2), .2, 70)
        if 8 <= b < 64:
            r = midi(c[0] + '2')
            for i in range(8): s.n(1, b + i * .5, r + (12 if i % 2 else 0), .35, 100)
    s.drums(0, 2, {36: 'x.......x.......', 42: '..x...x...x...x.'}, vel=80)
    s.drums(8, 14, {36: 'x...x...x...x...', 38: '....x.......x...', 42: 'x.x.x.x.x.x.x.x.'}, vel=95)
    k = 8
    for ph in [A, B]:
        for bar in ph: k = s.seq(0, k, bar, vel=92)
    for bar in A[:2]: k = s.seq(0, k, bar, vel=92)
    s.seq(0, 48, 'G5:.5 C6:.5 E6:.5 G6:1.5 r:1 F6:.5 E6:.5 D6:.5 E6:1.5 r:1 C6:.5 D6:.5 E6:.5 G6:.5 C7:2 E6:.5 G6:.5 C7:1 r:2', vel=96)
    # level complete hit
    s.notes(0, 64, ['C6', 'E6', 'G6', 'C7'], 1.9, 110); s.notes(2, 64, ['C5', 'G5'], 1.9, 90); s.n(1, 64, 'C2', 1.9, 120)
    s.n(9, 64, 49, 2, 120); s.n(9, 64, 36, 1, 120)
    s.mix = {0: -15, 1: -19, 2: -27, 9: -19}
    return s, 30.0

# 3 -------- Future bass, F major (30 s @ 128) --------
def futurebass():
    s = Song(128)
    s.inst(0, 81, vol=78); s.inst(1, 90, vol=92); s.inst(2, 38, vol=110); s.inst(3, 53, vol=96); s.inst(4, 98, vol=80); s.inst(5, 89, vol=70); s.inst(9, 25, drums=True, vol=110)
    prog = [('Dm7', 'D'), ('Bbmaj7', 'Bb'), ('F', 'F'), ('C', 'C')]
    for bar in range(16):
        b = bar * 4; cname, r = prog[bar % 4]; c = chord(cname, 4)
        if bar < 6:  # intro: soft crystal plucks + pad
            for i in (0, 1.5, 3): s.notes(4, b + i, c, .8, 60 if bar < 4 else 75)
            s.notes(5, b, c, 4, 55)
        elif bar < 12:  # drop
            for i, ch in enumerate('X..x..x...x.x...'):
                if ch != '.':
                    v = 115 if ch == 'X' else 92
                    s.notes(0, b + i * .25, [x + 12 for x in c], .22, v - 10); s.notes(1, b + i * .25, c, .22, v)
            s.n(2, b, f'{r}1', 1.6, 120); s.n(2, b + 2.5, f'{r}1', 1.2, 110)
        else:  # outro
            for i in (0, 1.5, 3): s.notes(4, b + i, c, .8, 80)
            s.notes(5, b, c, 4, 65); s.n(2, b, f'{r}1', 3.5, 90)
    s.drums(16, 2, {39: '....x.......x...', 42: 'x.x.x.x.x.x.x.x.'}, vel=85)
    for i in range(16): s.n(9, 20 + i * .25, 38, .2, 60 + i * 3)
    s.drums(24, 6, {36: 'X.........x.....', 39: '........X.......', 42: 'x.x.x.x.x.xxx.x.xxxx'[:16], 46: '..............x.'}, vel=100)
    s.drums(48, 3, {36: 'x.......x.......', 42: 'x.x.x.x.x.x.x.x.'}, vel=75)
    chop = ['A5:.5 G5:.25 F5:.25 G5:.5 A5:.5 C6:1 A5:1', 'F5:.5 G5:.5 A5:.5 Bb5:.5 A5:1 F5:1',
            'A5:.5 C6:.25 A5:.25 G5:.5 F5:.5 G5:1 A5:1', 'G5:.5 E5:.5 C5:.5 E5:.5 G5:2']
    k = 24
    for rep in range(2):
        for bar in chop: k = s.seq(3, k, bar, vel=105)
    k = 48
    for bar in chop[:3]: k = s.seq(4, k, bar, vel=90, octave_shift=1)
    s.notes(1, 60, chord('F', 4), 1.5, 100); s.notes(0, 60, chord('F', 5), 1.5, 95)
    s.notes(1, 62.5, chord('Fadd9', 4), 1.5, 115); s.notes(0, 62.5, chord('F', 5), 1.5, 105); s.n(2, 62.5, 'F1', 1.5, 120)
    s.n(9, 62.5, 49, 1.5, 120); s.n(9, 62.5, 36, 1, 120)
    s.env = [(0,-5),(23.4,0),(23.55,-28),(23.98,-28),(24,0),(64,0)]
    s.mix = {0: -22, 1: -18, 2: -19, 3: -16, 4: -20, 5: -27, 9: -18}
    return s, 30.0

# 4 -------- Disco funk, C major (30 s @ 116) --------
def disco():
    s = Song(116)
    s.inst(0, 36, vol=112); s.inst(1, 7, vol=78, pan=44); s.inst(2, 61, vol=96); s.inst(3, 48, vol=88, pan=84); s.inst(4, 4, vol=70); s.inst(9, 0, drums=True, vol=105)
    prog = [('Fmaj7', 'F'), ('Em7', 'E'), ('Dm7', 'D'), ('G7', 'G')]
    for bar in range(14):
        b = bar * 4; cname, r = prog[bar % 4] if bar < 10 else [('Fmaj7', 'F'), ('G7', 'G'), ('Em7', 'E'), ('Am7', 'A')][bar - 10]
        c = chord(cname, 4)
        for i in range(8): s.n(0, b + i * .5, f'{r}2' if i % 2 == 0 else f'{r}3', .3 if i % 2 else .4, 112 if i % 2 == 0 else 95)
        for i in (1, 3, 5, 7, 9, 11, 13, 15): s.notes(1, b + i * .25, c[1:], .12, 72)
        s.notes(2, b, c, .25, 100); s.notes(2, b + 1.5, c, .25, 92)
        s.notes(4, b, c, 3.8, 50)
    s.drums(0, 14, {36: 'x...x...x...x...', 38: '....x.......x...', 46: '..x...x...x...x.', 42: 'o.o.o.o.o.o.o.o.', 54: 'oooooooooooooooo'}, vel=92)
    strings = ['A5:1 C6:1 E6:1.5 D6:.5', 'B5:1 D6:1 G6:2', 'F6:.5 E6:.5 D6:.5 C6:.5 A5:2', 'B5:1 D6:1 F6:1 G6:1']
    k = 0
    while k < 40:
        for bar in strings:
            if k < 40: k = s.seq(3, k, bar, vel=96)
    s.seq(2, 40, 'A4:.5 C5:.5 E5:1 C5:.5 E5:1.5 B4:.5 D5:.5 G5:1 D5:.5 F5:1.5 G4:.5 B4:.5 E5:1 G5:1 r:1 A4:.5 C5:.5 E5:1 A5:2', vel=105)
    s.seq(3, 40, '[A5,C6]:4 [B5,D6]:4 [G5,B5]:4 [A5,C6]:4', vel=80)
    # final: C major hit at 56
    s.notes(2, 56, ['C4', 'E4', 'G4', 'C5', 'E5'], 1.9, 120); s.notes(3, 56, ['C6', 'E6', 'G6'], 1.9, 110); s.n(0, 56, 'C2', 1.9, 120)
    s.n(9, 56, 49, 2, 125); s.n(9, 56, 36, 1, 120); s.notes(4, 56, ['C4', 'E4', 'G4', 'B4'], 1.9, 80)
    s.mix = {0: -18, 1: -25, 2: -19, 3: -17, 4: -28, 9: -18}
    return s, 30.0

# 5 -------- Rainy piano -> sunny folk, G major (30 s @ 104) --------
def folk():
    s = Song(104)
    s.inst(0, 0, vol=90); s.inst(1, 25, vol=100); s.inst(2, 78, vol=96); s.inst(3, 32, vol=100); s.inst(4, 9, vol=60); s.inst(9, 0, drums=True, vol=95)
    for b, c in [(0, ['E3', 'B3', 'E4', 'G4']), (4, ['C3', 'G3', 'C4', 'E4']), (8, ['A2', 'E3', 'A3', 'C4']), (10, ['D3', 'A3', 'D4', 'F#4'])]:
        s.notes(0, b, c, 3.9 if b < 8 else 1.9, 55)
    s.seq(0, 0, 'B4:2 G4:2 E5:2 D5:2 C5:1 B4:1 A4:1.5 r:.5', vel=60)
    G = ['G2', 'D3', 'G3', 'B3', 'D4', 'G4']; D = ['D3', 'A3', 'D4', 'F#4']; Em = ['E2', 'B2', 'E3', 'G3', 'B3', 'E4']; C = ['C3', 'G3', 'C4', 'E4', 'G4']
    prog = [(G, 'G'), (D, 'D'), (Em, 'E'), (C, 'C')]
    for bar in range(8):
        b = 12 + bar * 4; c, r = prog[bar % 4]
        for off, dn, v in [(0, 1, 100), (1, 1, 85), (1.5, 0, 70), (2.5, 0, 75), (3, 1, 88), (3.5, 0, 70)]:
            strum(s, 1, b + off, [midi(x) for x in c], .45 if off else .9, v, down=bool(dn))
        s.n(3, b, f'{r}2', .9, 105); s.n(3, b + 2, f'{r}2' if r != 'E' else 'B1', .9, 95)
    for b, c, r in [(44, C, 'C'), (46, C, 'C'), (48, D, 'D')]:
        strum(s, 1, b, [midi(x) for x in c], .9, 95); strum(s, 1, b + 1, [midi(x) for x in c], .9, 80); s.n(3, b, f'{r}2', 1.8, 100)
    strum(s, 1, 50, [midi(x) for x in G], 2, 110); s.n(3, 50, 'G1', 2, 110)
    s.drums(12, 2, {36: 'x.......x.......'}, vel=80)
    s.drums(20, 6, {36: 'x.......x.......', 39: '....x.......x...'}, vel=90)
    s.drums(28, 4, {54: 'x.x.x.x.x.x.x.x.'}, vel=70)
    w1 = 'D5:1 G5:1 B5:1.5 A5:.5 A5:1 F#5:1 D5:2 E5:1 G5:1 B5:1 D6:1 C6:1.5 B5:.5 A5:1 G5:1'
    w2 = 'B5:1 D6:1 B5:1 G5:1 A5:1.5 B5:.5 A5:1 F#5:1 G5:1 E5:1 B4:1 E5:1 G5:2 A5:2'
    s.seq(2, 12, w1, vel=100); s.seq(2, 28, w2, vel=104); s.seq(4, 28, w2, vel=70, octave_shift=1)
    s.seq(2, 44, 'E5:1 G5:1 C6:1 B5:1 A5:1 F#5:1 G5:2', vel=108); s.seq(4, 50, 'G6:2', vel=90)
    s.n(9, 50, 49, 2, 100); s.n(9, 50, 36, 1, 100)
    s.env = [(0,-5),(11.9,-5),(12,0),(52,0)]
    s.mix = {0: -18, 1: -19, 2: -16, 3: -21, 4: -27, 9: -21}
    return s, 30.0

# 6 -------- Music box lullaby, F major (15 s @ 76) --------
def musicbox():
    s = Song(76)
    s.inst(0, 10, vol=105); s.inst(1, 46, vol=80); s.inst(2, 8, vol=70); s.inst(3, 89, vol=60)
    mel = ['A5:.5 C6:.5 F6:1 E6:.5 C6:.5 A5:1', 'D6:.5 F6:.5 A6:1 G6:.5 F6:.5 D6:1',
           'D6:.5 F6:.5 Bb6:1 A6:.5 F6:.5 D6:1', 'E6:.5 G6:.5 C7:1 Bb6:.5 G6:.5 E6:1']
    k = 0
    for m in mel: k = s.seq(0, k, m, vel=92)
    s.seq(0, 16, '[F6,A6,C7]:3', vel=100)
    for b, (r, c) in enumerate([('F', 'F'), ('D', 'Dm'), ('Bb', 'Bb'), ('C', 'C')]):
        ns = chord(c, 3); arp = [ns[0], ns[1] + 12 if False else ns[1], ns[2], ns[0] + 12, ns[2], ns[1]]
        for i in range(8): s.n(1, b * 4 + i * .5, [ns[0], ns[2], ns[0] + 12, ns[1] + 12, ns[2] + 12, ns[1] + 12, ns[0] + 12, ns[2]][i], .9, 70)
        s.notes(3, b * 4, chord(c, 4), 4, 48)
        s.n(2, b * 4 + 2, chord(c, 5)[2], 2, 55)
    s.notes(1, 16, ['F3', 'C4', 'F4', 'A4'], 3, 75); s.notes(3, 16, chord('F', 4), 3, 50); s.n(2, 16, 'F6', 3, 70)
    s.mix = {0: -15, 1: -21, 2: -24, 3: -28}
    return s, 15.0

# 7 -------- Dembow / reggaeton kids, A minor (15 s @ 96) --------
def dembow():
    s = Song(96)
    s.inst(0, 12, vol=110); s.inst(1, 38, vol=112); s.inst(2, 45, vol=80); s.inst(3, 114, vol=70); s.inst(9, 25, drums=True, vol=112)
    prog = [('Am', 'A'), ('F', 'F'), ('C', 'C'), ('G', 'G')]
    mel = ['E5:.5 E5:.25 C5:.25 E5:.5 A5:.5 G5:.5 E5:.5 C5:1', 'F5:.5 A5:.5 C6:.5 A5:.5 F5:.5 E5:.5 F5:1',
           'G5:.5 E5:.5 C5:.5 E5:.5 G5:.5 A5:.5 G5:1', 'D5:.5 G5:.5 B5:.5 D6:.5 B5:.5 G5:.5 D5:1']
    k = 0
    for rep in range(2):
        for m in mel:
            if k < 22: k = s.seq(0, k, m, vel=100)
    for bar in range(6):
        b = bar * 4; c, r = prog[bar % 4]
        for i, ch in enumerate('X..x..x.X..x..x.'):
            if ch != '.' and b + i * .25 < 22.5: s.n(1, b + i * .25, f'{r}1' if r in 'AG' else f'{r}2', .25, 115 if ch == 'X' else 95)
        for i in range(4):
            if b + i + .5 < 22.5: s.notes(2, b + i + .5, chord(c, 4), .2, 75)
    s.drums(0, 5, {36: 'x...x...x...x...', 38: '...x..x....x..x.', 42: 'x.x.x.x.x.x.x.x.', 61: 'o..x.o..o..x.o..'}, vel=100)
    s.drums(20, 1, {36: 'x...x...', 38: '...x..x.', 42: 'x.x.x.x.'}, steps=8, beats_per_bar=2, vel=100)
    for i in range(8): s.n(9, 22 + i * .0625, 38, .06, 70 + i * 6)
    s.notes(0, 23, ['A4', 'C5', 'E5', 'A5'], 1, 120); s.n(1, 23, 'A1', 1, 125); s.n(9, 23, 36, 1, 125); s.n(9, 23, 49, 1, 120); s.n(3, 23, 'A5', 1, 100)
    s.mix = {0: -16, 1: -18, 2: -24, 3: -22, 9: -17}
    return s, 15.0

# 8 -------- Grand-opening march, Bb major (15 s @ 120) --------
def march():
    s = Song(120)
    s.inst(0, 61, vol=100); s.inst(1, 56, vol=108); s.inst(2, 58, vol=110); s.inst(3, 9, vol=75); s.inst(4, 72, vol=70); s.inst(9, 0, drums=True, vol=105)
    s.seq(1, 0, 'Bb4:.5 D5:.5 F5:1 D5:.5 F5:1.5', vel=115)
    s.notes(0, 0, ['Bb3', 'D4', 'F4'], 1, 100); s.notes(0, 2, ['Bb3', 'D4', 'F4'], 1.8, 105)
    mel = 'D5:1 F5:.5 D5:.5 Bb4:1 D5:1 Eb5:1 G5:.5 Eb5:.5 Bb4:1 G5:1 F5:.5 G5:.5 A5:.5 Bb5:.5 C6:1 A5:1 Bb5:1.5 F5:.5 D5:1 Bb4:1 Eb5:1 G5:1 F5:1 A5:1'
    s.seq(1, 4, mel, vel=108); s.seq(3, 4, mel, vel=80, octave_shift=1); s.seq(4, 12, 'F6:.5 G6:.5 A6:.5 Bb6:.5 C7:1 A6:1', vel=70)
    chords = [(4, 'Bb', 'Bb'), (8, 'Eb', 'Eb'), (12, 'F', 'F'), (16, 'Bb', 'Bb'), (20, 'Eb', 'Eb'), (22, 'F', 'F')]
    for b, c, r in chords:
        span = 4 if b < 20 else 2
        for i in range(span):
            if i % 2 == 0: s.n(2, b + i, f'{r}1' if r in 'F' else f'{r}1', .8, 110)
            else: s.notes(0, b + i, chord(c, 3)[1:], .5, 85)
    s.drums(0, 6, {38: 'X..xx.x.X..xx.xx', 36: 'x.......x.......'}, vel=92)
    s.n(9, 0, 49, 2, 110); s.n(9, 4, 49, 2, 100); s.n(9, 16, 49, 2, 100)
    s.seq(1, 24, 'F5:.333 F5:.333 F5:.334 Bb5:2.5 r:.5', vel=118); s.notes(0, 24, ['Bb3', 'D4', 'F4'], 3, 95); s.n(2, 24, 'Bb1', 3, 105)
    for i in range(16): s.n(9, 26 + i * .125, 38, .1, 70 + i * 3)
    s.notes(0, 28, ['Bb3', 'D4', 'F4', 'Bb4'], 2, 125); s.notes(1, 28, ['D5', 'Bb5'], 2, 122); s.n(2, 28, 'Bb1', 2, 120); s.n(3, 28, 'Bb6', 2, 95)
    s.n(9, 28, 49, 2, 127); s.n(9, 28, 36, 1, 125)
    s.mix = {0: -19, 1: -16, 2: -20, 3: -24, 4: -24, 9: -19}
    return s, 15.0

# 9 -------- Swing, F major (15 s @ 150) --------
def swing():
    s = Song(150)
    s.inst(0, 71, vol=100); s.inst(1, 32, vol=110); s.inst(2, 0, vol=80); s.inst(3, 59, vol=80); s.inst(9, 32, drums=True, vol=95)
    s.seq(0, 0, 'C5:.667 D5:.333 F5:.667 A5:.333 r:.667 G5:.333 F5:1 '
                'F#5:.667 A5:.333 C6:1 A5:.667 F#5:.333 D5:1 '
                'Bb4:.667 D5:.333 F5:.667 G5:.333 Bb5:1 A5:1 '
                'G5:.667 E5:.333 C5:.667 Bb4:.333 C5:2 '
                'A5:.667 C6:.333 D6:.667 C6:.333 A5:1 F5:1 '
                'F#5:.667 G5:.333 A5:.667 C6:.333 D6:2 '
                'D6:.667 C6:.333 Bb5:.667 G5:.333 E5:.667 G5:.333 Bb5:1 '
                'A5:.667 G5:.333 F5:.667 D5:.333 C5:2 '
                'r:1 C5:.667 D5:.333 E5:.667 G5:.333 r:1', vel=98)
    walk = ['F2 A2 C3 D3', 'D2 F#2 A2 C3', 'G2 A2 Bb2 B2', 'C3 Bb2 A2 G2', 'F2 A2 C3 Eb3', 'D2 F#2 A2 C3', 'G2 Bb2 C3 E2', 'F2 A2 C3 A2', 'G2 A2 Bb2 B2']
    comp = [['A3', 'C4', 'D4', 'F4'], ['F#3', 'C4', 'E4'], ['F3', 'Bb3', 'D4'], ['E3', 'Bb3', 'D4'], ['A3', 'C4', 'D4', 'F4'], ['F#3', 'C4', 'E4'], ['F3', 'Bb3', 'D4'], ['A3', 'C4', 'D4', 'F4'], ['F3', 'Bb3', 'D4']]
    for bar in range(9):
        b = bar * 4
        for i, n in enumerate(walk[bar].split()): s.n(1, b + i, n, .9, 100 if i % 2 == 0 else 90)
        c = comp[bar]
        if bar == 6: s.notes(2, b, c, .5, 70); s.notes(2, b + 2, ['E3', 'Bb3', 'D4'], .5, 70)
        else: s.notes(2, b, c, .5, 72); s.notes(2, b + 1.667, c, .3, 66)
        for i in range(4):
            s.n(9, b + i, 51, .6, 80)
            if i % 2: s.n(9, b + i + .667, 51, .3, 60); s.n(9, b + i, 44, .3, 70)
    s.seq(3, 16, 'r:1 A4:.667 C5:.333 r:2 r:1 A4:.667 C5:.333 r:2', vel=70)
    s.notes(0, 36, ['A5'], 1.4, 105); s.notes(2, 36, ['F3', 'A3', 'C4', 'D4', 'G4'], 1.4, 95); s.n(1, 36, 'F1', 1.4, 115)
    s.n(3, 36, 'F5', 1.4, 95); s.n(9, 36, 49, 1.5, 110); s.n(9, 36, 36, 1, 100)
    s.mix = {0: -16, 1: -19, 2: -22, 3: -23, 9: -23}
    return s, 15.0

# 10 -------- Lo-fi, C major (15 s @ 84) --------
def lofi():
    s = Song(84)
    s.inst(0, 4, vol=95); s.inst(1, 33, vol=100); s.inst(2, 108, vol=95); s.inst(3, 89, vol=50); s.inst(9, 8, drums=True, vol=95)
    prog = ['Fmaj7', 'Em7', 'Dm7', 'Cmaj7', 'Fmaj7']
    for bar, c in enumerate(prog):
        b = bar * 4; ns = chord(c, 3)[1:] + [chord(c, 4)[0] + 12 if False else chord(c, 4)[-1]]
        for i, n in enumerate(chord(c, 4)): s.n(0, b + i * .04, n - 12 if i == 0 else n, 3.7, 70 - i * 3)
        s.n(0, b + 2.5, chord(c, 4)[2], 1.3, 55)
        s.n(1, b, c[0] + '2', 1.6, 95); s.n(1, b + 2.75, c[0] + '2', 1, 85)
        s.notes(3, b, chord(c, 4), 4, 40)
    s.drums(0, 5, {36: 'x.......x.x.....', 38: '....x.......x...', 42: 'o.x.o.x.o.x.o.x.'}, vel=88)
    s.seq(2, 0, 'E5:.5 G5:.5 C6:1 A5:1 G5:1 B5:1 G5:.5 E5:.5 D5:2 F5:.5 A5:.5 C6:1 A5:.5 F5:.5 E5:1 G5:1.5 E5:.5 D5:.5 E5:.5 C5:1 E5:.5 G5:.5 A5:3', vel=90)
    s.notes(0, 20, ['F3', 'A3', 'C4', 'E4', 'G4'], 1, 80); s.n(1, 20, 'F1', 1, 95); s.n(2, 20, 'C6', 1, 90); s.n(9, 20, 36, .5, 90)
    s.mix = {0: -18, 1: -20, 2: -17, 3: -29, 9: -19}
    return s, 15.0

SONGS = {'trailer': trailer, 'chip': chip, 'futurebass': futurebass, 'disco': disco, 'folk': folk,
         'musicbox': musicbox, 'dembow': dembow, 'march': march, 'swing': swing, 'lofi': lofi}
if __name__ == '__main__':
    import os; os.makedirs('out/music', exist_ok=True)
    for name in (sys.argv[1:] or SONGS):
        s, L = SONGS[name](); print(name, s.render(L, f'out/music/{name}.wav', tail=0.5, reverb=0.22 if name not in ('chip',) else 0.08))
