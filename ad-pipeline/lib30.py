import json,os,subprocess,imageio_ffmpeg,re
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance, ImageStat
FF=imageio_ffmpeg.get_ffmpeg_exe()
# Paths: fonts in ./fonts, rendered layers in ./out/v, media index from index_media.py (env WORK, default ./work)
S=os.path.dirname(os.path.abspath(__file__)); A=S+'/fonts'; O=S+'/out/v'
REPO=os.environ.get('LULULAND_REPO', os.path.expanduser('~/projects/lululand')); P=REPO+'/site/images/paint/'
os.makedirs(O,exist_ok=True)
WORK=os.environ.get('WORK', S+'/work'); IDX=json.load(open(WORK+'/index.json'))
items=IDX['videos']; photos=IDX['photos']
vsrc=lambda n: items[n]['path']; psrc=lambda n: photos[n]['path']
W,H=1080,1920
NAVY=(2,36,73,255); ROSE=(223,90,121,255); GOLD=(233,162,20,255); CREAM=(248,241,231,255); INK=(11,7,6,255); WHITE=(255,255,255,255); SAGE=(113,131,105,255); TEAL=(0,166,176,255)
R=lambda s: ImageFont.truetype(A+'/RammettoOne-d182e5.ttf',s)
def N(s):
    f=ImageFont.truetype(A+'/NunitoExtraLight-07454f.ttf',s)
    try: f.set_variation_by_axes([900])
    except Exception: pass
    return f
def canvas(): return Image.new('RGBA',(W,H),(0,0,0,0))
def shadowed(im,layer,xy,blur=10,op=0.45):
    sh=Image.new('RGBA',layer.size,(0,0,0,0)); sh.putalpha(layer.getchannel('A').point(lambda a:int(a*op))); sh=sh.filter(ImageFilter.GaussianBlur(blur))
    im.alpha_composite(sh,(xy[0]+6,xy[1]+12)); im.alpha_composite(layer,xy)
def paint(name,width):
    t=Image.open(P+name+'.webp').convert('RGBA'); return t.resize((width,round(t.height*width/t.width)),Image.LANCZOS)
def text_layer(txt,font,fill,stroke=0,stroke_fill=INK,pad=20):
    d=ImageDraw.Draw(Image.new('RGBA',(1,1))); b=d.textbbox((0,0),txt,font=font,stroke_width=stroke)
    im=Image.new('RGBA',(b[2]-b[0]+pad*2,b[3]-b[1]+pad*2),(0,0,0,0)); ImageDraw.Draw(im).text((pad-b[0],pad-b[1]),txt,font=font,fill=fill,stroke_width=stroke,stroke_fill=stroke_fill); return im
def pill(txt,font,fg,bg,padx=46,pady=26,rot=0):
    t=text_layer(txt,font,fg,pad=0); w,h=t.width+padx*2,t.height+pady*2
    im=Image.new('RGBA',(w+14,h+16),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle([10,12,w+10,h+12],h//2,fill=INK); d.rounded_rectangle([0,0,w,h],h//2,fill=bg,outline=INK,width=6)
    im.alpha_composite(t,(padx,pady)); return im.rotate(rot,expand=True,resample=Image.BICUBIC) if rot else im
def save(layers,name):
    im=canvas()
    for fn in layers: fn(im)
    im.save(f'{O}/{name}.png'); return name
def at(layer,x,y): return lambda im: im.alpha_composite(layer,(x if x is not None else (W-layer.width)//2,y))
def sh_at(layer,x,y): return lambda im: shadowed(im,layer,(x if x is not None else (W-layer.width)//2,y))
# ---------- photo prep (retouch + 9:16 crop at 1.5x for smooth zoom) ----------
def wb(im,s=0.45):
    r,g,b=ImageStat.Stat(im).mean; a=(r+g+b)/3
    return Image.merge('RGB',[c.point(lambda v,k=1+s*(a/m-1): min(255,int(v*k))) for c,m in zip(im.split(),(r,g,b))])
def prep_photo(n,fx=0.5,fy=0.5,z=1.0,rot=0,blur=0):
    im=ImageOps.exif_transpose(Image.open(psrc(n))).convert('RGB')
    if rot: im=im.rotate(rot,expand=True)
    im=wb(im); im=ImageOps.autocontrast(im,cutoff=(0.4,0.6),preserve_tone=True); im=ImageEnhance.Color(im).enhance(1.1)
    Wd,Hd=im.size; ar=9/16; cw=min(Wd,Hd*ar)*z; ch=cw/ar
    l=max(0,min(Wd-cw,fx*Wd-cw/2)); t=max(0,min(Hd-ch,fy*Hd-ch/2))
    im=im.crop((round(l),round(t),round(l+cw),round(t+ch))).resize((1620,2880),Image.LANCZOS)
    if blur: im=im.filter(ImageFilter.GaussianBlur(blur))
    p=f'{O}/ph{n}.png'; im.save(p); return p

chip=lambda t,bg=GOLD,fg=INK,rot=-3: pill(t,R(54),fg,bg,rot=rot)
def big(lines,y,gap=8):
    """lines: [(text,size,color)] stacked & centered, with stroke"""
    fns=[]; yy=y
    for t,sz,c in lines:
        l=text_layer(t,R(sz),c,stroke=max(6,sz//10)); fns.append(sh_at(l,None,yy)); yy+=l.height-40+gap
    return fns
def card(title,items,y0=1010,row=118,size=50):
    def f(im):
        d=ImageDraw.Draw(im); x0,x1=60,W-60; y1=y0+150+row*len(items)
        d.rounded_rectangle([x0+12,y0+14,x1+12,y1+14],48,fill=INK); d.rounded_rectangle([x0,y0,x1,y1],48,fill=WHITE,outline=INK,width=6)
        d.rounded_rectangle([x0,y0,x1,y0+130],48,fill=SAGE,outline=INK,width=6); d.rectangle([x0+6,y0+80,x1-6,y0+124],fill=SAGE); d.line([x0,y0+130,x1,y0+130],fill=INK,width=6)
        im.alpha_composite(text_layer(title,R(60),WHITE,pad=0),(x0+50,y0+30)); im.alpha_composite(pill('2 HOURS',R(38),INK,GOLD,padx=28,pady=16),(x1-300,y0+28))
    return f
def check(txt,i,y0=1010,row=118,size=50):
    def f(im):
        d=ImageDraw.Draw(im); y=y0+160+i*row; x=110
        d.ellipse([x,y,x+60,y+60],fill=SAGE,outline=INK,width=4); d.line([(x+15,y+31),(x+26,y+43),(x+46,y+19)],fill=WHITE,width=8,joint='curve')
        im.alpha_composite(text_layer(txt,N(size),NAVY,pad=0),(x+86,y+2))
    return f
def tint(a=165): return lambda im: im.alpha_composite(Image.new('RGBA',(W,H),(2,36,73,a)))
HOURS=['Mon–Thu 10am–8pm','Fri–Sat 10am–9pm','Sun 11am–7pm']
def walkin_end(prefix,top_title=None):
    L={}
    L['e0']=save([tint(150)],prefix+'e0')
    L['e1']=save([sh_at(paint('wordmark',430),None,70)],prefix+'e1')
    L['e2']=save(([sh_at(paint(top_title,820),None,560)] if top_title else big([('NOW OPEN',110,GOLD)],600)),prefix+'e2')
    def hours(im):
        d=ImageDraw.Draw(im); x0,y0,x1,y1=110,880,W-110,1250
        d.rounded_rectangle([x0+10,y0+12,x1+10,y1+12],44,fill=INK); d.rounded_rectangle([x0,y0,x1,y1],44,fill=CREAM,outline=INK,width=6)
        t=text_layer('WALK IN · NO BOOKING NEEDED',R(40),ROSE,pad=0); im.alpha_composite(t,((W-t.width)//2,y0+34))
        for i,h in enumerate(HOURS):
            t=text_layer(h,N(56),NAVY,pad=0); im.alpha_composite(t,((W-t.width)//2,y0+120+i*78))
    L['e3']=save([hours],prefix+'e3')
    L['e4']=save([at(pill('Westfield Topanga · 2nd Floor',R(46),INK,GOLD,padx=40,pady=24),None,1330),
                  sh_at(text_layer('lululandkids.com',R(64),WHITE,stroke=8),None,1470),
                  at(text_layer('Birthday parties: (818) 668-3342',N(42),CREAM,stroke=4),None,1590)],prefix+'e4')
    return [(prefix+'e0',0.0),(prefix+'e1',0.15),(prefix+'e2',0.45),(prefix+'e3',0.9),(prefix+'e4',1.4)]
def offer_end(prefix):
    save([tint(165)],prefix+'f0')
    save([at(pill('GRAND OPENING',R(70),INK,GOLD,rot=-4),None,90)],prefix+'f1')
    save([at(pill('FIRST 10 NEW FAMILIES',R(54),WHITE,ROSE),None,320)],prefix+'f2')
    def struck(im):
        t=text_layer('$65',R(130),(200,205,215,255),stroke=8); x=(W-t.width)//2; y=600; im.alpha_composite(t,(x,y))
        ImageDraw.Draw(im).line([(x+20,y+t.height-40),(x+t.width-20,y+40)],fill=ROSE,width=18)
    save([sh_at(text_layer('LULU PARTY · BIRTHDAYS',R(64),WHITE,stroke=8),None,490), struck],prefix+'f3')
    def price(im):
        p=text_layer('$59',R(300),GOLD,stroke=16); shadowed(im,p,((W-p.width)//2,760),blur=14,op=0.6)
        im.alpha_composite(paint('icon-cake',180),(20,860)); im.alpha_composite(paint('icon-balloons',165),(W-190,800))
        t=text_layer('PER KID',R(80),WHITE,stroke=8); im.alpha_composite(t,((W-t.width)//2,1110))
    save([price],prefix+'f4')
    save([at(pill('CALL NOW',R(66),WHITE,ROSE,padx=60,pady=30),None,1250),
          sh_at(text_layer('(818) 668-3342',R(92),WHITE,stroke=9),None,1405),
          at(text_layer('lululandkids.com · Westfield Topanga 2nd Floor',N(38),CREAM,stroke=4),None,1535),
          at(text_layer('*Lulu Party package. Min. 8 kids. 15% service fee not included. First 10 new families.',N(26),CREAM,stroke=3),None,1598)],prefix+'f5')
    return [(prefix+'f0',0.0),(prefix+'f1',0.15),(prefix+'f2',0.5),(prefix+'f3',0.9),(prefix+'f4',1.7),(prefix+'f5',2.6)]
V=lambda n,ss,ln,ov=(): ('v',n,ss,ln,list(ov))
Pp=lambda n,ln,ov=(),**kw: ('p',n,kw,ln,list(ov))
def render(SC,outname,amb=0.45):
    parts=[]; t0=0
    for k,seg in enumerate(SC):
        kind,n,arg,ln,ovs=seg; out=f'{O}/{outname}_s{k}.mp4'
        if kind=='v':
            inputs=['-ss',str(arg),'-t',str(ln),'-i',vsrc(n)]
            fc=f"[0:v]fps=30,scale={W}:{H}:flags=lanczos,setsar=1,eq=saturation=1.12:contrast=1.04:brightness=0.02,unsharp=5:5:0.6[v0]"
        else:
            ph=prep_photo(n,**arg); fr=int(round(ln*30))
            z=f"1.0+0.08*on/{fr}" if k%2 else f"1.08-0.08*on/{fr}"
            inputs=['-framerate','30','-loop','1','-t',str(ln),'-i',ph]
            fc=f"[0:v]zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps=30,setsar=1[v0]"
        last='v0'
        for j,(name,tin) in enumerate(ovs):
            inputs+=['-loop','1','-t',str(ln),'-i',f'{O}/{name}.png']
            slide=not (name.endswith('f0') or name.endswith('e0'))
            y=f":y='70*max(0\\,1-(t-{tin})/0.25)'" if slide else ''
            fc+=f";[{j+1}:v]format=rgba,fade=in:st={tin}:d=0.25:alpha=1[ov{j}];[{last}][ov{j}]overlay=0:0{y}:shortest=1[v{j+1}]"; last=f'v{j+1}'
        fc+=f";[{last}]null[v]"
        has_a=kind=='v' and 'Audio' in subprocess.run([FF,'-i',vsrc(n)],capture_output=True,text=True).stderr
        if has_a: af=f"[0:a]aresample=44100,pan=stereo|c0=c0|c1=c0,volume={amb},afade=in:d=0.06,afade=out:st={max(0,ln-0.08)}:d=0.08[a]"
        else: inputs+=['-f','lavfi','-t',str(ln),'-i','anullsrc=r=44100:cl=stereo']; af=f"[{len(ovs)+1}:a]anull[a]"
        subprocess.run([FF,'-y','-loglevel','error']+inputs+['-filter_complex',fc+';'+af,'-map','[v]','-map','[a]','-t',str(ln),'-c:v','libx264','-preset','medium','-crf','19','-pix_fmt','yuv420p','-r','30','-c:a','aac','-ar','44100','-b:a','160k',out],check=True)
        parts.append(out); t0+=ln
    open(f'{O}/{outname}.txt','w').write(''.join(f"file '{p}'\n" for p in parts))
    final=f'{A}/{outname}.mp4'
    subprocess.run([FF,'-y','-loglevel','error','-f','concat','-safe','0','-i',f'{O}/{outname}.txt','-c:v','copy','-af','alimiter=limit=0.8:level=false','-c:a','aac','-b:a','160k','-movflags','+faststart',final],check=True)
    subprocess.run([FF,'-y','-loglevel','error','-i',final,'-map','0:v','-c:v','copy','-an','-movflags','+faststart',final.replace('.mp4','_silent.mp4')],check=True)
    print(outname, 'timeline', round(t0,2), os.path.getsize(final)//1024,'KB')
