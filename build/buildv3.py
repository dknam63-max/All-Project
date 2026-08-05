import subprocess, os, urllib.request, wave
os.chdir("/home/user"); os.makedirs("v3",exist_ok=True); os.chdir("v3")
def run(c): print("+"," ".join(c)[:150]); subprocess.run(c,check=True)
def dl(u,o):
    for i in range(4):
        try: urllib.request.urlretrieve(u,o); return
        except Exception as e: print("retry",o,e)
    raise SystemExit("dl "+u)

DR="https://drive.usercontent.google.com/download?id=%s&export=download"
# 6 designs in 기획서 order: 해바라기 데이지 수국 올리브세이지 테라코타 모던한옥
IMG=[("s0","14KiDH92_rkYXOjl7Uv_ldHGbSTT1bu6F"),  # 해바라기 a
     ("s1","1D0gLYKRBUCagKzyc8COl-4DhO7ho6pNN"),  # 데이지 f
     ("s2","1TiNsMu0uXU1AXSkxoANjMOMmB07woeeL"),  # 수국 d
     ("s3","1Nwc1G1OLLTEICt0ieYUD3Amo4bpHKItK"),  # 올리브세이지 b
     ("s4","1KaNLPEDPwNThcRcWI-Xsu8fjzoCy5GM9"),  # 테라코타 e
     ("s5","11W_ZEW-HLkc3A7HEIzGTKVil3n9D3lIE")]  # 모던한옥 c
for k,v in IMG: dl(DR%v,k+".png")

CF="https://d8j0ntlcm91z4.cloudfront.net/user_3GSJKMpiMvaQXlBywoOArsxC3nk/"
# narration = each image's CORRECT mood (positions ①③⑤ 재식별 반영)
NAR={"n1":"hf_20260804_065106_6611c274-85cb-47de-bdb6-dfe8511ade4b.mp3", # 당신의 현관 취향은?
     "n2":"hf_20260804_065106_1a0e25d1-2836-4d84-82fd-545e6fce86ef.mp3", # ①테라코타 빈티지 감성
     "n3":"hf_20260804_065106_c9aa6fe5-3e72-4dd0-9232-16cd0a1fa934.mp3", # ②데이지 싱그러운 집
     "n4":"hf_20260804_065106_bb089e5a-11ce-42bb-97f6-038fbc86bb1e.mp3", # ③해바라기 밝고 따뜻한 집
     "n5":"hf_20260804_065106_6cfd887e-76da-4bd9-a9aa-181fa0fcdd96.mp3", # ④올리브세이지 차분한 집
     "n6":"hf_20260804_065106_722afe19-86fb-4492-8224-98339f8edf92.mp3", # ⑤수국 우아한 집
     "n7":"hf_20260804_065106_906d7cbd-9859-482e-a36e-77bfebcc8bf1.mp3", # ⑥모던한옥 단정한, 한국의 멋
     "n8":"hf_20260804_065106_5c7be389-97d1-4d21-b9ef-72beea29375a.mp3"} # 댓글로 번호를 골라주세요!
for k,v in NAR.items(): dl(CF+v,k+".mp3")
try:
    urllib.request.urlretrieve("https://raw.githubusercontent.com/google/fonts/main/ofl/nanumgothic/NanumGothic-Bold.ttf","NG.ttf")
except Exception as e: print(e)
os.makedirs("fdir",exist_ok=True); run(["cp","NG.ttf","fdir/NanumGothic-Bold.ttf"])

E=["-c:v","libx264","-crf","20","-preset","veryfast","-pix_fmt","yuv420p"]
COVER="scale=1920:1920:force_original_aspect_ratio=increase,crop=1080:1920"

# S1 hook: 6 fast cuts (~0.34s each) = ~2s
for i in range(6):
    run(["ffmpeg","-y","-loop","1","-t","0.34","-i",f"s{i}.png","-vf",f"{COVER},fps=24,setsar=1","-frames:v","8",*E,f"h{i}.mp4"])
with open("hc.txt","w") as f:
    for i in range(6): f.write(f"file 'h{i}.mp4'\n")
run(["ffmpeg","-y","-f","concat","-safe","0","-i","hc.txt","-c","copy","hook.mp4"])

# S2-S7: each design 4s with ken burns
def kb(img,z,out):
    run(["ffmpeg","-y","-loop","1","-t","5","-i",img,"-filter_complex",
      f"[0:v]{COVER},scale=1188:2112,zoompan=z='{z}':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=24,setsar=1[v]",
      "-map","[v]","-frames:v","96",*E,out])
zin="min(1.0+0.0005*on,1.06)"; zout="max(1.06-0.0004*on,1.0)"
for i in range(6):
    kb(f"s{i}.png", zin if i%2==0 else zout, f"d{i}.mp4")

# concat main (hook + 6 designs) = 2 + 24 = 26s
with open("mc.txt","w") as f:
    f.write("file 'hook.mp4'\n")
    for i in range(6): f.write(f"file 'd{i}.mp4'\n")
run(["ffmpeg","-y","-f","concat","-safe","0","-i","mc.txt","-c","copy","main.mp4"])

# subtitles for S1-S7 (number emphasized)
def at(t): return f"{int(t//3600):d}:{int((t%3600)//60):02d}:{t%60:05.2f}"
subs=[(0.15,2.0,"당신의 현관 취향은?"),(2.15,6.0,"①  빈티지 감성"),(6.15,10.0,"②  싱그러운 집"),
      (10.15,14.0,"③  밝고 따뜻한 집"),(14.15,18.0,"④  차분한 집"),(18.15,22.0,"⑤  우아한 집"),
      (22.15,26.0,"⑥  단정한 · 한국의 멋")]
head="[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: Def,NanumGothic,64,&H00FFFFFF,&H00202020,&H64000000,1,1,5,2,2,60,60,300,1\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
with open("subs.ass","w") as f:
    f.write(head)
    for a,b,t in subs: f.write(f"Dialogue: 0,{at(a)},{at(b)},Def,,0,0,0,,{t}\n")
run(["ffmpeg","-y","-i","main.mp4","-vf","subtitles=subs.ass:fontsdir=fdir","-c:a","copy",*E,"vsub.mp4"])

# S8 CTA grid (4s)
from PIL import Image,ImageDraw,ImageFont
W,H=1080,1920
cv=Image.new("RGB",(W,H),(246,243,235)); d=ImageDraw.Draw(cv)
ft=ImageFont.truetype("NG.ttf",66); fn=ImageFont.truetype("NG.ttf",46); fb=ImageFont.truetype("NG.ttf",64)
fm=ImageFont.truetype("NG.ttf",46); fp=ImageFont.truetype("NG.ttf",46)
def ctext(y,t,f,c):
    w=d.textlength(t,font=f); d.text(((W-w)/2,y),t,font=f,fill=c)
ctext(70,"당신의 취향은 몇 번?",ft,(40,40,40))
cw,ch=316,300; gap=16; gx=(W-cw*3-gap*2)//2; gy=190; vgap=40
for i in range(6):
    im=Image.open(f"s{i}.png").convert("RGB"); Wc,Hc=im.size
    cr=im.crop((int(Wc*0.12),int(Hc*0.40),int(Wc*0.90),int(Hc*0.99))).resize((cw,ch))
    x=gx+(i%3)*(cw+gap); y=gy+(i//3)*(ch+vgap)
    cv.paste(cr,(x,y))
    d.ellipse([x+8,y+8,x+58,y+58],fill=(3,199,90)); d.text((x+21,y+11),str(i+1),font=fn,fill=(255,255,255))
by=gy+2*ch+vgap+56
ctext(by,"댓글로 번호를 골라주세요!",fb,(213,98,46))
# brand card
x0,y0,x1,y1=110,by+120,970,by+300
d.rounded_rectangle([x0,y0,x1,y1],radius=40,fill=(250,247,238))
ctext(y0+26,"에어클린매트 · 6종 디자인",fm,(30,30,30))
pt="네이버 스마트스토어 검색"; pw=d.textlength(pt,font=fp); pad=40
px0=(W-pw)/2-pad; py0=y0+96
d.rounded_rectangle([px0,py0,(W+pw)/2+pad,py0+70],radius=35,fill=(3,199,90))
d.text(((W-pw)/2,py0+12),pt,font=fp,fill=(255,255,255))
cv.save("cta.png")
run(["ffmpeg","-y","-loop","1","-t","4","-i","cta.png","-filter_complex",
     "[0:v]scale=1080:1920,fps=24,setsar=1,fade=t=in:st=0:d=0.4[v]","-map","[v]","-frames:v","96",*E,"cta.mp4"])

# concat vsub + cta = 30s (re-encode via concat filter to normalize timestamps)
run(["ffmpeg","-y","-i","vsub.mp4","-i","cta.mp4","-filter_complex",
     "[0:v]fps=24,setsar=1[a];[1:v]fps=24,setsar=1[b];[a][b]concat=n=2:v=1:a=0[v]","-map","[v]",*E,"vfull.mp4"])

# BGM (bright, 30s)
import numpy as np
sr=44100; dur=30.0; N=int(sr*dur); t=np.arange(N)/sr; seglen=dur/6
prog=[[261.63,329.63,392.00],[293.66,369.99,440.00],[329.63,415.30,493.88],[261.63,329.63,392.00],[220.00,277.18,329.63],[293.66,369.99,440.00]]
bgm=np.zeros(N)
for i,ch in enumerate(prog):
    s=int(i*seglen*sr); e=int(min((i+1)*seglen,dur)*sr); tt=np.arange(e-s)/sr; seg=np.zeros(e-s)
    for f0 in ch: seg+=np.sin(2*np.pi*f0*tt)*0.45+np.sin(2*np.pi*f0*2*tt)*0.10
    env=np.clip(np.minimum(tt/0.3,(len(tt)/sr-tt)/0.3),0,1); bgm[s:e]+=seg*env
bgm*=(0.9+0.1*np.sin(2*np.pi*2.0*t))
fd=int(1.0*sr); bgm[:fd]*=np.linspace(0,1,fd); bgm[-fd:]*=np.linspace(1,0,fd)
bgm=bgm/np.max(np.abs(bgm))*0.5
with wave.open("bgm.wav","w") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(np.int16(bgm*32767).tobytes())

# narration timeline
offs={"n1":150,"n2":2200,"n3":6200,"n4":10200,"n5":14200,"n6":18200,"n7":22200,"n8":26300}
parts=[]
for k,ms in offs.items():
    run(["ffmpeg","-y","-i",k+".mp3","-af",f"aresample=44100,adelay={ms}|{ms},apad","-t","30","-ac","2","-ar","44100",k+"_d.wav"]); parts.append(k+"_d.wav")
cmd=["ffmpeg","-y"]
for p in parts: cmd+=["-i",p]
cmd+=["-filter_complex",f"amix=inputs={len(parts)}:duration=longest:normalize=0,volume=2.0,aresample=44100[nar]","-map","[nar]","-t","30","-ac","2","-ar","44100","nar.wav"]
run(cmd)
run(["ffmpeg","-y","-i","bgm.wav","-i","nar.wav","-filter_complex",
     "[1:a]asplit=2[nn][sc];[0:a][sc]sidechaincompress=threshold=0.04:ratio=9:attack=25:release=320[bd];[bd][nn]amix=inputs=2:duration=longest:normalize=0,loudnorm=I=-14:TP=-1:LRA=11[a]",
     "-map","[a]","-t","30","-ac","2","-ar","44100","mix.wav"])
run(["ffmpeg","-y","-i","vfull.mp4","-i","mix.wav","-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-b:a","192k","-shortest","/home/user/ACM_03_v1_916.mp4"])
print("DONE", os.path.getsize("/home/user/ACM_03_v1_916.mp4"))
