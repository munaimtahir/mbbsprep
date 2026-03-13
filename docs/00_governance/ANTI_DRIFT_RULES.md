# Anti-Drift Rules

This file is mandatory governance for repository hygiene and truth control.

## Mandatory Entry Order

Before implementation, contributors and agents must read in this order:

1. `README.md`
2. `docs/INDEX.md`
3. `docs/00_governance/*`
4. `docs/30_repo/REPOSITORY_TRUTH_MAP.md`
5. code
6. `tests/automated/`
7. archive/legacy paths only if needed for historical context

## Source-of-Truth Order

When conflicts exist, resolve in this order:

1. current executable code
2. models
3. views
4. forms
5. urls
6. templates
7. `tests/automated/*`
8. active docs under `docs/00_governance`, `docs/10_contracts`, `docs/20_workflows`, `docs/30_repo`
9. historical docs
10. old debug scripts and one-off verifiers

If docs disagree with code, update docs to code.

## Forbidden Behaviors

- no architecture migration (SPA/API-first rewrite) without explicit approval
- no speculative feature expansion during governance passes
- no machine-specific absolute paths in committed scripts
- no duplicate source-of-truth module patterns
- no fake completeness claims (`100% complete`, `production-ready`) without current validation evidence
- no one-off verification dumps in project root
- no edits to `staticfiles/` as source code

## Documentation Update Rules

- Any route/view/form/template contract change must update relevant docs in `docs/10_contracts` and `docs/20_workflows`.
- Any repository-structure or archival/deletion change must update `docs/30_repo/*`.
- Status snapshots must be archived under `docs/archive/`, not kept as active operational truth.

## Cleanup Rules

- classify before action using:
  - `KEEP_ACTIVE`
  - `KEEP_GENERATED_BUT_DO_NOT_EDIT`
  - `ARCHIVE_HISTORICAL`
  - `DELETE_IRRELEVANT`
  - `REWRITE_AS_THIN_SHIM`
  - `REPLACE_WITH_NEUTRAL_VERSION`
- prefer archive for historical context
- prefer delete for transient debug outputs, verifier dumps, misleading status artifacts
- never silently delete potentially useful historical material without classification in docs

## Consistency Rule (Route/View/Form/Template)

For any flow touched, route name, view handler, form contract, and template path must stay coherent together. Do not update one layer and leave others stale.

## Validation Rules

- Minor changes: targeted checks for touched area.
- Moderate/Major changes: run both:
  - `python3 manage.py check --settings=medprep.settings_test`
  - `pytest -q tests/automated`
- JS/test harness updates: run Node syntax checks or test command for changed files.

## Archival Rules

- archive location standards:
  - repository scripts/tests legacy material: `scripts/legacy/`, `tests/legacy/`
  - root legacy verifiers: `archive/root_legacy_verifiers/`
  - legacy documentation reports: `docs/archive/...`
- archived material is non-canonical and must be labeled as historical.
