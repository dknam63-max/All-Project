#!/usr/bin/env bash
# ACM_06 9:16 쇼츠 합성 파이프라인 (재현용)
# 입력: v1..v6.mp4 (AI 생성 씬 클립), a1..a6.wav (씬별 나레이션), subs.ass, fonts/NotoSansKR-Bold.otf
# 출력: ACM_06_v2_916.mp4  (1080x1920 / 24fps / H.264 High / AAC 48kHz stereo / 32.000s)
set -euo pipefail
cd "$(dirname "$0")"

# 한글 자막 폰트 (libass가 style Fontname "Noto Sans KR" 로 매칭)
mkdir -p fonts ~/.fonts
[ -s fonts/NotoSansKR-Bold.otf ] || curl -sSLf -o fonts/NotoSansKR-Bold.otf \
  "https://github.com/googlefonts/noto-cjk/raw/main/Sans/SubsetOTF/KR/NotoSansKR-Bold.otf"
cp -f fonts/NotoSansKR-Bold.otf ~/.fonts/ && fc-cache -f >/dev/null 2>&1 || true

# 씬 길이(초): 3 / 7 / 7 / 7 / 4 / 4  = 32초
# 나레이션 시작(초): 0 / 3 / 10 / 17 / 24 / 28
ffmpeg -y -hide_banner -loglevel error \
  -i v1.mp4 -i v2.mp4 -i v3.mp4 -i v4.mp4 -i v5.mp4 -i v6.mp4 \
  -i a1.wav -i a2.wav -i a3.wav -i a4.wav -i a5.wav -i a6.wav \
  -filter_complex "\
[0:v]trim=0:3,setpts=PTS-STARTPTS,fps=24,scale=1080:1920:flags=lanczos,setsar=1[v0];\
[1:v]trim=0:7,setpts=PTS-STARTPTS,fps=24,scale=1080:1920:flags=lanczos,setsar=1[v1];\
[2:v]trim=0:7,setpts=PTS-STARTPTS,fps=24,scale=1080:1920:flags=lanczos,setsar=1[v2];\
[3:v]trim=0:7,setpts=PTS-STARTPTS,fps=24,scale=1080:1920:flags=lanczos,setsar=1[v3];\
[4:v]trim=0:4,setpts=PTS-STARTPTS,fps=24,scale=1080:1920:flags=lanczos,setsar=1[v4];\
[5:v]trim=0:4,setpts=PTS-STARTPTS,fps=24,scale=1080:1920:flags=lanczos,setsar=1[v5];\
[v0][v1][v2][v3][v4][v5]concat=n=6:v=1:a=0[vc];\
[vc]ass=subs.ass:fontsdir=fonts[vsub];\
[vsub]fade=t=in:st=0:d=0.3,fade=t=out:st=31.55:d=0.45,format=yuv420p[vout];\
[6:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,adelay=0|0[b0];\
[7:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,adelay=3000|3000[b1];\
[8:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,adelay=10000|10000[b2];\
[9:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,adelay=17000|17000[b3];\
[10:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,adelay=24000|24000[b4];\
[11:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,adelay=28000|28000[b5];\
[b0][b1][b2][b3][b4][b5]amix=inputs=6:normalize=0:duration=longest,\
loudnorm=I=-14:TP=-1:LRA=11,aresample=48000,apad[amx];\
[amx]atrim=0:32,asetpts=PTS-STARTPTS[aout]" \
  -map "[vout]" -map "[aout]" -t 32 \
  -c:v libx264 -preset medium -crf 19 -profile:v high -level 4.1 -g 48 -pix_fmt yuv420p -r 24 \
  -c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart \
  ACM_06_v2_916.mp4

ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate \
  -show_entries format=duration,size -of default=nw=1 ACM_06_v2_916.mp4
