# Status Enums Registry

This document records meaningful workflow statuses that must stay consistent across the repository.

## Payment Review Statuses

Canonical semantics:

- **PENDING**: payment proof submitted or awaiting final review
- **APPROVED**: proof accepted / payment verified
- **REJECTED**: proof declined / not accepted

### Repository Rule
These semantics must remain aligned across:
- models
- forms
- staff dashboard counts/filters
- review actions
- user-facing status pages
- tests

## Profile Choice Statuses / Enumerations

### Year of Study
Any year-of-study value written through forms or defaults must belong to the current canonical choice set.

### Rule
Never hard-code informal values like `1st` if the model expects a different canonical representation.
