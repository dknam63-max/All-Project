import subprocess, os, json, urllib.request, math, struct, wave
os.chdir("/home/user")
def run(c):
    print("+"," ".join(c)[:180]); subprocess.run(c,check=True)
def dl(u,o):
    for i in range(4):
        try: urllib.request.urlretrieve(u,o); return
        except Exception as e:
            print("retry",o,e)
    raise SystemExit("dl fail "+u)

RAW="https://raw.githubusercontent.com/dknam63-max/All-Project/claude/beach-sunrise-video-c29b9q/assets/acm2/"
CF="https://d8j0ntlcm91z4.cloudfront.net/user_3GSJKMpiMvaQXlBywoOArsxC3nk/"
# assets
dl(RAW+"before.jpg","before.jpg")
dl(RAW+"after.jpg","after.jpg")
dl(RAW+"unroll_real.mp4","unroll.mp4")
dl(RAW+"feet.mp4","feet.mp4")
# narration
NAR={"a1":"hf_20260803_024908_0e0fdeb0-f5ce-4d4d-8740-6bb38deb22f4.mp3",
     "a2":"hf_20260803_024938_27d287e2-78f8-4496-9493-bb639648cf5a.mp3",
     "a3":"hf_20260803_024913_0165d335-cc82-4be5-a445-6e596e867023.mp3",
     "a5":"hf_20260803_024916_5fd94d2d-8302-42dd-9535-bea5721dfbd8.mp3",
     "a6":"hf_20260803_024920_75f37f2b-f95e-42a3-9cc1-7fd02c215333.mp3"}
for k,v in NAR.items(): dl(CF+v,k+".mp3")
# font
FONTS=["https://raw.githubusercontent.com/google/fonts/main/ofl/nanumgothic/NanumGothic-Bold.ttf",
       "https://raw.githubusercontent.com/googlefonts/nanum-gothic/master/fonts/ttf/NanumGothic-Bold.ttf"]
got=False
for u in FONTS:
    try: urllib.request.urlretrieve(u,"NG.ttf"); got=(os.path.getsize("NG.ttf")>50000);
    except Exception as e: print("font retry",e); got=False
    if got: break
if not got: raise SystemExit("font fail")
os.makedirs("fdir",exist_ok=True); run(["cp","NG.ttf","fdir/NanumGothic-Bold.ttf"])

E=["-c:v","libx264","-crf","20","-preset","veryfast","-pix_fmt","yuv420p"]
def probe(f):
    r=subprocess.run(["ffprobe","-v","0","-select_streams","v:0","-show_entries","stream=width,height","-of","json",f],capture_output=True,text=True)
    s=json.loads(r.stdout)["streams"][0]; return int(s["width"]),int(s["height"])
def vfit(f):
    w,h=probe(f)
    if w>h:  # landscape -> blur pad
        return ("[0:v]split=2[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=28[bg];"
                "[b]scale=1080:608[fg];[bg][fg]overlay=(W-w)/2:656,fps=24,setsar=1[v]")
    else:    # portrait/square -> cover crop
        return "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=24,setsar=1[v]"

# ---- segments ----
# S1 hook (before) 2.0s  subtle slow zoom-in
run(["ffmpeg","-y","-loop","1","-t","2.0","-i","before.jpg","-filter_complex",
     "[0:v]scale=1188:2112,zoompan=z='min(1.0+0.0006*on,1.06)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=24,setsar=1[v]",
     "-map","[v]","-frames:v","48",*E,"s1.mp4"])
# S2 unroll 3.0s
run(["ffmpeg","-y","-i","unroll.mp4","-filter_complex",vfit("unroll.mp4"),"-map","[v]","-t","3.0","-an",*E,"s2.mp4"])
# S3 after 4.0s subtle zoom-out
run(["ffmpeg","-y","-loop","1","-t","4.0","-i","after.jpg","-filter_complex",
     "[0:v]scale=1188:2112,zoompan=z='max(1.06-0.0004*on,1.0)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=24,setsar=1[v]",
     "-map","[v]","-frames:v","96",*E,"s3.mp4"])
# S4 before/after wiperight slider 4.0s with BEFORE/AFTER labels
run(["ffmpeg","-y","-loop","1","-t","4.2","-i","before.jpg","-loop","1","-t","4.2","-i","after.jpg","-filter_complex",
     "[0:v]scale=1080:1920,setsar=1,fps=24,drawtext=fontfile=NG.ttf:text='BEFORE':x=(w-tw)/2:y=150:fontsize=64:fontcolor=white:borderw=5:bordercolor=black@0.9[a];"
     "[1:v]scale=1080:1920,setsar=1,fps=24,drawtext=fontfile=NG.ttf:text='AFTER':x=(w-tw)/2:y=150:fontsize=64:fontcolor=white:borderw=5:bordercolor=0x2E7D32[b];"
     "[a][b]xfade=transition=wiperight:duration=1.6:offset=1.4,format=yuv420p[v]",
     "-map","[v]","-t","4.0",*E,"s4.mp4"])
# S5 feet 4.0s
run(["ffmpeg","-y","-i","feet.mp4","-filter_complex",vfit("feet.mp4"),"-map","[v]","-t","4.0","-an",*E,"s5.mp4"])
# S6 cta (after) 3.0s  (card overlaid later)
run(["ffmpeg","-y","-loop","1","-t","3.0","-i","after.jpg","-filter_complex",
     "[0:v]scale=1188:2112,zoompan=z='min(1.0+0.0005*on,1.05)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=24,setsar=1[v]",
     "-map","[v]","-frames:v","72",*E,"s6.mp4"])

# concat video
with open("cc.txt","w") as f:
    for s in ["s1","s2","s3","s4","s5","s6"]: f.write(f"file '{s}.mp4'\n")
run(["ffmpeg","-y","-f","concat","-safe","0","-i","cc.txt","-c","copy","vid.mp4"])

# ---- CTA card (Pillow) ----
from PIL import Image,ImageDraw,ImageFont
W,H=1080,1920
card=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(card)
fb=ImageFont.truetype("NG.ttf",92); fm=ImageFont.truetype("NG.ttf",50); fp=ImageFont.truetype("NG.ttf",46)
x0,y0,x1,y1=90,980,990,1300
d.rounded_rectangle([x0,y0,x1,y1],radius=44,fill=(250,247,238,242))
def ctext(y,txt,fnt,col):
    w=d.textlength(txt,font=fnt); d.text(((W-w)/2,y),txt,font=fnt,fill=col)
ctext(y0+40,"에어클린매트",fb,(30,30,30,255))
ctext(y0+160,"현관 인테리어 추천",fm,(90,90,90,255))
# pill
pt="네이버 스마트스토어 검색"; pw=d.textlength(pt,font=fp); pad=34
px0=(W-pw)/2-pad; px1=(W+pw)/2+pad; py0=y0+232; py1=py0+78
d.rounded_rectangle([px0,py0,px1,py1],radius=39,fill=(3,199,90,255))
d.text(((W-pw)/2,py0+16),pt,font=fp,fill=(255,255,255,255))
card.save("card.png")

# overlay card on last 3s (t=17..20)
run(["ffmpeg","-y","-i","vid.mp4","-i","card.png","-filter_complex",
     "[1:v]format=rgba,fade=t=in:st=17.2:d=0.4:alpha=1[c];[0:v][c]overlay=0:0:enable='gte(t,17.2)'[v]",
     "-map","[v]",*E,"vidc.mp4"])

# ---- subtitles ASS ----
def ass_time(t):
    h=int(t//3600); m=int((t%3600)//60); s=t%60; return f"{h:d}:{m:02d}:{s:05.2f}"
subs=[(0.15,2.0,"우리 집 현관, 그냥 두실 건가요?"),
      (2.15,5.0,"매트 하나만 바꿔도"),
      (5.15,9.0,"분위기가 달라집니다"),
      (13.15,17.0,"집의 첫인상을 바꾸는 방법")]
head="""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Def,NanumGothic Bold,60,&H00FFFFFF,&H00000000,&H64000000,1,1,4,2,2,60,60,190,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
with open("subs.ass","w") as f:
    f.write(head)
    for a,b,t in subs:
        f.write(f"Dialogue: 0,{ass_time(a)},{ass_time(b)},Def,,0,0,0,,{t}\n")
run(["ffmpeg","-y","-i","vidc.mp4","-vf","subtitles=subs.ass:fontsdir=fdir","-c:a","copy",*E,"vsub.mp4"])

# ---- BGM procedural (warm pad) ----
import numpy as np
sr=44100; dur=20.0; N=int(sr*dur)
t=np.arange(N)/sr
# chord progression C-G-Am-F, 5s each
prog=[[261.63,329.63,392.00],[196.00,246.94,392.00],[220.00,261.63,329.63],[174.61,220.00,349.23]]
bgm=np.zeros(N)
for i,ch in enumerate(prog):
    s=int(i*5*sr); e=int(min((i+1)*5,dur)*sr)
    seg=np.zeros(e-s); tt=np.arange(e-s)/sr
    for f0 in ch:
        seg+=np.sin(2*np.pi*f0*tt)*0.5+np.sin(2*np.pi*f0*2*tt)*0.12
    # soft attack/decay per chord
    env=np.minimum(1,np.minimum(tt/0.4,(len(tt)/sr-tt)/0.4)); env=np.clip(env,0,1)
    bgm[s:e]+=seg*env
# gentle tremolo + overall fade
bgm*= (0.9+0.1*np.sin(2*np.pi*1.5*t))
fade=int(1.2*sr); bgm[:fade]*=np.linspace(0,1,fade); bgm[-fade:]*=np.linspace(1,0,fade)
bgm=bgm/np.max(np.abs(bgm))*0.5
wav=np.int16(bgm*32767)
with wave.open("bgm.wav","w") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(wav.tobytes())

# ---- narration timeline ----
# place clips at offsets
def adelay(inp,ms,out):
    run(["ffmpeg","-y","-i",inp,"-af",f"adelay={ms}|{ms},apad","-t","20","-ac","2",out])
offs={"a1":150,"a2":2200,"a3":5200,"a5":13200,"a6":17100}
amix_in=[]
for k,ms in offs.items():
    adelay(k+".mp3",ms,k+"_d.wav"); amix_in.append(k+"_d.wav")
# combine narration into one bed
ni=[];
cmd=["ffmpeg","-y"]
for f in amix_in: cmd+=["-i",f]
cmd+=["-filter_complex",f"amix=inputs={len(amix_in)}:duration=long:normalize=0,volume=2.0[nar]","-map","[nar]","-t","20","-ac","2","nar.wav"]
run(cmd)
# duck BGM under narration via sidechaincompress, then mix
run(["ffmpeg","-y","-i","bgm.wav","-i","nar.wav","-filter_complex",
     "[1:a]asplit=2[nn][sc];[0:a][sc]sidechaincompress=threshold=0.04:ratio=9:attack=25:release=320[bd];"
     "[bd][nn]amix=inputs=2:duration=long:normalize=0,loudnorm=I=-14:TP=-1:LRA=11[a]",
     "-map","[a]","-t","20","-ac","2","-ar","44100","mix.wav"])

# ---- mux ----
run(["ffmpeg","-y","-i","vsub.mp4","-i","mix.wav","-map","0:v","-map","1:a",
     "-c:v","copy","-c:a","aac","-b:a","192k","-shortest","ACM_02_v1_916.mp4"])
print("DONE size", os.path.getsize("ACM_02_v1_916.mp4"))
