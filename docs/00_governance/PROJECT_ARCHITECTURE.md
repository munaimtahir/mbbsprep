# Project Architecture

## Architectural Style

MedPrep currently uses a **Django monolith** architecture.

This means the repository keeps application logic, views, forms, models, and template rendering within a unified server-side application. This architecture is currently appropriate for the maturity level of the project and should be preserved unless a deliberate future redesign is approved.

## Primary Application Boundaries

### `core`
Owns the public/student-facing experience, including authentication, dashboard, question bank, quizzes, profile, resources, and payment-proof flows.

### `staff`
Owns internal administrative workflows, including subject/topic/question management, user administration, bulk upload, payment review, resource administration, and support placeholders.

## Layer Model

The current monolith follows a conventional Django layered pattern:

- route layer
- view layer
- form layer
- template layer
- model layer

## Operational Principle

Because the repo already reached a verified baseline, the architectural goal is **coherence**, not modernization for its own sake.

## Architecture Boundaries To Preserve

1. Public/student workflows remain inside the existing app structure.
2. Staff/admin workflows remain distinct from student flows.
3. Stable routes should not be removed or renamed casually.
4. Template structure should evolve gradually rather than being broadly reorganized.
5. Existing working form/view/template chains should be repaired, not replaced, unless there is a compelling reason.
