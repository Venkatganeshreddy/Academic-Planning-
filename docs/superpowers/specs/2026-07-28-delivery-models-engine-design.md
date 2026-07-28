# Delivery-Models Engine — Design

**Date:** 2026-07-28
**Status:** Draft for review
**Scope:** An addition to the copilot's *"What could be better"* (unconstrained) view. It does **not** touch the grounded 8-section plan.

---

## 1. Purpose

The grounded plan answers *"when does each course run, and at what pace."* This engine answers a different question: **"HOW should each subject be taught — which delivery shape, in which phase — given this university's own track record on that subject?"**

It is a **pedagogy layer**, tagged `[recommendation]` (with `[evidence]` where a data signal forces the call), living inside the opt-in unconstrained view. Bolder than the grounded plan by design; never edits its numbers.

## 2. The four delivery models (fixed vocabulary)

These are the user-supplied model cards — the engine's fixed vocabulary, not something it invents:

| Model | Shape | Best for | Watch out |
|---|---|---|---|
| **1 · Tight micro-cycles** | learn A → practice → learn B → practice → code practice (one day, both subjects) | Concept acquisition — novices, new syntax; retrieval minutes after instruction | Fragmented; no long build stretches |
| **2 · Bootcamp studio day** | segmented AM teaching + one uninterrupted PM lab (one subject deep) | Skill consolidation — long labs build fluency | Never one continuous 2.5 h lecture; segment the morning |
| **3 · A/B day scheduling** | alternate full days per subject (Subject A M/W/F, B T/Th) | Two heavier subjects mid-course needing full-day depth | Halves weekly touchpoints — gates must watch decay |
| **4 · Block scheduling (3+2)** | 3 days Subject A, 2 days Subject B in one week | Project phases — context-carrying beats spacing | Novice content + weekend gap = measurable decay |

## 3. The engine (three steps)

### Step A — Subject nature → phase arc
Not every subject runs all three phases. Bucket each requested subject by nature:

- **Build / coding** (e.g. WAD-1, Computer Programming, GenAI): full arc — **concept → consolidation → project**.
- **Skills / quant** (e.g. Quantitative Skills, Mathematics, Professional Skills): **concept → consolidation** (no project immersion; assessment-driven).
- **Compliance / light** (e.g. Quantum Computing, IKS, Foreign Language, CAEG): **one lightweight model, low intensity** (typically micro-cycles or a light block).

Bucketing rule: use `courses.stack` / the subject's GRIT-skill mapping to decide nature; a subject that maps to a GRIT coding skill (Computational Thinking, UI Engineering, Applied GenAI) is *build*; a GRIT MCQ skill (Quant Reasoning, Critical Thinking) is *skills*; a Compliance-tagged subject is *light*.

### Step B — Phase → baseline model (fixed pedagogy)
- Concept phase → **Model 1 (micro-cycles)**
- Consolidation phase → **Model 2 (studio day)**
- Project phase → **Model 4 (block)**
- Model 3 (A/B) is **not a phase** — it is the experiment/variant arm overlaid on the consolidation phase when the data calls for it (Step C).

### Step C — Data signature → tunes intensity (never swaps the model)
The university's own per-subject signals tune *how hard* each phase's model runs. The model itself is fixed by phase; the data adjusts gates, protection, lab length, and whether the A/B experiment fires.

| Signal (per subject, this university) | Reads from | Tuning it triggers |
|---|---|---|
| **High attempt + low clear** (e.g. Quant 76% attempt / 18% clear) | `grit_readiness` | Consolidation studio gets **extra gates + fire the Model-3 A/B long-lab experiment** — the mastery gap needs depth, not more volume |
| **Low attempt / near-zero MCQ practice** (MRV 0–2%) | `grit_readiness`, `student_perf_by_subject` | Concept micro-cycles get **mandatory retrieval loops** — an engagement problem, not a depth one |
| **Collapsed / heavily slipped** (CAEG +64d, GenAI +85d) | `course_plan_vs_actual` | The subject's model is **protected / blocked** so it can't be deprioritised again |
| **Low rating / no ingested content** *(annotation only)* | `session_feedback_safe`, `content_all` | A ⚠ **delivery-risk note** — more instructor-led studio time; does NOT drive the model choice (feedback at some colleges doesn't discriminate) |

## 4. Output shape

One compact table per plan, inside the unconstrained view under a heading **"Delivery models — how to teach each subject":**

```
| Subject | Concept phase | Consolidation phase | Project phase | This uni's signal → tuning | Tag |
```

- Build subjects fill all three phase columns; skills subjects leave the project column "—"; light subjects show a single model spanning the row.
- Each phase cell names the model (1/2/4) and any intensity note.
- The "signal → tuning" column carries the one-line data justification.
- `Tag` = `[evidence]` (a real signal forced it) or `[recommendation]` (reasoned beyond the data).

Followed by:
- A short **legend** — the "signature → tuning" rules (from Step C) so the reader can audit the logic.
- **"The one delivery bet"** — the single highest-leverage delivery change if only one were adopted, and its risk.

## 5. Grounding

Reads the same tables through a new lens — no new data needed:
- `grit_readiness` (clear rate, attempt rate per skill → per subject via the GRIT skill→subject map)
- `student_perf_by_subject` (MCQ/coding attempt + completion)
- `course_plan_vs_actual` (start_slip_days, pct_completed)
- `session_feedback_safe`, `content_all` (annotation only)
- `courses.stack` / GRIT skill→subject map (subject-nature bucketing)

Every model recommendation cites its signal inline, exactly like the grounded plan.

## 6. Where it lives

An addition to the **`## What could be better — the unconstrained view`** spec in `docs/planning-method.md`: a new sub-block the model emits *only* on the unconstrained-view trigger, after the existing `[evidence]`/`[recommendation]` layer table. No change to the grounded plan's eight sections, and no change to when the unconstrained view fires.

## 7. Explicitly OUT of scope (a later, separate spec)

The ambitious framing *around* the engine — held for a second design once this is proven:
- The mapped-year **2-track execution scaffold** (34 weeks, bootcamp → shields → recesses → Demo Day)
- **Revision shields**, festival recesses, drop-back lanes, capacity arithmetic
- The **milestone ladder** (daily quiz → weekly gate → bi-weekly checkpoint → Demo Day) as a new slot-type system
- The randomized **delivery experiment** as an operational programme (the engine only *flags* where Model 3 should be A/B-tested; running it is ops)

These are design-led and largely university-agnostic; they deserve their own spec and should not bloat the groundable engine.

## 8. Success criteria

- For a given university + subject list, the engine emits a per-subject model recommendation per phase, each tuning line traceable to that university's own data.
- Runs on the same trigger as the unconstrained view; never appears in or alters the grounded plan.
- Subject-nature bucketing is correct (build vs skills vs light) for the MRV and CDU subject sets.
- Reproducible: the same university + subjects yields the same model/tuning recommendations (signals come from queries/views, not model guesswork).
