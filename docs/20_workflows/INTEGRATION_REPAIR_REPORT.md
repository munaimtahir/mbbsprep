# Integration Repair Report

Date: 2026-03-14

## Scope

Focused backend-frontend stabilization pass based on:

- `docs/30_repo/BACKEND_FRONTEND_TRUTH_MAP.md`
- `docs/30_repo/INTEGRATION_GAP_REGISTER.md`
- `docs/30_repo/NAVIGATION_TO_RUNTIME_MAP.md`
- `docs/20_workflows/ACTIVE_INTEGRATION_STATUS.md`

## Repaired Gaps

### GAP-001 — Topic detail drift
- Root cause: template referenced non-existent routes/context (`bookmark_topic`, `add_comment`, `question_stats`, etc.).
- Action taken: rewrote `templates/core/topic_detail.html` against actual `TopicDetailView` context only.
- Tests: `test_topic_detail_renders_with_real_contract`.

### GAP-002 — Contact frontend/backend mismatch
- Root cause: contact template intercepted submit and simulated success while backend expected `ContactForm`.
- Action taken: converted contact page to real server POST flow using `name/email/subject/message`.
- Tests: `test_contact_page_uses_backend_form_contract`.

### GAP-003 — Resources dead JS endpoints
- Root cause: runtime included `resources.js` with calls to non-existent APIs.
- Action taken: removed dead JS include from active resources template; kept server-rendered behavior.
- Tests: `test_resources_and_leaderboard_pages_do_not_load_dead_ajax_scripts`.

### GAP-004 — Leaderboard dead JS endpoints
- Root cause: runtime included `leaderboard.js` with non-existent AJAX routes.
- Action taken: removed dead JS include from active leaderboard template; kept server-rendered behavior.
- Tests: `test_resources_and_leaderboard_pages_do_not_load_dead_ajax_scripts`.

### GAP-005 — Staff bulk MCQ upload schema drift
- Root cause: bulk upload attempted `Option.option_label` (field does not exist) and had contract drift.
- Action taken: aligned upload mapping to `Option(option_text, order, is_correct)` and fixed create/update branch logic.
- Tests: `test_staff_bulk_question_upload_succeeds_with_current_schema`, `test_staff_bulk_question_upload_shows_validation_error_for_bad_columns`.

### GAP-006 — Staff quiz attempts malformed template
- Root cause: duplicated/corrupted template blocks.
- Action taken: replaced with clean truthful placeholder template.
- Tests: `test_staff_quiz_attempts_route_renders_clean_placeholder`.

### GAP-007 — Subject detail zero-topic break risk
- Root cause: quick-start URL always dereferenced `topics.first.pk`.
- Action taken: guarded quick-start CTA and added truthful disabled state when no topics.
- Tests: `test_subject_detail_handles_zero_topics_truthfully`.

### GAP-009 — Staff user export logic drift
- Root cause: stale `completed=True` filter and single-user rows leaking into multi-user export branch.
- Action taken: switched to status-based completion filtering and fixed branch-specific CSV output.
- Tests: `test_user_export_uses_status_based_quiz_completion`.

### GAP-010 — CSRF exemptions on authenticated mutators
- Root cause: active subject/topic AJAX mutators were marked `@csrf_exempt`.
- Action taken: removed CSRF exemptions from subject/topic mutating AJAX views used by active UI.
- Tests: `test_subject_ajax_add_requires_csrf_and_accepts_valid_csrf`.

### GAP-013 — Missing targeted tests
- Action taken: added `tests/automated/test_integration_repair_flows.py` with focused route/contract tests for repaired visible flows.

### GAP-011 — Contact help link
- Root cause: hardcoded `/help/` had no route.
- Action taken: removed dead link from active contact page and replaced quick-help links with real routes.
- Tests: covered through contact page render test.

## Compatibility Fix Applied (Validation Blocker)

- File: `staff/forms/resource_forms.py`
- Issue: `URLField(assume_scheme='https', ...)` raised import-time `TypeError` in current runtime.
- Action: removed unsupported kwarg and preserved URL normalization via `clean_video_url`.
- Purpose: unblock required repo-wide checks and tests.

## Remaining Deferred Items

- `GAP-008` quiz center quick-start placeholder action URL.
- `GAP-012` legacy `static/core/js/quiz.js` remains unreachable artifact.
- `GAP-014` tag route canonicalization.
- `GAP-015` support module remains truthful placeholder pending real model/workflow.

## Validation Executed

- `python3 manage.py check --settings=medprep.settings_test` ✅
- `pytest -q tests/automated` ✅ (`58 passed`, `1 warning`)
- `node --check playwright.config.js` ✅
- `node --check playwright/tests/public-smoke.spec.js` ✅
- `node --check playwright/tests/student-flows.spec.js` ✅
- `node --check playwright/tests/staff-smoke.spec.js` ✅

## Revised Readiness Verdict

**Integration-safe for controlled feature work** in repaired active paths.
