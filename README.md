# MedPrep

MedPrep is a Django-based MBBS exam preparation platform with two primary surfaces:

- **Public / Student side** for authentication, dashboard access, question-bank browsing, quiz practice, profile management, study resources, and subscription/payment proof flows.
- **Staff side** for subject/topic/question management, resource administration, user administration, bulk user upload, and payment review.

## Current State

The repository has reached a **verified v1 baseline with documented limits**. The immediate goal is not feature expansion; it is repository governance, documentation standardization, and safe future development.

## Technology

- Django monolith
- Template-rendered HTML
- Django ORM
- SQLite in local/test workflows
- Automated tests for critical flows

## Where to Start

Read:

1. `README.md`
2. `docs/INDEX.md`
3. `docs/00_governance/*`
4. `docs/30_repo/REPOSITORY_TRUTH_MAP.md`
5. code (`core/`, `staff/`, `medprep/`, `templates/`, `static/`)
6. `tests/automated/`
7. only then archive/legacy paths if needed (`docs/archive/`, `tests/legacy/`, `scripts/legacy/`, `archive/`)

## Developer Principle

This repository should evolve through **controlled, documented changes**. No major architectural shifts, cleanup passes, or model changes should occur without corresponding documentation updates and verification.
