# Academic Intelligence Platform (AIP) — Design Doc

**Date:** 2026-07-10
**Status:** Draft for review
**Owner:** Gen-AI Content team, NxtWave

---

## 1. Problem & Goal

NxtWave runs multiple products (NIAT, Intensive Online, Intensive Offline, Academy, MINIT, GRIT, Launchpad) teaching multiple stacks (Full Stack, GenAI, DS&ML incl. Maths, DS&Algo, Aptitude, English). Operational and academic issues are logged across Content-* boards in Google Sheets and tagged (inconsistently) against a 16-layer taxonomy (Student Motivation, Instructor Delivery, Mentors Delivery, Scheduling, Program Ops, Internships & Partnerships, Academic Planning, BOS, Assessments, five Learning Design layers, Founders).

Today there is no systematic loop from *issues observed* → *root cause* → *plan/curriculum change* → *did it work?*.

**Goal:** a self-improving agent system that ingests all boards and telemetry, classifies and diagnoses issues, recommends concrete academic-planning and curriculum changes, and learns from which recommendations the team accepts and whether they worked.

**Non-goals (v1):**
- Auto-applying changes to any live curriculum or timetable — every change is a human-approved proposal.
- Model fine-tuning — "learning" is an outcome-memory data flywheel, not training.
- Replacing the Sheets — teams keep working in them; the platform mirrors and normalizes.

**Scope decision (user-confirmed):** all products × all stacks from day one. Data-quality gaps in any board are surfaced as findings in the dashboard/reports rather than blocking ingestion.

---

## 2. Architecture Overview

```
Google Sheets/Drive boards ──┐
Internal APIs (ide-analytics,│──▶ [1] Ingestion (CSV sync) ──▶ [2] Canonical Store (CSV + DuckDB)
n8n-health, ...)  ───────────┘                                      │
                                                                    ▼
                              [4] Web Dashboard ◀──────── [3] Agent Layer (OpenRouter)
                              (heatmaps, rec queue,                 │
                               chat, reports)                       │
                                    │ Accept / Reject / Modify      │
                                    ▼                               │
                              [5] Learning Loop ────────────────────┘
```

| Component | Responsibility |
|---|---|
| Ingestion Service | Each stack board (Content-English, Content-GenAI, …), issue log, and semester plan lands as one CSV in `data/` — manual export from Sheets to start, a scheduled sync script (Sheets API → CSV) later. Telemetry from internal APIs lands as CSV snapshots the same way. Every sync emits a data-quality report. |
| Canonical Store | **CSV files queried in place with DuckDB** — no database server. Source boards stay as CSVs (the CSV is the table); system-generated data (classifications, recommendations, decisions, outcomes) lives in a single `aip.duckdb` file. Full SQL including cross-board joins. Upgrade path: swap the DuckDB file for Postgres only if/when a multi-user dashboard with concurrent writes ships — the schema and SQL carry over. |
| Agent Layer | Four LLM agents (classifier, diagnostician, recommender, chat) called via OpenRouter. |
| Web Dashboard | *(Phase 4, deferred)* Heatmaps, trends, recommendation queue with Accept/Reject/Modify, data-quality view, embedded chat. Google OAuth, org-domain restricted. Until then: fortnightly report + editable queue sheets + ad-hoc queries via Claude Code. |
| Learning Loop | Stores every decision and next-cycle outcome; injects that history into future agent runs. |

**Tech stack:**
- Data: CSV files per board in `data/` + DuckDB (in-place querying + `aip.duckdb` for system-generated tables). No database server in v1.
- Runtime (v1): Python scripts run in/from this Claude Code project — classification, diagnosis, and report generation operate directly on the CSVs. FastAPI backend + React dashboard are deferred until multi-user access is actually needed (see Phasing).
- LLM access: **OpenRouter** (OpenAI-compatible `/chat/completions`). Model per agent is a config value, not code — cheap model for classification, stronger model for diagnosis/recommendation. Structured outputs via tool-calling / `response_format`; agents pinned to models that support it reliably.
- Ingestion: manual CSV export from Sheets to start; scheduled sync script (Sheets API, service account) once the loop proves out
- Scheduling: Claude Code scheduled routine, cron, or existing n8n triggering the pipeline script

---

## 3. Canonical Data Model

Physical layout: source boards are CSVs in `data/` queried in place by DuckDB; reference tables are small seed CSVs checked into the repo; system-generated tables (classifications, recommendations, decisions, outcomes) live in `aip.duckdb`. The logical schema below is the same regardless of where a table physically lives — and is what would move to Postgres unchanged if that upgrade ever happens.

**Reference tables (mostly static):**
- `products` — NIAT, Intensive-Online, Intensive-Offline, Academy, MINIT, GRIT, Launchpad
- `stacks` — FullStack, GenAI, DS&ML, DS&Algo, Aptitude, English
- `layers` — the 16-layer taxonomy with `definition` and `example_issues` text. These definitions are the classifier agent's rubric, fed verbatim into its prompt.
- `topics` — belongs to a stack; ordered within a module/course; `topic_prerequisites` join table for sequencing analysis

**Content tables:**
- `content_artifacts` — one row per topic per artifact type (`reading_material`, `objective_practice`, `coding_practice`, `classroom_quiz`, `module_quiz`) with `status` (present / missing / draft) and Drive link. A topic with < 5 present artifacts = incomplete package → auto-flagged in Phase 2.

**Fact tables (grow every sync):**
- `issues` — raw ingested text + normalized fields: `product_id`, `stack_id`, `layer_id`, `topic_id` (nullable), `severity`, `status`, `source_board`, `source_row_ref` (every issue traces back to its exact Sheet row), `classified_by` (human | agent), `classifier_confidence`
- `metrics` — telemetry snapshots (quiz-unlock lag, IDE error rates, session completion) keyed by product / stack / topic / date

**Feedback tables (the learning loop):**
- `recommendations` — agent proposals: change description, target layer/stack/product, evidence (linked issue IDs), expected impact, cycle generated
- `decisions` — one per recommendation: accepted / rejected / modified, optional reason, and an `outcome` field filled next cycle (did linked metrics / issue counts improve?)

**Deliberate simplifications:**
- No versioned curriculum graph in v1 — topics are a flat ordered list with prerequisites. Full graph versioning only if Phase 3 demands it.
- Sheets remain the write surface for teams. The platform never edits source boards, except optionally writing classification labels back to a dedicated column.

---

## 4. Agent Layer

All agents are called via OpenRouter with per-agent model config (env/DB-configurable). All prompts include the layer taxonomy rubric. All outputs are strict JSON via tool-calling.

### 4.1 Classifier
- **Trigger:** each sync, for new/untagged issues.
- **Input:** raw issue text + board context + taxonomy rubric.
- **Output:** `{layer, stack, product, topic?, severity, confidence}`.
- **Rule:** confidence below threshold (start: 0.7) → human-review queue (editable sheet/CSV in v1) instead of auto-tagging. Human corrections are stored and included as few-shot examples in future classifier prompts.

### 4.2 Diagnostician
- **Trigger:** per report cycle (fortnightly).
- **Input:** classified issues + metrics for the cycle, plus prior cycles for trend context.
- **Output:** recurring patterns and cross-layer root-cause hypotheses (e.g., "GenAI disengagement issues cluster after scheduling disruptions — root cause Scheduling, not Content"), each with linked evidence issue IDs.

### 4.3 Recommender
- **Trigger:** after diagnosis, same cycle.
- **Input:** diagnoses + curriculum/topic data + content-package completeness + **decision/outcome history** (what was accepted, rejected, and what worked) + **hard constraints** (BOS/AICTE: mandated syllabus scope, credit requirements, exam calendar — stored as structured constraint records the prompt marks non-negotiable).
- **Output:** ranked recommendations: what to change, where, evidence, expected impact, effort estimate. Written to `recommendations` and surfaced in the recommendation-queue sheet (dashboard view in Phase 4).

### 4.4 Chat agent
- **Trigger:** on demand — in v1 this is simply asking Claude Code, which queries the CSVs/DuckDB directly; an embedded dashboard chat comes with Phase 4.
- **Capability:** answers questions ("why is GenAI engagement dropping in NIAT?") using read-only SQL over the canonical store. No write access.

### 4.5 Report generator
- Deterministic code (not an agent) that assembles the fortnightly report from diagnostician + recommender output: heatmap summary, top patterns, recommendations, data-quality gaps, and last cycle's decision outcomes. Exported to a Drive doc and linked in the dashboard.

---

## 5. Web Dashboard

**Deferred until multi-user access is a real need.** Until then, the same information is delivered by the fortnightly report (Drive doc), the human-review and recommendation queues as sheets/CSVs the team edits directly, and ad-hoc DuckDB queries run through Claude Code. When the dashboard does ship, these are its views, in priority order:
1. **Heatmap** — issue counts by layer × stack, filterable by product and date range; click-through to underlying issues (with their source Sheet row links).
2. **Recommendation queue** — each proposal with evidence; Accept / Reject / Modify buttons + reason field. This is the primary human-in-the-loop surface.
3. **Human-review queue** — low-confidence classifications awaiting a human tag.
4. **Data quality** — per-board sync health: untagged issues, malformed rows, stale boards, missing content artifacts.
5. **Trends** — issue volume and key metrics over cycles; recommendation hit-rate scoreboard.
6. **Chat** — embedded chat agent.

Auth: Google OAuth restricted to the org domain. Roles: viewer / reviewer (can decide on recommendations) / admin.

---

## 6. Learning Loop (how it "self-learns and evolves")

1. Every recommendation gets a decision (accept/reject/modify + reason).
2. Next cycle, the system computes an outcome per accepted recommendation: did the linked issue counts / metrics improve?
3. Decision + outcome history is injected into the recommender prompt each cycle: accepted-and-worked patterns are reinforced; rejected patterns are suppressed (with the rejection reasons quoted).
4. Human classification corrections become few-shot examples for the classifier.
5. The dashboard shows recommendation hit-rate over time — the observable measure that the system is actually improving.

No model training anywhere; the flywheel is entirely data + prompt context.

---

## 7. Phasing

### Phase 1 — Issue Triage (foundation)
CSV ingestion into `data/`, DuckDB store, classifier, data-quality + heatmap summary (delivered in the report), human-review queue as an editable sheet/CSV.
**Done when:** all boards land as CSVs on schedule; ≥90% of new issues auto-classified or queued for review; classifier accuracy ≥85% on a human-labeled golden set (~150 issues).

### Phase 2 — Curriculum Refinement
Diagnostician, recommender (curriculum/content scope), content-package completeness flags, recommendation queue, fortnightly report.
**Done when:** two full report cycles delivered; team has decided on every recommendation; content-gap flags verified against real boards.

### Phase 3 — Academic Planning + Outcomes
Semester-plan ingestion, BOS/AICTE constraint records, planning-scope recommendations (load balancing, practice-hour allocation, exam buffers), outcome computation, hit-rate scoreboard.
**Done when:** one semester-planning cycle ran with agent input; outcomes computed for all Phase 2 accepted recommendations.

### Phase 4 (optional) — Web Dashboard
FastAPI + React + Google OAuth, per section 5, backed by Postgres. Built only when concurrent multi-user access to the queues becomes a real constraint — the trigger is people stepping on each other in the shared sheets, not a calendar date.

Each phase ships and is used in a real cycle before the next starts.

---

## 8. Error Handling

- **Ingestion:** a malformed row never fails a sync — it becomes a data-quality finding. Syncs are idempotent (keyed on `source_board` + `source_row_ref`); re-running is always safe.
- **LLM calls:** retries with backoff; JSON schema validation on every response with one repair retry; on persistent failure the item goes to the human-review queue — the pipeline degrades to "human does it," never to "data is lost or wrong."
- **Classification:** below-threshold confidence → human queue (never silent auto-tag).
- **Source drift:** if a board's column structure changes, that board's sync is marked failed with a diff of expected vs found headers; other boards proceed.

## 9. Testing

- Unit tests for normalization (raw Sheet rows → canonical records), the golden path plus malformed-row cases.
- **Classifier golden set:** ~150 human-labeled issues sampled across all boards; accuracy measured on every prompt or model change. This is the regression suite for agent quality.
- Diagnostician/recommender: reviewed via report cycles (human judgment), plus schema-validation tests on outputs.
- Ingestion dry-run mode: sync against real Sheets, write nothing, print the diff.

---

## 10. Open Questions

1. **Content package shape:** is the 5-artifact package (reading, objective practice, coding practice, classroom quiz, module quiz) uniform across all stacks, or do e.g. English/Aptitude have different artifact sets? (Affects `content_artifacts` completeness rules.)
2. **Sheet-row traceability:** confirmed as the contract? Requires boards to have stable row identity (an ID column, or we write one back).
3. **Which internal API endpoints** beyond ide-analytics and n8n-health should Phase 1 ingest, and what auth do they need?
4. **Model selection on OpenRouter** for each agent — to be decided by running the classifier golden set against 2–3 candidate models and comparing accuracy vs cost.
5. **Deployment target** — Cloud Run vs existing VM/infra; who owns the GCP project and the service account for Sheets access?
