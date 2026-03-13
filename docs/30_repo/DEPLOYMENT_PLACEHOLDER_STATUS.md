# Deployment Placeholder Status

## Current State

The repository currently does **not** provide active production deployment automation.

Files:

- `deployment/deploy.sh`
- `deployment/gunicorn.conf.py`

are retained as explicit **non-operational placeholders**.

## Why They Exist

- to reserve deployment location and naming conventions
- to prevent accidental assumption that deployment files are missing
- to keep deployment work scoped to a future dedicated pass

## Governance Rule

- Do not infer production-readiness from these files.
- Do not treat placeholder deployment files as executable deployment truth.
- Any future deployment implementation must include docs updates in `docs/30_repo/` and `docs/00_governance/`.
