# Archive Usage Rules

## Core Rule

Archive and legacy paths are **reference-only**, not active implementation truth.

## Non-Canonical Areas

- `docs/archive/`
- `tests/legacy/`
- `scripts/legacy/`
- `archive/`

## Required Behavior

- Do not start implementation from archived material.
- Do not let archived docs override current code, forms, routes, templates, or tests.
- Use archives only for historical context after active docs/code are reviewed.
- Any recovery of historical logic must be revalidated against current code and `tests/automated/`.

## Agent Rule

Agents must begin from:
1. `README.md`
2. `docs/INDEX.md`
3. `docs/00_governance/*`
4. `docs/30_repo/REPOSITORY_TRUTH_MAP.md`
5. code
6. `tests/automated/`

Archive/legacy material may be consulted only after these steps.
