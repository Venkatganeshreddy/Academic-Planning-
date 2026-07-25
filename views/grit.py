"""GRIT page — job-readiness contests: who cleared what, and did delivery build it.

Three questions, one per tab:
  Readiness   — which colleges cleared which GRIT skill/level (L1 = the Year-1 benchmark)
  Delivery ↔ GRIT — the contest outcome next to the delivery meant to build that skill
  Contest ops — turnout, no-shows and proctoring flags per contest

Reads grit_best / grit_readiness / grit_vs_delivery (built in scripts/load_duckdb.py);
the raw grit_attempts table is only used for the ops tab, where a no-show IS the finding.
GRIT itself stays reference context — see docs/grit-programme.md and
docs/grit-skill-course-map.md for the programme and the skill→course linkage.
"""
import streamlit as st

from aip import dashboard

# §9 of grit-programme.md sets a DIFFERENT Silver threshold per skill (Critical Thinking
# L1 clears at 75%, Server-Side at 90%), so cleared % cannot be ranked across skills.
# `Points from clearing` (score − that skill's own Silver bar) can. Both are offered;
# the caption says which question each answers.
MEASURES = {
    "Cleared %": ("cleared_pct",
                  "Share of enrolled students who reached Gold or Silver. Comparable "
                  "**between colleges** — but **not between skills**, because each skill "
                  "has its own pass mark (Critical Thinking clears at 75%, Server-Side at 90%)."),
    "Points from clearing": ("avg_margin_to_silver",
                             "Average distance from that skill's **own** Silver bar, for "
                             "students who sat it. −5 means five points short, in every "
                             "skill — so this **is** comparable across skills. Positive "
                             "means the average student cleared."),
}

# Skills are stored upper-case. str.title() alone produces "Cs Fundamentals" / "Ds & Ml"
# / "Sql", so the acronyms are spelled out; anything new falls back to title case.
SKILL_NAMES = {"APPLIED GEN AI DEVELOPMENT": "Applied Gen AI Development",
               "CS FUNDAMENTALS": "CS Fundamentals",
               "DS & ML": "DS & ML",
               "SQL": "SQL",
               "UI ENGINEERING": "UI Engineering"}


def pretty(skill):
    return SKILL_NAMES.get(skill, str(skill).title())


def _levels(con):
    return [r[0] for r in con.execute(
        "SELECT DISTINCT level FROM grit_readiness ORDER BY 1").fetchall()]


def render():
    st.title("🏅 GRIT")
    st.caption("Job-readiness contests. One row per student per skill per level — best "
               "attempt only, which is GRIT's own rule (unlimited attempts, highest counts).")

    con = dashboard.conn()
    try:
        tab_ready, tab_delivery, tab_ops = st.tabs(
            ["Readiness", "Delivery ↔ GRIT", "Contest ops"])

        with tab_ready:
            _readiness(con)
        with tab_delivery:
            _delivery(con)
        with tab_ops:
            _ops(con)
    finally:
        con.close()


def _readiness(con):
    lvl = st.radio("Level", _levels(con), horizontal=True, key="grit_level",
                   help="L1 is the Year-1 readiness benchmark — every student is meant "
                        "to clear all required L1 by the end of Year 1.")

    k = con.execute("""SELECT count(DISTINCT niat_id), count(*),
               round(100.0 * count(*) FILTER (WHERE attempted) / count(*), 1),
               round(100.0 * count(*) FILTER (WHERE cleared) / count(*), 1)
        FROM grit_best WHERE level = ?""", [lvl]).fetchone()
    c = st.columns(4)
    c[0].metric("Students", f"{k[0]:,}")
    c[1].metric("Student × skill entries", f"{k[1]:,}")
    c[2].metric("Sat the contest", f"{k[2]}%")
    c[3].metric("Cleared (Gold/Silver)", f"{k[3]}%")

    st.subheader(f"{lvl} — college × skill")
    measure = st.radio("Measure", list(MEASURES), horizontal=True, key="grit_measure")
    col, note = MEASURES[measure]

    df = con.execute(f"""SELECT coalesce(institute_name, college_name) AS college,
                   skill, {col} AS v
            FROM grit_readiness
            WHERE level = ? AND college_name IS NOT NULL
              AND college_name NOT IN ('Program_Ops')
            """, [lvl]).df()
    if df.empty:
        st.info(f"No {lvl} results.")
        return
    matrix = df.pivot(index="college", columns="skill", values="v")
    matrix.columns = [pretty(c) for c in matrix.columns]
    matrix = matrix.reindex(sorted(matrix.columns), axis=1)
    # mean skips blanks on purpose, so this is "how they did on the skills they ran",
    # not an all-skills average — a college that ran 2 contests is not comparable to one
    # that ran 9. Named so nobody reads it as overall readiness.
    matrix["Avg (skills run)"] = matrix.mean(axis=1).round(1)
    matrix = matrix.sort_values("Avg (skills run)", ascending=False).reset_index()
    # ProgressColumn cannot render a negative bar, and the margin is mostly negative.
    cfg = (st.column_config.ProgressColumn(min_value=0, max_value=100, format="%.0f%%")
           if col == "cleared_pct" else st.column_config.NumberColumn(format="%+.1f"))
    st.dataframe(matrix, width="stretch", hide_index=True,
                 column_config={c: cfg for c in matrix.columns if c != "college"})
    st.caption(note + " Blank = that college ran no contest for that skill at this level.")

    st.subheader("Where the drop-off is")
    st.dataframe(con.execute("""
        SELECT r.skill AS "Skill", sum(r.students) AS "Students",
               round(100.0 * sum(r.attempted_students) / sum(r.students), 1) AS "Sat it %",
               round(100.0 * sum(r.cleared_students) / sum(r.students), 1)   AS "Cleared %",
               round(100.0 * sum(r.cleared_students)
                     / nullif(sum(r.attempted_students), 0), 1)            AS "Cleared, of those who sat %",
               max(TRY_CAST(b.silver_min AS DOUBLE))                       AS "Clears at %",
               -- student-weighted, so a college with 8 entrants can't swing the average
               round(sum(r.avg_margin_to_silver * r.attempted_students)
                     / nullif(sum(r.attempted_students), 0), 1)            AS "Points from clearing",
               sum(r.near_miss_students)                                   AS "Within 10 points"
        FROM grit_readiness r
        LEFT JOIN grit_score_bands b ON upper(b.skill) = r.skill AND b.level = r.level
        WHERE r.level = ? GROUP BY 1 ORDER BY 7 DESC
    """, [lvl]).df().assign(Skill=lambda d: d["Skill"].map(pretty)),
        width="stretch", hide_index=True)
    st.caption(
        "Three different problems, three different fixes. A low **Sat it %** is turnout/ops. "
        "A low **Cleared %** next to a high **Clears at %** is a hard pass mark, not weak "
        "students — read **Points from clearing** instead, which is on the same scale for "
        "every skill. **Within 10 points** is the size of the group a targeted intervention "
        "would actually convert.")


def _delivery(con):
    st.subheader("Contest outcome vs. the delivery meant to build it")
    lvl = st.radio("Level", _levels(con), horizontal=True, key="grit_dev_level")
    st.dataframe(con.execute("""
        SELECT institute_name AS "College", skill AS "GRIT skill",
               students AS "Students", cleared_pct AS "Cleared %",
               avg_margin_to_silver AS "Points from clearing",
               near_miss_students AS "Within 10 points",
               subjects_delivered AS "Subjects taught",
               mcq_attempt_pct AS "Practice attempt %",
               mcq_accuracy_pct AS "Practice accuracy %",
               coding_completion_pct AS "Coding completion %"
        FROM grit_vs_delivery WHERE level = ? AND subjects_delivered IS NOT NULL
        ORDER BY avg_margin_to_silver
    """, [lvl]).df().assign(**{"GRIT skill": lambda d: d["GRIT skill"].map(pretty)}),
        width="stretch", hide_index=True)
    st.caption(
        "Bridge: each GRIT skill maps to the Year-1 subjects that build it "
        "(`docs/grit-skill-course-map.md`). **Correlation, not proof** — the subject→skill "
        "assignment is a documented judgement, and practice metrics are per *section* while "
        "GRIT is per *student*, so the two describe the same cohort at different grains. "
        "Rows are missing where a college taught none of the mapped subjects.")


def _ops(con):
    st.subheader("Turnout and conduct, per college")
    st.dataframe(con.execute("""
        SELECT CASE WHEN u.institute_name IS NULL
                    THEN g.college_name || '  (no academic data)'
                    ELSE u.institute_name END                               AS "College",
               count(*)                                                     AS "Bookings",
               count(DISTINCT g.niat_id)                                    AS "Students",
               round(100.0 * count(*) FILTER (WHERE g.badge IN ('NOT ATTEMPTED','YET TO ATTEMPT'))
                     / count(*), 1)                                         AS "No-show %",
               round(100.0 * count(*) FILTER (WHERE lower(g.is_cancelled) = 'yes')
                     / count(*), 1)                                         AS "Cancelled %",
               round(avg(100.0 * g.time_spent_mins / nullif(g.duration_mins, 0)), 1)
                                                                            AS "Time used %",
               count(*) FILTER (WHERE g.face_not_detected > 0)              AS "Face-not-detected",
               count(*) FILTER (WHERE g.inactive_warnings > 0)              AS "Inactivity warnings"
        FROM grit_attempts g
        LEFT JOIN universities u ON u.institute_name = g.college_name
        WHERE g.college_name IS NOT NULL
        GROUP BY 1 ORDER BY 4 DESC
    """).df(), width="stretch", hide_index=True)
    st.caption("Every booking, not just best attempts — a no-show is the finding here. "
               "Colleges flagged *(no academic data)* run GRIT but have no delivery data "
               "in this store, so they appear here and nowhere else.")

    st.subheader("Contests over time")
    st.dataframe(con.execute("""
        SELECT contest_date AS "Date", skill AS "Skill", level AS "Level",
               count(*) AS "Booked", count(DISTINCT college_name) AS "Colleges",
               round(100.0 * count(*) FILTER (WHERE badge IN ('NOT ATTEMPTED','YET TO ATTEMPT'))
                     / count(*), 1) AS "No-show %",
               round(100.0 * count(*) FILTER (WHERE badge IN ('GOLD','SILVER'))
                     / nullif(count(*) FILTER (WHERE badge NOT IN ('NOT ATTEMPTED','YET TO ATTEMPT')), 0), 1)
                     AS "Cleared, of those who sat %"
        FROM grit_attempts GROUP BY 1, 2, 3 ORDER BY 1 DESC, 4 DESC
    """).df().assign(Skill=lambda d: d["Skill"].map(pretty)),
        width="stretch", hide_index=True)
