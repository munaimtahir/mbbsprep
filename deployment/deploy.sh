#!/usr/bin/env bash
# NON-OPERATIONAL PLACEHOLDER
# This repository intentionally does not provide a production deployment script yet.
# Do not treat this file as a deployable entrypoint.
#
# Canonical baseline CI only verifies:
# - python3 manage.py check --settings=medprep.settings_test
# - pytest -q tests/automated
# - node --check playwright config/spec files
#
# If real deployment automation is introduced, replace this file in a dedicated
# deployment change with matching governance/docs updates.

set -euo pipefail
echo "deployment/deploy.sh is a non-operational placeholder."
echo "See docs/30_repo/DEPLOYMENT_PLACEHOLDER_STATUS.md"
