# MedPrep Project Context

## What This Project Is

`mbbsprep` is a Django application for MBBS exam preparation. It has two major surfaces:

- `core`: the student-facing site for signup, login, dashboard, question bank, quizzes, leaderboard, resources, profile, and subscription/payment flows.
- `staff`: a custom backoffice/admin interface for managing users, subjects, topics, MCQs, tags, resources, and payments.

The product intent is clear: a medical exam preparation platform for Pakistani MBBS students, with free/premium access, manual payment verification, subject/topic structured MCQs, and a custom staff workflow for content and user operations.

## Current Reality In One Paragraph

The repository contains a real and fairly extensive Django codebase, but it is not in the fully finished state claimed by several historical docs. The custom staff area is the strongest implemented area. The public site is partially implemented. Several views point to templates that do not exist. Some utility modules and management commands still reference old model fields. The docs and many verification scripts describe a more complete system than the code currently guarantees.

## Source-Of-Truth Order

When understanding or changing this project, trust sources in this order:

1. Current models, views, forms, URLs, templates.
2. Database schema and current `db.sqlite3` contents.
3. New context in this file.
4. Existing docs in `docs/`.
5. Test and debug scripts in `tests/` and `scripts/`.

Historical docs are useful for intent, but not for exact implementation status.

## Tech Stack

- Python / Django 5.0.6
- SQLite by default in local settings
- `django-crispy-forms` + `crispy-bootstrap5`
- `pandas` / `openpyxl` for bulk import flows
- `Pillow` for image uploads
- Static HTML/CSS/JS templates, mostly without a modern frontend framework

## High-Level Folder Review

### Root

- `manage.py`: Django entrypoint.
- `db.sqlite3`: populated local development database.
- `requirements.txt`: Python dependencies.
- `start_server.sh`, `run_server.bat`, `start_server.bat`: convenience scripts, but Windows paths are hardcoded in the `.bat` files and `start_server.sh`.
- `deployment/`: deployment area, but `deploy.sh` is empty.
- Multiple `debug_*.py` and verification scripts exist at root. These are diagnostics, not stable product code.

### `medprep/`

Project configuration.

- `settings.py`: standard Django settings, SQLite default, static/media config, crispy forms config.
- `urls.py`: routes `admin/`, `staff/`, Django auth `accounts/`, and root `core/`.
- `wsgi.py`, `asgi.py`: standard entrypoints.

### `core/`

Student-facing domain app.

- `models/`: split by domain, which is good.
- `views/`: split into `main`, `auth`, `quiz`, `resource`, `payment`, `static`.
- `forms/`: user auth/profile, quiz settings, payment proof, contact.
- `utils/`: scoring, ranking, payment utilities, but some are stale/broken.
- `management/commands/`: sample data, test users, import questions, expire subscriptions.
- `signals.py`: auto-create profile and send emails, but some logic is stale.
- `admin.py`: Django admin registrations for core models.
- `fixtures/`: sample subjects fixture.

### `staff/`

Custom staff/backoffice app.

- `views/`: dashboard, auth, users, subjects/topics, questions, tags, resources, payments, support, settings.
- `forms/`: package-based form modules used by the app.
- `forms.py`: old monolithic duplicate file; appears stale/orphaned and should not be treated as source of truth.
- `urls.py`: large custom admin URL map.

### `templates/`

Server-rendered templates.

- `templates/core/`: public site templates.
- `templates/staff/`: custom staff templates.
- `templates/registration/`: password reset templates.
- `templates/emails/`: welcome emails.

Important: some templates referenced by views are missing from disk.

### `static/` and `staticfiles/`

- `static/`: source static assets.
- `staticfiles/`: collected/generated static assets, including Django admin files.

Do not edit `staticfiles/` unless the task is specifically about collected output. Source edits belong in `static/`.

### `docs/`

Large collection of status and fix notes. These are mostly July 2025 implementation notes. They are useful historical artifacts, but they overstate completeness.

Notable point:

- `docs/README.md` is empty.

### `tests/`

Contains many standalone verification scripts, not a coherent maintainable automated test suite. Several reference URL names or assumptions that do not match the current code.

### `scripts/`

Contains assorted debug helpers and demo scripts. Many are one-off/manual diagnostic utilities, not production tooling.

### `data/`

CSV samples for bulk uploads and seed/demo flows.

## Domain Model Summary

### Academic structure

- `Subject`
- `Topic`
- `Question`
- `Option`

Topics belong to subjects. Questions belong to topics. Options belong to questions.

### User and progress

- Django `User`
- `UserProfile`
- `QuizSession`
- `UserAnswer`
- `UserProgress`

Profiles store MBBS year, province, college info, premium flags, and aggregate quiz stats.

### Content/resources

- `Note`
- `Flashcard`
- `VideoResource`

Each belongs to a topic and can be premium/free.

### Payments/subscriptions

- `SubscriptionPlan`
- `PaymentProof`

Manual review flow is the intended payment model.

### Taxonomy

- `Tag`
- `Subtag`

Tags are linked to questions, topics, notes, flashcards, videos, and user profiles.

## Current Database Snapshot

Values observed in local `db.sqlite3`:

- Subjects: `11`
- Topics: `45`
- Questions: `36`
- Tags: `45`
- Users: `51`
- Subscription plans: free/monthly/quarterly/yearly present
- Notes: `0`
- Flashcards: `0`
- Videos: `0`
- Quiz sessions: `0`
- User answers: `0`
- Payment proofs: `0`

Implication: the data currently proves question-bank/admin setup more than end-user learning activity.

## What Is Clearly Implemented

### Public site

- Home page, dashboard, leaderboard, question bank, subject detail, topic detail.
- Signup/login/logout flows.
- Quiz creation, session answering, submission, and result pages in code.
- Subscription plans and payment proof upload/status views in code.
- Static pages: about, contact, FAQ, terms, privacy.

### Staff site

- Staff login/logout.
- Dashboard with top-level metrics.
- User list/detail/edit/create/bulk upload/export.
- Subject and topic CRUD, plus topic bulk upload.
- Question CRUD and bulk upload.
- Tag list/create/edit plus AJAX tag/subtag operations.
- Resource CRUD forms for notes/videos/flashcards.
- Payment list/review/history views in code.

### Infrastructure

- Modularized models/views/forms organization.
- Django admin setup.
- Basic signals.
- Sample data and test-user management commands.

## What Exists But Is Incomplete Or Broken

### Missing templates referenced by views

Public:

- `core/auth/profile_edit.html`
- `core/resources/notes_list.html`
- `core/resources/note_detail.html`
- `core/resources/flashcards_list.html`
- `core/resources/flashcard_study.html`
- `core/resources/videos_list.html`
- `core/resources/video_detail.html`
- `core/subscription/payment.html`
- `core/subscription/payment_proof_upload.html`
- `core/subscription/payment_status.html`
- `core/quiz/start_quiz.html`

Staff:

- `staff/payments/payment_review.html`
- `staff/payments/payment_history.html`
- `staff/tags/tag_confirm_delete.html`
- `staff/support/inbox.html`
- `staff/support/message_detail.html`

These routes may reverse correctly but will fail at runtime when rendered.

### Stubbed or placeholder logic

- `staff/views/resource_views.py`: `ResourceListView.get_queryset()` returns `None`.
- `staff/views/support_views.py`: support system is explicitly not implemented because there is no support/contact model.
- `core/models/tag_models.py`: tag/subtag resource counts are placeholders.
- `staff/views/dashboard_views.py`: revenue is mock data, not real payment aggregation.

### Stale or incorrect code paths

- `core/management/commands/import_questions.py` imports and uses `QuestionOption`, but the current model is `Option`.
- `core/utils/payment_check.py` references old/nonexistent fields and methods:
  - `proof_image`
  - `duration_months`
  - `subscription_plan` on `UserProfile`
  - calls `is_premium_active()` as if it were a method
- `core/signals.py` contains stale assumptions:
  - checks uppercase payment statuses like `APPROVED` / `REJECTED` while model uses lowercase
  - references nonexistent `duration_months`
  - writes dynamic fields like `average_score` and `total_quizzes` that are not model fields
- `staff/views/dashboard_views.py` checks `status='submitted'`, but `PaymentProof.STATUS_CHOICES` does not define `submitted`.

### Form/view mismatches

- `staff/views/user_views.py` expects `UserCreateForm` fields like `password`, `user_role`, `year_of_study`, `province`, `college_type`, `college_name`, `phone_number`, `is_premium`, `premium_expires_at`.
- `staff/forms/user_forms.py` `UserCreateForm` actually defines `password1` and `password2` and does not define most of those extra fields.

This means the add-user flow is likely inconsistent or broken without further changes.

### URL/test drift

Many standalone test scripts refer to names such as:

- `staff:user_add`
- `staff:subject_add`
- `staff:topic_add`

Current URL config defines:

- `staff:user_create`
- `staff:subject_create`
- `staff:topic_create`

Some templates and tests still use the older names, so historical “100% pass” claims cannot be treated as current truth.

### Environment/tooling gaps

- Django is not installed in the current shell environment, so runtime verification was not possible without creating/activating a venv.
- `deployment/deploy.sh` is empty.
- Several server-start scripts hardcode an old Windows path: `D:\PMC\Exam-Prep-Site\...`.

## Documentation Review

### What the docs do well

- They preserve intent and feature history.
- They describe the desired staff/admin workflows in detail.
- They capture many fixes that were probably applied at some point.

### What the docs do poorly

- They repeatedly claim “100% complete”, “production ready”, or “all tests passed”.
- Those claims do not match the current repository state.
- `docs/README.md` is empty, so there is no maintained central index.

Interpretation:

- The docs are best treated as a changelog/archive, not a current operational specification.

## Tests And Verification Review

The repository contains many files under `tests/`, but they are mostly custom scripts rather than a clean pytest or Django `TestCase` suite.

Observed characteristics:

- Several are manual/verifier scripts.
- Several embed outdated route names or stale assumptions.
- `core/tests.py` is effectively empty.
- The test directory functions more like a diagnostics archive than reliable CI coverage.

Practical conclusion:

- Before trusting any test, read it and compare it to current URLs/forms/templates.
- Future work should consolidate this into a small, real automated test suite around live critical flows.

## Duplications And Artifacts

- `staff/forms.py` and `staff/forms/` both exist. The package directory is the active source; the monolithic file appears historical.
- `static/` and `staticfiles/` both exist. `staticfiles/` is collected output.
- There are many debug and verification scripts spread across root, `scripts/`, and `tests/`.

This repository has clear accumulation of implementation artifacts from multiple development/debugging passes.

## What Has Been Done vs. What Is Pending

### Done enough to build on

- Core data model.
- Custom staff area foundation.
- Question/topic/subject management.
- Tagging model and topic bulk upload.
- Quiz session model and public quiz flow code.
- Manual subscription/payment domain model.

### Pending or needs repair before calling the app stable

- Create all missing templates referenced by existing views.
- Reconcile form/view mismatches in user creation and possibly bulk upload.
- Remove or repair stale utilities and management commands.
- Decide whether support inbox is real; if yes, add a model and templates.
- Decide whether payment review/history UI is real; if yes, add templates and complete workflow.
- Build a real automated test suite for critical paths.
- Replace optimistic docs with grounded documentation.
- Clean obsolete files and path-specific scripts.

## Recommended Near-Term Plan

### Phase 1: Make current code coherent

- Fix template/view mismatches.
- Fix stale model-field references in utils, signals, and management commands.
- Fix staff route/template inconsistencies.
- Audit user creation and bulk upload flows end to end.

### Phase 2: Stabilize product-critical flows

- Public quiz flow
- Public subscription/payment submission flow
- Staff payment review flow
- Staff subject/topic/question CRUD

### Phase 3: Reduce repository noise

- Remove or archive obsolete scripts/docs.
- Keep `staff/forms/` and retire `staff/forms.py`.
- Document which scripts are still useful.

### Phase 4: Build trustworthy verification

- Add real Django tests for:
  - auth
  - public quiz flow
  - staff question CRUD
  - topic bulk upload
  - payment review lifecycle

## Operational Notes

- Default local DB is SQLite.
- Current shell did not have Django installed, so runtime checks were limited to static code and SQLite inspection.
- Public/resource and payment sections should be treated as partially implemented until missing templates and stale code are resolved.
- The staff admin is the most mature part of the system, but it still contains unfinished sections.

## Bottom Line

This is not an empty or toy repository. It is a real Django application with a meaningful amount of product logic already built, especially around custom staff operations and structured MBBS content. But it is also not currently in the “fully complete / production-ready / fully verified” state claimed by historical docs. The correct framing is:

- strong foundation
- partially implemented product
- significant documentation drift
- moderate cleanup and completion work required before reliable production use
