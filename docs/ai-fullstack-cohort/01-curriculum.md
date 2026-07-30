# The Curriculum — Course Outlines & Design Rationale

*NIAT · AI FullStack Developer Track · Curriculum v1 — for HOD review*

This page answers **what we teach and why**. How it runs — tracks, weeks, delivery models, milestones — lives on the companion [Execution Plan](https://claude.ai/code/artifact/de43b09b-f9f1-4c9c-9319-8bf83aa73af3) page. Session counts in brackets; every module list sums to its course total.

**Stats:** 16 courses · 291 sessions (1-year cohort) · ~28% sessions tagged NEW · ~85% Claude Dev cert coverage

---

## Foundation

### Introduction to Software Development (7)
*prereq: none*

Orientation: shared vocabulary for the whole track — what software is, who builds it, where AI fits.

**Modules:** Tech landscape (1) · OS & Internet (1) · Frontend (1) · Backend (1) · AI (1) · ML (1) · GenAI (1)

**Why:** Already AI-forward (3 of 7 sessions). Compact, works — unchanged.

### Git, Linux & Developer Tools 101 (10)
*prereq: none*

Terminal fluency and version-control habits before any serious coding begins.

**Modules:** 🆕 Terminal & files (2) · 🆕 Processes, env & package managers (2) · 🆕 Git fundamentals (3) · 🆕 GitHub & PR workflow (2) · 🆕 Docs, Markdown & CI intro (1)

**Why:** No git/shell content exists anywhere in the current catalogue. Terminal fluency is a hard prerequisite for coding agents; from here on, every course submits work via git.

---

## Programming & Algorithms

### Computer Programming using Python (28)
*prereq: Induction*

Zero to correct, working Python — with fluency in Python's error patterns and disciplined, spec-first use of AI as a learning aid.

**Modules:** Intro & first programs (2) · Variables, types & IO (4) · Operators & conditionals (4) · Loops (5) · Strings & lists (5) · Functions & built-ins (3) · Tuples, sets & dicts (3) · Stdlib + mini-project (2)

**Why:** Strong base course, compressed 33→28 by merging overlap. The existing "GenAI for learning" session becomes a course-long thread: AI explains and reviews, the student writes — mastery gates are unaided.

### Data Structures & Algorithms (C++) (51)
*prereq: Python · thread strand*

The full BOS-examined Data Structures course, untrimmed and inside the program: C++/STL, complexity thinking and the core technique families — delivered as a year-long thread strand so it never competes with the build tracks.

**Modules:** Programming & computational foundations — C++ · STL · complexity (9) · Mathematical foundations & arrays (10) · Strings & recursion (12) · Sorting & searching (11) · Bit manipulation (9)

**Why:** Data Structures is BOS-approved at 4–6 credits and university-examined at every Sem-2 university. The course runs **whole — all 51 recorded sessions, zero trim** — with the C++ bridge as its own Module I, in-course (no sem-break bootcamp). Delivery: one problem-session per day in the thread lane, Sem A wk 10 → Sem B (45 sessions) + 6 Saturday sessions; consolidation labs, timed contests and university DSA exam-prep fill the Sem B wk 11–13 PM window. Syllabus substantially complete before Sem-2 Mid-1. Advanced DSA (linked lists, trees, graphs, DP) remains Year 2.

---

## AI FullStack

### Web Application Development — HTML · CSS · Tailwind (15)
*prereq: Induction*

Build responsive, styled pages — semantic HTML, the CSS mental models worth owning, and the Tailwind workflow AI tools speak.

**Modules:** HTML & semantic web (3) · CSS fundamentals & box model (4) · Flexbox, Grid & responsive (5) · Tailwind (3)

**Why:** Compressed from 40 HTML/CSS sessions to 15: fundamentals that let students *judge* AI-generated layout stay; craft depth that Tailwind + AI assistance now carries (second Grid session, sizing minutiae) merges away. Tailwind moved earlier — it is what AI tools emit. JS is no longer inside this course: it exists as its own recorded course (next).

### Frontend Development — JavaScript (16)
*prereq: Web App Dev*

The language of the browser, properly: DOM, events, network calls, and modern JS — ending exactly where React begins.

**Modules:** Dynamic web & JS foundations (5) · Events, network & builds (5) · Modern JS — ES6+, classes, promises, modules (6)

**Why:** The catalogue's JS prerequisite for React turned out to have full recorded content: two existing courses — **Build Your Own Dynamic Web Application** (17) and **JS Essentials** (12). Re-cut 29 → 16 by merging split sessions (forms, behind-the-scenes, promises) — **pure reuse, zero authoring**. MRV's React collapse traces to JS being rushed; this course is the fix, scheduled at full width before React starts.

### Frontend Development with React & TypeScript (28)
*prereq: Web App Dev*

Production-pattern React: typed components, server state, auth, and tests.

**Modules:** React fundamentals (5) · State & events (4) · Hooks, effects & API calls (5) · 🆕 TypeScript essentials (4) · Routing & auth (5) · Context & server state (3) · 🆕 Testing: Vitest & RTL (2)

**Why:** Implements our own gap analysis: testing was flagged High, React 19 features / TanStack Query flagged Medium. TypeScript added per HOD draft — it's the industry default and what agent SDKs speak.

### Database Management Systems (28)
*prereq: Python*

One coherent data story: model it, query it in SQL, know when to reach for NoSQL — proven by designing a schema for a real application.

**Modules:** Relational model & SQL basics (5) · Querying & aggregations (6) · ER modelling & normalization (5) · Joins, views & subqueries (5) · Transactions & indexes (2) · MongoDB (3) · 🆕 Schema-design capstone (2)

**Why:** Three current courses (40 sessions, transactions taught twice) merge into one narrative, ending with a schema-design capstone — design and build the data layer for a given product spec — plus a DB-for-AI bridge (text-to-SQL, vector-store awareness) feeding the GenAI stack.

### Backend with FastAPI (14)
*prereq: Python · Web App Dev · DBMS*

Just enough backend to ship: build, secure, stream from, and deploy the API a real application needs — in Python, the language of the AI layer.

**Modules:** 🆕 FastAPI & first API (3) · 🆕 Data & SQL integration (3) · 🆕 Auth-lite: JWT & protected routes (2) · 🆕 SSE, streaming & files (2) · 🆕 Ship it: env, deploy, frontend integration (4)

**Why:** Python-first backend aligns with the LLM layer (one language for backend + AI; JS/TS stays frontend-only) and frees weeks for DSA Essentials. Node/Express depth (existing 22-session content) moves to Year 2 — nothing is discarded.

### Application Development using Coding Agents (22)
*prereq: React · FastAPI · Git 101*

Work the way professional AI-native engineers work: specify, direct, review, and verify — with coding agents doing the typing.

**Modules:** 🆕 How agents work (3) · 🆕 Prompting & reasoning for code (3) · 🆕 Understanding codebases (3) · 🆕 Building features with agents (4) · 🆕 Code review & quality (3) · 🆕 Cloud & background agents (2) · 🆕 Deployment & operations (2) · 🆕 Self-learning & portfolio (2)

**Why:** The track's differentiator, from the HOD draft (AGENTS.md/rules/hooks, AFK vs HITL, self-learning for the long tail). Placed after React + Backend: directing an agent well presupposes being able to judge its output. Trimmed 25 → 22 via three merges (models & cost → configuration · cloud landscape + AFK/HITL · deployment 3 → 2); the three freed PM slots become protected maintenance windows in Sem B. Maps directly onto Claude Developer & Architect cert domains.

### AI FullStack Capstone (12 blocks + 6 comm)
*prereq: React · FastAPI · Agents · LLM Apps*

Ship a real product: React/TS frontend, Node backend, an LLM feature with evals — built AI-natively, with the agent workflow itself graded.

**Modules:** 🆕 Scope & spec (2) · 🆕 Build sprints (6) · 🆕 Evals & hardening (2) · 🆕 Demo & writeup (2) · 🆕 Business communication — embedded (6)

**Why:** Formalizes the catalogue's empty "AI FullStack Projects" row. This is where the role title gets proven — portfolio, demo day, and agent-transcript evidence.

---

## GenAI

### Introduction to GenAI (24)
*prereq: Induction*

AI literacy by building: prompting that works, no-code AI workflows, multimodal generation, and a first look at agents and MCP.

**Modules:** GenAI foundations & LLMs (4) · Prompt engineering (4) · AI workflows with n8n (6) · Multimodal: image & audio (4) · Agents & memory intro (4) · MCP intro (2)

**Why:** Keeps the successful build-first shape (n8n workflows, Telegram assistant); trims tool-listicle sessions. Runs in phase 1 so every later course assumes AI literacy.

### Building LLM Applications (30)
*prereq: Python · Intro GenAI*

Engineer LLM products in Python: portable across providers, retrieval-grounded, agentic, evaluated, and secured.

**Modules:** LLM fundamentals (3) · 🆕 Provider APIs: structured output, streaming, caching (4) · Tool calling (2) · LangChain (3) · RAG (4) · Agents & memory (4) · MCP: consume & author (2) · Multi-agent systems (2) · Evals & observability (3) · 🆕 Security & guardrails (2) · Local models & fine-tuning (1)

**Why:** Current course is framework-first on one vendor's keys. Adds what industry and every certification blueprint demand and the content lacks today: direct multi-provider APIs, security (2 guardrail mentions in 1,773 practice items today), eval depth, cost/caching, MCP authoring. Vendor-portable by design.

---

## English & Communication

### Communicative English Foundation (28)
*prereq: none*

Grammar ladder and spoken fluency — parts of speech through present/past simple, with live speaking sessions.

**Why:** Well-structured with observable outcomes; light touch only.

### Communicative English Advanced (22)
*prereq: English Foundation*

Future forms, modals, perfect tenses, question-making, articulation.

**Why:** Solid; light touch only.

### Business Communication for Engineers (16)
*prereq: English Advanced*

The communication the role actually demands: explain, scope, document, demo.

**Modules:** 🆕 Explaining tech to non-technical audiences (4) · 🆕 Scoping & requirements conversations (4) · 🆕 Written artifacts: PRs, ADRs, docs (4) · 🆕 Demos & interview communication (4)

**Why:** HOD-draft requirement. Retargets the existing Applied English course rather than building new. **6 of these sessions run in Year 1, embedded in the Capstone** (scoping/spec communication at the start; explaining-tech + demo communication at the end) — the remaining 10 run in Year 2.

---

## Footer notes

**Parallel thread, unchanged:** Aptitude — Quantitative (30) · Numerical (28) · Logical Reasoning (~26) · Advanced (~26) — the placement-prep engine with its company-specific session cadence. Deferred to Year 2 for this cohort.

**Deferred courses:** Advanced DSA, Problem Solving Techniques (contents pending).

Delivery, weeks, and milestones: see the [Execution Plan](https://claude.ai/code/artifact/de43b09b-f9f1-4c9c-9319-8bf83aa73af3).
