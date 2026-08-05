import subprocess, os, urllib.request, wave, numpy as np
os.chdir("/home/user"); os.makedirs("hook",exist_ok=True); os.chdir("hook")
def run(c): print("+"," ".join(c)[:140]); subprocess.run(c,check=True)
def dl(u,o):
    for i in range(4):
        try: urllib.request.urlretrieve(u,o); return
        except Exception as e: print("retry",e)
    raise SystemExit("dl "+u)
CF="https://d8j0ntlcm91z4.cloudfront.net/user_3GSJKMpiMvaQXlBywoOArsxC3nk/"
dl(CF+"hf_20260805_040608_a46722fd-cf96-4daf-a693-adca056c28db.mp4","clip.mp4")
dl(CF+"hf_20260805_041231_717ac723-0400-46f3-8ba2-19be3406d34d.mp3","vo.mp3")
dl("https://raw.githubusercontent.com/google/fonts/main/ofl/nanumgothic/NanumGothic-Bold.ttf","NG.ttf")
os.makedirs("fdir",exist_ok=True); run(["cp","NG.ttf","fdir/NanumGothic-Bold.ttf"])
E=["-c:v","libx264","-crf","19","-preset","veryfast","-pix_fmt","yuv420p"]
# normalize clip to 1080x1920, 24fps, exactly 5s
run(["ffmpeg","-y","-i","clip.mp4","-t","5","-an","-vf",
     "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=24,setsar=1",
     *E,"base.mp4"])
# subtitles (two beats)
def at(t): return f"{int(t//60):d}:{t%60:05.2f}".rjust(0)
def ts(t): return f"0:{int(t//60):02d}:{t%60:05.2f}"
subs=[(0.3,2.2,"현관에 들어서는 순간"),(2.3,4.9,"신발에서 흙먼지가 이만큼!")]
head=("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\n"
"[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
"Style: Def,NanumGothic,72,&H00FFFFFF,&H00101010,&H80000000,1,1,6,3,2,60,60,250,1\n"
"[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
with open("s.ass","w") as f:
    f.write(head)
    for a,b,t in subs: f.write(f"Dialogue: 0,{ts(a)},{ts(b)},Def,,0,0,0,,{t}\n")
run(["ffmpeg","-y","-i","base.mp4","-vf","subtitles=s.ass:fontsdir=fdir","-c:a","copy",*E,"vsub.mp4"])
# --- audio: whoosh + tense pad, 5s ---
sr=44100; dur=5.0; N=int(sr*dur); t=np.arange(N)/sr
# tense low drone pad
pad=np.zeros(N)
for f0 in [110.0,146.83,220.0]:
    pad+=np.sin(2*np.pi*f0*t)*0.25+np.sin(2*np.pi*f0*2*t)*0.05
pad*=np.clip(np.minimum(t/0.6,(dur-t)/0.8),0,1)
# dust whoosh: filtered noise burst around 0.7s
wh=np.zeros(N); c=0.75
env=np.exp(-((t-c)**2)/(2*0.18**2))
noise=np.zeros(N)
n=np.random.RandomState(3).randn(N)  # seeded via RandomState (allowed in sandbox)
# simple lowpass by cumulative smoothing
k=200; kernel=np.ones(k)/k
noise=np.convolve(n,kernel,mode="same")
wh=noise*env*1.6
# rising pitch tick at impact
tick=np.sin(2*np.pi*(300+400*np.clip((t-0.6)/0.3,0,1))*t)*np.exp(-((t-0.85)**2)/(2*0.05**2))*0.4
mix=pad*0.6+wh*0.9+tick
mix/=np.max(np.abs(mix))+1e-6; mix*=0.55
fd=int(sr*0.15); mix[:fd]*=np.linspace(0,1,fd); mix[-int(sr*0.3):]*=np.linspace(1,0,int(sr*0.3))
with wave.open("bed.wav","w") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(np.int16(mix*32767).tobytes())
# VO delayed to 0.35s, pad to 5s, stereo
run(["ffmpeg","-y","-i","vo.mp3","-af","aresample=44100,adelay=350|350,apad","-t","5","-ac","2","-ar","44100","vo_d.wav"])
run(["ffmpeg","-y","-i","bed.wav","-ac","2","-ar","44100","bed2.wav"])
# duck bed under VO, mix
run(["ffmpeg","-y","-i","bed2.wav","-i","vo_d.wav","-filter_complex",
     "[1:a]asplit=2[v1][v2];[0:a][v2]sidechaincompress=threshold=0.05:ratio=8:attack=20:release=250[bd];[bd][v1]amix=inputs=2:duration=first:normalize=0,volume=1.8,loudnorm=I=-14:TP=-1:LRA=11[a]",
     "-map","[a]","-t","5","-ac","2","-ar","44100","mix.wav"])
run(["ffmpeg","-y","-i","vsub.mp4","-i","mix.wav","-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-b:a","192k","-shortest","/home/user/ACM_HOOK_dust_916.mp4"])
print("DONE", os.path.getsize("/home/user/ACM_HOOK_dust_916.mp4"))
