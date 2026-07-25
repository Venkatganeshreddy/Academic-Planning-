#!/usr/bin/env python3
"""Flatten the GRIT contest export -> data/canonical/grit/.

Source: the assessment-platform booking export (one row per student per contest
attempt) in data/raw/grit/. It is the ONLY GRIT export with identity: it carries
`niat_id` and `college_name`, and college_name matches universities.institute_name
verbatim for all 16 partner colleges — so GRIT joins to the rest of the store with
no crosswalk.

NOT ingested: the newer GRIT-app exports (grit_attempts_results.csv,
grit_feedback.csv). Their niat_id / name / email columns are 100% NULL, so they
join to no college, no course and no student. Held back until the platform team
re-exports them with identity populated.

Also emits grit_skill_subject.csv — the GRIT skill -> delivered Year-1 subject
reverse index, transcribed from docs/grit-skill-course-map.md (that doc is the
source of truth; this is the queryable copy). It is what lets a delivered subject's
performance be compared against the GRIT outcome it is supposed to build.

Usage: python scripts/build_grit.py
"""
import csv, glob, os, sys

import duckdb

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

RAW_DIR = "data/raw/grit"
OUT_DIR = "data/canonical/grit"

# Dropped on purpose: report/assessment links and screenshot URLs (megabytes of
# signed S3 URLs, no analytical value), ip_addresses (PII, and the repo deploys to
# third-party infra), assessment_tag_str (redundant with specific_tag), and the
# override/access-time columns nobody asks about. niat_id is the student key and is
# pseudonymous — there is no name or email column in this export at all.
SELECT = """
    booking_id,
    niat_id,
    college_name,
    skill,
    level,
    assessment_title,
    specific_tag                                  AS contest_tag,
    -- "March 26, 2026, 4:30 PM" -> a real timestamp. try_ because a no-show has no
    -- start/end time at all, and strptime would abort the whole COPY on the first one.
    try_strptime(assessment_start_datetime,     '%B %d, %Y, %-I:%M %p')::DATE AS contest_date,
    try_strptime(user_assessment_start_datetime, '%B %d, %Y, %-I:%M %p')      AS started_at,
    try_strptime(user_assessment_end_datetime,   '%B %d, %Y, %-I:%M %p')      AS ended_at,
    TRY_CAST(assessment_duration_in_mins AS DOUBLE)          AS duration_mins,
    TRY_CAST(user_assessment_time_spent_in_mins AS DOUBLE)   AS time_spent_mins,
    TRY_CAST(assessment_actual_score AS DOUBLE)              AS max_score,
    TRY_CAST(user_assessment_score AS DOUBLE)                AS score,
    TRY_CAST(user_assessment_score_percentage AS DOUBLE)     AS score_pct,
    upper(trim(badge))                                       AS badge,
    qr_attendance_status                                     AS attendance_status,
    is_disqualified_attempt                                  AS is_disqualified,
    is_cancelled_attempt                                     AS is_cancelled,
    aggregated_section_attempt_end_reasons                   AS end_reason,
    TRY_CAST(face_not_detected_count AS BIGINT)              AS face_not_detected,
    TRY_CAST(inactive_warning_raised_count AS BIGINT)        AS inactive_warnings,
    TRY_CAST(noise_detected_count AS BIGINT)                 AS noise_detected
"""

# GRIT skill -> the delivered Year-1 subjects that build it. Verbatim from
# docs/grit-skill-course-map.md "Delivered Year-1 subject -> GRIT skill" (all 22
# student_performance.subject names). Edit the doc first, then this list.
SKILL_SUBJECT = [
    ("Computational Thinking",            "Programming Foundations"),
    ("Computational Thinking",            "NIAT - DSA"),
    ("Computational Thinking",            "Math For Computer Science"),
    ("Applied Gen AI Development",        "Generative AI"),
    ("Applied Gen AI Development",        "Building LLM Applications"),
    ("UI Engineering",                    "Build Your Own Static Website"),
    ("UI Engineering",                    "Build Your Own Responsive Website"),
    ("UI Engineering",                    "Modern Responsive Web Design"),
    ("UI Engineering",                    "JS Essentials"),
    ("UI Engineering",                    "Introduction to React JS"),
    ("UI Engineering",                    "Build Your Own Dynamic Web Application"),
    ("Server-Side Engineering",           "Building Rest APIs with Flask"),
    ("Server-Side Engineering",           "Node JS"),
    ("Server-Side Engineering",           "MongoDB"),
    ("SQL",                               "Introduction to Databases"),
    ("SQL",                               "DBMS Fundamentals"),
    ("Quantitative Reasoning",            "Quantitative Aptitude"),
    ("Quantitative Reasoning",            "Numerical Ability"),
    ("Quantitative Reasoning",            "NUMERICAL ABILITY AND REASONING SKILLS FOR ENGINEERS"),
    ("Critical Thinking & Communication", "Communicative English Foundation- I"),
    ("Critical Thinking & Communication", "English Course"),
    ("Critical Thinking & Communication", "Communicative English Advanced"),
]


# Score bands, from grit-programme.md §9. A skill clears at Silver, and the Silver bar is
# NOT the same everywhere — Critical Thinking L1 clears at 75%, Server-Side L1 at 90% — so
# raw clear rates are not comparable across skills without these. Verified against the
# export: for every skill x level the observed Silver/Gold boundary matches §9 exactly
# (tests/test_db.py re-checks it, so a band drifting out of date fails loudly).
# Server-Side L2 is "TBU" in §9 and has no attempts yet — deliberately absent, and the
# views LEFT JOIN so a missing band shows as NULL rather than dropping the row.
#                      skill                            level  silver  gold   pattern            mins
BANDS = [
    ("Computational Thinking",            "L1",  83.33, 100.0, "Coding",            90),
    ("Computational Thinking",            "L2",  75.0,  100.0, "Coding",            90),
    ("UI Engineering",                    "L1",  70.0,   85.0, "MCQs + Coding",     90),
    ("UI Engineering",                    "L2",  80.0,   90.0, "MCQs + IDE Coding", 90),
    ("CS Fundamentals",                   "L1",  85.0,   90.0, "MCQs",              40),
    ("CS Fundamentals",                   "L2",  85.0,   90.0, "MCQs",              60),
    ("Applied Gen AI Development",        "L1",  80.0,   90.0, "MCQs",              45),
    ("Applied Gen AI Development",        "L2",  80.0,   90.0, "MCQs",              45),
    ("Critical Thinking & Communication", "L1",  75.0,   95.0, "MCQs",              40),
    ("Critical Thinking & Communication", "L2",  80.0,   90.0, "MCQ",               30),
    ("Server-Side Engineering",           "L1",  90.0,   95.0, "MCQs + Coding",     90),
    ("Quantitative Reasoning",            "L1",  75.0,   90.0, "MCQs",              30),
    ("Quantitative Reasoning",            "L2",  80.0,   95.0, "MCQ",               40),
    ("SQL",                               "L1",  85.0,   90.0, "MCQs + Coding",     90),
    ("SQL",                               "L2",  80.0,   90.0, "MCQs + Coding",     90),
    ("DS & ML",                           "L1",  85.0,   90.0, "MCQs + Coding",     90),
    ("Physical AI",                       "L1",  70.0,   85.0, "MCQs + Coding",     90),
]


def _write_csv(name, header, rows):
    with open(f"{OUT_DIR}/{name}", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def build():
    os.makedirs(OUT_DIR, exist_ok=True)
    src = sorted(glob.glob(f"{RAW_DIR}/*.csv"))
    if not src:
        sys.exit(f"no GRIT export found in {RAW_DIR}/ — drop the booking export there")

    con = duckdb.connect()
    files = "[" + ", ".join(f"'{p.replace(os.sep, '/')}'" for p in src) + "]"
    # sample_size=-1: the proctoring columns are empty for thousands of rows before the
    # first value, so a sampled sniff types them as NULL and silently drops the counts.
    con.execute(f"CREATE VIEW raw AS SELECT * FROM read_csv_auto({files}, sample_size=-1, all_varchar=true)")

    # parquet, not csv: 49k rows x 24 cols is 14 MB as text and 1 MB compressed, and
    # load_duckdb.py already globs parquet alongside csv. It also keeps the real types
    # (the csv path forces all_varchar), so score_pct arrives as a number.
    out = f"{OUT_DIR}/grit_attempts.parquet"
    con.execute(f"""COPY (
        SELECT {SELECT} FROM raw
        WHERE booking_id IS NOT NULL
        ORDER BY contest_date, skill, level, niat_id
    ) TO '{out}' (FORMAT PARQUET, COMPRESSION ZSTD)""")

    _write_csv("grit_skill_subject.csv", ["grit_skill", "subject"], SKILL_SUBJECT)
    _write_csv("grit_score_bands.csv",
               ["skill", "level", "silver_min", "gold_min", "pattern", "duration_mins"], BANDS)

    n, students, colleges = con.execute(
        f"SELECT count(*), count(DISTINCT niat_id), count(DISTINCT college_name) "
        f"FROM read_parquet('{out}')").fetchone()
    print(f"=== grit ===\n  grit_attempts.parquet: {n} rows, {students} students, {colleges} colleges "
          f"({os.path.getsize(out)/1e6:.1f} MB)")
    print(f"  grit_skill_subject.csv: {len(SKILL_SUBJECT)} rows")
    print(f"  grit_score_bands.csv: {len(BANDS)} rows")

    # Loud about what will NOT join, rather than letting it show up as a silent hole.
    unmatched = con.execute(f"""
        SELECT coalesce(college_name, '(blank)') AS college, count(*) AS n
        FROM read_parquet('{out}')
        WHERE college_name IS NULL
           OR college_name NOT IN (SELECT institute_name
                                   FROM read_csv_auto('data/canonical/planning/standards/universities.csv'))
        GROUP BY 1 ORDER BY 2 DESC""").fetchall()
    if unmatched:
        print("  colleges with no academic data (GRIT-only, excluded from joins):")
        for c, k in unmatched:
            print(f"    {c}: {k} rows")
    con.close()


if __name__ == "__main__":
    build()
