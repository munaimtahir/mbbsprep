
> Historical / may not reflect current code truth.
>
> This document was archived during the documentation freeze. Use the structured docs under `docs/` for current repository guidance.

# Testing

This repository now includes a repository-local automated testing stack with isolated Django settings and Playwright browser automation.

## Layers

- `pytest` smoke tests for route-level render and auth-gate coverage.
- `pytest` integration tests for signup, login, quiz completion, and payment proof upload.
- `pytest` quality tests for Django checks, database connectivity, URL contract coverage, and i18n/timezone settings.
- Playwright browser tests for public navigation, student flows, and staff login.

Note: the repository contains a large set of historical ad hoc scripts under `tests/` that are not lint-clean. The `test:quality` target intentionally gates the new automated suite and test settings rather than the entire legacy tree.

## Python setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

## Playwright setup

```bash
npm install
npm run test:install-browsers
```

## Common commands

```bash
npm run test:quality
npm run test:smoke
npm run test:integration
npm run test:e2e
npm run test:all
```

## Isolated runtime

- `medprep.settings_test` is used by `pytest`.
- `medprep.settings_playwright` uses a dedicated `playwright.sqlite3` database.
- `scripts/run_playwright_server.sh` migrates, seeds deterministic users and quiz data, and then starts Django for browser tests.

## Seeded Playwright credentials

- Student: `playwright_student` / `PlaywrightPass123!`
- Staff: `playwright_staff` / `PlaywrightStaff123!`
