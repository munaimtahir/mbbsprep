# Import / Export Contracts

This document records the current practical contracts for import-oriented workflows.

## Bulk User Upload

### Workflow
1. upload file
2. preview parsed result
3. confirm import
4. process import
5. redirect/report completion

### Contract Expectations
- route names must be correct and stable
- preview must carry required state into confirmation
- confirmation must not depend on fragile re-validation without preserving upload context
- error states must fail clearly rather than silently

## Question Import

### Purpose
Bulk creation or ingestion of question/MCQ content.

### Contract Expectations
- import utilities must reference current question/option structures
- stale option imports or outdated entity assumptions must be corrected promptly
- import failures should be explicit and diagnosable
