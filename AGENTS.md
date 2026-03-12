# AGENTS.md

This file defines how AI agents and future maintainers must operate inside the MedPrep repository.

## Mission

Preserve the verified v1 baseline while improving the project in a controlled way.

## Non-Negotiable Rules

1. Treat the **existing codebase** as the source of truth.
2. Respect `docs/00_governance/V1_BASELINE_FREEZE.md`.
3. Respect `docs/00_governance/DEVELOPMENT_GUARDRAILS.md`.
4. Do not redesign the architecture unless explicitly approved.
5. Do not introduce React, DRF-first rewrites, or SPA migration by default.
6. Do not delete active routes because they are inconvenient; either repair them or formally document why they are retired.
7. Do not rename critical models, apps, or template paths casually.
8. Do not perform broad cleanup without a written cleanup decision log.
9. Every meaningful structural change must update the relevant docs.
10. Validation is mandatory after implementation.

## Required Validation After Changes

At minimum, run:

- `python3 manage.py check --settings=medprep.settings_test`
- `pytest -q tests/automated`

## Preferred Working Style

- small, local, reversible changes
- explicit acceptance criteria
- evidence-driven implementation
- no speculative refactors
- low regression risk
