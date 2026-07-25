# GRIT skill × level → course map (job-readiness benchmark)

Served via `guide()` alongside `grit-programme.md`. **GRIT is the job-readiness benchmark** — its per-skill
**Levels L1–L4** are the target skill outcomes, not a co-curricular activity. **GRIT L1 is the Year-1 readiness
benchmark**: the objective is that every student **clears all required GRIT Level 1** by the end of Year 1. This
doc maps each GRIT skill/level (`grit-programme.md` §8) to the **courses that build it**, so the copilot can check
coverage and propose a valid Year-1 plan.

## The full linkage chain (this is what "linked and aligned" means)
Every hop below is a real link in the data — only the **§8-topic → level** judgement is inferred (that's what
stays PROPOSED):
```
GRIT skill ─▶ §8 level topics ─▶ courses.stack ─▶ course_title  ─▶ student_performance.subject ─▶ NIAT 2025
(grit-programme  (authoritative   (11 stacks)     (+ course_id,     (delivered; joins on          Year-1 subject
 §8)              per-level                        ordered by the    course_id, dash-less,         (+ credits, from
                  topics)                          prereq chain)     ~60% resolve)                 the milestone sheet)
```
- **skill → stack → course:** `courses` table (`stack`, `course_title`, `course_ids`, `prereq_course_ids`).
- **course → delivered subject:** `replace(courses.course_ids,'-','')` = `replace(student_performance.course_id,'-','')`
  (data-notes §Join-key — ~60% resolve, sometimes wrong, so `subject` is the label of record).
- **delivered subject → Year-1 milestone:** the NIAT 2025 curriculum (below), with credits.

> ⚠️ **PROPOSED — the linkage is real; the level assignment is inferred.** Stacks, course names, `course_id`s,
> the prereq ladder, and delivery are all from the data. What is *constructed* is which GRIT **level** each course
> satisfies: the source crosswalk (`grit-skills-course-levels-mapp.csv`) is a near-empty stub, so levels are
> aligned from **§8 Topics-by-level ↔ course outcomes ↔ the prerequisite chain** (method below). The only hard
> per-course anchor is UI Engineering (2 filled `courses-levels.csv` rows). Treat level cells as a planning aid.

GRIT itself stays **reference context, not a queryable table** — answer GRIT questions from this doc +
`grit-programme.md`, never `run_sql` for GRIT. The **courses** it points at *are* queryable (recipe below).

## How the levels are assigned (the alignment logic)
1. **Levels are GRIT's, from §8.** A course sits at the level whose **§8 Topics-by-level** its outcomes/contents
   cover. Only levels that exist in §8 are shown (e.g. UI Engineering has L1–L2 only; Critical Thinking L3 is 🔒).
2. **The prerequisite chain IS the level ladder.** `courses.prereq_course_ids` orders a stack into levels:
   - Computer Programming using Python → Data Structures and Algorithms using C++ *(prereq: Python)* → Advanced
     Data Structures and Algorithms  ⇒  Computational Thinking **L1 → L2 → L3–L4**.
   - Web Application Development → Frontend Development *(prereq: WAD)* → Advanced Frontend Development Using React
     *(prereq: Frontend)*  ⇒  UI Engineering **L1 → L2**.
3. **The one hard anchor.** `courses-levels.csv` is filled for exactly 2 of 63 courses — Web Application
   Development **CL1** (Semantic HTML · CSS Box Model · Flexbox · Basic JS & DOM) and Frontend-React **CL1** —
   and those topics match §8 **UI Engineering L1 / L2** verbatim, confirming the method. The other 61 CL rows are
   empty, so every other level cell is a topic↔outcome inference, not a per-course source of truth.

## How to query coverage (use the table, not just this prose)
```sql
-- 1. Which catalogue courses build a GRIT skill (via its stack), and do we have content?
SELECT stack, course_title, course_ids, ingest_status
FROM   courses WHERE stack = 'CS Core';

-- 2. Bridge a course to real student mastery. course_id is the NxtWave UUID; in student_performance it is
--    dash-less. Only ~60% resolve and the mapping is sometimes wrong (data-notes §Join-key) — so student_
--    performance.subject is the label of record; course_id → catalogue is best-effort enrichment.
SELECT subject, course_id FROM student_performance
WHERE  replace(course_id,'-','') = replace('25c1a72c-216e-47e1-9bc6-b2f16c66e0ca','-','');
```
`ingest_status` is a **content-pipeline** flag (is the course's content loaded), **not** "delivered in Year-1."
A course is **Delivered** in Year-1 iff it maps to one of the **22 `student_performance.subject`s** (below).

## 1st-year milestone (target set) — the NIAT 2025 Year-1 curriculum
Source: **`NIAT 2025 - 1st Year All Subjects Data.xlsx`** (`Sem-1` / `Sem-2 subjects status` tabs; MRV as the
reference design). The authoritative Year-1 curriculum, by semester, with **credits** and course type:

- **Semester 1:** Computer Programming (5) · Web Application Development 1 (5) · Mathematics for Computer Science
  (3) · Quantitative Aptitude (3) · Communicative English Foundation (2) · Introduction to Generative AI (0,
  workshop) · Compliance (2).
- **Semester 2:** Web Application Development 2 (5, Master) · Data Structures (5, Master) · Database Management
  Systems (4, Master) · Numerical Ability (3, Master) · Communicative English Advanced (2, Master) · Building LLM
  Applications (0, workshop) · Compliance (0).

**The Year-1 pass set — which GRIT L1 this curriculum targets:**

| Year-1 subject(s) (NIAT 2025) | GRIT skill | Level reached |
|---|---|---|
| Computer Programming · Data Structures · Mathematics for Computer Science | Computational Thinking | L1 → **L2** ✅ |
| Web Application Development 1 · Web Application Development 2 | UI Engineering | L1 → **L2** ✅ |
| Database Management Systems | SQL · CS Fundamentals *(DBMS only)* | **L1** ✅ / 🟡 |
| Quantitative Aptitude · Numerical Ability | Quantitative Reasoning | **L1** ✅ (+ L2 partial) |
| Communicative English Foundation · Communicative English Advanced | Critical Thinking & Communication | L1 → **L2** ✅ |
| Introduction to Generative AI · Building LLM Applications | Applied Gen AI Development | L1 → **L2** ✅ |
| Compliance | *(not a GRIT skill — compliance/orientation)* | — |

So the NIAT 2025 curriculum targets **GRIT L1 for ~6–7 skills** (Computational Thinking, UI Engineering, SQL,
Quantitative Reasoning, Critical Thinking & Communication, Applied Gen AI) **plus CS Fundamentals L1 partial**
(DBMS is taught; OS/networking are absent). This maps to the **Novice track badges** (`grit-programme.md` §10) —
and because several skills reach **L2** (see coverage), it comes within one gap of **AI Product Specialist**.

> Notes: this is the **designed** curriculum (credits, WAD1/WAD2 as single courses). The **delivered** per-section
> data is the 22 `student_performance` subjects, which split WAD into component courses (Static/Responsive Website,
> JS Essentials, React, …) and add standalone **Server-Side** courses (Node JS, Flask, MongoDB) not shown as a
> credit line here. DS & ML, Data Intelligence, and Physical AI are **not** in Year 1 (later-year / other-track).

## The map  *(GRIT §8 `Skill | Level` shape + §8 topics / Stack / Catalogue course / Delivered? / Coverage)*
**L1 = the Year-1 benchmark.** Coverage: ✅ dedicated Year-1 course · 🟡 partial · ⚠️ gap (no Year-1 course) ·
🔒 locked (level not open / not required now). "Delivered?" = does the catalogue course map to one of the 22 subjects.

| GRIT Skill | Level *(§8 topics)* | Stack | Catalogue course that builds it | Delivered in Y1? | Coverage |
|---|---|---|---|---|---|
| **Computational Thinking** | **L1** *(arrays/strings, loops, basic math, time-complexity)* | Programming & Algorithms · DS/ML | Computer Programming using Python, Data Structures and Algorithms using C++, Math for CSE | ✅ Delivered | ✅ Covered |
| Computational Thinking | L2 *(binary search, hashing, sliding window, stacks/queues, prefix sum)* | Programming & Algorithms | Data Structures and Algorithms using C++ | ✅ Delivered | ✅ Covered |
| Computational Thinking | L3–L4 *(greedy, graphs, DP, backtracking · segment trees, shortest-path)* | Programming & Algorithms | Advanced Data Structures and Algorithms | Catalogue-only | ⚠️ Gap |
| **CS Fundamentals** | **L1** *(OS/DBMS/networking basics, OOPS)* | CS Core · Prog & Algorithms *(OOPS)* | Database Management Systems, Computer Programming using Python *(OOPS)* — **but** Operating Systems, Computer Networks | Partly (DBMS + OOPS) | 🟡 Partial — no OS/networking |
| CS Fundamentals | L2 *(OS scheduling, indexing internals, transactions, memory mgmt)* | CS Core | Operating Systems, Database Management Systems | Catalogue-only (OS) | ⚠️ Gap |
| **SQL** | **L1** *(SELECT/WHERE/GROUP BY/JOIN/subqueries)* | CS Core | Database Management Systems | ✅ Delivered | ✅ Covered |
| SQL | L2 *(indexing, window functions, normalization, transactions)* | CS Core | Database Management Systems | ✅ Delivered | 🟡 Partial (depth) |
| **Applied Gen AI Development** | **L1** *(prompt engineering, zero/few-shot, output validation)* | GenAI | Introduction to GenAI | ✅ Delivered | ✅ Covered |
| Applied Gen AI Development | L2 *(API integration, RAG basics, embeddings)* | GenAI | Building LLM Applications | ✅ Delivered | ✅ Covered |
| Applied Gen AI Development | L3–L4 *(vector DBs, chaining, guardrails · fine-tuning, multi-agent, cost opt)* | GenAI · DS/ML | Advanced GenAI, Practical Software Engineering | Catalogue-only | ⚠️ Gap |
| **UI Engineering** | **L1** *(semantic HTML, CSS box model, flexbox, JS/DOM)* | FullStack | Web Application Development **(CL1 ≡ these §8 topics — the one filled anchor)** | ✅ Delivered | ✅ Covered |
| UI Engineering | L2 *(API integration, state, async JS, error handling)* | FullStack | Frontend Development, Advanced Frontend Development Using React | ✅ Delivered | ✅ Covered |
| **Server-Side Engineering** | **L1** *(REST, routing, middleware, auth basics)* | FullStack | Backend Development Using Node, MongoDB *(delivered as Node JS + Building Rest APIs with Flask)* | ✅ Delivered | ✅ Covered |
| Server-Side Engineering | L2 *(JWT auth, caching, rate limiting, transactions)* | FullStack | Backend Development Using Node, MongoDB; Django / SpringBoot Backend Development | Partly (Node/Mongo only) | 🟡 Partial |
| **Quantitative Reasoning** | **L1** *(%, ratios, averages, P&L, SI/CI, time&work, speed–distance, number systems)* | Aptitude | Quantitative Aptitude, Numerical Ability | ✅ Delivered | ✅ Covered |
| Quantitative Reasoning | L2 *(P&C, probability, DI, puzzles)* | Aptitude | Numerical Ability *(P&C/prob/DI)*, Logical Reasoning *(puzzles)* | Partly (Num. Ability yes) | 🟡 Partial |
| **Critical Thinking & Communication** | **L1** *(grammar/tenses/prepositions, sentence correction, RC basics)* | English | Communicative English Foundation | ✅ Delivered | ✅ Covered |
| Critical Thinking & Communication | L2 *(para jumbles, critical reasoning, inference RC)* | English | Communicative English Advanced | ✅ Delivered | ✅ Covered |
| Critical Thinking & Communication | L3 🔒 *(Locked)* | English | — | — | 🔒 Locked |
| **System Design** | L1 *(HLD, DB schema, APIs, monolith vs microservices)* | System Design | High-Level System Design | Catalogue-only | ⚠️ Gap |
| System Design | L2 *(caching, load balancing, sharding, message queues)* | System Design | High-Level + Low Level System Design | Catalogue-only | ⚠️ Gap |
| **DS & ML** | L1 *(Python for DS, stats, supervised ML, model eval)* | DS/ML | Data Science Foundations, Probability and Statistics, Introduction to ML and Classification Algorithms | Catalogue-only | ⚠️ Gap |
| DS & ML | L2 *(inferential stats, feature eng, ensembles, unsupervised, tuning)* · L3–L4 🔒 | DS/ML | Ensemble Learning, Unsupervised Learning | Catalogue-only | ⚠️ Gap |
| **Data Intelligence** | L1 *(analytics workflow, data cleaning, Power BI/Tableau/Excel, descriptive)* | DS/ML | Data Analytics Foundation, Data Analytics with PowerBI/Tableau | Catalogue-only | ⚠️ Gap |
| Data Intelligence | L2 *(advanced viz, star schema, DAX, storytelling)* | DS/ML | Data Analytics with PowerBI | Catalogue-only | ⚠️ Gap |
| **Physical AI** | L1 *(Linux/ROS2, robot modelling, Gazebo, SLAM, nav, CV, embedded)* | Physical AI | Course 1–4 *(names TBD)* | Catalogue-only | ⚠️ Gap |
| Physical AI | L2 *(advanced ROS2, MoveIt2, path planning, sensor fusion)* · L3–L4 🔒 | Physical AI | Course 1–4 *(names TBD)* | Catalogue-only | ⚠️ Gap |
| **Human Skills for the AI Era** | L1–L2 🔒 *(Locked)* | *(no dedicated stack)* | — | — | 🔒 Locked |
| **Quantitative Finance Foundation** | L1–L3 🔒 *(Locked)* | GenAI *(adjacent: AI For Finance)* | — | — | 🔒 Locked |

## Coverage summary — for proposing a valid Year-1 plan
- **L1 fully covered (7 skills):** Computational Thinking · Applied Gen AI Development · UI Engineering ·
  Server-Side Engineering · SQL · Quantitative Reasoning · Critical Thinking & Communication.
- **L1 partial (1):** CS Fundamentals — DBMS + OOPS are taught; **Operating Systems + Computer Networks are not**.
- **Reaches L2 already (5 skills):** Computational Thinking (DSA), UI Engineering (React), SQL, Applied Gen AI
  (LLM apps), Critical Thinking (Advanced English) — plus Quantitative Reasoning L2 partial (Numerical Ability).
  So Year-1 clears the **AI Product Specialist** set (`grit-programme.md` §10) **except CS Fundamentals L1**.
- **Gaps — no Year-1 course (4 skills):** System Design · DS & ML · Data Intelligence · Physical AI.
- **Locked — not open / not required now (2):** Human Skills for the AI Era · Quantitative Finance Foundation.
- **Bottom line:** the single concrete blocker to the required-L1 milestone (and to Specialist) is **CS Fundamentals
  L1 (OS/networking)** — the first thing a valid plan must add.

### Closing the gaps — the valid-implementation path
Every gap-closer **already exists as a row in the `courses` table** (its content just isn't delivered in Year-1),
so closing a gap = **deliver an existing catalogue course**, not build new content:
- **CS Fundamentals L1 — OS / networking** → `Operating Systems`, `Computer Networks` (stack **CS Core**).
- **System Design** → `High-Level System Design`, `Low Level System Design` (stack **System Design**).
- **DS & ML** → the **DS/ML** stack (`Probability and Statistics`, `Introduction to ML and Classification
  Algorithms`, … — later-year).
- **Data Intelligence** → `Data Analytics Foundation`, `Data Analytics with PowerBI/Tableau` (stack **DS/ML**).
- **Physical AI** → the **Physical AI** stack (`Course 1–4`, names TBD — roadmap).

So the valid Year-1 plan to hit the Novice-badge L1 set = keep the 7 covered skills + **add the CS Core
`Operating Systems` / `Computer Networks` course** for CS Fundamentals L1. The other gaps are later-year /
other-track stacks — out of the Year-1 L1 target unless the milestone says otherwise.

## Delivered Year-1 subject → GRIT skill  *(reverse index — all 22 `student_performance.subject`s)*
- **Computational Thinking:** Programming Foundations · NIAT - DSA · Math For Computer Science
- **Applied Gen AI Development:** Generative AI · Building LLM Applications
- **UI Engineering:** Build Your Own Static Website · Build Your Own Responsive Website · Modern Responsive Web Design · JS Essentials · Introduction to React JS · Build Your Own Dynamic Web Application
- **Server-Side Engineering:** Building Rest APIs with Flask · Node JS · MongoDB
- **SQL:** Introduction to Databases · DBMS Fundamentals
- **Quantitative Reasoning:** Quantitative Aptitude · Numerical Ability · NUMERICAL ABILITY AND REASONING SKILLS FOR ENGINEERS
- **Critical Thinking & Communication:** Communicative English Foundation- I · English Course · Communicative English Advanced

*(These are student-UI names; the catalogue names differ — bridge via `course_id`. CS Fundamentals draws on the
DBMS delivery + OOPS in Computer Programming; OS/networking are not delivered.)*

See `grit-programme.md` for the GRIT programme, §8 skill topics-by-level, §9 contest score bands, and §10 track
badges; `courses` (table) for the full catalogue with stacks, `course_id`s, and prerequisites.
