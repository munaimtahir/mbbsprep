# Root Structure Standard

Defines allowed root contents and this pass disposition.

## Allowed at Project Root

- project control files (`manage.py`, dependency manifests, test config)
- top-level governance entry docs (`README.md`, `AGENTS.md`)
- launch helpers that are neutral and portable
- local DB/runtime files only when intentionally retained and documented

Do not place one-off debug scripts, ad-hoc verification dumps, or optimistic status files in root.

## Current Root Disposition

| Root Item | Status |
| --- | --- |
| `.env.example` | keep |
| `.gitignore` | keep |
| `AGENTS.md` | keep |
| `PROJECT_CONTEXT.md` | keep (historical/context) |
| `README.md` | keep |
| `manage.py` | keep |
| `requirements.txt`, `requirements-dev.txt` | keep |
| `pyproject.toml` | keep |
| `pytest.ini` | keep |
| `package.json`, `package-lock.json`, `playwright.config.js` | keep |
| `db.sqlite3` | keep (intentional local DB artifact) |
| `playwright.sqlite3` | keep (test/runtime artifact) |
| `start_server.sh` | replace (neutralized) |
| `start_server.bat` | replace (neutralized) |
| `run_server.bat` | replace (neutralized) |
| `simple_verification.py` | archive |
| `final_verification.py` | archive |
| `debug_bulk_detailed.py` | delete |
| `debug_bulk_simple.py` | delete |
| `debug_bulk_upload.py` | delete |
| `debug_issues.py` | delete |
| `debug_edit_response.html` | delete |
| `csrf_test.html` | delete |
| `verification_results.txt` | delete |
