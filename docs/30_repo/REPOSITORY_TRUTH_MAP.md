# Repository Truth Map

## Canonical Active Areas

- Runtime code: `core/`, `staff/`, `medprep/`, `templates/`, `static/`
- Entry/control files: `manage.py`, `README.md`, `AGENTS.md`, `docs/INDEX.md`
- Canonical tests: `tests/automated/`
- Governance/contracts/workflows/repo docs:
  - `docs/00_governance/`
  - `docs/10_contracts/`
  - `docs/20_workflows/`
  - `docs/30_repo/`

## Historical Areas (Non-Canonical)

- `docs/archive/`
- `tests/legacy/`
- `scripts/legacy/`
- `archive/root_legacy_verifiers/`
- `PROJECT_CONTEXT.md` (retained background, not primary authority)

## Generated Areas (Keep, Do Not Edit as Source)

- `staticfiles/` (collected static output)
- `playwright-report/`, `test-results/` (test outputs)
- `playwright.sqlite3` (playwright runtime DB artifact)

## Deprecated / Retired Areas

- root debug and one-off verifier artifacts removed in this pass:
  - `debug_*.py`, `debug_*.html`, `csrf_test.html`, `verification_results.txt`
- duplicate `staff/forms.py` removed; canonical forms live in `staff/forms/`.

## Root File Purpose Map

- active control/config: `manage.py`, `pyproject.toml`, `pytest.ini`, `requirements*.txt`, `package*.json`, `.gitignore`
- launch helpers (neutralized): `start_server.sh`, `start_server.bat`, `run_server.bat`
- local DB/runtime artifacts intentionally retained: `db.sqlite3`, `playwright.sqlite3`
- non-canonical historical/context: `PROJECT_CONTEXT.md`

## Contributor Navigation Order

1. `README.md`
2. `docs/INDEX.md`
3. `docs/00_governance/*`
4. `docs/30_repo/REPOSITORY_TRUTH_MAP.md`
5. code
6. `tests/automated/`
7. only then archive/legacy paths if needed
