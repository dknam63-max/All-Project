import subprocess, os, urllib.request, wave
os.chdir("/home/user"); os.makedirs("fin",exist_ok=True); os.chdir("fin")
def run(c):
    print("+"," ".join(c)[:170]); subprocess.run(c,check=True)
def dl(u,o):
    for i in range(4):
        try: urllib.request.urlretrieve(u,o); return
        except Exception as e: print("retry",o,e)
    raise SystemExit("dl fail "+u)

# --- 6 final source files from Google Drive (public) ---
DRIVE={"1_messy.png":"1-UBRcEnEDWB9CXmLLXQeWDwKjIQeZW3p",
       "2_tidy.png":"10AxXiJhGlr-i_kktg2-sJ3XQHc5WcRGY",
       "3_unroll.mp4":"1voaLi20LjzMRiKPc0Pd0PexYz4U0iQKo",
       "5_enter.mp4":"1Q646NFB_ik2IEG8EcwuKN1B8WnJ1zd6v",
       "6_final.png":"1_FQ7B-ynHH5SL4AuYrvB6AZwX83vxXTg"}
for n,i in DRIVE.items():
    dl(f"https://drive.usercontent.google.com/download?id={i}&export=download",n)
# narration (Ava)
CF="https://d8j0ntlcm91z4.cloudfront.net/user_3GSJKMpiMvaQXlBywoOArsxC3nk/"
NAR={"a1":"hf_20260803_024908_0e0fdeb0-f5ce-4d4d-8740-6bb38deb22f4.mp3",
     "a2":"hf_20260803_024938_27d287e2-78f8-4496-9493-bb639648cf5a.mp3",
     "a3":"hf_20260803_024913_0165d335-cc82-4be5-a445-6e596e867023.mp3",
     "a5":"hf_20260803_024916_5fd94d2d-8302-42dd-9535-bea5721dfbd8.mp3",
     "a6":"hf_20260803_024920_75f37f2b-f95e-42a3-9cc1-7fd02c215333.mp3"}
for k,v in NAR.items(): dl(CF+v,k+".mp3")
# font
for u in ["https://raw.githubusercontent.com/google/fonts/main/ofl/nanumgothic/NanumGothic-Bold.ttf",
          "https://raw.githubusercontent.com/googlefonts/nanum-gothic/master/fonts/ttf/NanumGothic-Bold.ttf"]:
    try:
        urllib.request.urlretrieve(u,"NG.ttf")
        if os.path.getsize("NG.ttf")>50000: break
    except Exception as e: print("font",e)
os.makedirs("fdir",exist_ok=True); run(["cp","NG.ttf","fdir/NanumGothic-Bold.ttf"])

E=["-c:v","libx264","-crf","20","-preset","veryfast","-pix_fmt","yuv420p"]
COVER="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"
def imgseg(img,dur,frames,z,out):
    run(["ffmpeg","-y","-loop","1","-t",str(dur),"-i",img,"-filter_complex",
      f"[0:v]{COVER},scale=1188:2112,zoompan=z='{z}':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=24,setsar=1[v]",
      "-map","[v]","-frames:v",str(frames),*E,out])
def vidseg(vid,dur,out):
    run(["ffmpeg","-y","-i",vid,"-filter_complex",f"[0:v]{COVER},fps=24,setsar=1[v]","-map","[v]","-t",str(dur),"-an",*E,out])

# ① hook  2.0s
imgseg("1_messy.png",2.0,48,"min(1.0+0.0006*on,1.06)","s1.mp4")
# ② unroll 3.0s
vidseg("3_unroll.mp4",3.0,"s2.mp4")
# ③ after 4.0s
imgseg("2_tidy.png",4.0,96,"max(1.06-0.0004*on,1.0)","s3.mp4")
# ④ before/after swipe (씬①·③ 소스) 4.0s + labels
run(["ffmpeg","-y","-loop","1","-t","4.2","-i","1_messy.png","-loop","1","-t","4.2","-i","2_tidy.png","-filter_complex",
     f"[0:v]{COVER},setsar=1,fps=24,drawtext=fontfile=NG.ttf:text='BEFORE':x=(w-tw)/2:y=150:fontsize=64:fontcolor=white:borderw=5:bordercolor=black@0.9[a];"
     f"[1:v]{COVER},setsar=1,fps=24,drawtext=fontfile=NG.ttf:text='AFTER':x=(w-tw)/2:y=150:fontsize=64:fontcolor=white:borderw=5:bordercolor=0x2E7D32[b];"
     "[a][b]xfade=transition=wiperight:duration=1.6:offset=1.4,format=yuv420p[v]","-map","[v]","-t","4.0",*E,"s4.mp4"])
# ⑤ enter 4.0s
vidseg("5_enter.mp4",4.0,"s5.mp4")
# ⑥ final 3.0s (card later)
imgseg("6_final.png",5.0,120,"min(1.0+0.0004*on,1.05)","s6.mp4")

with open("cc.txt","w") as f:
    for s in ["s1","s2","s3","s4","s5","s6"]: f.write(f"file '{s}.mp4'\n")
run(["ffmpeg","-y","-f","concat","-safe","0","-i","cc.txt","-c","copy","vid.mp4"])

# CTA card
from PIL import Image,ImageDraw,ImageFont
W,H=1080,1920
card=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(card)
fb=ImageFont.truetype("NG.ttf",58); fm=ImageFont.truetype("NG.ttf",34); fp=ImageFont.truetype("NG.ttf",40)
# card placed on the empty floor right behind the mat (mat back/top edge ~y1150)
x0,y0,x1,y1=165,955,915,1155
d.rounded_rectangle([x0+6,y0+9,x1+6,y1+9],radius=38,fill=(0,0,0,80))
d.rounded_rectangle([x0,y0,x1,y1],radius=38,fill=(250,247,238,250))
def ctext(y,txt,fnt,col):
    w=d.textlength(txt,font=fnt); d.text(((W-w)/2,y),txt,font=fnt,fill=col)
ctext(y0+16,"에어클린매트",fb,(28,28,28,255))
ctext(y0+80,"현관 인테리어 추천",fm,(95,95,95,255))
pt="네이버 스마트스토어 검색"; pw=d.textlength(pt,font=fp); pad=44
px0=(W-pw)/2-pad; px1=(W+pw)/2+pad; py0=y0+120; py1=py0+70
d.rounded_rectangle([px0,py0,px1,py1],radius=35,fill=(3,199,90,255))
d.ellipse([px0+30,py0+22,px0+50,py0+42],outline=(255,255,255,255),width=5)
d.line([px0+47,py0+39,px0+58,py0+50],fill=(255,255,255,255),width=5)
d.text(((W-pw)/2+28,py0+14),pt,font=fp,fill=(255,255,255,255))
card.save("card.png")
run(["ffmpeg","-y","-i","vid.mp4","-loop","1","-i","card.png","-filter_complex",
     "[1:v]format=rgba,fade=t=in:st=17.0:d=0.5:alpha=1[c];[0:v][c]overlay=0:0:enable='gte(t,17.0)':shortest=1[v]","-map","[v]",*E,"vidc.mp4"])

# subtitles
def at(t): return f"{int(t//3600):d}:{int((t%3600)//60):02d}:{t%60:05.2f}"
subs=[(0.15,2.0,"우리 집 현관, 그냥 두실 건가요?"),(2.15,5.0,"매트 하나만 바꿔도"),
      (5.15,9.0,"분위기가 달라집니다"),(13.15,17.0,"집의 첫인상을 바꾸는 방법")]
head="[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: Def,NanumGothic Bold,60,&H00FFFFFF,&H00000000,&H64000000,1,1,4,2,2,60,60,190,1\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
with open("subs.ass","w") as f:
    f.write(head)
    for a,b,t in subs: f.write(f"Dialogue: 0,{at(a)},{at(b)},Def,,0,0,0,,{t}\n")
run(["ffmpeg","-y","-i","vidc.mp4","-vf","subtitles=subs.ass:fontsdir=fdir","-c:a","copy",*E,"vsub.mp4"])

# BGM
import numpy as np
sr=44100; dur=22.0; N=int(sr*dur); t=np.arange(N)/sr; seglen=dur/4
prog=[[261.63,329.63,392.00],[196.00,246.94,392.00],[220.00,261.63,329.63],[174.61,220.00,349.23]]
bgm=np.zeros(N)
for i,ch in enumerate(prog):
    s=int(i*seglen*sr); e=int(min((i+1)*seglen,dur)*sr); tt=np.arange(e-s)/sr; seg=np.zeros(e-s)
    for f0 in ch: seg+=np.sin(2*np.pi*f0*tt)*0.5+np.sin(2*np.pi*f0*2*tt)*0.12
    env=np.clip(np.minimum(tt/0.4,(len(tt)/sr-tt)/0.4),0,1); bgm[s:e]+=seg*env
bgm*=(0.9+0.1*np.sin(2*np.pi*1.5*t))
fd=int(1.2*sr); bgm[:fd]*=np.linspace(0,1,fd); bgm[-fd:]*=np.linspace(1,0,fd)
bgm=bgm/np.max(np.abs(bgm))*0.5
with wave.open("bgm.wav","w") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(np.int16(bgm*32767).tobytes())

# narration timeline
offs={"a1":150,"a2":2200,"a3":5200,"a5":13200,"a6":17100}; parts=[]
for k,ms in offs.items():
    run(["ffmpeg","-y","-i",k+".mp3","-af",f"aresample=44100,adelay={ms}|{ms},apad","-t","22","-ac","2","-ar","44100",k+"_d.wav"]); parts.append(k+"_d.wav")
cmd=["ffmpeg","-y"]
for p in parts: cmd+=["-i",p]
cmd+=["-filter_complex",f"amix=inputs={len(parts)}:duration=longest:normalize=0,volume=2.0,aresample=44100[nar]","-map","[nar]","-t","22","-ac","2","-ar","44100","nar.wav"]
run(cmd)
run(["ffmpeg","-y","-i","bgm.wav","-i","nar.wav","-filter_complex",
     "[1:a]asplit=2[nn][sc];[0:a][sc]sidechaincompress=threshold=0.04:ratio=9:attack=25:release=320[bd];[bd][nn]amix=inputs=2:duration=longest:normalize=0,loudnorm=I=-14:TP=-1:LRA=11[a]",
     "-map","[a]","-t","22","-ac","2","-ar","44100","mix.wav"])
run(["ffmpeg","-y","-i","vsub.mp4","-i","mix.wav","-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-b:a","192k","-shortest","/home/user/ACM_02_final5_916.mp4"])
print("DONE", os.path.getsize("/home/user/ACM_02_final5_916.mp4"))
