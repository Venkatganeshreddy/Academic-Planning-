# Student View

*Prototype · Student journey layer · v1 spec for product team*

What a cohort student sees daily. The platform already renders content (videos, PPTs, MCQs, coding practice); this layer adds what it lacks — **calendar awareness**: today's plan, gates & skill assessments, revision shields before university exams, and breaks as first-class objects. Mock data anchored to the MRV almanac.

---

## Mockup: `niat.app/today` — Ananya K · Cohort MRV-E1

**Week 11 of 34 · Sem A · Wednesday**
Status chips: `Gates 6/6` ✅ · `Skill assessments 3/3` ✅ · `Mid-2 in 12 days · shield starts in 8` ⚠️

### Week strip
| Mon | Tue | Wed | Thu | Fri | Sat |
|---|---|---|---|---|---|
| done | done | **today** | — | GATE PM | BOS DAY |

### Today's plan
- **AM · 09:00 — React + TypeScript · S10 — Effect Hook & Rules of Hooks**
  Teach + live-code 45 m → continuous lab 2 h 15 · lab task: fetch-on-mount with cleanup
  `▶ session` `⌨ lab task` `✓ classroom quiz`
- **12:00 — Thread — DSA strand · S8: Space Complexity** (+ Python maintenance 15′)
- **PM · 14:00 — DBMS · S11 — CASE Clause & Set Operations**
  Teach 45 m → lab 2 h 15 · lab: report queries on the store schema
  `▶ session` `⌨ SQL lab` `✓ classroom quiz`
- **Evening · optional — Maintenance — Python practice set 6 · 20 min**

### Coming up
- **Fri PM** — Weekly mastery gate — React + DBMS (proctored)
- **Sat** — BOS day — Maths for CSE · Quant Aptitude · English Foundation
- **Tue, wk 12** — Skill assessment — build: typed component with API states
- **Wk 14, Mon** — **Revision shield begins** — no new sessions; university Mid-2 prep + maintenance only
- **Wk 14** — University Mid-2 examinations
- **Wk 15–16** — Sem-A end exams → inter-sem break

### My semester

**Sem A (current, highlighted):**
`Bootcamp` → `Python ‖ Web (wk 2–5)` → `Dasara recess` → `React ‖ DBMS (wk 7–8)` → `🛡 Shield + Mid-1` → **`React ‖ DBMS (wk 10–13) ● you are here`** → `🛡 Shield + Mid-2` → `Exams` → `Inter-sem break`

**Sem B (shown dimmed, upcoming):**
`LLM ‖ Backend` → `Sankranthi recess` → `LLM ‖ Backend` → `🛡 Shield + Mid-1` → `Capstone ‖ Agents` → `🛡 Shield + Mid-2` → `Exams · Demo Day`

*Legend: 🛡 = revision shield (4–5 days, new content frozen) · dark = exams · dotted = breaks · ● = you are here · Sem B shown dimmed*

---

## Prototype → product notes

- **Data sources:** prod sequence (sessions/slots) + university almanac (exams, breaks, shields derived) + gate/assessment results. All three exist today; the join is the new work.
- **Shield behaviour:** platform hides new LEARNING_SET slots during shields and surfaces maintenance pools + university-exam countdown instead — enforcing practice protection in the UI, not just policy.
- **Gate day:** Saturday view swaps to assessment mode (proctored gate + checkpoint lab). Failing a gate pins a catch-up plan to Monday.
- Desktop-first (lab environment), responsive down to mobile for the schedule/status surfaces.
