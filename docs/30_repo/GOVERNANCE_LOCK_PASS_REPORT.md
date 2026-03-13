# Governance Lock Pass Report

## Findings

- Root contained one-off debug scripts and verification dumps mixed with active control files.
- Non-automated legacy tests were mixed with canonical automated tests.
- `scripts/` mixed operational helpers with one-off debug/demo/fix scripts.
- Launcher scripts contained machine-specific absolute paths and unsupported completeness claims.
- `staff/forms.py` duplicated and conflicted conceptually with canonical `staff/forms/` package.
- Repair-pass status docs were active-path clutter; appropriate as historical archive.

## Actions Performed

- Deleted transient root debug/output files.
- Archived root verification scripts into `archive/root_legacy_verifiers/`.
- Archived repair reports into `docs/archive/repair-pass-reports/`.
- Moved legacy scripts to `scripts/legacy/`; kept only operational scripts at `scripts/` root.
- Moved non-automated tests to `tests/legacy/`; preserved `tests/automated/` as canonical test suite.
- Replaced launcher scripts with neutral, portable versions.
- Removed duplicate `staff/forms.py` to enforce `staff/forms/` as sole forms source.
- Added governance lock documentation pack (`REPOSITORY_TRUTH_MAP`, cleanup plan, anti-drift rules, root standard, updated legacy registry).

## Risks Left Unresolved

- `db.sqlite3` remains committed; this is intentional but can still cause snapshot drift if edited casually.
- `deployment/deploy.sh` and `deployment/gunicorn.conf.py` remain empty placeholders; no runtime change made in this pass.
- Archived legacy scripts/tests still exist and may be mistaken for active by inattentive readers (mitigated via registry docs).

## Follow-Up Recommendations

- Add a short `README` in `tests/legacy/` and `scripts/legacy/` stating non-canonical status.
- Decide policy on committed local DB artifacts (`db.sqlite3`, `playwright.sqlite3`) for long-term governance.
- Add CI guardrail to run `python3 manage.py check --settings=medprep.settings_test` and `pytest -q tests/automated`.

## Validation Results

- `python3 manage.py check --settings=medprep.settings_test` -> PASS
- `pytest -q tests/automated` -> PASS (`44 passed`, `1 warning`)
- `node --check playwright.config.js` -> PASS
- `node --check playwright/tests/public-smoke.spec.js` -> PASS
- `node --check playwright/tests/student-flows.spec.js` -> PASS
- `node --check playwright/tests/staff-smoke.spec.js` -> PASS
