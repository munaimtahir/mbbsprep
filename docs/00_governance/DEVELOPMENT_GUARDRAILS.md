# Development Guardrails

These guardrails exist to protect the verified v1 baseline and keep future work coherent.

## Architecture Guardrails

1. The project remains a Django monolith by default.
2. Do not introduce SPA architecture, frontend rewrites, or API-first redesign without explicit approval.
3. Do not rename apps, critical modules, or template roots casually.
4. Do not create parallel workflow implementations when an existing workflow can be repaired or extended.

## Stability Guardrails

The following flows are baseline-protected and must not be broken by unrelated work:

- signup / login / logout
- dashboard access
- profile view/edit
- question-bank browsing
- quiz start -> session -> submit -> result
- resource viewing in active categories
- payment proof submission and status visibility
- staff payment review/history
- staff subject/topic/question workflows already stabilized
- staff bulk user upload after verified repair

## Model Guardrails

1. Do not change model fields, choices, or relationships casually.
2. Any change to status fields, year-of-study fields, or relationship semantics must update the relevant contract docs.
3. Avoid adding duplicate status concepts where one canonical status already exists.

## Cleanup Guardrails

1. No broad cleanup passes without documented scope.
2. Prefer archival over deletion for historical material.
3. Do not move files purely for aesthetics if import paths or template paths could break.
4. Every cleanup decision must be recorded in `docs/30_repo/CLEANUP_DECISIONS.md`.
