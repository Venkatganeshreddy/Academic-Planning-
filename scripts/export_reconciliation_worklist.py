#!/usr/bin/env python3
"""Export the course-reconciliation worklist for the curriculum team.

course_plan_vs_actual leaves some courses unmatched between the designed plan and
delivery because course_crosswalk / course_alias.csv don't yet link the two names
(gaps), or link the wrong ones (over-merges). Only the curriculum team can say which
delivered name IS which catalogue course. This writes the open items to a CSV they
fill in; the answers go into data/canonical/course_alias.csv (raw_title,
catalogue_course_title, stack) and the next rebuild reconciles them.

Output: docs/course-reconciliation-worklist.csv
Usage:  python scripts/export_reconciliation_worklist.py
"""
import csv, duckdb, re

con = duckdb.connect("data/aip.duckdb", read_only=True)


def toks(s):
    return set(re.sub(r"[^a-z0-9 ]", " ", (s or "").lower()).split())


rows = con.execute("""
    SELECT university, institute_name, coverage,
           designed_course, delivered_course
    FROM course_plan_vs_actual
    WHERE coverage IN ('planned_not_delivered', 'delivered_not_planned')
      -- don't make the team reconcile orientation/assessment noise (it has no
      -- catalogue course by design); designed side is all real courses already
      AND (coverage = 'planned_not_delivered' OR is_curriculum(delivered_course))
""").fetchall()

# group the two sides per institute so a delivered gap can be suggested against the
# designed gaps sitting next to it (token overlap — a hint, the team decides).
designed, delivered = {}, {}
for uni, inst, cov, dz, dv in rows:
    if cov == "planned_not_delivered":
        designed.setdefault((uni, inst), []).append(dz)
    else:
        delivered.setdefault((uni, inst), []).append(dv)


def suggest(name, candidates):
    t = toks(name)
    best, score = "", 0
    for c in candidates:
        s = len(t & toks(c))
        if s > score:
            best, score = c, s
    return best if score else ""


out = []
for key in sorted(set(designed) | set(delivered)):
    uni, inst = key
    for dv in sorted(delivered.get(key, [])):
        out.append([uni, inst, "DELIVERED (no designed match)", dv,
                    suggest(dv, designed.get(key, [])), ""])
    for dz in sorted(designed.get(key, [])):
        out.append([uni, inst, "DESIGNED (never delivered?)", dz,
                    suggest(dz, delivered.get(key, [])), ""])

path = "docs/course-reconciliation-worklist.csv"
with open(path, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["university", "institute", "side", "course_name_as_it_appears",
                "our_best_guess_match", "CORRECT_catalogue_course_FILL_ME"])
    w.writerows(out)

print(f"{len(out)} rows -> {path}")
print(f"  {sum(1 for r in out if r[2].startswith('DELIVERED'))} delivered gaps, "
      f"{sum(1 for r in out if r[2].startswith('DESIGNED'))} designed gaps")
