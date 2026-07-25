# GRIT skill × level → Year-1 course map (job-readiness benchmark)

Served via `guide()` alongside `grit-programme.md`. **GRIT is the job-readiness benchmark** — its per-skill
**Levels L1–L4** are the target skill outcomes, not a co-curricular activity. **GRIT L1 is the Year-1 readiness
benchmark**: the objective is that every student **clears all required GRIT Level 1** by the end of Year 1. This
doc maps each GRIT skill/level (from `grit-programme.md` §8) to the **courses that build it**, so the copilot can
check coverage and propose a valid Year-1 plan.

> ⚠️ **PROPOSED — needs academic sign-off.** Mappings are derived from GRIT's *Topics-by-level* (§8) against
> **course names**, not verified syllabus content. Refine with the authoritative GRIT data + 1st-year milestone.

GRIT is **reference context, not queryable data** — no GRIT tables; answer from this doc + `grit-programme.md`,
never `run_sql`. Courses here are the **22 delivered Year-1 (Sem 1-2) subjects** in `student_performance.subject`.

## 1st-year milestone (target set)  *(authoritative list — to be confirmed)*
Which GRIT skills×levels a Year-1 student must clear. **Pending the official milestone** — the working default is
the **Novice track badges** (`grit-programme.md` §10), which the current curriculum can support:
- **AI Product Mastery — Novice:** Computational Thinking L1 · CS Fundamentals L1 · Applied Gen AI L1 · UI Engineering L2
- **AI Systems Mastery — Novice:** Computational Thinking L1 · CS Fundamentals L1 · Applied Gen AI L1 · Quantitative Reasoning L1 · Critical Thinking & Communication L2

> The stated objective is "**clear all GRIT Level 1**." Treat "all" as **all *required* L1** — some skills
> (Physical AI, DS & ML, Data Intelligence) belong to later-year / other-track paths and have no Year-1 course.
> The official milestone should confirm the exact required set.

## The map  *(mirrors GRIT §8 format: Skill | Level | … + Corresponding courses)*
Grain = one row per (skill, level). **L1 = the Year-1 benchmark.** Courses are exact `student_performance.subject`
names. Coverage: ✅ covered by a dedicated Year-1 course · 🟡 partial · ⚠️ gap (no Year-1 course) · 🔒 locked (not
required now).

| GRIT Skill | Level | Corresponding Year-1 courses | Coverage |
|---|---|---|---|
| **Computational Thinking** | **L1** | Programming Foundations, NIAT - DSA, Math For Computer Science | ✅ Covered |
| Computational Thinking | L2–L4 | NIAT - DSA *(advanced DSA depth)* | 🟡 Partial |
| **Applied Gen AI Development** | **L1** | Generative AI | ✅ Covered |
| Applied Gen AI Development | L2 | Building LLM Applications | ✅ Covered |
| Applied Gen AI Development | L3–L4 | — | ⚠️ Gap |
| **UI Engineering** | **L1** | Build Your Own Static Website, Build Your Own Responsive Website, Modern Responsive Web Design, JS Essentials | ✅ Covered |
| UI Engineering | L2 | Introduction to React JS, Build Your Own Dynamic Web Application | ✅ Covered |
| **Server-Side Engineering** | **L1** | Building Rest APIs with Flask, Node JS | ✅ Covered |
| Server-Side Engineering | L2 | Node JS, MongoDB *(persistence)* | 🟡 Partial |
| **SQL** | **L1** | Introduction to Databases, DBMS Fundamentals | ✅ Covered |
| SQL | L2 | DBMS Fundamentals *(indexing/transactions)* | 🟡 Partial |
| **CS Fundamentals** | **L1** | DBMS Fundamentals *(DBMS)*, Programming Foundations *(OOPS)* | 🟡 Partial — no OS/networking course |
| CS Fundamentals | L2 | — | ⚠️ Gap |
| **Quantitative Reasoning** | **L1** | Quantitative Aptitude, Numerical Ability, NUMERICAL ABILITY AND REASONING SKILLS FOR ENGINEERS | ✅ Covered |
| Quantitative Reasoning | L2 | — *(P&C / probability / DI not a dedicated Year-1 course)* | 🟡 Partial |
| **Critical Thinking & Communication** | **L1** | Communicative English Foundation- I, English Course | ✅ Covered |
| Critical Thinking & Communication | L2 | Communicative English Advanced | ✅ Covered |
| **System Design** | L1–L2 | — *(only API/DB-schema exposure via Building Rest APIs with Flask, Introduction to Databases)* | ⚠️ Gap |
| **DS & ML** | L1–L4 | — *(no Python-for-DS / stats / ML course in Year 1)* | ⚠️ Gap |
| **Data Intelligence** | L1–L2 | — *(no BI / Power BI / Tableau course)* | ⚠️ Gap |
| **Physical AI** | L1–L4 | — *(no Linux/ROS2 / robotics course)* | ⚠️ Gap |
| **Human Skills for the AI Era** | L1–L2 | — | 🔒 Locked |
| **Quantitative Finance Foundation** | L1–L3 | — | 🔒 Locked |

## Coverage summary — for proposing a valid Year-1 plan
- **L1 fully covered (7 skills):** Computational Thinking · Applied Gen AI Development · UI Engineering ·
  Server-Side Engineering · SQL · Quantitative Reasoning · Critical Thinking & Communication.
- **L1 partial (1):** CS Fundamentals — DBMS + OOPS are taught; **OS / networking have no dedicated Year-1 course**.
- **Gaps — no Year-1 course (4):** System Design · DS & ML · Data Intelligence · Physical AI.
- **Locked — not required now (2):** Human Skills for the AI Era · Quantitative Finance Foundation.
- **Bottom line:** the current Year-1 curriculum can carry a student to the **Novice badge** on the AI Product /
  AI Systems tracks. The one gap inside that target is **CS Fundamentals L1 (OS/networking)** — the concrete
  blocker to "all required L1," and the first thing a valid plan must add.

### Closing the gaps — the valid-implementation path
The gap skills already exist as **NxtWave catalogue courses** (`courses` table), so closing a gap usually means
**pulling an existing course into Year-1**, not building new content:
- **CS Fundamentals L1 — OS / networking** → `Operating Systems`, `Computer Networks` (CS Core stack).
- **System Design** → `HLD`, `LLD` (System Design stack).
- **DS & ML** → the DS/ML stack (Python for DS, stats, ML — later-year).
- **Physical AI** → the Physical AI stack (ROS2/robotics — roadmap).
So a valid Year-1 plan to hit the Novice-badge L1 set = keep the 7 covered skills + **add the CS Core OS/Networking
course** for CS Fundamentals L1. (The other gaps belong to later-year / other-track paths — out of the Year-1 L1 target unless the milestone says otherwise.)

## Year-1 subject → GRIT skill  *(reverse index — all 22 subjects)*
- **Computational Thinking:** Programming Foundations · NIAT - DSA · Math For Computer Science
- **Applied Gen AI Development:** Generative AI · Building LLM Applications
- **UI Engineering:** Build Your Own Static Website · Build Your Own Responsive Website · Modern Responsive Web Design · JS Essentials · Introduction to React JS · Build Your Own Dynamic Web Application
- **Server-Side Engineering:** Building Rest APIs with Flask · Node JS · MongoDB
- **SQL:** Introduction to Databases · DBMS Fundamentals
- **Quantitative Reasoning:** Quantitative Aptitude · Numerical Ability · NUMERICAL ABILITY AND REASONING SKILLS FOR ENGINEERS
- **Critical Thinking & Communication:** Communicative English Foundation- I · English Course · Communicative English Advanced

*(CS Fundamentals draws on DBMS Fundamentals + Programming Foundations rather than a dedicated course.)*

See `grit-programme.md` for the GRIT programme, skill topics (§8), and track badges (§10).
