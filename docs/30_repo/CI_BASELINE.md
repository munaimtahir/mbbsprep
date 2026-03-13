# CI Baseline

## Purpose

Provide minimal, truthful baseline enforcement to reduce drift.

## Workflow

GitHub Actions workflow: `.github/workflows/baseline-checks.yml`

Runs on push and pull_request:

- `python3 manage.py check --settings=medprep.settings_test`
- `pytest -q tests/automated`
- `node --check playwright.config.js`
- `node --check playwright/tests/public-smoke.spec.js`
- `node --check playwright/tests/student-flows.spec.js`
- `node --check playwright/tests/staff-smoke.spec.js`

## Scope Guardrail

- CI does not perform deployment.
- CI does not claim production readiness.
- CI is baseline integrity enforcement only.
