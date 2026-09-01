# ACM_06 씬 시트 — 「우리 집 현관엔, 어떤 사이즈?」

기준 문서: `ACM_06_기획서.html` (Google Drive · 에어클린매트/영상6)
콘텐츠 기둥 F(사이즈 선택) · 목표: 구매 망설임 제거 · 전환 완성
규격: 9:16 · 1080×1920 · 24fps · 32초 · 6씬 · 추천 디자인 데이지

## 씬 구성 (실제 제작본)

| 씬 | 시간 | 단계 | 화면 | 자막(= 나레이션 표기) | 나레이션 실제 발화 | 사이즈 배지 |
|---|---|---|---|---|---|---|
| ① | 0.0–3.0s | 훅 | 줄자로 맨바닥 현관을 재는 손 클로즈업 (제품 풀샷 없음) | 현관 매트, **사이즈**가 반이에요 | "현관 매트, 사이즈가 반이에요." | — |
| ② | 3.0–10.0s | 90×60 | 원룸·일반 현관에 90×60 데이지 매트 설치 | 90×60, **원룸**·일반 현관에 딱 | "구공에 육공, 원룸이나 일반 현관에 딱 맞아요." | `90 × 60` (3.3s~) |
| ③ | 10.0–17.0s | 120×80 | 신혼집·넓은 현관에 120×80 설치 | 120×80, **신혼집**·넓은 현관에 | "백이십에 팔십, 신혼집이나 넓은 현관에 딱이에요." | `120 × 80` (10.3s~) |
| ④ | 17.0–24.0s | 120×140 | 대형 전실·베란다에 120×140 설치 | 120×140, 대형 **전실**·베란다까지 | "백이십에 백사십, 대형 전실과 베란다까지 커버해요." | `120 × 140` (17.3s~) |
| ⑤ | 24.0–28.0s | 비교 | 3사이즈 오버헤드 플랫레이 비교 | 공간에 맞게<br>**딱 맞는** 사이즈로 | "공간에 맞게, 딱 맞는 사이즈로." | `90×60 · 120×80 · 120×140` (24.3s~) |
| ⑥ | 28.0–32.0s | CTA | 완성된 현관 풀샷 + 브랜드 카드 | [카드] 에어클린매트 \| 3가지 사이즈 · 6종 디자인 | "네이버 스마트스토어에서 에어클린매트를 검색해 보세요." | — |

**볼드 = 강조 색 적용 단어** (`#d5622e`). 기획서 지정 강조 후보: 사이즈 / 원룸 / 신혼집 / 전실 / 딱 맞는 / 추천

## AI 영상 생성 프롬프트 (기획서 원문 그대로 사용)

공통 프리픽스 — 모든 씬 앞에 삽입:

```
9:16 vertical video, 1080x1920, 24fps. Bright warm Korean apartment entryway,
soft natural daylight, clean minimal beige-white interior. Realistic product
commercial style, smooth stable camera, no text, no watermark, no faces
(hands and feet only).
```

| 씬 | 프롬프트 (공통 프리픽스 + 아래 문장) | 모델 / 생성 길이 |
|---|---|---|
| ① | Close-up of two hands stretching a yellow tape measure across the bare entryway tile floor by a Korean apartment front door, measuring the space, no entrance mat visible yet. | veo3_1_lite / 4s → 3s 사용 |
| ② | A compact 90x60 cm 13mm thick PVC coil entrance mat with printed daisy design laid neatly by the front door of a small one-room / studio apartment entryway, fitting the modest space, visible coil texture. | veo3_1_lite / 8s → 7s |
| ③ | A larger 120x80 cm 13mm thick PVC coil entrance mat with printed daisy design laid across a wider newlywed apartment entryway, comfortably filling the roomier foyer, visible coil texture. | veo3_1_lite / 8s → 7s |
| ④ | An extra-large 120x140 cm 13mm thick PVC coil entrance mat with printed daisy design covering a spacious large vestibule / veranda entrance area, generous full-floor coverage, visible coil texture. | veo3_1_lite / 8s → 7s |
| ⑤ | Overhead flat-lay of three daisy-printed PVC coil entrance mats of different sizes arranged side by side on a clean light wood floor for size comparison, tidy composition, generous empty space around them for size labels. | veo3_1_lite / 4s |
| ⑥ | Wide full shot of a finished bright entryway with the daisy PVC coil entrance mat laid neatly by the door, a pair of slippers beside it, inviting composition, space at the bottom for a text card. | veo3_1_lite / 4s |

씬 단위 분할 생성(일괄 생성 금지) 지침 준수. 사이즈 수치·자막·카드는 AI 생성이 아니라 편집 단계(`subs.ass`)에서 삽입.

## 나레이션

- 엔진: ByteDance Seed Audio 1.0 (seed_audio), 여성 프리셋 보이스 1종 고정 (`caeba733-3c17-43db-863e-69c7025512cd`)
- 전 씬 동일 보이스 — 기획서의 "고정 여성 보이스 1종" 요건 충족
- 사이즈 수치는 "구공에 육공", "백이십에 팔십"처럼 또렷하게 읽어 오독 방지 (기획서 지침)
- 씬별 발화 길이: 3.20s / 4.76s / 3.84s / 4.41s / 3.24s / 3.35s — 전부 해당 씬 창 안에서 종료
- 검수: faster-whisper(ko)로 6개 트랙 전부 역전사하여 대본 일치 확인

## 캡션 & 해시태그 (기획서 템플릿 F)

```
현관 사이즈, 재보셨나요? 📏
90×60 · 120×80 · 120×140 — 공간에 딱 맞는 3가지 사이즈.
원룸부터 대형 전실까지, 우리 집 현관에 맞는 에어클린매트 ✨
👉 네이버에서 '에어클린매트'를 검색해보세요!
```

`#에어클린매트 #현관매트 #디자인매트 #사이즈추천 #현관인테리어 #홈스타일링 #원룸인테리어 #신혼집꾸미기 #데이지인테리어`
