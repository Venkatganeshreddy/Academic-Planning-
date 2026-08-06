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
        -- one row per delivered session (the schedule table repeats a session once per
        -- content-resource; keep a single row so counts aren't ~3.5x inflated)
        QUALIFY row_number() OVER (
            PARTITION BY s.session_id, s.section_name, s.session_start_datetime
            ORDER BY s.session_status) = 1
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
WITH supported_university_roster AS (
    SELECT DISTINCT
        institute_name AS source_institute_name,
        institute_id,
        batch_id,
        batch_name,
        section_id,
        section_name,
        user_id,
        student_name,
        college_roll_no,
        institute_name AS university_name
    FROM `kossip-helpers.content_and_learning_analytics_ai_workspace.niat_and_intensive_offline_users_details`
    WHERE institute_name IN (
        'A Dy Patil University','AMET','Annamacharya University','Aurora University',
        'Chaitanya Deemed-to-be University','Chalapathy (CIET)','Chalapathy (CITY)','Crescent University',
        'Malla Reddy Vishwavidyapeeth','NIAT Chevella','NRI','NSRIT University','Noida International University',
        'S-VYASA','Sanjay Ghodawat University','Takshasila University','Vivekananda global University','Yenapoya University'
    )
    AND user_id IS NOT NULL
    AND section_id IS NOT NULL
),
section_students AS (
    SELECT university_name, source_institute_name, institute_id, batch_id, batch_name, section_id, section_name,
        COUNT(DISTINCT user_id) AS students_in_section
    FROM supported_university_roster GROUP BY 1,2,3,4,5,6,7
),
semester_windows AS (
    SELECT DISTINCT section_id, batch_id, semester_id, semester_title AS semester, semester_start_date, semester_end_date
    FROM `kossip-helpers.content_and_learning_analytics_ai_workspace.curriculum_ops_semester_subject_wise_portal_course_details`
    WHERE section_id IS NOT NULL AND semester_start_date IS NOT NULL AND semester_end_date IS NOT NULL
),
semester_courses AS (
    SELECT DISTINCT section_id, batch_id, semester_id, portal_course_id AS course_id, sem_course_title AS subject
    FROM `kossip-helpers.content_and_learning_analytics_ai_workspace.curriculum_ops_semester_subject_wise_portal_course_details`
    WHERE section_id IS NOT NULL AND portal_course_id IS NOT NULL
),
content_hierarchy AS (
    SELECT unit_id, course_id, course_title AS course_name
    FROM `kossip-helpers.content_and_learning_analytics_ai_workspace.content_all_products_unit_wise_content_hierarchy_details`
    WHERE unit_id IS NOT NULL
    QUALIFY ROW_NUMBER() OVER (PARTITION BY unit_id ORDER BY is_primary DESC, is_primary_course DESC, is_primary_topic DESC, is_primary_program DESC, available_status DESC, course_order, topic_order, unit_order) = 1
),
practice_schedule AS (
    SELECT DISTINCT
        s.session_section_id, s.session_date, s.session_start_datetime, s.content_unlock_datetime,
        r.university_name, r.source_institute_name, s.batch_id, s.batch_name, s.section_id, s.section_name,
        sw.semester_id, sw.semester, sw.semester_start_date, sw.semester_end_date, ch.course_id,
        COALESCE(ch.course_name, sc.subject, 'Unmapped course') AS course_name,
        COALESCE(sc.subject, ch.course_name, 'Unmapped subject') AS subject,
        s.resource_id AS unit_id, s.resource_title AS unit_title
    FROM `kossip-helpers.content_and_learning_analytics_ai_workspace.niat_and_intensive_offline_section_wise_daily_learning_schedule_details` AS s
    INNER JOIN section_students AS r ON s.batch_id = r.batch_id AND s.section_id = r.section_id
    LEFT JOIN semester_windows AS sw ON s.section_id = sw.section_id AND s.batch_id = sw.batch_id AND s.session_date BETWEEN sw.semester_start_date AND sw.semester_end_date
    LEFT JOIN content_hierarchy AS ch ON s.resource_id = ch.unit_id
    LEFT JOIN semester_courses AS sc ON s.section_id = sc.section_id AND s.batch_id = sc.batch_id AND COALESCE(sw.semester_id,'') = COALESCE(sc.semester_id,'') AND ch.course_id = sc.course_id
    WHERE s.resource_id IS NOT NULL AND s.session_type = 'PRACTICE'
),
scheduled_mcq AS (
    SELECT ps.*, COALESCE(MAX(e.total_no_of_questions), COUNT(DISTINCT q.question_id)) AS total_questions
    FROM practice_schedule AS ps
    INNER JOIN `kossip-helpers.content_and_learning_analytics_ai_workspace.content_exam_units_details` AS e ON ps.unit_id = e.exam_id
    INNER JOIN `kossip-helpers.content_and_learning_analytics_ai_workspace.content_exam_and_practice_units_question_details` AS q ON ps.unit_id = q.exam_id
    WHERE q.question_type IN ('MULTIPLE_CHOICE','MORE_THAN_ONE_MULTIPLE_CHOICE','CODE_ANALYSIS_MULTIPLE_CHOICE','CODE_ANALYSIS_MORE_THAN_ONE_MULTIPLE_CHOICE')
    GROUP BY 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19
),
scheduled_coding AS (
    SELECT ps.*, COUNT(DISTINCT q.question_id) AS total_questions
    FROM practice_schedule AS ps
    INNER JOIN `kossip-helpers.content_and_learning_analytics_ai_workspace.content_question_set_units_questions_details` AS q ON ps.unit_id = q.question_set_id
    WHERE q.question_type IN ('CODING','SQL_CODING','HTML_CODING','IDE_BASED_CODING','INTERACTIVE_BUILDER_TEXTUAL')
    GROUP BY 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19
),
mcq_attendance AS (
    SELECT sm.university_name, sm.semester_id, sm.semester, sm.section_id, sm.course_id, sm.course_name, sm.subject,
        COUNT(DISTINCT a.user_id) AS mcq_attendance_students
    FROM scheduled_mcq AS sm
    INNER JOIN supported_university_roster AS r ON sm.batch_id = r.batch_id AND sm.section_id = r.section_id
    INNER JOIN `kossip-helpers.content_and_learning_analytics_ai_workspace.all_users_exam_or_practice_units_attempts_details` AS a
        ON sm.unit_id = a.exam_id AND r.user_id = a.user_id AND a.examattempt_start_datetime >= COALESCE(sm.content_unlock_datetime, sm.session_start_datetime)
    GROUP BY 1,2,3,4,5,6,7
),
mcq_attempts AS (
    SELECT sm.university_name, sm.semester_id, sm.semester, sm.section_id, sm.course_id, sm.course_name, sm.subject,
        COUNT(DISTINCT IF(a.exam_question_completion_status='ANSWERED', CONCAT(a.user_id,'|',sm.session_section_id,'|',a.question_id), NULL)) AS mcq_actual_attempts,
        COUNT(DISTINCT IF(a.exam_question_completion_status='ANSWERED' AND a.exam_question_evaluation_result='CORRECT', CONCAT(a.user_id,'|',sm.session_section_id,'|',a.question_id), NULL)) AS mcq_correct_answers
    FROM scheduled_mcq AS sm
    INNER JOIN supported_university_roster AS r ON sm.batch_id = r.batch_id AND sm.section_id = r.section_id
    INNER JOIN `kossip-helpers.content_and_learning_analytics_ai_workspace.curriculum_ops_exam_practice_question_attempt_details` AS a
        ON sm.unit_id = a.exam_id AND r.user_id = a.user_id AND a.derived_unit_type='MCQ_PRACTICE' AND a.examattempt_start_datetime >= COALESCE(sm.content_unlock_datetime, sm.session_start_datetime)
    GROUP BY 1,2,3,4,5,6,7
),
coding_open_events AS (
    SELECT DISTINCT sc.university_name, sc.semester_id, sc.semester, sc.section_id, sc.course_id, sc.course_name, sc.subject, c.user_id
    FROM scheduled_coding AS sc
    INNER JOIN supported_university_roster AS r ON sc.batch_id = r.batch_id AND sc.section_id = r.section_id
    INNER JOIN `kossip-helpers.content_and_learning_analytics_ai_workspace.all_users_resource_wise_completion_details` AS c
        ON sc.unit_id = c.resource_id AND r.user_id = c.user_id AND c.last_progress_datetime >= COALESCE(sc.content_unlock_datetime, sc.session_start_datetime)
    UNION DISTINCT
    SELECT DISTINCT sc.university_name, sc.semester_id, sc.semester, sc.section_id, sc.course_id, sc.course_name, sc.subject, t.user_id
    FROM scheduled_coding AS sc
    INNER JOIN supported_university_roster AS r ON sc.batch_id = r.batch_id AND sc.section_id = r.section_id
    INNER JOIN `kossip-helpers.content_and_learning_analytics_ai_workspace.all_users_day_wise_and_unit_wise_timespent_from_cloudwatch_log` AS t
        ON sc.unit_id = t.unit_id AND r.user_id = t.user_id AND t.date >= DATE(COALESCE(sc.content_unlock_datetime, sc.session_start_datetime)) AND t.total_time_spent_in_mins > 0
),
coding_attendance AS (
    SELECT university_name, semester_id, semester, section_id, course_id, course_name, subject,
        COUNT(DISTINCT user_id) AS coding_attendance_students
    FROM coding_open_events GROUP BY 1,2,3,4,5,6,7
),
coding_attempts AS (
    SELECT sc.university_name, sc.semester_id, sc.semester, sc.section_id, sc.course_id, sc.course_name, sc.subject,
        COUNT(DISTINCT IF(q.question_start_datetime IS NOT NULL, CONCAT(q.user_id,'|',sc.session_section_id,'|',q.question_id), NULL)) AS coding_actual_attempts,
        COUNT(DISTINCT IF(q.first_correct_attempt_submission_datetime IS NOT NULL OR q.best_score_attempt_evaluation_result='CORRECT', CONCAT(q.user_id,'|',sc.session_section_id,'|',q.question_id), NULL)) AS coding_completions
    FROM scheduled_coding AS sc
    INNER JOIN supported_university_roster AS r ON sc.batch_id = r.batch_id AND sc.section_id = r.section_id
    INNER JOIN `kossip-helpers.content_and_learning_analytics_ai_workspace.all_users_question_wise_responses_summary_details_for_question_set_units` AS q
        ON sc.unit_id = q.question_set_id AND r.user_id = q.user_id AND q.question_start_datetime >= COALESCE(sc.content_unlock_datetime, sc.session_start_datetime)
        AND q.question_type IN ('CODING','SQL_CODING','HTML_CODING','IDE_BASED_CODING','INTERACTIVE_BUILDER_TEXTUAL')
    GROUP BY 1,2,3,4,5,6,7
),
mcq_rollup AS (
    SELECT university_name, semester_id, semester, section_id, course_id, course_name, subject,
        COUNT(DISTINCT session_section_id) AS scheduled_mcq_practices, SUM(total_questions) AS total_mcq_questions
    FROM scheduled_mcq GROUP BY 1,2,3,4,5,6,7
),
coding_rollup AS (
    SELECT university_name, semester_id, semester, section_id, course_id, course_name, subject,
        COUNT(DISTINCT session_section_id) AS scheduled_coding_practices, SUM(total_questions) AS total_coding_problems
    FROM scheduled_coding GROUP BY 1,2,3,4,5,6,7
),
section_semester_course_base AS (
    SELECT DISTINCT ps.university_name, ps.source_institute_name, ps.batch_id, ps.batch_name, ps.section_id, ps.section_name,
        ps.semester_id, COALESCE(ps.semester,'Unmapped semester') AS semester, ps.semester_start_date, ps.semester_end_date,
        COALESCE(ps.course_id,'Unmapped course id') AS course_id, COALESCE(ps.course_name,'Unmapped course') AS course_name,
        COALESCE(ps.subject,'Unmapped subject') AS subject, ss.students_in_section
    FROM practice_schedule AS ps
    INNER JOIN section_students AS ss ON ps.batch_id = ss.batch_id AND ps.section_id = ss.section_id
),
final_report AS (
    SELECT
        b.source_institute_name, b.semester, b.subject, b.course_id, b.course_name, b.batch_name, b.section_name, b.section_id,
        b.students_in_section,
        COUNT(DISTINCT b.section_id) OVER (PARTITION BY b.university_name, b.semester) AS num_sections_in_semester,
        COALESCE(mr.scheduled_mcq_practices,0) AS scheduled_mcq_practices,
        COALESCE(ma.mcq_attendance_students,0) AS mcq_attendance_students,
        IFNULL(ROUND(100*SAFE_DIVIDE(COALESCE(ma.mcq_attendance_students,0), b.students_in_section),2),0) AS mcq_attendance_pct,
        COALESCE(mr.total_mcq_questions,0) AS total_mcq_questions,
        COALESCE(mqa.mcq_actual_attempts,0) AS mcq_actual_attempts,
        b.students_in_section * COALESCE(mr.total_mcq_questions,0) AS mcq_expected_attempts,
        IFNULL(ROUND(100*SAFE_DIVIDE(COALESCE(mqa.mcq_actual_attempts,0), b.students_in_section*COALESCE(mr.total_mcq_questions,0)),2),0) AS mcq_attempt_pct,
        COALESCE(mqa.mcq_correct_answers,0) AS mcq_correct_answers,
        IFNULL(ROUND(100*SAFE_DIVIDE(COALESCE(mqa.mcq_correct_answers,0), COALESCE(mqa.mcq_actual_attempts,0)),2),0) AS mcq_accuracy_pct,
        COALESCE(cr.scheduled_coding_practices,0) AS scheduled_coding_practices,
        COALESCE(ca.coding_attendance_students,0) AS coding_attendance_students,
        IFNULL(ROUND(100*SAFE_DIVIDE(COALESCE(ca.coding_attendance_students,0), b.students_in_section),2),0) AS coding_attendance_pct,
        COALESCE(cr.total_coding_problems,0) AS total_coding_problems,
        COALESCE(cqa.coding_actual_attempts,0) AS coding_actual_attempts,
        b.students_in_section * COALESCE(cr.total_coding_problems,0) AS coding_expected_attempts,
        IFNULL(ROUND(100*SAFE_DIVIDE(COALESCE(cqa.coding_actual_attempts,0), b.students_in_section*COALESCE(cr.total_coding_problems,0)),2),0) AS coding_attempt_pct,
        COALESCE(cqa.coding_completions,0) AS coding_completions,
        IFNULL(ROUND(100*SAFE_DIVIDE(COALESCE(cqa.coding_completions,0), COALESCE(cqa.coding_actual_attempts,0)),2),0) AS coding_completion_pct
    FROM section_semester_course_base AS b
    LEFT JOIN mcq_rollup AS mr ON b.university_name=mr.university_name AND COALESCE(b.semester_id,'')=COALESCE(mr.semester_id,'') AND b.section_id=mr.section_id AND b.course_id=COALESCE(mr.course_id,'Unmapped course id') AND b.course_name=COALESCE(mr.course_name,'Unmapped course') AND b.subject=COALESCE(mr.subject,'Unmapped subject')
    LEFT JOIN mcq_attendance AS ma ON b.university_name=ma.university_name AND COALESCE(b.semester_id,'')=COALESCE(ma.semester_id,'') AND b.section_id=ma.section_id AND b.course_id=COALESCE(ma.course_id,'Unmapped course id') AND b.course_name=COALESCE(ma.course_name,'Unmapped course') AND b.subject=COALESCE(ma.subject,'Unmapped subject')
    LEFT JOIN mcq_attempts AS mqa ON b.university_name=mqa.university_name AND COALESCE(b.semester_id,'')=COALESCE(mqa.semester_id,'') AND b.section_id=mqa.section_id AND b.course_id=COALESCE(mqa.course_id,'Unmapped course id') AND b.course_name=COALESCE(mqa.course_name,'Unmapped course') AND b.subject=COALESCE(mqa.subject,'Unmapped subject')
    LEFT JOIN coding_rollup AS cr ON b.university_name=cr.university_name AND COALESCE(b.semester_id,'')=COALESCE(cr.semester_id,'') AND b.section_id=cr.section_id AND b.course_id=COALESCE(cr.course_id,'Unmapped course id') AND b.course_name=COALESCE(cr.course_name,'Unmapped course') AND b.subject=COALESCE(cr.subject,'Unmapped subject')
    LEFT JOIN coding_attendance AS ca ON b.university_name=ca.university_name AND COALESCE(b.semester_id,'')=COALESCE(ca.semester_id,'') AND b.section_id=ca.section_id AND b.course_id=COALESCE(ca.course_id,'Unmapped course id') AND b.course_name=COALESCE(ca.course_name,'Unmapped course') AND b.subject=COALESCE(ca.subject,'Unmapped subject')
    LEFT JOIN coding_attempts AS cqa ON b.university_name=cqa.university_name AND COALESCE(b.semester_id,'')=COALESCE(cqa.semester_id,'') AND b.section_id=cqa.section_id AND b.course_id=COALESCE(cqa.course_id,'Unmapped course id') AND b.course_name=COALESCE(cqa.course_name,'Unmapped course') AND b.subject=COALESCE(cqa.subject,'Unmapped subject')
)
SELECT
    source_institute_name AS institute_name, source_institute_name AS university, semester, subject, course_id,
    batch_name AS batch, section_name AS section, num_sections_in_semester AS num_sections, students_in_section AS students,
    scheduled_mcq_practices, mcq_attendance_students AS mcq_attendance, mcq_attendance_pct, total_mcq_questions,
    mcq_actual_attempts AS mcq_attempts, mcq_expected_attempts, mcq_attempt_pct, mcq_correct_answers AS mcq_correct, mcq_accuracy_pct,
    scheduled_coding_practices, coding_attendance_students AS coding_attendance, coding_attendance_pct, total_coding_problems,
    coding_actual_attempts AS coding_attempts, coding_expected_attempts, coding_attempt_pct, coding_completions, coding_completion_pct
FROM final_report
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
