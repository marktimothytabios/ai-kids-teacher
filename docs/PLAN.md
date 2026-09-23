# AI Kids Teacher — Architecture & Product Plan

An interactive, voice-first AI teacher for children aged 2–5. It teaches talking, counting, letters,
colors, shapes and more, and has a free-play zone (puzzles, animals, music). Parents can make the
teacher look like a picture they upload and speak in a voice they record.

Status: planning. Nothing here is built yet.

---

## 1. Product principles

1. **Voice-first, reading-optional.** Toddlers can't read or type. Every interaction is speech, big
   tap targets or drag gestures.
2. **Wait for the child.** What Ms Rachel does on video (ask, pause, praise) we do for real:
   listen, react to what the child actually said or did, and adapt.
3. **Short sessions.** Ages 2–5 hold attention for about 5–10 minutes. Lessons are 3–7 minute
   "episodes", and the app includes a parent-set daily limit (the AAP suggests about 1 hour/day of
   high-quality content for ages 2–5, ideally watched together).
4. **Scripted spine, AI where it adds value.** A lesson has a fixed structure written by us. The
   LLM only fills in the live parts: reacting to answers, rephrasing, praise, small talk. This keeps
   content safe and predictable, and keeps costs low.
5. **Privacy by default.** Children's voice recordings are personal information under COPPA.
   Process audio, don't keep it.

---

## 2. Curriculum (ages 2–5)

Built from the **CDC developmental milestones** (what most kids can do by each age) and the
**Head Start Early Learning Outcomes Framework (ELOF)**, which covers five domains: Language &
Literacy, Cognition (math + science), Social-Emotional, Approaches to Learning, and
Perceptual/Motor.

| Track | Age 2–3 ("Tiny Talkers") | Age 3–4 ("Explorers") | Age 4–5 ("Pre-K Ready") |
|---|---|---|---|
| **Talking / language** | Name everyday objects, body parts, animal sounds; 2–3 word phrases ("more milk"); copy words; answer "what's this?" | 3–4 word sentences; who/what/where questions; describe pictures; tell what happened | Tell short stories in order; use "yesterday / tomorrow"; rhyming words; follow 3-step directions |
| **Letters & phonics** | Sing the ABC song; notice letters in their own name | Recognize ~10 letters (start with their name); letter sounds for common letters | Recognize most upper/lowercase letters; beginning sounds ("ball starts with /b/"); rhyming; syllable clapping |
| **Numbers & math** | Count 1–3 objects; "one" vs "many"; big/small | Count to 10; 1-to-1 counting of 5 objects; basic shapes; sort by color | Count to 20+; recognize numerals 1–10; compare more/less; simple patterns (ABAB); add/take away within 5 |
| **Colors & shapes** | Match colors; circle, square | Name 4–6 colors; triangle, star, heart | All basic colors and shapes; shapes in real objects |
| **Social-emotional** | Name feelings (happy, sad); take turns; say hi/bye | Understand why someone feels a way; calm-down breathing; sharing | Name more feelings; solve small conflicts; manners in context |
| **World / science** | Animals and their sounds; food; vehicles | Weather, seasons, where animals live, body parts and what they do | Plants grow, day/night, sink/float, the five senses, community helpers |
| **Movement / music** | Clap, stomp, dance along; finger plays | Action songs ("Head, Shoulders"); freeze dance | Follow-the-leader sequences; rhythm patterns |

**Structure**

- Curriculum is data, not code: `track → unit → lesson → activity` stored as JSON/YAML with an
  age band and required skills. The app downloads new lessons without an app update.
- Each **skill** has a mastery level per child (not seen → exposed → practicing → mastered). A
  simple spaced-repetition scheduler picks what to review.
- **Adaptive by level, not just age.** The age band sets the starting point; performance moves the
  child up or down.
- Have an early-childhood educator or speech-language pathologist review the scope and sequence
  before launch. This matters both for quality and for marketing claims.

**Episode template (about 5 min)**

1. Hello song + child's name (teacher greets the child by name)
2. Warm-up: review 1–2 mastered items
3. Teach 1 new thing (model → child tries → praise/help)
4. Game: tap, drag or say it
5. Movement break (song/dance)
6. Recap + goodbye song, with a parent note ("Today we practiced the letter B")

---

## 3. Free-play zone

Runs almost entirely **on the device**, with no AI cost per minute.

- **Puzzles:** shape sorters, jigsaws with 2–12 pieces, matching pairs
- **Animals:** tap an animal to hear its sound and name; "Where does it live?" drag game
- **Drawing:** trace letters and numbers, color by number
- **Music:** xylophone, drums, sing-along
- **Build:** stacking blocks, dress the teacher
- **Stories:** picture books read by the teacher's voice (pre-generated audio)

The teacher can appear in free play as a light companion ("You found the lion! What sound does a
lion make?"). These lines come from a pre-written phrase bank, and the live LLM is called only
when the child talks to the teacher.

---

## 4. Recommended architecture

### 4.1 Mobile app

**Recommendation: React Native with Expo (TypeScript).**

- Works on iOS and Android from one codebase, has good audio and animation libraries, and makes
  OTA updates easy for content and fixes.
- Animation: **Rive** (`rive-react-native`) for the teacher character and games, with state
  machines driven by visemes. **react-native-skia** for drawing and tracing.
- Audio: WebRTC through the LiveKit React Native SDK for live conversation, and `expo-audio` for
  pre-rendered clips.
- On-device voice activity detection (VAD) so we only stream audio while the child is speaking.

Alternative: Flutter (Flame for games) is also strong. Choose it only if the team already knows
Dart.

### 4.2 System diagram

```
┌──────────────────────── Mobile app (Expo / React Native) ────────────────────────┐
│  Lesson player (runs lesson JSON)   Free-play games (Rive/Skia, offline)           │
│  Teacher avatar (Rive 2D rig, lip-sync from visemes)                               │
│  Mic → on-device VAD → WebRTC  ◄──►  audio + viseme stream                         │
│  Local cache: lesson packs, pre-rendered audio, avatar assets                      │
│  Parent area (behind a parent gate): profiles, limits, progress, consent            │
└───────────────┬───────────────────────────────────────────┬─────────────────────┘
                │ WebRTC (LiveKit)                          │ HTTPS
┌───────────────▼──────────────────────┐   ┌───────────────▼──────────────────────┐
│  Realtime voice agent (LiveKit Agents)│   │  Backend API (Supabase: Postgres,     │
│  1. STT (streaming)                   │   │  Auth, Storage, Edge Functions)       │
│  2. Answer check (fuzzy/phonetic)     │   │  - child profiles, skill mastery      │
│  3. LLM (small, cheap) + safety filter│   │  - curriculum / lesson packs          │
│  4. TTS in the parent's cloned voice  │   │  - avatar + voice creation jobs       │
│     → audio + word timings → visemes  │   │  - billing (RevenueCat)               │
└──────────────────────────────────────┘   └───────────────────────────────────────┘
                │                                           │
        Model providers (swappable)             Offline batch jobs:
        STT / LLM / TTS                          pre-render lesson audio in each
                                                 teacher voice; cartoonize photo
```

### 4.3 Why a cascaded pipeline (STT → LLM → TTS), not speech-to-speech

Speech-to-speech models such as OpenAI Realtime and Gemini Live feel more natural, but they only
offer **preset voices**. They can't speak in a voice the parent uploads. The cascaded pipeline
also:

- gives us **text in between**, so we can run safety filters, check answers and log the lesson
  flow (as text only, no audio)
- produces **word/phoneme timestamps** from the TTS, which drive the avatar's lip-sync
- lets us swap any part for a cheaper or better provider

With streaming at every step, latency of about 800 ms to 1.2 s is realistic, and that is fine for
toddlers. The teacher can also say a filler line ("Hmm, let me see…") from cache while it waits.

### 4.4 Handling toddler speech (the hardest technical problem)

Speech recognition is much less accurate on 2–3-year-olds. Design around it:

- Most prompts have an **expected answer**. Match it phonetically and fuzzily ("tat" ≈ "cat"), and
  keep a list of common toddler variants for each word.
- **Any attempt is praised.** For ages 2–3, "the child made a sound after the prompt" (from VAD)
  already counts as a success signal.
- Always offer a **tap alternative** (show 2–3 pictures) so a non-verbal or shy child can still
  move forward.
- Only use the LLM's open conversation for ages 4–5 or free chat, where speech is clearer.
- Later: fine-tune or add a child-speech-adapted speech recognition model using data from
  consenting parents only, stored under COPPA rules.

### 4.5 Custom teacher: look ("upload any picture")

A one-time **character creation** job for each teacher:

1. Parent uploads a photo (of themselves, a grandparent, a pet, a drawing).
2. The backend makes a **friendly cartoon version** with an image model, finds the face landmarks
   (eyes, mouth) and generates mouth-shape and blink layers.
3. These are placed into a template **Rive 2D rig**, so the teacher animates on the phone at
   60 fps with **no cost per minute**. Lip-sync comes from the TTS visemes.

Premium option, later: photo-realistic talking head using LivePortrait-style models on a server
GPU. This is expensive for each minute of live use, so use it only to pre-render fixed content
such as songs and intros.

Guardrails: the parent must confirm they have the right to use the image. Block known public
figures and celebrities (for example, don't let users recreate Ms Rachel). Stylizing the photo
into a cartoon also lowers the risk of deepfake misuse.

### 4.6 Custom teacher: voice ("make it talk")

- Parent records about 30–60 seconds of their voice in the app, including a **spoken consent
  phrase**. We check that the phrase matches, to prevent cloning someone else's voice.
- Create a cloned voice with a TTS provider that supports zero-shot cloning.
- **Pre-render** all fixed lesson lines in that voice once, in a batch job, and cache them on the
  device. Only the live replies generated by the LLM are synthesized in real time. This removes
  most TTS cost.
- Also offer a few built-in "house" voices for families who don't want to clone.

---

## 5. Model recommendations (free → cheap)

| Layer | MVP pick (cheap, managed) | Cheaper / self-hosted later | Notes |
|---|---|---|---|
| **LLM** (teacher replies) | **Gemini Flash-Lite** (has a free tier for development) or **Claude Haiku 4.5** ($1 / $5 per 1M tokens) | Open model (e.g. Gemma / Llama small) on a GPU host | Replies are 1–2 short sentences. Use prompt caching on the long, fixed system prompt. Pick the one that scores best on our safety/tone eval set. |
| **STT** (speech-to-text) | Deepgram or Gemini/OpenAI streaming STT | Whisper (e.g. faster-whisper) self-hosted | Must stream. Test with real toddler audio from consenting families. |
| **TTS + voice clone** | **Cartesia Sonic** (~90 ms latency) or **Fish Audio** (cheap per character) | **Chatterbox** (MIT, zero-shot clone from ~5 s) or F5-TTS self-hosted | ElevenLabs sounds best but costs the most. **Kokoro** is free and fast but can't clone, so use it only for house voices. |
| **Realtime transport** | **LiveKit Cloud** (free tier) + LiveKit Agents | Self-hosted LiveKit server | Handles WebRTC, echo cancellation, interruptions. |
| **Photo → cartoon** | Any image-generation API, run once per teacher | Open image model (SDXL/Flux-class) self-hosted | One-time cost for each avatar. |
| **Safety** | Our own rules + a moderation model on both input and output text | — | Kid-specific blocklist, topic allowlist, "redirect to lesson" fallback. |

**Rough cost for live conversation** (estimates; test before relying on them):

- Cascaded pipeline: STT ≈ $0.005/min, LLM < $0.001/min, TTS ≈ $0.005–0.012/min (only for live
  replies). Total **≈ $0.01–0.02 per minute of live talk**.
- If a child uses **10 min/day of live AI** (the rest is pre-rendered lessons + on-device play),
  that is about **$3–6 per child per month**. Free play and pre-rendered lessons cost roughly $0.
- Lower costs by: caching TTS, pre-rendering, VAD so we never stream silence, a short LLM context
  (the lesson state lives in code, not in the chat history), and moving to self-hosted STT/TTS
  once there are enough users.

**Business model hint:** a free tier with the scripted lessons, house voices and full free-play;
a paid tier ($5–8/month) for the custom face and voice plus live conversation.

---

## 6. Data model (first draft)

```
parent(id, email, consent_status, consent_method, created_at)
child(id, parent_id, first_name, birth_year_month, avatar_teacher_id, daily_limit_min)
teacher(id, parent_id, name, rive_asset_url, voice_provider_id, voice_consent_at)
curriculum_skill(id, track, age_min, age_max, description, prerequisites[])
lesson(id, unit_id, age_band, version, json_spec)
child_skill(child_id, skill_id, level, last_seen_at, next_review_at)
session(id, child_id, lesson_id, started_at, ended_at, summary_text)   -- text only, no audio
```

---

## 7. Safety, privacy & compliance (non-negotiable)

- **COPPA (amended rule, compliance required since April 22, 2026):** voice recordings and
  biometric data such as voiceprints and face templates are personal information. We need
  **verifiable parental consent** before any recording, a written data-retention policy, and
  separate consent before sharing data with third parties (our AI providers count). Delete audio
  right after transcription, and never use children's data for training without explicit opt-in.
- Choose AI vendors that offer **zero data retention / no training** on API data, and sign data
  processing agreements (DPAs).
- A **parent gate** (e.g. "hold 3 fingers" or a math question) guards settings, purchases and
  external links. No ads, no open chat with other users, no external links in the kids' area.
- The LLM follows a tight persona: always kind, never asks for personal information (address,
  last name), steers away from off-topic subjects, and never pretends to be a real person. The
  output filter blocks anything that isn't age-appropriate.
- App store requirements: Apple Kids Category and Google Families policy (limits on third-party
  SDKs and analytics).
- Screen-time respect: parent-set limits, a "goodbye" wind-down, and encouraging co-play
  ("Ask a grown-up to count with you!").

---

## 8. Roadmap

| Phase | Scope | Goal |
|---|---|---|
| **0. Prototype (2–3 wks)** | Expo app, one house avatar (Rive), 3 scripted lessons (counting 1–5, letter A, animal sounds), live voice loop with LiveKit + cheap STT/LLM/TTS | Measure latency and how well STT works on real toddler speech |
| **1. MVP (6–8 wks)** | Curriculum engine (JSON lessons + mastery), ~20 lessons across tracks, 4 free-play games, parent area, COPPA consent flow, Supabase backend | Closed beta with ~20 families |
| **2. Personalization** | Photo → cartoon teacher, voice cloning with consent, batch pre-rendering, progress reports | Paid tier |
| **3. Scale** | Self-hosted STT/TTS, more lessons (educator-reviewed), Spanish/Tagalog, offline mode | Lower cost per user, more markets |

---

## 9. Open questions

1. Which languages at launch? (English only, or bilingual such as English + Tagalog/Spanish?)
2. Is the teacher allowed to look like a real photo, or is it always cartoonized? (Cartoon is
   recommended for safety and cost.)
3. Budget for an early-childhood / speech-language consultant to review the curriculum?
4. Solo developer or a team? This affects the choice between managed services and self-hosting.

---

## Sources

- CDC milestones: https://www.cdc.gov/act-early/milestones/index.html
- Head Start ELOF: https://headstart.gov/school-readiness/article/head-start-early-learning-outcomes-framework
- Amended COPPA rule: https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule
- AAP screen-time guidance summary: https://health.choc.org/updated-aap-recommendations-for-screen-time/
- Voice agent cost comparisons: https://inworld.ai/resources/voice-agent-cost-per-minute-2026
- TTS / voice cloning options: https://ocdevel.com/blog/20250720-tts
- Talking-head models: https://lipsync.com/blog/open-source-lip-sync
