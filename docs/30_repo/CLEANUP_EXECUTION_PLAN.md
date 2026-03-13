# Cleanup Execution Plan

This file records reviewed groups, classification, action taken, and safety rationale.

## Reviewed Groups and Actions

| Group | Classification | Action Taken | Why Safe |
| --- | --- | --- | --- |
| Root debug artifacts (`debug_*.py`, `debug_issues.py`, `debug_edit_response.html`, `csrf_test.html`, `verification_results.txt`) | DELETE_IRRELEVANT | Deleted | One-off diagnostics/output; not imported by runtime code or tests/automated |
| Root verifier scripts (`simple_verification.py`, `final_verification.py`) | ARCHIVE_HISTORICAL | Moved to `archive/root_legacy_verifiers/` | Historical context preserved without polluting root |
| Status snapshot docs (`docs/REPAIR_PASS_STATUS.md`, `docs/REPAIR_PASS_VERIFICATION.md`) | ARCHIVE_HISTORICAL | Moved to `docs/archive/repair-pass-reports/` | Important history retained, removed from active doc surface |
| Legacy scripts (`scripts/debug_*`, `scripts/demo_*`, `scripts/fix_*`, `scripts/check_*`, `scripts/show_*`, `scripts/start_*`, `scripts/logout_fix_verification.py`, `scripts/generate_testing_checklist.py`) | ARCHIVE_HISTORICAL | Moved to `scripts/legacy/` | Preserves diagnostics history; active scripts remain explicit |
| Operational scripts (`scripts/run_playwright_server.sh`, `scripts/create_test_users.py`, `scripts/create_sample_bulk_users.py`, `scripts/add_sample_tags.py`) | KEEP_ACTIVE | Kept in `scripts/` | Recurring utility/seed/test setup value |
| Non-automated tests (`tests/*.py`, `tests/*.bat` excluding `tests/automated/`) | ARCHIVE_HISTORICAL | Moved to `tests/legacy/` | Clarifies canonical test suite while preserving historical verifiers |
| Launcher scripts (`start_server.sh`, `start_server.bat`, `run_server.bat`) | REPLACE_WITH_NEUTRAL_VERSION | Rewritten | Removed machine-specific paths and unverifiable claims |
| `staff/forms.py` duplicate monolith | DELETE_IRRELEVANT | Deleted | Eliminated ambiguity; canonical forms package is `staff/forms/` |
| `staticfiles/` | KEEP_GENERATED_BUT_DO_NOT_EDIT | Kept unchanged | Generated output required in some workflows; not source |

## What Was Archived Instead of Deleted

- `archive/root_legacy_verifiers/*`
- `scripts/legacy/*`
- `tests/legacy/*`
- `docs/archive/repair-pass-reports/*`

## Intentionally Preserved

- `db.sqlite3` and `playwright.sqlite3` retained as current local/runtime artifacts
- `PROJECT_CONTEXT.md` retained as historical context
- existing `docs/archive/legacy-implementation-notes/` retained
