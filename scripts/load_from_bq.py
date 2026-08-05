"""Pull live data from BigQuery into data/canonical/bq/*.parquet, which scripts/load_duckdb.build()
then picks up unchanged. Creds + dataset come from .streamlit/secrets.toml.

Deps: google-cloud-bigquery, pandas, pyarrow, db-dtypes.
Run:  python scripts/load_from_bq.py                # all configured tables
      python scripts/load_from_bq.py delivered_sessions

ponytail: thin wrapper — the reshape SQL is the only real content; build() and the app are untouched.
GRIT stays on the file path; issues stays on Google Sheets; the designed/HLID plan stays authored.
"""
import os, sys, tomllib

SECRETS = ".streamlit/secrets.toml"
OUT = "data/bq_live"   # separate from data/canonical/ during validation (swap in once verified)

# our 18 universities (BQ institute_name matches ours; extras like 'Intensive Offline DC' are excluded)
INSTITUTES = (
    "('A Dy Patil University','AMET','Annamacharya University','Aurora University',"
    "'Chaitanya Deemed-to-be University','Chalapathy (CIET)','Chalapathy (CITY)','Crescent University',"
    "'Malla Reddy Vishwavidyapeeth','NIAT Chevella','NRI','NSRIT University','Noida International University',"
    "'S-VYASA','Sanjay Ghodawat University','Takshasila University','Vivekananda global University','Yenapoya University')"
)

# our-table -> reshape SQL. {ds} = `project.dataset`, {inst} = institute filter.
# NOTE: exact per-table filters/dedup to match the current DuckDB row counts are STILL BEING FINALISED
#       (the original Excel-ingestion filters aren't recorded in the repo). Validate each against the
#       live app numbers before trusting it. delivered_sessions below is the worked example.
QUERIES = {
    "delivered_sessions": """
        SELECT s.institute_name,
               concat(s.batch_name, '-', s.section_name)      AS batch_section_name,
               a.semester_title                                AS semester,
               replace(s.session_id, '-', '')                 AS session_id,   -- dash-less contract
               s.session_name                                 AS session_title,
               s.session_type,
               s.session_status,                                              -- kept: all statuses
               s.resource_id                                  AS unit_id,
               s.resource_type,
               s.session_start_datetime                       AS start_ts,
               s.session_end_datetime                         AS end_ts
        FROM `{ds}.niat_and_intensive_offline_section_wise_daily_learning_schedule_details` s
        LEFT JOIN (                                            -- dedup: one semester per session_id (avoids 24x fan-out)
               SELECT session_id, ANY_VALUE(semester_title) AS semester_title
               FROM `{ds}.curriculum_ops_niat_2025_users_week_wise_session_completion_adherence_details`
               GROUP BY session_id
        ) a ON a.session_id = s.session_id
        WHERE s.institute_name IN {inst}                       -- all statuses kept (incl. CANCELLED/PENDING)
    """,
    "delivered_niat": """
        SELECT s.institute_name,
               s.batch_name,
               s.section_name,
               a.semester_title                               AS semester,
               a.course_title,
               s.session_name                                 AS session_title,
               s.session_type,
               s.session_status,
               s.instructor_name_enum                         AS instructor_name,
               s.instructor_category,
               a.week_count,
               a.week_status,
               replace(s.session_id, '-', '')                 AS session_id,   -- NEW: exact join, no fuzzy bridge
               s.session_start_datetime                       AS start_ts,
               s.session_end_datetime                         AS end_ts,
               (s.session_status != 'CANCELLED')              AS is_scheduled
        FROM `{ds}.niat_and_intensive_offline_section_wise_daily_learning_schedule_details` s
        LEFT JOIN (
               SELECT session_id,
                      ANY_VALUE(semester_title) AS semester_title,
                      ANY_VALUE(course_title)   AS course_title,
                      ANY_VALUE(week_count)     AS week_count,
                      ANY_VALUE(week_status)    AS week_status
               FROM `{ds}.curriculum_ops_niat_2025_users_week_wise_session_completion_adherence_details`
               GROUP BY session_id
        ) a ON a.session_id = s.session_id
        WHERE s.institute_name IN {inst}
    """,
    "session_feedback": """
        WITH usr AS (   -- user -> institute (feedback table has no institute)
            SELECT user_id, any_value(institute_name) AS institute_name
            FROM `{ds}.niat_and_intensive_offline_users_details` GROUP BY user_id
        ),
        fb AS (         -- per (institute, session): counts + rating averages
            SELECT f.entity_id AS sid_raw, u.institute_name,
                   count(DISTINCT f.feedback_submission_id) AS total_feedbacks,
                   avg(CASE WHEN f.feedback_question_enum='LEARNING_SESSION_UNDERSTANDING_RATING'
                            THEN safe_cast(f.user_answer AS FLOAT64) END) AS session_understanding_rating,
                   avg(CASE WHEN f.feedback_question_enum='LEARNING_SESSION_TEACHING_QUALITY_RATING'
                            THEN safe_cast(f.user_answer AS FLOAT64) END) AS teaching_quality_rating
            FROM `{ds}.all_users_feedbacks_question_enum_wise_user_answers` f
            JOIN usr u ON u.user_id = replace(f.user_id, '-', '')   -- feedback user_id is dashed, roster is not
            WHERE f.feedback_entity_type='NIAT_SESSION' AND u.institute_name IN {inst}
            GROUP BY f.entity_id, u.institute_name
        ),
        sess AS (       -- session_id -> title + unit
            SELECT replace(session_id,'-','') AS sid,
                   any_value(session_name) AS session_title, any_value(resource_id) AS unit_ids
            FROM `{ds}.niat_and_intensive_offline_section_wise_daily_learning_schedule_details`
            GROUP BY replace(session_id,'-','')
        )
        SELECT fb.institute_name, replace(fb.sid_raw,'-','') AS session_id,
               sess.session_title, sess.unit_ids,
               fb.total_feedbacks, fb.session_understanding_rating, fb.teaching_quality_rating,
               CAST(NULL AS STRING) AS positive_feedbacks,   -- sentiment buckets: derived elsewhere, not in BQ
               CAST(NULL AS STRING) AS neutral_feedbacks,
               CAST(NULL AS STRING) AS negative_feedbacks
        FROM fb LEFT JOIN sess ON sess.sid = replace(fb.sid_raw,'-','')
    """,
    "student_performance": """
        WITH sem AS (   -- (institute, section, course) -> semester
            SELECT institute_name, section_name, portal_course_id AS course_id, any_value(semester_title) AS semester
            FROM `{ds}.curriculum_ops_semester_subject_wise_portal_course_details` GROUP BY 1,2,3
        ),
        mcq_meta AS (   -- section-aware MCQ practice metadata (validated)
            SELECT institute_name, section_name, any_value(batch_name) AS batch, course_id,
                   any_value(course_title) AS subject,
                   count(DISTINCT quiz_id) AS scheduled_mcq_practices,
                   count(DISTINCT user_id) AS students,
                   count(DISTINCT IF(quiz_completion_status!='YET TO START', user_id, NULL)) AS mcq_attendance
            FROM `{ds}.curriculum_ops_niat_2025_users_batch_wise_quiz_best_attempts_and_completion_details`
            WHERE derived_unit_type='MCQ_PRACTICE' AND institute_name IN {inst}
            GROUP BY institute_name, section_name, course_id
        ),
        u2s AS (        -- user -> section (complete NIAT roster, for the question-level table)
            SELECT user_id, any_value(institute_name) AS institute_name, any_value(section_name) AS section_name
            FROM `{ds}.curriculum_ops_niat_2025_users_batch_wise_quiz_best_attempts_and_completion_details`
            WHERE institute_name IN {inst} GROUP BY user_id
        ),
        tq AS (         -- total MCQ questions per course
            SELECT course_id, sum(tot) AS total_mcq_questions FROM (
                SELECT course_id, exam_id, any_value(total_no_of_questions) AS tot
                FROM `{ds}.curriculum_ops_exam_practice_question_attempt_details`
                WHERE derived_unit_type='MCQ_PRACTICE' GROUP BY course_id, exam_id
            ) GROUP BY course_id
        ),
        mcq_q AS (      -- question-level attempts/correct (validated)
            SELECT u.institute_name, u.section_name, a.course_id,
                   countif(a.exam_question_completion_status='ANSWERED') AS mcq_attempts,
                   countif(a.exam_question_evaluation_result='CORRECT')   AS mcq_correct
            FROM `{ds}.curriculum_ops_exam_practice_question_attempt_details` a
            JOIN u2s u ON u.user_id=a.user_id
            WHERE a.derived_unit_type='MCQ_PRACTICE'
            GROUP BY u.institute_name, u.section_name, a.course_id
        ),
        cod_meta AS (   -- coding practice scheduled + attendance (question-set units)
            SELECT institute_name, section_name, course_id,
                   count(DISTINCT unit_id) AS scheduled_coding_practices,
                   count(DISTINCT IF(unit_completion_status!='YET_TO_START', user_id, NULL)) AS coding_attendance
            FROM `{ds}.curriculum_ops_niat_2025_users_batch_wise_unlocked_units_completion_details`
            WHERE unit_type='QUESTION_SET' AND institute_name IN {inst}
            GROUP BY institute_name, section_name, course_id
        ),
        qs2c AS (       -- question_set -> course
            SELECT DISTINCT unit_id AS qsid, course_id
            FROM `{ds}.curriculum_ops_niat_2025_users_batch_wise_unlocked_units_completion_details`
            WHERE unit_type='QUESTION_SET' AND institute_name IN {inst}
        ),
        cod_q AS (      -- coding attempts/completions (best-attempt) via summary + user->section + set->course
            SELECT u.institute_name, u.section_name, qc.course_id,
                   count(*) AS coding_attempts,
                   countif(s.best_score_attempt_evaluation_result='CORRECT') AS coding_completions,
                   count(DISTINCT s.question_id) AS total_coding_problems
            FROM `{ds}.all_users_question_wise_responses_summary_details_for_question_set_units` s
            JOIN u2s u   ON u.user_id = s.user_id
            JOIN qs2c qc ON qc.qsid = s.question_set_id
            WHERE s.question_type IN ('CODING','SQL_CODING','HTML_CODING','IDE_BASED_CODING')
            GROUP BY u.institute_name, u.section_name, qc.course_id
        )
        SELECT m.institute_name, m.institute_name AS university,
               coalesce(sem.semester,'Semester 1') AS semester,
               m.subject, m.course_id, m.batch, m.section_name AS section,
               count(*) OVER (PARTITION BY m.institute_name, m.course_id) AS num_sections,
               m.students, m.scheduled_mcq_practices, m.mcq_attendance,
               round(100.0*m.mcq_attendance/nullif(m.students,0),2) AS mcq_attendance_pct,
               tq.total_mcq_questions, q.mcq_attempts,
               m.students*tq.total_mcq_questions AS mcq_expected_attempts,
               round(100.0*q.mcq_attempts/nullif(m.students*tq.total_mcq_questions,0),2) AS mcq_attempt_pct,
               q.mcq_correct, round(100.0*q.mcq_correct/nullif(q.mcq_attempts,0),2) AS mcq_accuracy_pct,
               cm.scheduled_coding_practices, cm.coding_attendance,
               round(100.0*cm.coding_attendance/nullif(m.students,0),2) AS coding_attendance_pct,
               cq.total_coding_problems,
               cq.coding_attempts,
               m.students*cq.total_coding_problems AS coding_expected_attempts,
               round(100.0*cq.coding_attempts/nullif(m.students*cq.total_coding_problems,0),2) AS coding_attempt_pct,
               cq.coding_completions,
               round(100.0*cq.coding_completions/nullif(cq.coding_attempts,0),2) AS coding_completion_pct
        FROM mcq_meta m
        LEFT JOIN mcq_q q  ON q.institute_name=m.institute_name AND q.section_name=m.section_name AND q.course_id=m.course_id
        LEFT JOIN tq       ON tq.course_id=m.course_id
        LEFT JOIN cod_meta cm ON cm.institute_name=m.institute_name AND cm.section_name=m.section_name AND cm.course_id=m.course_id
        LEFT JOIN cod_q cq ON cq.institute_name=m.institute_name AND cq.section_name=m.section_name AND cq.course_id=m.course_id
        LEFT JOIN sem      ON sem.institute_name=m.institute_name AND sem.section_name=m.section_name AND sem.course_id=m.course_id
    """,
    # TODO (same pattern, each needs a validate pass):
    #   course_content, coding_questions, objective_questions, reading_materials,
    #   subject_tags, tag_content_map, course_crosswalk, universities, instructor_sessions, sessions, editorials
}


def _client():
    s = tomllib.load(open(SECRETS, "rb"))
    sa, bq = s["gcp_service_account"], s["bigquery"]
    from google.oauth2 import service_account
    from google.cloud import bigquery
    c = bigquery.Client(credentials=service_account.Credentials.from_service_account_info(sa), project=bq["project"])
    return c, f"{bq['project']}.{bq['dataset']}"


def run(name):
    c, ds = _client()
    job = c.query(QUERIES[name].format(ds=ds, inst=INSTITUTES))
    df = job.to_dataframe()
    os.makedirs(OUT, exist_ok=True)
    df.to_parquet(f"{OUT}/{name}.parquet")
    print(f"{name}: {len(df)} rows, {job.total_bytes_billed/1e6:.1f} MB billed -> {OUT}/{name}.parquet")


if __name__ == "__main__":
    for n in (sys.argv[1:] or QUERIES):
        run(n)
