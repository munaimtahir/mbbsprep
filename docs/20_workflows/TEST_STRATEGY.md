# Test Strategy

## Philosophy

The project uses a **practical protection strategy**:

- smoke tests ensure routes/pages load
- behavioral tests protect the most important workflows

## Current Priority Coverage

Highest-value coverage areas include:

1. authentication
2. dashboard access
3. profile edit behavior
4. quiz start/session/result flow
5. payment proof and staff payment review branching
6. question-bank filtering behavior
7. representative staff CRUD behavior
8. bulk user upload workflow
9. staff question create flow
10. topic bulk upload flow
11. management command import behavior for questions/options

## Validation Minimum

After moderate or major work, run:

- `python3 manage.py check --settings=medprep.settings_test`
- `pytest -q tests/automated`
