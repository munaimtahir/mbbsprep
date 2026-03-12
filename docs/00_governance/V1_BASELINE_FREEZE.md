# V1 Baseline Freeze

This document records the current trusted baseline of the MedPrep repository.

## Meaning of “Verified V1 Baseline”

The repository has passed through:

1. repair of known runtime blockers
2. verification of claimed repairs against actual code
3. patch round 2 to close meaningful remaining gaps
4. test strengthening for critical flows

This does **not** mean the product is feature-complete. It means the project has a stable, trustworthy baseline for controlled future development.

## Stable Public Flows

- signup
- login
- logout
- dashboard access
- profile view/edit
- question-bank browsing
- quiz start/session/submit/result
- active resource viewing flows
- payment/subscription proof submission and payment status visibility

## Stable Staff Flows

- staff dashboard loading
- subject/topic/question management in the current architecture
- payment queue/review/history in scope
- resource overview/list functionality in scope
- bulk user upload after patch round 2 verification
- support placeholder rendering without crashing

## Intentionally Incomplete or Limited Areas

- payment processing remains manual or semi-manual
- support system remains placeholder-level
- some resource analytics and counts may remain lightweight
- advanced product polish and analytics are not baseline commitments
