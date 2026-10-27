# Reference only: the Oct 20 batch. Clip/photo numbers point at the OLD shoot, not the new one.
import sys, random
from lib2 import *
import lib30
_paint = lib30.paint
def _capped(name, width):
    t = _paint(name, width)
    if name.startswith('t-') and t.height > 290: t = _paint(name, int(width * 290 / t.height))
    return t
lib30.paint = _capped
M = OUT + '/music/'
FINE = '*Lulu Party package. Min. 8 kids. 15% service fee not included. First 10 new families.'
PHONE = '(818) 668-3342'

def confetti(seed=1, n=90, area=(0, 0, W, H)):
    def f(im):
        r = random.Random(seed); d = ImageDraw.Draw(im)
        for _ in range(n):
            x = r.randint(area[0], area[2]); y = r.randint(area[1], area[3]); c = r.choice([ROSE, GOLD, (17, 144, 223, 255), TEAL, WHITE, SAGE])
            if r.random() < .5: d.ellipse([x, y, x + 18, y + 18], fill=c)
            else:
                w_, h_ = r.randint(10, 16), r.randint(26, 40); p = Image.new('RGBA', (w_, h_), c).rotate(r.randint(0, 180), expand=True); im.alpha_composite(p, (x, y))
    return f
def stars(n, of=5, y=1360):
    def f(im):
        for i in range(of):
            s = paint('star-gold' if i < n else 'star-navy', 96); x = (W - of * 110) // 2 + i * 110; im.alpha_composite(s, (x, y))
    return f
def rain(seed=4):
    def f(im):
        r = random.Random(seed); d = ImageDraw.Draw(im)
        for _ in range(260):
            x = r.randint(-100, W); y = r.randint(-120, H); l = r.randint(40, 90); d.line([(x, y), (x + l * .25, y + l)], fill=(220, 230, 245, r.randint(70, 150)), width=3)
    return f
def struck_price(y, size=130):
    def f(im):
        t = text_layer('$65', R(size), (200, 205, 215, 255), stroke=8); x = (W - t.width) // 2; im.alpha_composite(t, (x, y))
        ImageDraw.Draw(im).line([(x + 20, y + t.height - 40), (x + t.width - 20, y + 40)], fill=ROSE, width=18)
    return f

# ======================= 1. Trailer: THE BIRTHDAY (30s) =======================
def ad_trailer():
    p = 'N1_'; LB = letterbox(250)
    card = lambda nm, lines, y=860: layer(p + nm, [center_text(t, N(sz), WHITE, y + i * (sz + 30), spacing=sp) for i, (t, sz, sp) in enumerate(lines)])
    lb = layer(p + 'lb', [LB])
    lower = lambda nm, t: layer(p + nm, [LB, center_text(t, N(58), CREAM, 1500, spacing=10)])
    end_bg = layer(p + 'e0', [solid((0, 0, 0, 170)), LB])
    e1 = layer(p + 'e1', [img_at('wordmark', 420, None, 300)])
    e2 = layer(p + 'e2', [center_text('LULU PARTY', R(120), GOLD, 520, stroke=10), center_text('NOW BOOKING · GRAND OPENING', N(44), WHITE, 690, spacing=6)])
    e3 = layer(p + 'e3', [center_text('FIRST 10 NEW FAMILIES', R(52), WHITE, 800), struck_price(880, 110),
                          center_text('$59 PER KID', R(140), GOLD, 1010, stroke=12)])
    e4 = layer(p + 'e4', [center_text('STARRING  your kid', N(40), CREAM, 1230, spacing=4), center_text('DIRECTED BY  your kid', N(40), CREAM, 1285, spacing=4),
                          center_text('CLEANUP BY  us', N(40), CREAM, 1340, spacing=4)])
    e5 = layer(p + 'e5', [center_text('CALL NOW ' + PHONE, R(62), WHITE, 1420, stroke=7), center_text(FINE, N(24), CREAM, 1520)])
    SC = [
        C('black', 4, [(card('c1', [('THIS SATURDAY', 84, 20)]), 0.4, 'fade')], tr=('fadeblack', 1)),
        V(0, 0.4, 4, [(lower('l1', 'ONE BIRTHDAY'), 0.4, 'fade')], film=True, tr=('fadeblack', 1)),
        C('black', 2, [(card('c2', [('ONE MISSION', 84, 20)]), 0.2, 'fade')], tr=('fadeblack', .5)),
        V(22, 3.0, 4, [(lower('l2', 'MAKE SOMETHING EPIC'), 0.3, 'fade')], film=True, tr=('fadeblack', .5)),
        C('black', 2, [(card('c3', [('ZERO MESS', 84, 20), ('AT HOME', 84, 20)]), 0.2, 'fade')]),
        V(5, 2.0, 2, [(lb, 0, 'none')], film=True, punch=[0.0]),
        P(145, 2, [(lb, 0, 'none')], film=True, move='left'),
        V(12, 1.0, 2, [(lb, 0, 'none')], film=True, punch=[0.0]),
        P(15, 2, [(lb, 0, 'none')], film=True, move='in'),
        V(21, 9.0, 2, [(lb, 0, 'none')], film=True),
        V(29, 0.3, 2, [(lb, 0, 'none')], film=True, tr=('fadeblack', .5)),
        C('black', 4, [(card('c4', [('THIS IS', 70, 22), ('LULU LAND', 110, 24)], 780), 0.3, 'fade')]),
        P(160, 18, [(end_bg, 0, 'none'), (e1, 0.15, 'pop'), (e2, 0.6, 'up'), (e3, 2.2, 'up'), (e4, 4.4, 'fade'), (e5, 6.0, 'up')], crop=dict(blur=9), film=True, flash=0.0),
    ]
    spb = 0.6
    sfx = [(0.0, 'boom', 0.5), (4.8, 'whoosh', 0.5), (17.9, 'riser', 0.55), (19.2, 'boom', 0.9)]
    return build('LuluLand_30s_F_Trailer', M + 'trailer.wav', 100, SC, 30.0, sfx, 'The Birthday (trailer)')

# ======================= 2. TOP 5 (30s, chiptune) =======================
def ad_top5():
    p = 'N2_'
    hud = lambda n: layer(p + f'hud{n}', [lambda im: im.alpha_composite(pill('LULU LAND TOP 5', R(34), WHITE, NAVY, padx=26, pady=14), (60, 170)), stars(6 - n, y=1380)])
    num = lambda n, label, bg: layer(p + f'n{n}', [center_text(f'#{n}', R(260), GOLD, 260, stroke=16), lambda im: im.alpha_composite(pill(label, R(64), WHITE if bg != GOLD else INK, bg, padx=50, pady=26), ((W - pill(label, R(64), WHITE, bg, padx=50, pady=26).width) // 2, 590))])
    t0 = layer(p + 't0', [solid((2, 36, 73, 120)), center_text('TOP 5 THINGS', R(110), WHITE, 520, stroke=10), center_text('TO MAKE AT', R(80), GOLD, 690, stroke=8), img_at('wordmark', 560, None, 830)])
    lv = layer(p + 'lv', [confetti(3, 70), center_text('LEVEL', R(150), GOLD, 520, stroke=14), center_text('COMPLETE!', R(130), WHITE, 700, stroke=12), stars(5, y=950)])
    SC = [
        P(123, 8, [(t0, 0.1, 'pop')], move='in', tr=('pixelize', 1)),
        P(142, 4, [(hud(5), 0, 'none'), (num(5, 'PICK YOUR CHARMS', TEAL), 0.05, 'pop')], move='left'),
        P(100, 4, [(hud(5), 0, 'none')], move='right', tr=('pixelize', 1)),
        P(155, 4, [(hud(4), 0, 'none'), (num(4, 'PATCH BAR', ROSE), 0.05, 'pop')], move='in'),
        P(162, 4, [(hud(4), 0, 'none')], crop=dict(rot=90), move='out', tr=('pixelize', 1)),
        P(66, 4, [(hud(3), 0, 'none'), (num(3, 'DECODEN', SAGE), 0.05, 'pop')], move='in'),
        P(136, 4, [(hud(3), 0, 'none')], move='out', tr=('pixelize', 1)),
        V(10, 0.3, 4, [(hud(2), 0, 'none'), (num(2, 'SLIME BAR', TEAL), 0.05, 'pop')]),
        V(11, 0.5, 4, [(hud(2), 0, 'none')], tr=('pixelize', 1)),
        V(5, 2.6, 8, [(hud(1), 0, 'none'), (num(1, 'POUR ART', GOLD), 0.05, 'pop')], punch=[3.2]),
        C('#022449', 6, [(lv, 0.05, 'pop')], tr=('pixelize', 1)),
        P(127, 12, walkin_end(p), crop=dict(blur=10)),
    ]
    spb = 60 / 132; sfx = [(8 * spb * k + 8 * spb, 'coin', 0.55) for k in range(5)] + [(48 * spb, 'coin', 0.6)]
    return build('LuluLand_30s_G_Top5', M + 'chip.wav', 132, SC, 30.0, sfx, 'Top 5 things to make')

# ======================= 3. BEFORE -> AFTER (30s, future bass) =======================
def ad_beforeafter():
    p = 'N3_'
    tag = lambda nm, t, bg, fg=WHITE: layer(p + nm, [lambda im: im.alpha_composite(pill(t, R(58), fg, bg, padx=40, pady=22, rot=-3), (60, 200))])
    tagb = lambda nm, t, bg, fg=WHITE: layer(p + nm, [lambda im: im.alpha_composite(pill(t, R(50), fg, bg, padx=34, pady=18, rot=-3), (60, 1150))])
    SC = [
        P(99, 4, [(tag('b1', 'BEFORE', NAVY), 0.1, 'pop')], move='in', tr=('wipeleft', .5)),
        P(25, 4, [(tag('a1', 'AFTER', ROSE), 0.1, 'pop')], move='out', tr=('wiperight', .5)),
        V(1, 0.4, 4, [(tag('b2', 'BEFORE', NAVY), 0.1, 'pop')], tr=('wipeleft', .5)),
        P(29, 4, [(tag('a2', 'AFTER', ROSE), 0.1, 'pop')], move='in', tr=('slideup', .5)),
        SPLIT(('v', 10, 0.2, 480), ('v', 11, 4.0, 520), 6, [(tag('b3', 'BEFORE', NAVY), 0.1, 'pop'), (tagb('a3', 'AFTER', ROSE), 1.2, 'pop')]),
        C('#022449', 2, [(layer(p + 'nw', [center_text('NOW', R(140), WHITE, 700, stroke=12), center_text('WATCH THIS', R(100), GOLD, 880, stroke=10)]), 0.05, 'pop')]),
        V(12, 8.6, 4, punch=[0.0], flash=0.0),
        V(5, 6.0, 4, punch=[0.0, 0.94]),
        P(14, 2, move='in', punch=[0.0]), P(16, 2, move='out', punch=[0.0]), P(136, 2, move='in', punch=[0.0]), P(162, 2, crop=dict(rot=90), move='out', punch=[0.0], tr=('radial', .5)),
        GRID([('p', 25), ('p', 136), ('p', 162, dict(rot=90)), ('p', 2)], 8, [(layer(p + 'mb', [lambda im: im.alpha_composite(pill('MADE BY THEM', R(70), INK, GOLD, padx=50, pady=26, rot=-3), ((W - 700) // 2, 860))]), 0.2, 'pop')], tr=('fadewhite', .5)),
        P(127, 16, walkin_end(p, 't-create-your-way'), crop=dict(blur=10)),
    ]
    spb = 60 / 128; sfx = [(4 * spb, 'whoosh', .5), (8 * spb, 'whoosh', .5), (12 * spb, 'whoosh', .5), (16 * spb, 'whoosh', .5), (21.5 * spb, 'riser', .5), (24 * spb, 'boom', .7)]
    return build('LuluLand_30s_H_BeforeAfter', M + 'futurebass.wav', 128, SC, 30.0, sfx, 'Before and after')

# ======================= 4. A birthday in 5 scenes (30s, disco) =======================
def ad_scenes():
    p = 'N4_'
    scene = lambda n, t: layer(p + f's{n}', [lambda im: im.alpha_composite(pill(f'SCENE {n}', R(40), WHITE, INK, padx=28, pady=14, rot=-3), (60, 180)),
                                             lambda im, t=t: shadowed(im, text_layer(t, R(70), WHITE, stroke=8), ((W - text_layer(t, R(70), WHITE, stroke=8).width) // 2, 290))])
    def invite(im):
        d = ImageDraw.Draw(im); x0, y0, x1, y1 = 130, 560, W - 130, 1240
        d.rounded_rectangle([x0 + 14, y0 + 18, x1 + 14, y1 + 18], 40, fill=INK); d.rounded_rectangle([x0, y0, x1, y1], 40, fill=CREAM, outline=INK, width=8)
        for t, f_, c, y in [("YOU'RE", R(70), ROSE, 610), ('INVITED!', R(104), NAVY, 690), ('a Lulu Party', N(60), NAVY, 860), ('at Lulu Land', N(60), NAVY, 940), ('make · create · celebrate', N(40), ROSE, 1060)]:
            t_ = text_layer(t, f_, c, pad=0); im.alpha_composite(t_, ((W - t_.width) // 2, y))
        im.alpha_composite(paint('icon-balloons', 190), (x1 - 150, y0 - 120)); im.alpha_composite(paint('icon-cake', 170), (x0 - 40, y1 - 150))
    inv = layer(p + 'inv', [invite])
    end0 = layer(p + 'e0', [solid((2, 36, 73, 175))])
    def polas(im):
        for (n, x, y, r) in [(160, 90, 230, -8), (120, 560, 260, 7)]:
            ph = pola_photo(n, 330, 440); fr = Image.new('RGBA', (370, 520), WHITE); fr.paste(ph, (20, 20)); fr = fr.rotate(r, expand=True, resample=Image.BICUBIC); im.alpha_composite(fr, (x, y))
    e1 = layer(p + 'e1', [polas])
    e2 = layer(p + 'e2', [center_text('THE LULU PARTY', R(66), WHITE, 830, stroke=7), center_text('FIRST 10 NEW FAMILIES', N(46), GOLD, 930)])
    e3 = layer(p + 'e3', [struck_price(1000, 100), center_text('$59 PER KID', R(130), GOLD, 1100, stroke=12)])
    e4 = layer(p + 'e4', [lambda im: im.alpha_composite(pill('CALL NOW ' + PHONE, R(54), WHITE, ROSE, padx=44, pady=24), ((W - pill('CALL NOW ' + PHONE, R(54), WHITE, ROSE, padx=44, pady=24).width) // 2, 1300)),
                          center_text('2 hours · we set up · we clean up · lululandkids.com', N(34), CREAM, 1440), center_text(FINE, N(24), CREAM, 1500)])
    SC = [
        C('#df5a79', 8, [(scene(1, 'THE INVITE'), 0.1, 'left'), (inv, 0.5, 'pop')], tr=('coverleft', 1)),
        V(0, 3.2, 4, [(scene(2, 'FRIENDS ARRIVE'), 0.1, 'left')]), P(88, 4, [(scene(2, 'FRIENDS ARRIVE'), 0, 'none')], move='right', tr=('coverleft', 1)),
        V(22, 8.0, 4, [(scene(3, 'EVERYBODY CREATES'), 0.1, 'left')]), P(148, 2, move='in'), P(150, 2, move='out', tr=('coverleft', 1)),
        V(29, 0.2, 4, [(scene(4, 'SAY CHEESE!'), 0.1, 'left')], flash=1.6, tr=('fadewhite', .5)),
        POLA(161, 4, (248, 241, 231, 255), rot=-5, cap='best day ever', tr=('coverleft', 1)),
        P(120, 4, [(scene(5, 'GOODIE BAGS TO GO'), 0.1, 'left')], move='in'), P(3, 4, [(scene(5, 'GOODIE BAGS TO GO'), 0, 'none')], move='out', tr=('slideup', 1)),
        P(165, 18, [(end0, 0, 'none'), (e1, 0.1, 'down'), (e2, 0.8, 'up'), (e3, 1.8, 'pop'), (e4, 3.2, 'up')], crop=dict(blur=10)),
    ]
    spb = 60 / 116; sfx = [(T, 'whoosh', .45) for T in (8 * spb, 16 * spb, 24 * spb, 32 * spb, 40 * spb)] + [(24 * spb + 1.6, 'shutter', .8), (40 * spb + 1.8 + 0.1, 'pop', .5)]
    return build('LuluLand_30s_I_BirthdayScenes', M + 'disco.wav', 116, SC, 30.0, sfx, 'A birthday in 5 scenes')

# ======================= 5. Rainy weekend -> Lulu Land (30s, folk) =======================
def ad_rainy():
    p = 'N5_'
    rn = layer(p + 'rain', [rain()])
    cap = lambda nm, t, y=300, c=WHITE, sz=84: layer(p + nm, [center_text(t, R(sz), c, y, stroke=9)])
    SC = [
        C('#3b4656', 4, [(rn, 0, 'rain'), (cap('r1', 'RAINY', 640, WHITE, 130), 0.2, 'fade'), (cap('r2', 'WEEKEND?', 800, WHITE, 120), 0.6, 'fade')], tr=('dissolve', 1)),
        V(13, 0.5, 4, [(rn, 0, 'rain'), (cap('r3', 'SKIP THE SCREENS.', 300, WHITE, 76), 0.3, 'fade')], gray=True, tr=('dissolve', 1)),
        V(14, 3.9, 4, [(cap('r4', 'HEAD TO', 260, WHITE, 70), 0.3, 'fade'), (cap('r5', 'WESTFIELD TOPANGA', 360, GOLD, 70), 0.6, 'fade')], gray=True, tr=('fadewhite', .5)),
        V(0, 3.0, 4, [(cap('s1', 'HELLO,', 220, WHITE, 90), 0.1, 'pop'), (cap('s2', 'LULU LAND!', 340, GOLD, 110), 0.35, 'pop')], warm=True, tr=('smoothleft', .5)),
        V(3, 0.8, 4, warm=True, tr=('smoothleft', .5)),
        V(11, 1.0, 4, warm=True, tr=('smoothleft', .5)),
        V(16, 0.5, 4, warm=True, tr=('smoothleft', .5)),
        P(66, 4, move='in', warm=True, tr=('smoothleft', .5)),
        P(12, 4, [(cap('b1', 'BEST.', 980, WHITE, 120), 0.1, 'pop'), (cap('b2', 'SATURDAY.', 1130, GOLD, 120), 0.6, 'pop'), (cap('b3', 'EVER.', 1280, WHITE, 120), 1.1, 'pop')], move='in', warm=True, tr=('circleopen', 1)),
        P(127, 16, walkin_end(p, 't-see-you-soon'), crop=dict(blur=10)),
    ]
    spb = 60 / 104
    sfx = [(0.0, 'rain', 0.5), (12 * spb - 0.25, 'whoosh', .5), (32 * spb + 0.1, 'pop', .5), (32 * spb + 0.6, 'pop', .5), (32 * spb + 1.1, 'pop', .5)]
    return build('LuluLand_30s_J_RainyWeekend', M + 'folk.wav', 104, SC, 30.0, sfx, 'Rainy weekend rescue')

# ======================= 6. Oddly satisfying (15s, music box) =======================
def ad_asmr():
    p = 'N6_'
    lc = lambda nm, t: layer(p + nm, [center_text(t, N(72), WHITE, 1180, stroke=5, stroke_fill=(0, 0, 0, 160))])
    top = layer(p + 'top', [center_text('oddly satisfying', N(64), WHITE, 230, stroke=5, stroke_fill=(0, 0, 0, 160))])
    e = layer(p + 'end', [img_at('wordmark', 400, None, 420), center_text('pour art · slime bar · decoden', N(52), NAVY, 1000),
                          center_text('Westfield Topanga · 2nd floor', N(46), NAVY, 1090), center_text('lululandkids.com', R(64), ROSE, 1190)])
    SC = [
        V(5, 2.6, 4, [(top, 0.2, 'fade'), (lc('c1', 'pour…'), 0.8, 'fade')], slow=1.4, soft=True, tr=('dissolve', 1)),
        V(10, 0.2, 4, [(lc('c2', 'stretch…'), 0.6, 'fade')], slow=1.3, soft=True, tr=('dissolve', 1)),
        V(12, 8.4, 4, [(lc('c3', 'lift…'), 0.6, 'fade')], slow=1.3, soft=True, tr=('dissolve', 1)),
        V(9, 4.0, 3, [(lc('c4', 'squish…'), 0.4, 'fade')], slow=1.2, soft=True, tr=('fadewhite', 1)),
        C('#f8f1e7', 4, [(e, 0.1, 'fade')]),
    ]
    return build('LuluLand_15s_K_OddlySatisfying', M + 'musicbox.wav', 76, SC, 15.0, [], 'Oddly satisfying')

# ======================= 7. Slime beat (15s, dembow) =======================
def ad_slimebeat():
    p = 'N7_'
    w = lambda nm, t, c=WHITE: layer(p + nm, [center_text(t, R(150), c, 760, stroke=14)])
    end = layer(p + 'end', [solid((2, 36, 73, 150)), img_at('t-slime-bar', 860, None, 330), center_text('WALK IN · NO BOOKING NEEDED', R(42), GOLD, 760),
                            lambda im: im.alpha_composite(pill('Westfield Topanga · 2nd Floor', R(46), INK, GOLD, padx=40, pady=24), ((W - pill('Westfield Topanga · 2nd Floor', R(46), INK, GOLD, padx=40, pady=24).width) // 2, 880)),
                            center_text('lululandkids.com', R(64), WHITE, 1020, stroke=7)])
    SC = [
        V(11, 0.2, 2, [(w('w1', 'SLIME'), 0.0, 'pop')], punch=[0.0]),
        V(10, 1.0, 2, [(w('w2', 'STRETCH', GOLD), 0.0, 'pop')], punch=[0.0], shake=True),
        V(9, 4.0, 2, [(w('w3', 'SQUISH'), 0.0, 'pop')], punch=[0.0], tr=('zoomin', .25)),
        V(11, 4.0, 2, [(w('w4', 'BUBBLE', GOLD), 0.0, 'pop')], punch=[0.0]),
        P(53, 2, [(w('w5', 'MIX'), 0.0, 'pop')], move='in', flash=0.0),
        P(100, 2, [(w('w6', 'CHARMS', GOLD), 0.0, 'pop')], move='left', flash=0.0, tr=('hblur', .25)),
        V(10, 3.4, 2, [(w('w7', 'PULL'), 0.0, 'pop')], punch=[0.0], shake=True),
        V(4, 0.3, 2, [(w('w8', 'POKE', GOLD), 0.0, 'pop')], punch=[0.0]),
        P(54, 2, [(layer(p + 'w9', [center_text('TAKE IT', R(120), WHITE, 700, stroke=12), center_text('HOME!', R(150), GOLD, 860, stroke=14)]), 0.0, 'pop')], move='in', flash=0.0, tr=('zoomin', .5)),
        V(11, 5.0, 6, [(end, 0.05, 'pop')]),
    ]
    spb = 60 / 96; sfx = [(2 * spb * k, 'pop', .35) for k in range(9)]
    return build('LuluLand_15s_L_SlimeBeat', M + 'dembow.wav', 96, SC, 15.0, sfx, 'Slime beat')

# ======================= 8. Grand opening march (15s) =======================
def ad_grand():
    p = 'N8_'
    now = layer(p + 'now', [confetti(7, 120), img_at('crown', 260, None, 380), lambda im: im.alpha_composite(pill('NOW OPEN!', R(120), WHITE, ROSE, padx=60, pady=34, rot=-5), ((W - 860) // 2, 640)),
                            center_text('WESTFIELD TOPANGA', R(64), NAVY, 960), center_text('2ND FLOOR', R(64), NAVY, 1050)])
    g = layer(p + 'g', [lambda im: im.alpha_composite(pill('POUR · SLIME · PATCH · DECODEN', R(44), INK, GOLD, padx=36, pady=22, rot=-2), ((W - 980) // 2, 900))])
    def ticket(im):
        d = ImageDraw.Draw(im); x0, y0, x1, y1 = 80, 330, W - 80, 1330
        d.rounded_rectangle([x0 + 14, y0 + 18, x1 + 14, y1 + 18], 36, fill=INK); d.rounded_rectangle([x0, y0, x1, y1], 36, fill=CREAM, outline=INK, width=8)
        for yy in range(y0 + 40, y1 - 20, 46): d.ellipse([x0 - 14, yy, x0 + 14, yy + 24], fill=GOLD); d.ellipse([x1 - 14, yy, x1 + 14, yy + 24], fill=GOLD)
        d.line([(x0 + 40, y0 + 250), (x1 - 40, y0 + 250)], fill=INK, width=4)
    t0 = layer(p + 't0', [confetti(9, 60), ticket, center_text('GRAND OPENING', R(84), ROSE, 380), center_text('DEAL', R(84), NAVY, 470)])
    t1 = layer(p + 't1', [center_text('FIRST 10 NEW FAMILIES', R(50), NAVY, 610), struck_price(690, 100)])
    t2 = layer(p + 't2', [center_text('$59', R(260), GOLD, 790, stroke=14), center_text('PER KID · LULU PARTY · 2 HOURS', R(36), NAVY, 1070)])
    t3 = layer(p + 't3', [lambda im: im.alpha_composite(pill('CALL NOW ' + PHONE, R(54), WHITE, ROSE, padx=44, pady=24), ((W - pill('CALL NOW ' + PHONE, R(54), WHITE, ROSE, padx=44, pady=24).width) // 2, 1160)),
                          center_text('lululandkids.com', R(54), NAVY, 1400), center_text(FINE, N(24), NAVY, 1490)])
    SC = [
        C('#e9a214', 4, [(now, 0.05, 'pop')], tr=('slideup', .5)),
        GRID([('v', 1, 2.0), ('v', 11, 1.0), ('v', 16, 1.0), ('v', 22, 3.0)], 4, [(g, 0.1, 'pop')], tr=('slideup', .5)),
        V(21, 10.0, 4, [(layer(p + 'w', [center_text('FAMILIES ARE', R(76), WHITE, 300, stroke=8), center_text('LOVING IT', R(96), GOLD, 410, stroke=9)]), 0.1, 'up')], tr=('slideup', .5)),
        P(165, 4, [(layer(p + 'b', [center_text('BIRTHDAY', R(110), WHITE, 300, stroke=10), center_text('PARTIES', R(110), GOLD, 430, stroke=10)]), 0.1, 'pop')], move='in', tr=('slideup', .5)),
        C('#00a6b0', 14, [(t0, 0.05, 'pop'), (t1, 0.7, 'up'), (t2, 1.4, 'pop'), (t3, 2.4, 'up')]),
    ]
    return build('LuluLand_15s_M_GrandOpening', M + 'march.wav', 120, SC, 15.0, [(16 * .5 + 1.4, 'coin', .4)], 'Grand opening deal')

# ======================= 9. Shopping break (15s, swing) =======================
def ad_shopping():
    p = 'N9_'
    cap = lambda nm, t1, t2: layer(p + nm, [center_text(t1, R(72), WHITE, 260, stroke=8), center_text(t2, R(84), GOLD, 360, stroke=9)])
    def hours(im):
        d = ImageDraw.Draw(im); x0, y0, x1, y1 = 110, 760, W - 110, 1180
        d.rounded_rectangle([x0 + 10, y0 + 12, x1 + 10, y1 + 12], 44, fill=INK); d.rounded_rectangle([x0, y0, x1, y1], 44, fill=CREAM, outline=INK, width=6)
        t = text_layer('WALK IN · NO BOOKING NEEDED', R(40), ROSE, pad=0); im.alpha_composite(t, ((W - t.width) // 2, y0 + 34))
        for i, h in enumerate(HOURS): t = text_layer(h, N(56), NAVY, pad=0); im.alpha_composite(t, ((W - t.width) // 2, y0 + 120 + i * 78))
    end = layer(p + 'end', [solid((2, 36, 73, 160)), img_at('icon-clock', 200, None, 300), center_text('CREATIVE BREAK?', R(76), WHITE, 540, stroke=8), hours,
                            lambda im: im.alpha_composite(pill('Westfield Topanga · 2nd Floor', R(46), INK, GOLD, padx=40, pady=24), ((W - pill('Westfield Topanga · 2nd Floor', R(46), INK, GOLD, padx=40, pady=24).width) // 2, 1250)),
                            center_text('lululandkids.com', R(60), WHITE, 1380, stroke=7)])
    SC = [
        V(14, 3.9, 4, [(cap('c1', 'SHOPPING AT', 'WESTFIELD TOPANGA?'), 0.1, 'right')], tr=('coverleft', .5)),
        V(13, 0.6, 4, [(cap('c2', 'TAKE A', 'CREATIVE BREAK'), 0.1, 'right')], tr=('coverleft', .5)),
        V(0, 4.0, 4, [(cap('c3', 'UP TO THE', '2ND FLOOR'), 0.1, 'right')], tr=('revealleft', .5)),
        V(1, 6.0, 4, tr=('slideleft', .5)), P(142, 4, move='left', tr=('slideleft', .5)), V(11, 1.0, 4, tr=('slideleft', .5)),
        P(2, 4, [(cap('c4', 'WALK OUT WITH', 'SOMETHING YOU MADE'), 0.1, 'right')], move='in', tr=('coverup', .5)),
        P(127, 9.5, [(end, 0.05, 'pop')], crop=dict(blur=10)),
    ]
    return build('LuluLand_15s_N_ShoppingBreak', M + 'swing.wav', 150, SC, 15.0, [], 'Shopping break')

# ======================= 10. POV first visit (15s, lo-fi) =======================
def ad_pov():
    p = 'N10_'
    tb = lambda nm, t, y=1180: layer(p + nm, [tbox(t, 56, y=y)])
    def note(im):
        d = ImageDraw.Draw(im); x0, y0, x1, y1 = 120, 380, W - 120, 1400
        d.rounded_rectangle([x0 + 10, y0 + 14, x1 + 10, y1 + 14], 24, fill=(0, 0, 0, 90)); d.rounded_rectangle([x0, y0, x1, y1], 24, fill=CREAM)
        for yy in range(y0 + 430, y1 - 40, 90): d.line([(x0 + 40, yy), (x1 - 40, yy)], fill=(200, 210, 225, 255), width=3)
        im.alpha_composite(paint('wordmark', 360), ((W - 360) // 2, y0 + 40))
        for i, (t, c) in enumerate([('walk in & create', NAVY), ('pour art · slime · patches', NAVY), ('Westfield Topanga · 2nd floor', NAVY), ('lululandkids.com', ROSE)]):
            tt = text_layer(t, N(52), c, pad=0); im.alpha_composite(tt, ((W - tt.width) // 2, y0 + 470 + i * 90))
    SC = [
        V(0, 1.0, 4, [(tb('t1', 'POV: your first time at Lulu Land', 300), 0.2, 'fade')], lofi=True, tr=('fade', .5)),
        P(73, 3, [(tb('t2', 'step 1: pick your piece'), 0.15, 'fade')], move='in', lofi=True, tr=('fade', .5)),
        P(142, 3, [(tb('t3', 'step 2: pick your charms'), 0.15, 'fade')], move='right', lofi=True, tr=('fade', .5)),
        V(1, 6.0, 3, [(tb('t4', 'step 3: make it yours'), 0.15, 'fade')], lofi=True, tr=('fade', .5)),
        P(2, 3, [(tb('t5', 'leaving with stuff we made 🫶'.replace(' 🫶', '')), 0.15, 'fade')], move='in', lofi=True, tr=('fade', .5)),
        C('#e8dccb', 5, [(layer(p + 'n', [note]), 0.05, 'up')], lofi=True),
    ]
    return build('LuluLand_15s_O_POV', M + 'lofi.wav', 84, SC, 15.0, [], 'POV: first visit')

ADS = {'F': ad_trailer, 'G': ad_top5, 'H': ad_beforeafter, 'I': ad_scenes, 'J': ad_rainy, 'K': ad_asmr, 'L': ad_slimebeat, 'M': ad_grand, 'N': ad_shopping, 'O': ad_pov}
if __name__ == '__main__':
    for k in (sys.argv[1:] or ADS): ADS[k]()
