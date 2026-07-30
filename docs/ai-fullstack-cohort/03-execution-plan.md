# Delivery Models & the 1-Year Execution Plan

*NIAT · AI FullStack Developer Track · Design v1 — §7.3 / §7.4*

How the elite cohort's year (34 mapped weeks: 28 teaching + shields, recesses & exams) is structured: which delivery model runs when, every subject with its session count, and the milestone rhythm that holds the pace together.

**Stats:** 291 sessions (~1,085 h load) · 5+1 track days + BOS day (~7 h/day) · 34-week mapped year (shields & recesses in-plan) · ~10% slot headroom (restored in v2) · 2+1 tracks + DSA thread strand

---

## The four delivery models

Same content, four ways to cut a week. The current platform session (learning set → quiz → practice) is an artifact of online self-paced delivery — an offline cohort with instructors can use all four.

### Model 1 — Tight micro-cycles
One day · both subjects · learn→quiz→practice loops (Learn A → Practice → Learn B → Practice → Code practice)
- **Best for:** Concept acquisition — novices, new syntax, first exposure. Retrieval happens minutes after instruction.
- **Watch out:** Fragmented; no long build stretches. Wrong for project work.
- **Used here:** first ~⅓ of every course

### Model 2 — Bootcamp studio day
One day · one subject deep · segmented AM (Teach → Live-code → Teach), uninterrupted PM lab on the same subject
- **Best for:** Skill consolidation. Long labs build fluency; same-day proximity keeps feedback tight.
- **Watch out:** Never one continuous 2.5 h lecture — novice attention holds ~20–25 min. Segment the morning.
- **Used here:** middle ⅓ of every course

### Model 3 — A/B day scheduling
Alternate days · full-day depth · both subjects stay spaced (Day 1 = all Subject A + code practice; Day 2 = all Subject B + code practice)
- **Best for:** Two heavier subjects mid-course, when each needs full-day depth but neither can afford a multi-day gap.
- **Watch out:** Halves each subject's weekly touchpoints — gates must watch decay.
- **Used here:** optional experiment arm during studio phases

### Model 4 — Block scheduling (3+2)
One week · 3 days Subject A (Mon–Wed), 2 days Subject B (Thu–Fri)
- **Best for:** Project phases — context-carrying beats spacing once skills are integrated.
- **Watch out:** For novice content, massed days + weekend gap = measurable decay. Blocking *feels* effective, measures worse on retention.
- **Used here:** project phase (last ⅓) and capstone weeks

---

## The rule: delivery model follows course phase

No single model wins globally. Each course migrates through three delivery phases as students move from first exposure to shipping.

| Phase | Model | Description |
|---|---|---|
| **Phase 1 · Concept acquisition** | → Tight micro-cycles | First ~⅓ of the course. Both subjects daily, short loops, spacing protects novices. |
| **Phase 2 · Skill consolidation** | → Studio days | Middle ⅓. Segmented morning instruction, one long afternoon lab on the same material. |
| **Phase 3 · Project work** | → Immersion / blocking | Last ⅓ + capstone. Full-day builds; weekly blocking acceptable; checkpoints are the assessment. |

---

## A studio week, concretely

When both tracks are in studio phase (e.g., Python + Web App Dev mid-course), two shapes are possible — the default keeps the tracks; the variant is its A/B-test counterpart in the delivery experiment.

### Default — Studio slot, tracks stay
Mon–Fri · both subjects daily · gates Friday PM · day 6 = BOS subjects
Inside each 3 h slot: Teach 45m → Python lab 2h15 → Code practice → Teach 45m → Web lab 2h15
- **Shape:** Inside each 3 h slot: segmented teaching (teach → live-code → check), then one uninterrupted lab on that material.
- **Wins:** Daily spacing for both subjects; simplest for ops — track structure unchanged.

### Variant · experiment arm — A/B studio days, full-day depth
Whole days alternate · Python M/W/F · Web T/Th · gates Friday PM (Sat gates)
- **Shape:** Segmented AM instruction + a ~3 h continuous PM lab, one subject per day.
- **Wins:** Labs twice as long; max 1-day gap per subject. Cost: half the weekly touchpoints — gates must watch decay.

---

## Execution plan — the mapped year, two tracks

Sessions in brackets. Year mapped to the real almanac approximation: **Sem A wk 1–16** (Dasara wk 6 · 🛡 shield+Mid-1 wk 9 · 🛡 shield+Mid-2 wk 14 · exams wk 15–16 with drop-back) → inter-sem break wk 17–18 → **Sem B wk 19–34** (Sankranthi wk 20 · shield+Mid-1 wk 27 · shield+Mid-2 wk 32 · exams + Demo Day wk 33–34). Courses pause across shields/recesses (maintenance only) and resume — prereq order is never broken. Capacity: ~230 usable AM/PM slots vs 210 core AM/PM sessions (~10% headroom); the DSA strand (51) and Intro GenAI (24) ride the thread lane, and the 6 embedded comm sessions ride the capstone window.

### Timeline by lane and week

**Morning track** (Python → React/TS → LLM Apps):
| Weeks | Content |
|---|---|
| 1 | Bootcamp: Introduction (7) · Git 101 (10) |
| 2–6 | Python (28) |
| 6 | *Dasara recess* |
| 7 | Python continues |
| 8 | React + TS starts |
| 9 | *🛡 shield · Mid-1* |
| 10–14 | React + TypeScript (28) |
| 14 | *🛡 shield · Mid-2* |
| 15–16 | *Sem-A exams · drop-back* |
| 17–18 | *Inter-sem break* |
| 19 | LLM Apps starts |
| 20 | *Sankranthi recess* |
| 21–26 | Building LLM Apps (30) |
| 26 | *🛡 shield · Mid-1 (Sem B)* |
| 27–32 | Capstone — mornings (12 + 6 comm), paired with Agents PM |
| 32 | *🛡 shield · Mid-2 (Sem B)* |
| 33–34 | *Sem-B exams · Demo Day* |

**Afternoon track** (Web → JS → DBMS → Backend → Agents → DSA windows):
| Weeks | Content |
|---|---|
| 2–4 | Web — HTML · CSS · Tailwind (15) |
| 5 | Frontend JS (16) starts |
| 7 | JS finishes |
| 8 | DBMS starts |
| 10–14 | DBMS + schema capstone (28) |
| 19 | FastAPI starts |
| 21–23 | FastAPI (14) |
| 23–26 | Coding Agents (22) |
| 27–29 | Coding Agents continues (+3 protected maintenance slots) |
| 29–32 | DSA consolidation · contests · DSA exam-prep (in-course) |

**Thread lane** (~1 h):
| Weeks | Content |
|---|---|
| 2–9 | Intro to GenAI (24) · daily code practice |
| 10–14 | **DSA strand starts wk 10** — C++/STL · complexity: shaped ~3 new/wk + drill days (React ‖ DBMS window) |
| 19 | DSA |
| 21–32 | **DSA strand — patterns** (45 across the year · ~3 new/wk during LLM ‖ FastAPI, daily once one track goes project-mode) · code practice · portfolio prep |

**BOS day** (day 6, full day):
| Weeks | Content |
|---|---|
| 2–15 | Maths for CSE (21) · Quant Aptitude (30) · English F (29) |
| 19–33 | Numerical (28) · English Adv (22) · DSA Saturday sessions ×6 + contests · exam-prep |

**Gates:** weekly, across weeks 2–15 and 19–33.
**Skill assessments:** bi-weekly, across weeks 2–15 and 19–33.

### Legend
- **Morning track (A):** Python → React/TS → LLM Apps
- **Afternoon track (B):** Web → JS → DBMS → Backend → Agents → DSA windows
- **Thread lane:** Intro GenAI, then the DSA strand (1 problem-session/day from Sem A wk 10)
- **Capstone (merged)**
- In-course delivery phases progress: micro-cycles → studio days → project immersion
- **Arc exceptions** (per course-by-course review): Building LLM Apps = build-first spiral, kept deliberately · DBMS ends in a schema-design capstone · Python's project tail is short by design · Web→JS seam is soft (JS micro-cycles begin inside wk 4 as Web's build tail runs)
- Dashed teal columns = 🛡 revision shields (4–5 d, new content frozen) and exam windows; faint dashed = recesses/breaks (Dasara, Sankranthi, inter-sem). Teal ticks = weekly gates · spaced marks = bi-weekly skill assessments. Weeks are **cohort-relative**: university starts spread Aug 4 – Sept 15, so each university anchors week 1 to its own start and ops tracking runs on cohort-week-number, never calendar date. Per-course phase detail: see the Phase Anatomy page.

---

## Calendar-tuned year map — approximation v1

Approximated from the four real calendars (MRV, CDU, VGU, SGU); to be re-tuned when implementation stats arrive. Rule adopted: **revision shield** — new content freezes 4–5 days before every internal and end-sem exam; shield days run maintenance practice + university-course prep only. Festival recesses per real almanacs (Dasara ~1 wk in Sem A; Sankranthi ~1 wk in Sem B).

### Sem A · Aug-anchored (16 wks) — Bootcamp → Mid-2
| Week(s) | Activity |
|---|---|
| W1 | Bootcamp (Induction 7 · Git 101 10) |
| W2–5 | Teach — Python ‖ Web (15) → JS (16, soft seam wk 4–5) |
| W6 | **Dasara recess** — maintenance-only |
| W7–8 | Teach — Python/JS finish → React ‖ DBMS start |
| W9 | **Shield (4–5 d) + Mid-1** |
| W10–13 | Teach — React ‖ DBMS (full pace) · **DSA thread strand starts wk 10** (C++/STL · 1/day) |
| W14 | **Shield + Mid-2** |
| W15–16 | **End-sem exams** · drop-back decision → inter-sem break = rest (no bootcamp — the C++ bridge is DSA Module I, in-course) |

### Sem B · Jan-anchored (16 wks) — LLM layer → Demo Day
| Week(s) | Activity |
|---|---|
| W1 | Teach — LLM Apps ‖ FastAPI start · DSA thread continues + Saturday block |
| W2 | **Sankranthi recess** — maintenance-only |
| W3–7 | Teach — LLM Apps ‖ FastAPI (→W4) → Coding Agents (W5–, 22) |
| W8 | **Shield + Mid-1** |
| W9–13 | Teach — Capstone mornings (incl. 6 comm) ‖ Agents (→W10; 3 freed slots = maintenance windows) → DSA consolidation · contests · exam-prep (W11–13) |
| W14 | **Shield + Mid-2** · capstone hardening |
| W15–16 | **End-sem exams + Demo Day** |

**Capacity arithmetic under this approximation (v2):** full-pace teaching ≈ 21 weeks + partial capacity in shield/recess weeks ≈ **~230 usable AM/PM slots vs 210 core AM/PM sessions — ~10% headroom restored** (v1 was knife-edge at ~250/250). What changed: DSA's 51 sessions moved to the thread lane + Saturdays (45 + 6, ~75 thread days available), Web App Dev trimmed 18 → 15, the 12 planned-new JS sessions became 16 reused ones in the same PM window, and Agents' trim funds 3 protected maintenance windows. Tightest residual seam: Web+JS's 31 sessions across wk 2–7 PM (micro-cycle packing carries the peak; thread absorbs overflow). SME trim advisory (~5%) stands; shield-week Saturdays remain gate days only.

**Thread-shaping rule (parallel-load control, NRI-inspired):** never let three lanes carry new content at once — during double-new-content phases (React ‖ DBMS wk 10–14 · LLM ‖ FastAPI Sem B wk 1–4) the DSA strand runs new sessions only ~3/wk with drill-only days between (funded by the strand's ~30 spare days); the heavy recursion/backtracking module is steered toward lighter-PM weeks, and a slipped React gate auto-downshifts the thread to drill-only that week.

---

## Milestone ladder (per track)
1. **Daily** — classroom quiz inside the session *(exists)*
2. **Weekly** — mastery gate, day 6, from existing item pools *(new slot type — the intervention trigger)*
3. **Bi-weekly** — build checkpoint, EXAM-weight *(new slot type)*
4. **Module end** — module quiz *(exists in fullstack courses; must be added to both GenAI courses)*
5. **Course end** — practical exam *(new)* · Week 36 — Demo Day

## Non-negotiables
- **Timetable ownership** — the cohort's day must give ~6 h. Make-or-break.
- **Entry screening** — the pace has no remediation slack.
- **Drop-back lane** — course boundaries align with standard NIAT semester flow, so a mid-year exit lands cleanly in a standard batch.
- **Lean practice budgets** — checkpoints, not MCQ volume, are the assessment spine.
- **Run the delivery experiment** — randomize sections micro-cycle vs studio day on one 3-week Python stretch; let mastery data pick the standard.
