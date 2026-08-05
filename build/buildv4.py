import subprocess, os, urllib.request, wave
os.chdir("/home/user"); os.makedirs("v4",exist_ok=True); os.chdir("v4")
def run(c): print("+"," ".join(c)[:150]); subprocess.run(c,check=True)
def dl(u,o):
    for i in range(4):
        try: urllib.request.urlretrieve(u,o); return
        except Exception as e: print("retry",o,e)
    raise SystemExit("dl "+u)

CF="https://d8j0ntlcm91z4.cloudfront.net/user_3GSJKMpiMvaQXlBywoOArsxC3nk/"
IMG={"s1":"hf_20260805_021738_b8448d9a-d0c5-4b97-926b-83f8273e95f0.png",  # 신발 흙먼지
     "s2":"__S2__",                                                       # 문제(먼지 날림) - filled below
     "s3":"hf_20260805_021738_5a003243-5fe4-47b0-b2ce-a7a7f0500bfa.png",  # 요철 질감
     "s4":"hf_20260805_021738_ce182d6c-8ff4-489d-bfe7-175205c67fa1.png",  # 뒤집어 먼지
     "s5":"hf_20260805_021739_b4acc3f6-bd15-477a-bf3a-923cc0d49e9c.png",  # 물방울
     "s6":"hf_20260805_021738_c44609aa-7c1b-480e-b7de-1cce688f9176.png"}  # 깨끗한 현관
S2URL=os.environ.get("S2URL","")
IMG["s2"]=S2URL.split("/")[-1] if S2URL else IMG["s1"]
for k,v in IMG.items():
    url = S2URL if (k=="s2" and S2URL) else CF+v
    dl(url,k+".png")

NAR={"n1":"hf_20260805_021706_b2835ed8-51f2-47ca-b57e-337d77cf677e.mp3",
     "n2":"hf_20260805_021706_3d067592-56e3-4edb-8686-c737179f99e8.mp3",
     "n3":"hf_20260805_021707_edc9da88-8302-432d-b34d-ad8ea3a63ecc.mp3",
     "n4":"hf_20260805_021706_4b229a2f-bd6a-4f09-9e8e-d3060e11169d.mp3",
     "n5":"hf_20260805_021706_dde1e6d1-0b99-42d9-bb48-3d25fb5d0974.mp3",
     "n6":"hf_20260805_021706_20fccc57-df9d-41c6-8772-50d8ed71f345.mp3"}
for k,v in NAR.items(): dl(CF+v,k+".mp3")
dl("https://raw.githubusercontent.com/google/fonts/main/ofl/nanumgothic/NanumGothic-Bold.ttf","NG.ttf")
os.makedirs("fdir",exist_ok=True); run(["cp","NG.ttf","fdir/NanumGothic-Bold.ttf"])

E=["-c:v","libx264","-crf","20","-preset","veryfast","-pix_fmt","yuv420p"]
COVER="scale=1920:1920:force_original_aspect_ratio=increase,crop=1080:1920"
def kb(img,frames,z,out):
    run(["ffmpeg","-y","-loop","1","-t","10","-i",img,"-filter_complex",
      f"[0:v]{COVER},scale=1188:2112,zoompan=z='{z}':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=24,setsar=1[v]",
      "-map","[v]","-frames:v",str(frames),*E,out])
zin="min(1.0+0.0006*on,1.10)"; zout="max(1.10-0.0005*on,1.0)"
# S1..S5 durations (frames@24): 84,108,144,144,120
kb("s1.png",84, zin, "d1.mp4")
kb("s2.png",108,zout,"d2.mp4")
kb("s3.png",144,zin, "d3.mp4")
kb("s4.png",144,zout,"d4.mp4")
kb("s5.png",120,zin, "d5.mp4")

# S6 CTA (5s=120f): clean entryway + brand card overlay
from PIL import Image,ImageDraw,ImageFont
im=Image.open("s6.png").convert("RGB")
Wc,Hc=im.size; s=max(1080/Wc,1920/Hc); im=im.resize((int(Wc*s),int(Hc*s)))
x=(im.width-1080)//2; y=(im.height-1920)//2; im=im.crop((x,y,x+1080,y+1920))
d=ImageDraw.Draw(im,"RGBA")
d.rectangle([0,1180,1080,1920],fill=(15,20,16,150))
ft=ImageFont.truetype("NG.ttf",70); fm=ImageFont.truetype("NG.ttf",40); fp=ImageFont.truetype("NG.ttf",46)
def ctext(yy,t,f,c):
    w=d.textlength(t,font=f); d.text(((1080-w)/2,yy),t,font=f,fill=c)
ctext(1300,"우리집 현관도 바꿔보세요",ft,(255,255,255))
ctext(1400,"미끄럼방지 · 세탁기 OK · 6가지 디자인",fm,(220,225,215))
pt="네이버 '에어클린매트' 검색"; pw=d.textlength(pt,font=fp); pad=44
px=(1080-pw)/2-pad; py=1500
d.rounded_rectangle([px,py,(1080+pw)/2+pad,py+82],radius=41,fill=(3,199,90,255))
d.text(((1080-pw)/2,py+16),pt,font=fp,fill=(255,255,255))
im.save("cta.png")
run(["ffmpeg","-y","-loop","1","-t","5","-i","cta.png","-filter_complex",
     f"[0:v]{COVER},scale=1123:1997,zoompan=z='min(1.0+0.0004*on,1.05)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=24,setsar=1,fade=t=in:st=0:d=0.4[v]",
     "-map","[v]","-frames:v","120",*E,"d6.mp4"])

# concat all
with open("mc.txt","w") as f:
    for i in range(1,7): f.write(f"file 'd{i}.mp4'\n")
run(["ffmpeg","-y","-f","concat","-safe","0","-i","mc.txt","-c","copy","main.mp4"])

# subtitles S1-S5 (S6 baked)
def at(t): return f"{int(t//3600):d}:{int((t%3600)//60):02d}:{t%60:05.2f}"
subs=[(0.2,3.5,"현관 흙먼지, 실화?!"),(3.7,8.0,"일반 매트는 먼지가 그대로 날려요"),
      (8.2,14.0,"미세 요철이 흙먼지를 꽉 붙잡아요"),(14.2,20.0,"뒤집으니 이만큼?!"),
      (20.2,25.0,"미끄럼방지 · 통째로 세탁기 OK")]
head="[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: Def,NanumGothic,60,&H00FFFFFF,&H00202020,&H64000000,1,1,5,2,2,60,60,300,1\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
with open("subs.ass","w") as f:
    f.write(head)
    for a,b,t in subs: f.write(f"Dialogue: 0,{at(a)},{at(b)},Def,,0,0,0,,{t}\n")
run(["ffmpeg","-y","-i","main.mp4","-vf","subtitles=subs.ass:fontsdir=fdir","-c:a","copy",*E,"vfull.mp4"])

# BGM (curiosity beat, 30s)
import numpy as np
sr=44100; dur=30.0; N=int(sr*dur); t=np.arange(N)/sr
prog=[[220.00,277.18,329.63],[246.94,311.13,369.99],[261.63,329.63,392.00],[293.66,349.23,440.00],[220.00,277.18,329.63]]
seglen=dur/len(prog); bgm=np.zeros(N)
for i,ch in enumerate(prog):
    a=int(i*seglen*sr); b=int(min((i+1)*seglen,dur)*sr); tt=np.arange(b-a)/sr; seg=np.zeros(b-a)
    for f0 in ch: seg+=np.sin(2*np.pi*f0*tt)*0.4+np.sin(2*np.pi*f0*2*tt)*0.08
    env=np.clip(np.minimum(tt/0.25,(len(tt)/sr-tt)/0.25),0,1); bgm[a:b]+=seg*env
pulse=0.5+0.5*(np.sin(2*np.pi*2.0*t)>0); bgm*=(0.75+0.25*pulse)
fd=int(sr); bgm[:fd]*=np.linspace(0,1,fd); bgm[-fd:]*=np.linspace(1,0,fd)
bgm=bgm/np.max(np.abs(bgm))*0.5
with wave.open("bgm.wav","w") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(np.int16(bgm*32767).tobytes())

offs={"n1":200,"n2":3700,"n3":8200,"n4":14200,"n5":20200,"n6":25200}
parts=[]
for k,ms in offs.items():
    run(["ffmpeg","-y","-i",k+".mp3","-af",f"aresample=44100,adelay={ms}|{ms},apad","-t","30","-ac","2","-ar","44100",k+"_d.wav"]); parts.append(k+"_d.wav")
cmd=["ffmpeg","-y"]
for p in parts: cmd+=["-i",p]
cmd+=["-filter_complex",f"amix=inputs={len(parts)}:duration=longest:normalize=0,volume=2.2,aresample=44100[nar]","-map","[nar]","-t","30","-ac","2","-ar","44100","nar.wav"]
run(cmd)
run(["ffmpeg","-y","-i","bgm.wav","-i","nar.wav","-filter_complex",
     "[1:a]asplit=2[nn][sc];[0:a][sc]sidechaincompress=threshold=0.04:ratio=9:attack=25:release=320[bd];[bd][nn]amix=inputs=2:duration=longest:normalize=0,loudnorm=I=-14:TP=-1:LRA=11[a]",
     "-map","[a]","-t","30","-ac","2","-ar","44100","mix.wav"])
run(["ffmpeg","-y","-i","vfull.mp4","-i","mix.wav","-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-b:a","192k","-shortest","/home/user/ACM_04_v1_916.mp4"])
print("DONE", os.path.getsize("/home/user/ACM_04_v1_916.mp4"))
