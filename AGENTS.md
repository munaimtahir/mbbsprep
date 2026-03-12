# AGENTS.md

## Purpose

This repository is a Django-based MBBS exam preparation platform called MedPrep. Future agents should treat it as a partially completed production-style app with real structure, real data, and real drift between docs and code.

Read [`PROJECT_CONTEXT.md`](/home/munaim/srv/apps/mbbsprep/PROJECT_CONTEXT.md) first before making substantial changes.

## Ground Rules

- Trust current code over historical docs.
- Trust current templates and URLs over old test scripts.
- Do not assume anything is “100% complete” because a doc in `docs/` says so.
- Verify route names, template names, and form fields before changing related code.
- Prefer fixing the real source file instead of editing generated or duplicated artifacts.

## Source Of Truth

Use this order:

1. Models
2. Views
3. Forms
4. URLs
5. Templates
6. `PROJECT_CONTEXT.md`
7. Historical docs in `docs/`
8. Debug/test scripts in `tests/` and `scripts/`

## Important Repository Facts

- `core` is the public/student-facing app.
- `staff` is the custom backoffice app.
- `static/` is source static content.
- `staticfiles/` is collected output; avoid editing it.
- `staff/forms/` is the active forms package.
- `staff/forms.py` is a stale duplicate artifact unless proven otherwise.
- `docs/README.md` is empty.
- `deployment/deploy.sh` is empty.
- The current local database is `db.sqlite3`.

## Known Gaps You Must Keep In Mind

- Some views reference templates that do not exist.
- Some utilities and management commands still reference old model fields.
- Some standalone tests reference outdated URL names.
- Support inbox/message pages are stubbed, not truly implemented.
- Staff resource aggregation view is stubbed.
- Payment review/history templates are missing.
- Public resource/payment/profile-edit templates are missing.

Do not reinforce these inconsistencies. When touching an area, reconcile the full chain:

- URL
- view
- form
- template
- model fields

## Safe Editing Priorities

When making changes, prefer this order:

1. Fix broken runtime paths first.
2. Fix stale field references and import errors.
3. Fix template/view mismatches.
4. Add tests for the repaired flow.
5. Update documentation.

## Files And Areas To Avoid Touching Casually

- `staticfiles/`
- `__pycache__/`
- `db.sqlite3`
- historical debug scripts unless the task is specifically about them

Do not “clean up” old docs or scripts unless the task requires it. Some are stale, but they are also historical context.

## Environment Notes

- The current shell may not have Django installed globally.
- If runtime verification is needed, check for a project virtualenv first.
- Some helper scripts still contain old Windows-specific paths like `D:\PMC\Exam-Prep-Site\...`; do not copy those assumptions into new code.

## Working Style For This Repo

- Prefer small, coherent fixes over broad rewrites.
- For any new view, ensure the template actually exists.
- For any form/view pair, verify field names line up exactly.
- For any payment or subscription change, verify against the current `SubscriptionPlan` and `PaymentProof` models, not historical assumptions.
- For any tag-related change, remember `Tag.get_resource_count()` and `Subtag.get_resource_count()` are placeholders unless you implement them.

## Recommended Verification After Changes

For the area you touch, verify at minimum:

- imports resolve
- URL reverses work
- template exists
- form fields match the view logic
- model fields referenced actually exist

If you add or fix a flow, prefer adding a real Django test instead of another one-off debug script.

## If You Need Context Fast

Read these first:

1. [`PROJECT_CONTEXT.md`](/home/munaim/srv/apps/mbbsprep/PROJECT_CONTEXT.md)
2. [`medprep/settings.py`](/home/munaim/srv/apps/mbbsprep/medprep/settings.py)
3. [`medprep/urls.py`](/home/munaim/srv/apps/mbbsprep/medprep/urls.py)
4. [`core/models/__init__.py`](/home/munaim/srv/apps/mbbsprep/core/models/__init__.py)
5. [`core/urls.py`](/home/munaim/srv/apps/mbbsprep/core/urls.py)
6. [`staff/urls.py`](/home/munaim/srv/apps/mbbsprep/staff/urls.py)

## Default Assumption

Assume the project is a strong foundation with incomplete execution, not a finished system. Work from the actual codebase state and leave the repository more internally consistent than you found it.
