#!/usr/bin/env bash
set -euo pipefail

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-medprep.settings_playwright}"

python3 manage.py migrate --noinput --settings="$DJANGO_SETTINGS_MODULE"
python3 manage.py seed_test_environment --settings="$DJANGO_SETTINGS_MODULE"
exec python3 manage.py runserver 127.0.0.1:8000 --settings="$DJANGO_SETTINGS_MODULE"
