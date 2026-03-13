# Legacy and Historical Files Registry

Concrete registry for this repository.

## Archived Implementation Notes

- `docs/archive/legacy-implementation-notes/*`
- Contains historical fix summaries and implementation notes.
- Status: `ARCHIVE_HISTORICAL`

## Archived Repair Reports

- `docs/archive/repair-pass-reports/REPAIR_PASS_STATUS.md`
- `docs/archive/repair-pass-reports/REPAIR_PASS_VERIFICATION.md`
- Status: `ARCHIVE_HISTORICAL`

## Debug Scripts (Archived)

- `scripts/legacy/debug_*.py`
- Status: `ARCHIVE_HISTORICAL`

## Demo and One-Off Fix Scripts (Archived)

- `scripts/legacy/demo_*.py`
- `scripts/legacy/fix_*.py`
- `scripts/legacy/start_*.py`
- `scripts/legacy/check_*.py`
- `scripts/legacy/show_*.py`
- `scripts/legacy/logout_fix_verification.py`
- `scripts/legacy/generate_testing_checklist.py`
- Status: `ARCHIVE_HISTORICAL`

## Verification Artifacts

- Root transient verification output files were removed in governance lock pass.
- `simple_verification.py` and `final_verification.py` moved to `archive/root_legacy_verifiers/`.
- Status: `DELETE_IRRELEVANT` (for dumps) and `ARCHIVE_HISTORICAL` (for scripts)

## Legacy Tests

- `tests/legacy/*` (all non-canonical verification scripts and ad-hoc tests)
- Canonical suite is `tests/automated/*`.
- Status: `ARCHIVE_HISTORICAL`

## Compatibility Files

- `docs/V1_BASELINE_FREEZE.md` retained as a compatibility pointer to canonical governance doc.
- Status: `KEEP_ACTIVE` (as compatibility pointer, not canonical content body)

## Generated Artifacts

- `staticfiles/` is generated collected static output.
- `playwright-report/`, `test-results/` are generated test outputs.
- Status: `KEEP_GENERATED_BUT_DO_NOT_EDIT`

## Retained Historical Notes

- `PROJECT_CONTEXT.md` retained for background context with explicit historical warning.
- Status: `ARCHIVE_HISTORICAL` in spirit, but kept at root for compatibility and orientation.
