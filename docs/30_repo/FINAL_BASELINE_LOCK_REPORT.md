# Final Baseline Lock Report

## Pass Scope

Final stabilization pass only:

- sqlite artifact policy finalization
- deployment placeholder truth pass
- CI baseline enforcement
- onboarding order normalization
- archive usage rule hardening

No feature work and no business-logic refactor were performed.

## Changes Made

### 1) SQLite policy

- Added `docs/30_repo/LOCAL_DATABASE_ARTIFACT_POLICY.md`.
- Decision: keep `db.sqlite3` and `playwright.sqlite3` committed but explicitly non-authoritative.
- Updated `.gitignore` to remove misleading `playwright.sqlite3` ignore entry.

### 2) Deployment placeholders

- Replaced empty placeholders with explicit non-operational content:
  - `deployment/deploy.sh`
  - `deployment/gunicorn.conf.py`
- Added `docs/30_repo/DEPLOYMENT_PLACEHOLDER_STATUS.md`.

### 3) CI baseline enforcement

- Added `.github/workflows/baseline-checks.yml`.
- Added `docs/30_repo/CI_BASELINE.md`.

### 4) Entry order consistency

- Updated onboarding order in:
  - `README.md`
  - `docs/INDEX.md`
  - `docs/30_repo/REPOSITORY_TRUTH_MAP.md`
  - `docs/00_governance/ANTI_DRIFT_RULES.md`

### 5) Archive handling rules

- Added `docs/30_repo/ARCHIVE_USAGE_RULES.md`.

## Validation Run

Required:

- `python3 manage.py check --settings=medprep.settings_test` -> PASS
- `pytest -q tests/automated` -> PASS (`44 passed`, `1 warning`)

Additional (included in this pass):

- `node --check playwright.config.js` -> PASS
- `node --check playwright/tests/public-smoke.spec.js` -> PASS
- `node --check playwright/tests/student-flows.spec.js` -> PASS
- `node --check playwright/tests/staff-smoke.spec.js` -> PASS

## Unresolved Risks

- `db.sqlite3` and `playwright.sqlite3` still carry mutable local state; policy now documents they are non-authoritative.
- Deployment remains intentionally non-operational in-repo until a dedicated deployment pass is approved.

## Baseline Status

Repository is baseline-locked for controlled development under documented governance constraints, with CI enforcement for core validation.
