# Cleanup Decisions

This document records cleanup and structure decisions made during the governance/documentation freeze.

## Current Documentation-Freeze Decisions

### 1. Centralized governance docs under `docs/`
Decision:
Created a standardized documentation structure with governance, contracts, workflows, and repository sections.

### 2. Preserved monolith architecture
Decision:
Did not perform application restructuring or architectural modernization.

### 3. Chose archival-over-deletion policy
Decision:
Historical materials should be archived or labeled rather than broadly deleted.

### 4. Avoided code moves for cosmetic reasons
Decision:
Did not recommend moving app files, templates, or route definitions purely for neatness.

### 5. Elevated README and AGENTS as entry controls
Decision:
README and AGENTS were updated as top-level orientation/control docs.

### 6. Separated canonical and legacy tests
Decision:
Moved non-automated historical tests to `tests/legacy/` and kept `tests/automated/` as canonical automated suite.

### 7. Separated operational and legacy scripts
Decision:
Moved one-off debug/demo/fix/check/show/start scripts to `scripts/legacy/`; kept only recurring operational helpers in `scripts/`.

### 8. Neutralized launcher scripts
Decision:
Replaced machine-specific launcher paths and removed unverifiable success/completeness claims from root launch scripts.

### 9. Removed duplicate forms source
Decision:
Deleted `staff/forms.py` duplicate monolith and retained `staff/forms/` package as the sole forms source-of-truth.
