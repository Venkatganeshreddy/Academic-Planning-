# GRIT skill × level → course map (job-readiness benchmark)

Served via `guide()` alongside `grit-programme.md`. **GRIT is the job-readiness benchmark** — its per-skill
**Levels L1–L4** are the target skill outcomes, not a co-curricular activity. **GRIT L1 is the Year-1 readiness
benchmark**: the objective is that every student **clears all required GRIT Level 1** by the end of Year 1. This
doc maps each GRIT skill/level (`grit-programme.md` §8) to the **courses that build it**, so the copilot can check
coverage and propose a valid Year-1 plan.

**Grounded in the `courses` table.** Each GRIT skill maps to a **`courses.stack`** (11 stacks); every course in a
stack carries a **`course_id`** (`courses.course_ids`) that joins to `student_performance` and `subject_tags`.
So the copilot can walk **GRIT skill → stack → `courses` → actual student mastery** — this is a real join path,
not a name-match guess. "Catalogue course" below is the exact `courses.course_title`.

> ⚠️ **PROPOSED — catalogue-grounded, but the skill→level crosswalk still needs academic sign-off.** The stacks,
> course names, and `course_id`s are real (`courses` table). What is *constructed* is which GRIT **level** each
> course satisfies — the source crosswalk (`grit-skills-course-levels-mapp.csv`) is a near-empty stub, so levels
> are inferred from GRIT §8 topics against course outcomes. Treat coverage flags as a planning aid, not a ruling.

GRIT itself stays **reference context, not a queryable table** — answer GRIT questions from this doc +
`grit-programme.md`, never `run_sql` for GRIT. The **courses** it points at *are* queryable (see the recipe below).

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

## 1st-year milestone (target set)  *(working definition — no authoritative list in the data yet)*
Which GRIT skills×levels a Year-1 student must clear. **No explicit milestone file exists** in the supplied data
(`roles-mapping.csv` is empty), so the working default is the **Novice track badges** (`grit-programme.md` §10),
which the delivered stacks can support:
- **AI Product Mastery — Novice:** Computational Thinking L1 · CS Fundamentals L1 · Applied Gen AI L1 · UI Engineering L2
- **AI Systems Mastery — Novice:** Computational Thinking L1 · CS Fundamentals L1 · Applied Gen AI L1 · Quantitative Reasoning L1 · Critical Thinking & Communication L2

> The stated objective is "**clear all GRIT Level 1**." Read "all" as **all *required* L1** — DS & ML, Data
> Intelligence, and Physical AI are later-year / other-track stacks with no Year-1 course. The official milestone
> should confirm the exact required set (and turn the coverage flags below into a hard pass/gap checklist).

## The map  *(GRIT §8 `Skill | Level` shape + Stack / Catalogue course / Delivered? / Coverage)*
**L1 = the Year-1 benchmark.** Coverage: ✅ dedicated Year-1 course · 🟡 partial · ⚠️ gap (no Year-1 course) ·
🔒 locked (not required now). "Delivered?" = does the catalogue course map to one of the 22 delivered subjects.

| GRIT Skill | Level | Stack | Catalogue course(s) (`courses.course_title`) | Delivered in Y1? | Coverage |
|---|---|---|---|---|---|
| **Computational Thinking** | **L1** | Programming & Algorithms · DS/ML | Computer Programming using Python, Data Structures and Algorithms using C++, Math for CSE | ✅ Delivered | ✅ Covered |
| Computational Thinking | L2–L4 | Programming & Algorithms | Advanced Data Structures and Algorithms, Problem Solving Techniques | Catalogue-only | 🟡 Partial (DSA depth) |
| **CS Fundamentals** | **L1** | CS Core | Database Management Systems *(DBMS)* — **but** Operating Systems, Computer Networks | Partly (DBMS only) | 🟡 Partial — no OS/networking |
| CS Fundamentals | L2 | CS Core | Operating Systems, Computer Networks | Catalogue-only | ⚠️ Gap |
| **SQL** | **L1** | CS Core | Database Management Systems | ✅ Delivered | ✅ Covered |
| SQL | L2 | CS Core | Database Management Systems *(indexing/transactions)* | ✅ Delivered | 🟡 Partial |
| **Applied Gen AI Development** | **L1** | GenAI | Introduction to GenAI | ✅ Delivered | ✅ Covered |
| Applied Gen AI Development | L2 | GenAI | Building LLM Applications | ✅ Delivered | ✅ Covered |
| Applied Gen AI Development | L3–L4 | GenAI · DS/ML | Practical Software Engineering, Advanced GenAI, AI For Finance/Sales/HR | Catalogue-only | ⚠️ Gap |
| **UI Engineering** | **L1** | FullStack | Web Application Development, Frontend Development | ✅ Delivered | ✅ Covered |
| UI Engineering | L2 | FullStack | Advanced Frontend Development Using React | ✅ Delivered | ✅ Covered |
| **Server-Side Engineering** | **L1** | FullStack | Backend Development Using Node, MongoDB *(delivered as Node JS + Building Rest APIs with Flask)* | ✅ Delivered | ✅ Covered |
| Server-Side Engineering | L2 | FullStack | Backend Development Using Node, MongoDB *(persistence)*; Django / SpringBoot Backend Development | Partly (Node/Mongo only) | 🟡 Partial |
| **Quantitative Reasoning** | **L1** | Aptitude | Quantitative Aptitude, Numerical Ability | ✅ Delivered | ✅ Covered |
| Quantitative Reasoning | L2 | Aptitude | Logical Reasoning, Advanced Aptitude | Catalogue-only | 🟡 Partial |
| **Critical Thinking & Communication** | **L1** | English | Communicative English Foundation | ✅ Delivered | ✅ Covered |
| Critical Thinking & Communication | L2 | English | Communicative English Advanced | ✅ Delivered | ✅ Covered |
| Critical Thinking & Communication | L3–L4 | English | Applied Communicative English, Language Analytics | Catalogue-only | 🟡 Partial |
| **System Design** | L1–L2 | System Design | High-Level System Design, Low Level System Design | Catalogue-only | ⚠️ Gap |
| **DS & ML** | L1–L4 | DS/ML | Probability and Statistics → Supervised/Unsupervised/Ensemble Learning → Deep Learning / NLP / CV | Catalogue-only | ⚠️ Gap |
| **Data Intelligence** | L1–L2 | DS/ML | Data Analytics Foundation, Data Analytics with PowerBI, Data Analytics with Tableau | Catalogue-only | ⚠️ Gap |
| **Physical AI** | L1–L4 | Physical AI | Course 1–4 *(names yet to confirm)* | Catalogue-only | ⚠️ Gap |
| **Human Skills for the AI Era** | L1–L2 | *(no dedicated stack)* | — | — | 🔒 Locked |
| **Quantitative Finance Foundation** | L1–L3 | GenAI *(adjacent: AI For Finance)* | — | — | 🔒 Locked |

## Coverage summary — for proposing a valid Year-1 plan
- **L1 fully covered (7 skills):** Computational Thinking · Applied Gen AI Development · UI Engineering ·
  Server-Side Engineering · SQL · Quantitative Reasoning · Critical Thinking & Communication.
- **L1 partial (1):** CS Fundamentals — DBMS is delivered; **Operating Systems + Computer Networks are not**.
- **Gaps — no Year-1 course (4 skills):** System Design · DS & ML · Data Intelligence · Physical AI.
- **Locked — not required now (2):** Human Skills for the AI Era · Quantitative Finance Foundation.
- **Bottom line:** the delivered stacks carry a student to the **Novice badge** on the AI Product / AI Systems
  tracks. The one gap inside that target is **CS Fundamentals L1 (OS/networking)** — the concrete blocker to
  "all required L1," and the first thing a valid plan must add.

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

## The GRIT-level ⇄ course-level linkage mechanism *(from `courses-levels.csv` — model only, mostly unfilled)*
The catalogue defines a per-course **Course Level (CL1, CL2, …)** with **medal bands** (Gold ≥85% · Silver
70–84.99% · Try Again <70%), and states that **"Course Quiz evaluation should shadow GRIT Assessment
evaluation."** That is the intended mechanism by which clearing a course level ⇒ progress on a GRIT skill level.
**Only 2 of 63 courses are populated** (Web Application Development CL1, Frontend Development Using React CL1), so
this is documented as the *model*, not a per-course source of truth. Populate as the catalogue fills in.

## Delivered Year-1 subject → GRIT skill  *(reverse index — all 22 `student_performance.subject`s)*
- **Computational Thinking:** Programming Foundations · NIAT - DSA · Math For Computer Science
- **Applied Gen AI Development:** Generative AI · Building LLM Applications
- **UI Engineering:** Build Your Own Static Website · Build Your Own Responsive Website · Modern Responsive Web Design · JS Essentials · Introduction to React JS · Build Your Own Dynamic Web Application
- **Server-Side Engineering:** Building Rest APIs with Flask · Node JS · MongoDB
- **SQL:** Introduction to Databases · DBMS Fundamentals
- **Quantitative Reasoning:** Quantitative Aptitude · Numerical Ability · NUMERICAL ABILITY AND REASONING SKILLS FOR ENGINEERS
- **Critical Thinking & Communication:** Communicative English Foundation- I · English Course · Communicative English Advanced

*(These are student-UI names; the catalogue names differ — bridge via `course_id`. CS Fundamentals draws on the
DBMS delivery; OS/networking are not delivered.)*

See `grit-programme.md` for the GRIT programme, skill topics (§8), and track badges (§10); `courses` (table) for
the full catalogue with stacks, `course_id`s, and prerequisites.
