# GRIT 2026–27 — programme knowledge (reference context)

Served via `guide()` alongside the academic-delivery notes. This is a **second product** the
copilot must know: **G.R.I.T — Global Readiness Immersion Trips**, NIAT/NxtWave's sponsored
international tech-immersion + gamified-contest programme.

**GRIT is reference context, NOT queryable data.** There are **no GRIT tables** in the DuckDB
store — do not write `run_sql` against it. Answer GRIT questions from THIS document. The
delivery/planning data (`delivered_*`, `course_plan_vs_actual`, …) is a different product
(NIAT university delivery) and never mixes with GRIT numbers.

**Confirmed vs WIP.** Source consolidates the programme write-up + two internal planning
workbooks. Where the sources disagree, the *confirmed* value and the *superseded* one are both
named below — quote the confirmed one and flag the conflict. Dates, destinations, budget, seat
splits, role names, and ownership are **indicative/internal, subject to change**; NIAT reserves
the right to revise skill content, scoring, Miles, attempt rules, tracks, and criteria anytime.

---

## 1. Snapshot

| Attribute | Detail |
|---|---|
| Name | G.R.I.T — Global Readiness Immersion Trips 2026–27 |
| Run by | NIAT / NxtWave |
| Eligible batches | 2023, 2024, 2025 |
| Programme duration | 15 Feb 2026 → 15 Feb 2027 (12 months) |
| Contest / qualification window | Feb 2026 → Feb 2027 |
| Travel window | May – Jul 2027 (tentative) |
| Total seats | 1,000 announced (**not** a guarantee all fill — base criteria must be met) |
| Seat split (2023 : 2024 : 2025) | **2 : 132 : 866** (confirmed) |
| Selection routes | Top of the Leaderboard (merit) + Lucky Draw (basic eligibility) |
| Candidate destinations | UAE, Singapore, China, UK, Europe, USA, South Korea, Japan (tentative) |
| Sponsored | Return economy airfare, accommodation, food, local travel (official schedule) |
| Student pays | Passport & visa (by design — "skin in the game"); expenses outside itinerary |
| Immersions per student | One |
| Budget (internal) | ~₹20 crore INR |
| Delivery (internal) | 6 cohorts (~167 each); 1 staff : 12 students (~84 staff) |

**Mission line:** "make every one of you compete globally… skill up, become stronger, aim higher."

---

## 2. Eligibility & selection

**Eligibility:** enrolled in batch 2023/24/25 · **≥75% attendance** from 15 Feb 2026 · on-time
semester registration, kept every semester through the programme · valid passport with **≥1 year
validity at travel**.

**Two routes to a seat** — both require base criteria, and **clearing the interview is mandatory
to keep a finale position active**:
- **Top of the Leaderboard** — purely merit, highest Miles scorers.
- **Lucky Draw** — luck-based among students meeting basic eligibility ("Lucky Draw" is a working
  label, may be renamed).

Seats allocated by weighted distribution across batches; equal opportunity within a batch, no
campus weighting. Final list confirmed **only after successful visa approval**; no visa ⇒ deferred
or reassigned.

---

## 3. The Miles economy

Loop: **complete skill assessments → gain certifications → earn Miles → climb the leaderboard.**
Higher Miles also raises the probability of extra goodies/surprises.

**Medals** (each Skill-Level assessment returns one):

| Outcome | Meaning | Miles | Unlocks next level? |
|---|---|---|---|
| Gold | Top band | Full Miles for the level | Yes |
| Silver | Strong pass | ~90% of Gold | Yes |
| Try Again | Below pass | Flat **5** (participation) | No — must re-attempt to ≥ Silver |

**Attempt rules:** unlimited attempts via later contests · only the **highest** score counts · a
level unlocks only after Gold/Silver on the previous one · **≥5-day gap** between re-attempts of
the same level.

**Miles per level by weight** (Gold shown; Silver ≈ 90%, Try Again = 5):

| Level weight | Gold |
|---|---|
| Light (L1 basic) | 10 |
| Standard — L1 flagship / L2 basic | 20 / 40 |
| Advanced — L2 flagship / L3 | 80 / 200 |
| Elite (L4) | 400 |

> Superseded: an earlier model used **Grade A / B / RA** with per-skill multipliers. Current model
> is Gold / Silver / Try-Again with fixed Miles per level (above).

---

## 4. Skills & Levels catalogue

Gold Miles per level. "Locked" levels open progressively.

| Skill | L1 | L2 | L3 | L4 | Topics (by level) |
|---|---|---|---|---|---|
| Computational Thinking | 20 | 80 | 200 | 400 | L1 arrays/strings, loops, basic math, simulation, time-complexity · L2 binary search, hashing, sliding window, stacks/queues, prefix sum · L3 greedy, graphs, BFS/DFS, basic DP, backtracking, heap · L4 advanced DP/graphs, segment trees, shortest-path |
| Applied Gen AI Development | 20 | 80 | 200 | 400 | L1 prompt engineering, zero/few-shot, output validation · L2 API integration, RAG basics, embeddings · L3 vector DBs, prompt chaining, guardrails · L4 fine-tuning, multi-agent workflows, cost optimisation |
| UI Engineering | 10 | 40 | — | — | L1 semantic HTML, CSS box model, flexbox, JS/DOM · L2 API integration, state, async JS, error handling |
| Server-Side Engineering | 10 | 40 | — | — | L1 REST, routing, middleware, auth basics · L2 JWT auth, caching, rate limiting, transactions |
| SQL | 10 | 40 | — | — | L1 SELECT/WHERE/GROUP BY/JOIN/subqueries · L2 indexing, window functions, normalization, transactions |
| CS Fundamentals | 10 | 40 | — | — | L1 OS/DBMS/networking basics, OOPS · L2 OS scheduling, indexing internals, transactions, memory mgmt |
| System Design | 20 | 80 | — | — | L1 HLD, DB schema, APIs, monolith vs microservices · L2 caching, load balancing, sharding, message queues |
| Quantitative Reasoning | 10 | 40 | — | — | L1 percentages, ratios, averages, P&L, SI/CI, time&work, speed–distance, number systems · L2 P&C, probability, DI, puzzles |
| Critical Thinking & Communication | 10 | 20 | 40 🔒 | — | L1 grammar/tenses/prepositions, sentence correction, RC basics · L2 para jumbles, critical reasoning, inference RC · L3 Locked |
| DS & ML | 20 | 80 | 200 🔒 | 400 🔒 | L1 Python for DS (NumPy/Pandas/EDA), stats, supervised ML, model eval · L2 inferential stats, feature eng, ensembles, unsupervised, tuning · L3/L4 Locked |
| Data Intelligence | 10 | 40 | — | — | L1 analytics workflow, data cleaning, Power BI/Tableau/Excel, descriptive · L2 advanced viz, data modeling (star schema), DAX, storytelling |
| Physical AI | 20 | 80 | 200 🔒 | 400 🔒 | L1 Linux/ROS2, robot modelling/maths, Gazebo, SLAM, nav, CV, embedded · L2 advanced ROS2, ros2_control, MoveIt2, path planning, sensor fusion · L3/L4 Locked |
| Human Skills for the AI Era | 10 🔒 | 40 🔒 | — | — | Locked |
| Quantitative Finance Foundations | 20 🔒 | 80 🔒 | 200 🔒 | — | Locked |

---

## 5. Contest formats & score bands

Pattern · duration · band → medal (Gold / Silver / Try-Again). Syllabus + sample questions live in
the Assessments workbook (not reproduced — they change as the question bank evolves).

| Skill · Lvl | Pattern | Duration | Gold / Silver / Try-Again |
|---|---|---|---|
| Computational Thinking L1 | Coding | 90 min | 100 / 83.33–99.99 / 0–83.32 |
| Computational Thinking L2 | Coding | 90 min | 100 / 75–99.99 / 0–74.99 |
| UI Engineering L1 | MCQs + Coding | 90 min | 85–100 / 70–84.99 / 0–69.99 |
| UI Engineering L2 | MCQs + IDE Coding | 90 min | 90–100 / 80–89.99 / <80 |
| CS Fundamentals L1 | MCQs | 40 min | 90–100 / 85–89.99 / 0–84.99 |
| CS Fundamentals L2 | MCQs | 60 min | 90–100 / 85–89.99 / 0–84.99 |
| Applied Gen AI L1 | MCQs | 45 min | 90–100 / 80–89.99 / 0–79.99 |
| Applied Gen AI L2 | MCQs | 45 min | 90–100 / 80–89.99 / 0–79.99 |
| Critical Thinking & Comm. L1 | MCQs | 40 min | 95–100 / 75–94.99 / 0–74.99 |
| Critical Thinking & Comm. L2 | MCQ | 30 min | 90–100 / 80–89.99 / <80 |
| Server-Side Engineering L1 | MCQs + Coding | 90 min | 95–100 / 90–94.99 / 0–89.99 |
| Server-Side Engineering L2 | MCQs + Coding | **TBU** | Will be updated shortly |
| Quantitative Reasoning L1 | MCQs | 30 min | 90–100 / 75–89.99 / 0–74.99 |
| Quantitative Reasoning L2 | MCQ | 40 min | 95–100 / 80–94.99 / 0–79.99 |
| SQL L1 | MCQs + Coding | 90 min | 90–100 / 85–89.99 / 0–84.99 |
| SQL L2 | MCQs + Coding | 90 min | 90–100 / 80–89.99 / 0–79.99 |
| DS & ML L1 | MCQs + Coding | 90 min | 90–100 / 85–89.99 / 0–84.99 |
| Physical AI L1 | MCQs + Coding | 90 min | 85–100 / 70–84.99 / 0–69.99 |

---

## 6. Certifications — tracks & badges

Certifications ("Tracks") sit above individual skills: earned by clearing a defined skill+level
combination **plus a mandatory interview where applicable**. Badges are **sequential (no skipping)**,
Novice → Grand Master.

**Track types:** AI Product Mastery · AI Systems Mastery · AI Models Mastery · AI Robotics Mastery
(Physical AI) · more TBA. (AI Models & AI Robotics matrices still being finalised.)

**Badge → indicative salary band (internal):** Novice 3.5–6 · Specialist 6–12 · Expert 12–18 ·
Master 18–25 · Grand Master 25+ LPA.

**Track composition (skill levels required per badge):**

*AI Product Mastery* — Novice: Comp.Thinking L1, CS Fund L1, GenAI L1, UI Eng L2 · Specialist:
CT L2, CS L1, GenAI L2, UI L2, Backend L1, SQL L1 · Expert: System Design L1 · Master / Grand
Master: TBD (rows empty in source).

*AI Systems Mastery* — Novice: CT L1, CS L1, GenAI L1, Quant Reasoning L1, Critical Thinking L2 ·
Specialist: CT L2, CS L1, GenAI L2, Quant L1, CritThink L2 · Expert: CT L3, CS L2, GenAI L3, SysDesign
L1, Quant L1, CritThink L2 · Master: CT L4, CS L2, GenAI L4, Quant L1, CritThink L2 · Grand Master: TBD.

Expert/Master/Grand-Master badges are **Locked**, unlocked progressively.

---

## 7. Additional ways to earn Miles

All require verification — typically an equivalent NxtWave **offline proctored test** — before Miles credit.

**Competitive programming:** Codeforces Pupil ≥1200 → 80 · Specialist ≥1400 → 200 · Expert ≥1600 →
400 · Candidate Master ≥1900 → 1000 (requires Problem-Solving L1). CodeChef 1★→6★ = 20/40/80/200/400/1000.
LeetCode 1600 → 40 · 1800/2000/2200/2400 → 80/200/400/1000 (sustain 3 consecutive contests).

**Hackathons (finalist / winner):** SIH National 150/200 · VBYLD / Design for Bharat 150/200 ·
NIAT Makers Conclave 100/150.

**Ticket to Finale (skip the leaderboard):** ICPC Regionals selection · GSoC selection · raising
capital / renowned incubator or accelerator.

**WIP avenues:** Open Source, Entrepreneurship, Content Creation, AI-led perf marketing, UI/UX —
Miles values being designed; proofs required.

---

## 8. Governance & rollout (internal)

Scale: ~1,000 students / 6 cohorts (~167 each) · 1:12 staffing (~84 staff) · ~₹20 cr. Owners (GRIT
POD, working assignments): Overall SJ · Program Design SG & SJ · Assessment Design + Leaderboard
formula SG · Assessment Ops Srikar & PD · Perf monitoring VT & PD · Engineering Gayathri · Data &
Analytics Sagar (TBC).

Rollout phases: 1 Announcement → 2 Registrations → 3 Mini Contests (warm-up) → 4 First Assessments
(go-live from March) → 5 Surprise Elements → 6 Final Winner Announcement.

Engagement mechanics: physical certificates per level; group penalties/rewards; batch-wise
leaderboards; first-50 / early-mover + on-time-registration bonus Miles; UGC / viral-video campaigns.

---

## 9. Known conflicts & open items (flag these, don't state one side as settled)

- **Seat split** — confirmed **2 / 132 / 866**. Workbooks also cite a **10 : 988 : 6502** weighting
  and an earlier **500 / 500** leaderboard-vs-lucky-draw split. Use 2/132/866; the others are superseded.
- **Placement benchmark** — public write-up: "crack at least entry-level Tech roles"; workbook:
  "crack at least **3.5 LPA**." Treat the LPA figure as an **internal benchmark**, not a published promise.
- **Medals** — Gold/Silver/Try-Again is current; **Grade A/B/RA** with multipliers is legacy.
- **Locked / TBU** — Server-Side L2 duration TBU; ~10 Locked levels; AI Models & AI Robotics track
  matrices unfinished; Grand Master rows empty in both defined tracks.
- **Naming / indicative** — "Lucky Draw" label may change; destinations, dates, budget, role names,
  and ownership are indicative and subject to revision.
