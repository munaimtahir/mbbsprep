# Local Database Artifact Policy

## Decision

Policy selected: **A — keep committed, explicitly non-authoritative**.

`db.sqlite3` and `playwright.sqlite3` are intentionally retained in-repo for local/dev and test harness continuity. They are not canonical truth for application behavior.

## Artifact Roles

- `db.sqlite3`
  - Role: local development snapshot and convenience seed state.
  - Authority: **not** source of truth (code/models/tests are source of truth).
- `playwright.sqlite3`
  - Role: local Playwright/runtime test artifact.
  - Authority: **not** source of truth.

## Editing and Regeneration Rules

- Developers may regenerate either file when local workflows require it.
- Changes to these files must never be used to justify contract, model, or behavior claims.
- Treat them as disposable local state snapshots.

## Rebuild/Delete Guidance

- Rebuild/delete when schema drift, stale local state, or flaky local runs are observed.
- Prefer running migrations and seed/setup commands over manual DB edits.
- Any baseline verification claim must be backed by:
  - `python3 manage.py check --settings=medprep.settings_test`
  - `pytest -q tests/automated`

## Guardrail

If DB file contents conflict with current code/contracts/tests, code/contracts/tests win.
