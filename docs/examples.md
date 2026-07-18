# Worked examples — how a good answer looks

These are the standard the copilot should match: right table, right filter, reasoning
shown, and **length matched to the question**. Study the shape, not the exact numbers.

---

**Q: How many coding questions are there for DSA?**

**159 coding questions** for *Data Structures and Algorithms using C++*.
*From `coding_questions`, filtered to that `course_title`.*

> Why this is good: a lookup gets one line, the number first, the source named. No preamble, no essay, no caveats it doesn't need.

---

**Q: How many sessions did MRV run for Computer Programming?**

**~118 sessions per student** (59 lecture · 46 practice · 13 exam). Across MRV's 5 sections that's 590 scheduled sessions total.
*From `delivered_niat` (institute `Malla Reddy Vishwavidyapeeth`, `is_scheduled = true`), divided by 5 sections — a student sits in one section, so the per-section figure is what matters.*

> Why this is good: uses `delivered_niat` (has `course_title`) not `delivered_sessions`; normalises per section instead of quoting the raw 590; filters out never-scheduled rows; states which table and filter in one line.

---

**Q: Which college had the worst pacing last semester?**

Lead with the single answer (the college + the one number that proves it), then a 3-row table of the contenders, then one sentence on what "pacing" means here (peak week load vs the ~33/week ceiling). Cite `delivered_niat` and `planning_standards`. Stop there — do not turn a comparison into five full diagnoses.

> Why this is good: a comparison question wants a ranked answer, not a report on each option. Depth is earned by the question; a "which is worst" question earns one paragraph, a "design a plan" question earns the full structure.

---

## The rules these examples encode
- **Lead with the answer.** First sentence = the number or the name asked for.
- **Match length to the question.** Lookup → 1-2 lines. Comparison → short + a small table. "Design/diagnose" → the full planning structure. Never pad a small question or truncate a big one.
- **Name the table and filter** in one line, always — it is what lets the reader trust the number.
- **Only the caveats that matter here.** Do not recite every data-quality note on every answer; surface the one that changes *this* number.
- **Answer what was asked.** If they asked "how many", give the count, not a lecture on the course.
