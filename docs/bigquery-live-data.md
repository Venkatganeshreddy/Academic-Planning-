# Live data from BigQuery — mapping & plan

Goal: replace the manual Excel ingestion with a live pull from the NxtWave BigQuery warehouse,
**for all universities**, keeping the app and its DuckDB views unchanged. "Stack knowledge"
(docs → system prompt, planning rules, the designed/HLID plan) stays authored.

Service account + dataset config live in `.streamlit/secrets.toml` (`[gcp_service_account]`, `[bigquery]`).
The dataset holds **41 raw warehouse tables** (documented in the ClickUp "Metabase/hex tables" dictionary).
Our clean tables are **reshaped** from them — not 1:1 renames.

## The linkage keys (the "common ids")

| Key | Meaning | Fixes |
|---|---|---|
| `session_id` | one delivered/planned session | **the known break** — both delivery sides carry it in BQ |
| `section_id` / `section_name` + `institute_name` + `semester` | the section grain | every tab |
| `resource_id` (= our `unit_id`) | session ↔ content unit | Subjects→Content, Courses→Sessions |
| `user_id` / `niat_id` | student | Student Performance, Feedback |
| `sem_course_id` ↔ `portal_course_id` | course crosswalk (semester ↔ NxtWave portal course) | Subjects→Content, Academic Planning |
| `entity_id` | feedback ↔ session/unit | Feedback |

**Known break, fixed:** today `delivered_sessions` has `session_id`+`unit_id` but no instructor/status/course;
`delivered_niat` has instructor/status/course but no `session_id` → they're joined by a fuzzy bridge
(institute + title + start-time) in `session_link`. In BigQuery the schedule table
`niat_and_intensive_offline_section_wise_daily_learning_schedule_details` carries `session_id` **and**
`resource_id` **and** instructor + status together, so the join becomes exact.

## Our table → BigQuery source

| Our table | BigQuery source(s) | Notes |
|---|---|---|
| `delivered_sessions` | `niat_and_intensive_offline_section_wise_daily_learning_schedule_details` | `session_id`, `resource_id`→`unit_id`, `session_name`→`session_title`, type, section, institute, start/end. **semester + course_title** join in via `session_id` → adherence table |
| `delivered_niat` | schedule table (instructor, status, course via join) + `curriculum_ops_niat_2025_users_week_wise_session_completion_adherence_details` | now carries `session_id` too → update `session_link` to exact join |
| `student_performance` (+ `student_perf_by_*`) | `curriculum_ops_niat_2025_users_batch_wise_skill_and_graded_assessment_scores` (core) + `..._quiz_best_attempts_and_completion_details` + `..._unlocked_units_completion_details` + `curriculum_ops_exam_practice_question_attempt_details` | derived/aggregated; link on institute+semester+section+user+course |
| `session_feedback` | `all_users_feedbacks_question_enum_wise_user_answers` (+ `content_feedbacks_entity_wise_question_enums` for the enum meanings) | join to session via `entity_id`; enums → understanding/teaching |
| `course_content`, `coding_questions`, `objective_questions`, `reading_materials` | `content_all_questions_details`, `content_all_resources_details`, `content_all_products_unit_wise_content_hierarchy_details`, `content_learning_resource_set_wise_learning_resource_details` | content library; link via `unit_id`/`resource_id` |
| `subject_tags`, `tag_content_map`, `course_crosswalk` | `curriculum_ops_semester_subject_wise_portal_course_details` (`sem_course_id`↔`portal_course_id`) + content hierarchy | the crosswalk, live |
| `universities` | distinct institutes from `niat_and_intensive_offline_users_details` / schedule table | |
| `instructor_sessions`, `sessions`, `editorials` | schedule table (instructor grain) / content tables | confirm grain |

## Stays as-is (NOT from BigQuery)
- `issues` → Google Sheet (`GOOGLE_SERVICE_ACCOUNT_JSON` + `AIP_SHEET_ID`).
- `designed_course_plan`, `designed_sequence` → authored HLID plan (stack knowledge). The BQ
  `niat_schedule_details_as_per_prod_sequence` is **empty (0 rows)**; planned-vs-actual uses the
  `total_sessions_planned` / `total_sessions_delivered` columns already in the adherence table.

## Practical notes
- **Cost:** the `niat_*` / `curriculum_ops_niat_2025_*` / schedule tables are small (~10 MB/scan). The broad
  `all_users_*` tables are large (26–91 M rows) — **column-prune + filter to our institutes/semester**, never `SELECT *`.
- **Contract:** after each pull, assert `unit_id` non-null, `session_id` **dash-less** (strip dashes if BQ stores them),
  crosswalk resolves, row counts sane, and a known anchor (e.g. MRV persona 62/161/66/15) before shipping the DuckDB.
- **Institute names** in BQ match ours (Aurora, Chaitanya, NRI, …) + extras (Intensive Offline DC, etc.) — filter to our 18.
- **Open semantics to confirm with data team:** instructor *name* source (schedule has `instructor_user_id` + `instructor_name_enum`, not a clean name); feedback `entity_id` grain (= `session_id`?).
