# NRI Planning System — Semester 1 (Baseline)

*Academic Planning · NRI Institute of Technology · Co-Delivery · NIAT'26 Sem 1 · v1 (weeks 1–9 detailed)*

Per-university academic plan for the as-approved NIAT'26 curriculum, in the APD/APF planning system. Anchor: start **12 Jul 2026**, end ~15 Dec 2026 (tentative) · 6-day week · 7 slots/day · Mid-1 window ~wk 9. Weeks are cohort-relative; dates resolve from NRI's almanac at ops time.

**Priority order:** 1 · Job / Placement outcomes → 2 · Student learning outcomes → 3 · Assessment outcomes (Skill Assessments, GRIT) → 4 · Degree outcomes (BOS subjects)

---

## Terminology

### Delivery modes
| Mode | Description |
|---|---|
| **MC** | Micro Cycles — short learn→quiz→practice loops. Course openings & light subjects. |
| **Studio — AM/PM** | One subject owns a half-day: Lecture slot → adjacent Practice slot(s). Default for WAD & Programming. |
| **Studio — A/B** | Full days alternate between two subjects. Experiment arm. |
| **Side Thread** | 2–3 slots/wk steady cadence — Maths, Quant, English, GenAI. |
| **Immersion — 3A/2B** | 3 days subject A + 2 days subject B. Reserved for project phases. |

### Slot types (canonical → legacy labels in existing sequences)
| Type | Description |
|---|---|
| **Lecture** | = Session / LEARNING_SET. Riders inside the same slot: Reading Material · Cheat Sheet · Classroom Quiz A/B (2×5 min). |
| **Practice** | = Practice / MCQ Practice / Daily Practice / Coding Practice / QUESTION_SET — **including NxtMock (mock-interview) units**. Protected — never converts to Lecture. |
| **Module Quiz** | = Module Quiz / ASSESSMENT / Quiz (topic). 30–45 min, rides or owns a slot at module boundaries. |
| **Skill Assessment** | **NEW layer** — rubric-graded build, 6 slots each, min 5/sem (APF). Zero exist in current sequences; inserted at wks 4, 7, 11, 14, 17. |
| **Revision** | **NEW layer** — reactivation before advancement. Three forms: **warm-start rider** (10–15 min retrieval opening the first Lecture after every weekend) · **re-entry slots** (MC reactivation, day 1 after festival/exam gaps) · **shield revision** (pre-Mid/End windows). Protected like Practice — never converted to Lecture. |

---

## High-Level Academic Plan

### 1 · Slot Economics (NRI APD row)
| Ledger | Value | Notes |
|---|---|---|
| Total days (12 Jul → 15 Dec) | 134 | 6-day week, Sundays off |
| − Public holidays / univ. days | 6 / 128 | |
| − University mid-assessment days | 6 | Mid-1 + Mid-2 windows |
| NIAT working days × 7 slots | 122 × 7 = 854 | |
| − NIAT assessment slots | 70 | Module Quizzes ~40 + Skill Assessments 30 (5×6) |
| **Net executional slots** | **784** | **≈ 18.7 net weeks · 42 slots/wk** |
| Subject-wise slot demand | 402 (≈22/wk) | see split below |
| **Buffer slots** | **382 (≈20/wk)** | daily practice extensions, self-study, NxtMocks, revision shields, slippage |

### 2 · Course-wise Prod Sequences (slot-encoded)
| Course (NxtWave) | Budget | Sequence built | Composition | Weekly cadence · mode |
|---|---|---|---|---|
| Web Application Development 1 | 90 | 80 slots | 43 L + P slots | 3L + 2P · Studio-AM/PM |
| Computer Programming (Python) | 101 | 79 slots | 41 L · 39 P (incl. 11 NxtMock) · 11 MQ | 3L + 2.5P · Studio-AM/PM |
| Mathematics for Computer Science | 31 | 30 slots (+overview) | L·P consolidated · 5 MQ · has Week column | 1.5L + 0.5P · Side Thread |
| Quantitative Aptitude | 45 | 46 slots | Session(45m + 2×5m quiz riders) · Daily Practice · Company-Specific | 1.5L + 1P · Side Thread |
| Introduction to Generative AI | 55 | 48 slots | LEARNING_SET · PRACTICE · MQ + Mock-Interview rows | 2L + 1P · Side Thread |
| Communicative English Foundation | 50 | 50 slots | multi-unit 60-min slots · 7 MQ · Practical ×5 · RTS · Project ×9 | 2L + 0.7P · Side Thread |
| **Developer Tools Lab = Git & Linux 101** | 30 | 14 slots built | 7 Sessions (CLI→files→git→GitHub) + 7 MCQ | concentrated in wk 1 (onboarding week) · MC; authored tail (~4) rides S7 wks 3–4 |

**Gaps this plan makes explicit:** Dev Tools needs ~4 authored sessions to reach its 30-slot budget (processes/env/package managers · undo & history · PR-review workflow · Markdown + CI) — the rest exists as recorded 2026 content. **Skill Assessments exist in no sequence** — 5 SA briefs are the net-new assessment work (SA-1 WAD static-site build wk 4 · SA-2 Python build wk 7 · SA-3 WAD responsive wk 11 · SA-4 Python+GenAI wk 14 · SA-5 integrated wk 17).

---

## Low-Level Academic Plan

### 3 · Scheduling rules — anchored to the weekly pattern

Rules are grouped by where they bite in the week pattern (Mon–Fri tracks · Fri assessment block · Sat BOS day · gaps). Legacy-validated rules (S-VYASA 1.0.1) marked ▸; additions from this program design marked ●.

**In-week (Mon–Fri):**
- ▸ **R1** — No back-to-back Lectures for the same course — alternate with Practice.
- ▸ **R2** — Lecture-to-Practice gap ≤ 30 hours.
- ▸ **R3** — Lecture content <30 min never occupies a 50-min Lecture slot — flag to Central Ops.
- ● **R4** — **Warm-start Monday:** the first Lecture slot after the weekend opens with a Revision rider (retrieval + Friday-assessment debrief). Friday MQ pass <80% → Monday Practice becomes remediation (logged).
- ● **R5** — **Module boundaries land Tue–Thu** — never on the first day after any gap.
- ▸ **R6** — Uniform pacing — no slow-start-then-cram; weekly deviation review enforces.
- ▸ **R7** — Prerequisite order preserved; foundations never compressed.

**Assessments (Fri block + windows):**
- ▸ **R8** — No consecutive Module Quizzes; ≥1 learning activity between.
- ▸ **R9** — MQs available immediately after corresponding content.
- ▸ **R10** — All prerequisite Lectures + Practice complete before the corresponding MQ / SA.
- ▸ **R11** — Academic & Skill Assessment slots are immutable once configured.
- ● **R12** — Friday assessment block = MQ / SA cadence; shield weeks convert it to Revision.
- ● **R13** — **No MQ/SA in the first two days after a festival/exam gap.**

**Protection & priority:**
- ● **R14** — Practice and Revision slots are protected — buffer absorbs compression, never these.
- ▸ **R15** — Dedicated revision before Mid/End exams; shield = zero new content.
- ● **R16** — Priority order resolves conflicts: Job/Placement > Learning > Assessment > Degree.
- ● **R17** — Cohort-week tracking only; weekly Ideal-vs-Reality deviation logging with remarks.

**Gap & re-entry:**
- ● **R18** — **Weekend gap (2.5 d, weekly):** no mode change — current mode + warm-start slot (R4).
- ● **R19** — **Festival gap (~1 wk):** day 1 back = MC reactivation (no new content in slot 1); SME mode resumes day 2–3. Topic starts move off re-entry day 1 by **boundary-shifting**; if a heavy topic must start immediately, substitute **Studio-A/B** (full-day immersion on the cold topic) — substitution logged with rationale.
- ● **R20** — **Mid exams:** day 1 back = light MC + exam debrief; day 2 = studio. Course boundaries align with exam boundaries — complete before mids, never straddle.
- ● **R21** — **Sem break:** semester opens with a 2–3 day reactivation bootcamp + diagnostic gate; dependent courses start only after the bridge passes.

### 4 · Semester goals
| Timeline (tentative) | Goal | Description |
|---|---|---|
| ~05 Sep 2026 (wk 8) | Complete syllabus for Mid-1 | 100% of Mid-1-scoped content delivered before the exam window; shield from wk 8 day 3 |
| ~mid-Sep (wk 9) | Mid-1 with integrity | University Mid-1 conducted per schedule; SEB/proctored formats for NIAT assessments |
| ~14 Nov 2026 | Complete syllabus for Mid-2 | 100% of Mid-2 scope before window |
| ~08 Dec 2026 | Complete full syllabus | All 7 sequences fully delivered before end-sem |
| ~15 Dec 2026 | End-sem with integrity | Per NRI schedule |
| Recurring · weekly | Lectures · Classroom Quizzes · Practice · MQs · SAs | All scheduled slots delivered with zero backlog; deviations logged with remarks (S-VYASA discipline) |
| Semester | Outcome targets | Practice completion ≥70%/course · MQ pass ≥80% · all 5 SAs executed · GRIT Applied-GenAI margin positive · 100% Mid/End sitting |

### 5 · Weekly scheduling goals — ideal slot budget & weeks 1–9

Ideal slots per subject per week (ops logs Reality + Deviation + Remarks weekly, per the tracker format). L = Lecture · P = Practice · MA = Micro-Assessment (MQ/quiz).

| Subject | L | P | MA | ≈/wk |
|---|---|---|---|---|
| Web App Development 1 | 3 | 2 | 0.5 | 5.5 |
| Computer Programming | 3 | 2.5 | 0.5 | 6 |
| Maths for CS | 1.5 | 0.5 | 0.3 | 2.3 |
| Quantitative Aptitude | 1.5 | 1 | 0.3 | 2.8 |
| Intro to GenAI | 2 | 1 | 0.3 | 3.3 |
| English Foundation | 2 | 0.7 | 0.3 | 3 |
| Dev Tools (Git 101) | — | — | — | 14 in wk 1 (onboarding) |
| **Total subject slots** | | | | **≈22 + 20 buffer/practice = 42** |

**Week-by-week (weeks 1–9):**
| Wk | Focus | Assessments (Fri block) | Exit criteria |
|---|---|---|---|
| 1 | **Onboarding week** — Induction track (7) · Dev Tools 1–14 (CLI → files → git → GitHub) · env + platform + community setup · BOS threads start Sat | — | Env working · **first commit pushed** · platform fluent |
| 2 | **Courses start** — WAD S1–5 (HTML) · Python S1–5 (intro → variables) · Maths number systems | MQ: Python M1 | MQ pass ≥80% |
| 3 | WAD CSS arc · Python conditionals · Dev Tools authored tail (S7) · Quant numbers | MQ: WAD M1 · Maths M1 · GenAI M1 | First page styled end-to-end |
| 4 | WAD layout/box model · Python loops | **SA-1: WAD static-site build (6 slots)** | SA-1 ≥75% first attempt |
| 5 | WAD flexbox · Python loops/patterns · English MQ arc | MQ: Python M2 · Quant M1 | — |
| 6 | WAD responsive builds · Python strings/lists · GenAI workflows | MQ: WAD M2 · English M2–3 | Responsive page shipped |
| 7 | Python functions · WAD Tailwind-equiv arc · NxtMock 1–2 window | **SA-2: Python build (6 slots)** | SA-2 ≥75% · NxtMock participation 100% |
| 8 | Mid-1 scope completion · pacing check vs uniform-pacing rule · **shield from day 3** | MQ catch-up only | 100% Mid-1 syllabus delivered · zero new content after shield start |
| 9 | **Mid-1 window + revision** · maintenance practice only | → revision | 100% sit Mid-1 · deviation log clean |

*Weeks 10–18.7 (Mid-2 arc, SA-3/4/5, Dasara/festival adjustments, end-sem shield) extend in the next iteration, same format.*

### 6 · Daily schedule (7-slot day templates)

**Standard day (Mon–Thu):**
S1 WAD — Lecture (+quiz riders) · S2 WAD — Practice · S3 Programming — Lecture · S4 Programming — Practice · S5 Maths / Quant — Lecture (alt days) · S6 GenAI / English — Lecture·Practice (alt) · S7 Daily practice · self-study (Dev Tools lives in the wk-1 onboarding week; authored tail rides here wks 3–4)

**Friday (assessment day):**
S1–S4 as standard · S5–S6 **Assessment block**: Module Quizzes or Skill Assessment window · S7 Guided practice / catch-up

**Saturday:**
S1–S2 WAD / Programming continuation · S3–S4 Thread subjects catch-up · S5 NxtMock window (from wk 5) · S6–S7 Revision · buffer

**Skill-Assessment day (wks 4, 7, 11, 14, 17):**
S1–S2 as standard · S3–S6 **Skill Assessment (6-slot budget spans Fri S5–S6 + Sat S3–S6)** · Rubric-graded build · results feed weekly deviation review

---

## Semester 2 — baseline (default delivery)

Anchor ~Jan 2027 (APD Sem-2 row pending — placeholder economics: ~17 net weeks, 42 slots/wk, same deduction ledger shape). Courses per NRI's approved curriculum; slot data from APF Sem-2.

| Course | Sessions | Practice | MQ slots | Total | Ideal /wk (÷17) |
|---|---|---|---|---|---|
| Frontend Development (WAD-2: JS Essentials → React) | 27 | 24 | 6 | 57 | 3.4 |
| Foundations of Data Structures & Problem-Solving (DSA) | 45 | 36 | 5 | 86 | 5.1 |
| Database Management Systems | 40 | 30 | 7 | 77 | 4.5 |
| Building LLM Applications | 32 | 18 | 8 | 58 | 3.4 |
| Numerical Ability | 29 | 20 | 6 | 55 | 3.2 |
| Advanced Communicative English | 24 | 21 | 5 | 50 | 2.9 |
| Environmental Science (compliance) | guidance in shields + exam buffer | | | | — |
| **Total** | | | | **383 subject slots** | **≈22.5/wk + buffer** |

Baseline semester goals mirror Sem 1's tracker: syllabus-before-Mid-1/Mid-2/End with dates from the almanac; recurring weekly goals; 5 Skill Assessments; DSA carries the heaviest load (86 slots) and the university's flagship exam — its pacing is the semester's watch-lane. The **5+1 re-sequencing of this semester** lives on the NRI 5+1 page.

---

**Footer:** Instruments this page feeds: Goals Tracker sheet (weekly Reality/Deviation logging) · Prod Sequence sheets (slot order authority) · sign-off chain University PMs → Dean → Program Design → COOPS BOA. Weeks 10+ and remaining universities follow turn by turn in this same format.
