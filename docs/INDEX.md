# MedPrep Documentation Index

This documentation pack establishes the governance, contracts, workflows, and repository standards for the **MedPrep / mbbsprep** Django project.

## Purpose

This pack exists to protect the repository after the verified v1 baseline was reached. It provides a stable reference for:

- project purpose and scope
- architecture and current boundaries
- development guardrails
- change control
- internal technical contracts
- public and staff workflows
- repository structure and cleanup decisions
- AI-agent operating rules

## How to Use This Pack

Read documents in this order:

1. `README.md`
2. `docs/INDEX.md`
3. `docs/00_governance/*`
4. `docs/30_repo/REPOSITORY_TRUTH_MAP.md`
5. code (`core/`, `staff/`, `medprep/`, `templates/`, `static/`)
6. `tests/automated/*`
7. only then use archive/legacy paths (`docs/archive/`, `tests/legacy/`, `scripts/legacy/`, `archive/`)

Governance lock additions:

- `docs/00_governance/ANTI_DRIFT_RULES.md`
- `docs/30_repo/REPOSITORY_TRUTH_MAP.md`
- `docs/30_repo/ROOT_STRUCTURE_STANDARD.md`
- `docs/30_repo/CLEANUP_EXECUTION_PLAN.md`
- `docs/30_repo/GOVERNANCE_LOCK_PASS_REPORT.md`
- `docs/30_repo/LOCAL_DATABASE_ARTIFACT_POLICY.md`
- `docs/30_repo/DEPLOYMENT_PLACEHOLDER_STATUS.md`
- `docs/30_repo/CI_BASELINE.md`
- `docs/30_repo/ARCHIVE_USAGE_RULES.md`
- `docs/30_repo/FINAL_BASELINE_LOCK_REPORT.md`

## Source of Truth Rule

When documentation and code disagree, the **current verified codebase** is the source of truth. Documentation must then be updated to match reality.
