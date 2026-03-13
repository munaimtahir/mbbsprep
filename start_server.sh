#!/usr/bin/env bash
set -euo pipefail

echo "Starting MedPrep development server at http://127.0.0.1:8000/"

if command -v python3 >/dev/null 2>&1; then
  exec python3 manage.py runserver
fi

exec python manage.py runserver
