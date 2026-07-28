# AI FullStack Elite Cohort — Program Design (reference)

**Provenance:** Extracted verbatim from the design artifact *"AI FullStack Elite Cohort — Program Design"* (NIAT · AI FullStack Developer Track · Design v1, §7.3/§7.4). Companion artifact pages: Curriculum · Course Contents · Execution Plan · Phase Anatomy · Student View.

**Why it's here:** the fully-worked *target* for the delivery-model engine (see [`superpowers/specs/2026-07-28-delivery-models-engine-design.md`](superpowers/specs/2026-07-28-delivery-models-engine-design.md)). It is the reference exemplar the engine reasons *toward* — the four delivery models, the phase rule, the per-course phase arcs, the mapped year, the milestone ladder. Weeks are **cohort-relative**: each university anchors week 1 to its own start date, so this design can be instantiated per college and re-tested with each university's data.

**Headline numbers:** 15 courses · **256 sessions** · ~955 h load · ~7 h/day scheduled · **34-week mapped year** (28 teaching + shields, recesses & exams) · **2 parallel tracks** (AM / PM) · ≈250/250 slots vs core sessions (knife-edge).

---

## 1. The four delivery models

Same content, four ways to cut a week. The current platform session (learning set → quiz → practice) is an artifact of online self-paced delivery — an offline cohort with instructors can use all four.

| Model | Shape | Best for | Watch out | Used here |
|---|---|---|---|---|
| **1 · Tight micro-cycles** | Learn A → Practice → Learn B → Practice → Code practice (one day, both subjects, learn→quiz→practice loops) | Concept acquisition — novices, new syntax, first exposure. Retrieval minutes after instruction. | Fragmented; no long build stretches. Wrong for project work. | first ~⅓ of every course |
| **2 · Bootcamp studio day** | Teach → Live-code → Teach → one long lab, same subject (segmented AM, uninterrupted PM lab) | Skill consolidation. Long labs build fluency; same-day proximity keeps feedback tight. | Never one continuous 2.5 h lecture — novice attention holds ~20–25 min. Segment the morning. | middle ⅓ of every course |
| **3 · A/B day scheduling** | Day 1 = all Subject A + code practice · Day 2 = all Subject B + code practice (alternate days, full-day depth, both subjects stay spaced) | Two heavier subjects mid-course, each needs full-day depth but neither can afford a multi-day gap. | Halves each subject's weekly touchpoints — gates must watch decay. | **optional experiment arm** during studio phases |
| **4 · Block scheduling (3+2)** | One week: 3 days Subject A, 2 days Subject B | Project phases — context-carrying beats spacing once skills are integrated. | For novice content, massed days + weekend gap = measurable decay. Blocking *feels* effective, measures worse on retention. | project phase (last ⅓) and capstone weeks |

## 2. The rule: delivery model follows course phase

No single model wins globally. Each course migrates through three delivery phases as students move from first exposure to shipping.

| Phase | → Model | What it is |
|---|---|---|
| **Phase 1 · Concept acquisition** | → Tight micro-cycles (M1) | First ~⅓. Both subjects daily, short loops, spacing protects novices. |
| **Phase 2 · Skill consolidation** | → Studio days (M2) | Middle ⅓. Segmented morning instruction, one long afternoon lab on the same material. |
| **Phase 3 · Project work** | → Immersion / blocking (M4) | Last ⅓ + capstone. Full-day builds; weekly blocking acceptable; checkpoints are the assessment. |

**Model 3 (A/B) is not a phase** — it is the experiment/variant arm overlaid on the studio phase.

### A studio week, concretely
- **Default (tracks stay):** each 3 h slot = Teach 45m → subject lab 2h15, both subjects daily; Mon–Fri identical; Sat = gates + checkpoint lab (~4 h). *Wins:* daily spacing for both subjects; simplest for ops.
- **Variant (A/B studio days — experiment arm):** whole days alternate (e.g. Python M/W/F · Web T/Th) + 1 h thread daily; segmented AM + ~3 h continuous PM lab, one subject per day. *Wins:* labs twice as long, max 1-day gap. *Cost:* half the weekly touchpoints — gates must watch decay.

## 3. Phase anatomy — practice rhythm per phase

| Phase | Function | Rhythm & practice |
|---|---|---|
| **Micro-cycles** | Encode & retrieve | Short learn→quiz→practice loops. Practice: **6–12 MCQs per concept node + short coding drills.** Builds accurate foundations; spacing protects novices. |
| **Studio** | Fluency & feedback | 45 min segmented teaching + 2 h 15 continuous lab. Practice: **2–4 build tasks per skill node.** Long labs create fluency; same-day feedback. |
| **Project** | Transfer & integration | Multi-session builds with rubrics. Practice: **skill assessments (checkpoints) + review/debug items.** The phase employers see — the arc exists to reach it. |

Gates: **weekly mastery gate (day 6)** = the intervention trigger. **Skill assessment** = bi-weekly checkpoint, EXAM-weight.

## 4. The curriculum (15 courses · 256 sessions)

Session counts in brackets; ~30% of sessions tagged NEW; ~85% Claude Dev cert coverage.

**Foundation**
- **Introduction to Software Development (7)** — orientation; shared vocabulary. *(unchanged, already AI-forward)*
- **Git, Linux & Developer Tools 101 (10, NEW)** — terminal fluency + version control before serious coding. *(no git/shell content existed; hard prereq for agents)*

**Programming & Algorithms**
- **Computer Programming using Python (28)** — zero to correct Python; AI as spec-first learning aid, gates unaided. *(compressed 33→28)*
- **Data Structures & Algorithms using C++ (34)** — interview-grade; full course runs Year 2. *(trimmed 51→34)*
- **DSA Essentials (C++) (14)** — just-enough patterns; re-cut from the 51-session course, runs Sem B wk 11–13.

**AI FullStack**
- **Web Application Development (30)** — HTML, CSS, Tailwind, **JS language core (NEW)**. *(fixes the missing-JS hole; double arc)*
- **Frontend with React & TypeScript (28)** — typed components, server state, auth, **TS + Testing (NEW)**.
- **Database Management Systems (28)** — SQL, modelling, Mongo, **schema-design capstone (NEW)**. *(3 courses merged)*
- **Backend with FastAPI (14, NEW)** — just-enough Python backend; Node depth → Year 2.
- **Application Development using Coding Agents (25, NEW)** — the track's differentiator; specify/direct/review/verify with agents.
- **AI FullStack Capstone (12 blocks + 6 comm)** — shipped product + agent-workflow portfolio + Demo Day.
- **Building LLM Applications (30)** — build-first spiral; provider-portable, RAG-grounded, evaluated, guarded LLM app.
- **Introduction to GenAI (24)** — thread, ~1 h/day, micro-format, exempt from the phase arc.

## 5. Course-by-course phase arcs (from Phase Anatomy)

| Course | Track · Window | Arc | Exit outcome |
|---|---|---|---|
| Computer Programming (Python) (28) | AM · Sem A wk 2–7 | MICRO syntax→loops · STUDIO strings/lists/functions/dicts · MINI-PROJ (45/45/10) | Writes correct Python unaided; first git-submitted mini-project |
| Web App Dev — HTML/CSS/TW/JS (30) | PM · Sem A wk 2–7 | **double arc:** MICRO HTML/CSS · STUDIO layout/Tailwind · PAGE BUILD ‖ MICRO JS core · STUDIO DOM/fetch · MINI-BUILD | Ships responsive page + interactive JS — hands off where React begins |
| Frontend React + TS (28) | AM · Sem A wk 8–14 | MICRO components/props/state · STUDIO hooks/effects/TS · PROJECT routing→auth→context | Typed, tested, auth-guarded React app deployed. ⚠ Tightest window (1.18) — Sat labs load-bearing |
| Database Management Systems (28) | PM · Sem A wk 8–14 | MICRO SQL drills · STUDIO modelling/joins/Mongo · SCHEMA CAPSTONE | Designs + builds the data layer for a product spec (graded); Backend consumes it wk 17 |
| Building LLM Applications (30) | AM · Sem B wk 1–7 | **build-first spiral:** BUILD → CONCEPT LLMs → STUDIO tools/RAG/agents → BUILD RAG agent/MCP → CONCEPT evals/security → BUILD evaluated app | Ships provider-portable, RAG-grounded, evaluated, guarded LLM app |
| Backend with FastAPI (14) | PM · Sem B wk 1–4 | MICRO FastAPI/routing/models · STUDIO SQL/auth/SSE · SHIP deploy + FE integration | Deployed, JWT-secured, streaming API integrated with React |
| Coding Agents (25) | PM · Sem B wk 5–10 | MICRO how agents work/config/prompting · STUDIO codebases/features/review labs · PROJECT cloud agents/deploy/portfolio | Directs/reviews/verifies agent work; skill assessments = review/debug format |
| DSA Essentials (C++) (14) | PM · Sem B wk 11–13 | **substitute arc (no project):** MICRO C++/STL/complexity · STUDIO pattern problem-sets · CONTEST | Solves core interview patterns under time pressure |
| AI FullStack Capstone (12 + 6 comm) | AM · Sem B wk 9–13 | **all-project:** SCOPE & SPEC · BUILD SPRINTS (agent-native) · EVALS & HARDENING · DEMO PREP | Shipped product + agent-workflow portfolio + Demo Day in Sem-B exam window |

*Arc exceptions: Web App Dev = double arc (CSS ramp, then JS ramp) · Building LLM Apps = build-first spiral (kept deliberately) · DBMS ends in schema-design capstone · Python's project tail is short by design.*

## 6. The mapped year — two tracks, 34 weeks

**Structure:** Sem A wk 1–16 → inter-sem break wk 17–18 → Sem B wk 19–34. Courses pause across shields/recesses (maintenance only) and resume — prereq order is never broken.

**Morning track (~3 h):** Bootcamp [Induction (7) · Git (10)] → Python (28) → React + TypeScript (28) → Building LLM Apps (30) → Capstone mornings (12 + 6 comm, paired w/ Agents PM).

**Afternoon track (~3 h):** Web App Dev — HTML·CSS·TW·JS (30) → DBMS + schema capstone (28) → FastAPI (14) → Coding Agents (25) → DSA Essentials (14).

**Threads (~1 h):** Intro to GenAI (24) · daily code practice · maintenance · portfolio prep.

**In-course delivery phases:** micro-cycles → studio days → project immersion.

### Calendar-tuned year map (approximation v1)
Approximated from four real calendars (MRV, CDU, VGU, SGU); re-tune when implementation stats arrive. **Revision shield rule:** new content freezes 4–5 days before every internal and end-sem exam; shield days = maintenance practice + university-course prep only. Festival recesses per real almanacs (Dasara ~1 wk Sem A; Sankranthi ~1 wk Sem B).

**Sem A · Aug-anchored (16 wks) — Bootcamp → Mid-2:**
- W1 — Bootcamp (Induction 7 · Git 101 10)
- W2–5 — Teach: Python ‖ Web (full pace)
- W6 — Dasara recess (maintenance-only)
- W7–8 — Python/Web finish → React ‖ DBMS start
- W9 — Shield (4–5 d) + Mid-1
- W10–13 — React ‖ DBMS (full pace)
- W14 — Shield + Mid-2
- W15–16 — End-sem exams · drop-back decision → ~2 wk inter-sem break

**Sem B · Jan-anchored (16 wks) — LLM layer → Demo Day:**
- W1 — Teach: LLM Apps ‖ FastAPI start
- W2 — Sankranthi recess (maintenance-only)
- W3–7 — LLM Apps ‖ FastAPI (→W4) → Coding Agents (W5–)
- W8 — Shield + Mid-1
- W9–13 — Capstone mornings (incl. 6 comm) ‖ Agents (→W10) → DSA Essentials (W11–13)
- W14 — Shield + Mid-2 · capstone hardening
- W15–16 — End-sem exams + Demo Day

**Capacity arithmetic:** full-pace teaching ≈ 21 weeks (231 track-slots) + partial capacity in shield/recess weeks ≈ ~250 slots vs 250 core sessions (256 total; 6 embedded comm ride the capstone window) — knife-edge. **Recommendation:** trim ~10–15 sessions (~5%) at SME module review; treat shield-week Saturdays as gate days only. In-timetable slot-ratio slack (~15%) is the working buffer.

**Cohort-relative weeks:** university starts spread **Aug 4 – Sept 15**, so each university anchors week 1 to its own start; ops tracking runs on **cohort-week-number, never calendar date.**

## 7. Milestone ladder (per track)

- **Daily** — classroom quiz inside the session *(exists)*
- **Weekly** — mastery gate, day 6, from existing item pools *(NEW slot type — the intervention trigger)*
- **Bi-weekly** — build checkpoint, EXAM-weight *(NEW slot type)*
- **Module end** — module quiz *(exists in fullstack courses; must be added to both GenAI courses)*
- **Course end** — practical exam *(NEW)*
- **Week 36** — Demo Day

## 8. Student view (what a cohort student sees daily)

Adds **calendar awareness** to the existing platform: today's plan, gates & skill assessments, revision shields before university exams, and breaks as first-class objects. Example (MRV-E1, Week 11 of 34, Sem A):
- **AM 09:00** — React + TS S10 (Effect Hook): teach + live-code 45 m → lab 2 h 15 (fetch-on-mount with cleanup) → classroom quiz
- **12:00** — Thread: daily code practice (Python maintenance + SQL drill)
- **PM 14:00** — DBMS S11 (CASE clause & set ops): teach 45 m → lab 2 h 15 → classroom quiz
- **Evening (optional)** — maintenance practice 20 min
- **Coming up:** Sat weekly mastery gate (proctored) · Tue wk 12 skill assessment · Wk 14 revision shield → University Mid-2 · Wk 15–16 end exams → inter-sem break

## 9. Non-negotiables

1. **Timetable ownership** — the cohort's day must give ~6 h. Make-or-break.
2. **Entry screening** — the pace has no remediation slack.
3. **Drop-back lane** — course boundaries align with standard NIAT semester flow, so a mid-year exit lands cleanly in a standard batch.
4. **Lean practice budgets** — checkpoints, not MCQ volume, are the assessment spine.
5. **Run the delivery experiment** — randomize sections micro-cycle vs studio-day on one 3-week Python stretch; let mastery data pick the standard.

## 10. How the delivery-model engine uses this

This design is the *target*, not a fixed template to paste onto every college. The engine (spec: [`delivery-models-engine-design.md`](superpowers/specs/2026-07-28-delivery-models-engine-design.md)) instantiates it **per university**:
- **Same fixed vocabulary** — the four models and the phase rule above are the constants.
- **Data tunes the intensity** — each university's own GRIT clear rates, practice engagement, and slippage decide which subjects get the A/B experiment, extra gates, or protected blocking (never swaps the phase→model default).
- **Cohort-relative anchoring** — week 1 = that university's own start date; everything runs on cohort-week-number.
- **Testing across universities** — re-run per college (MRV, CDU, Aurora, NRI, …) and compare how the tuning differs given each one's data.
