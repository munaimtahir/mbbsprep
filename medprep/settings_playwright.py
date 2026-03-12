# ruff: noqa: I001
from .settings_test import *  # noqa: F403


DATABASES['default']['NAME'] = BASE_DIR / 'playwright.sqlite3'  # noqa: F405
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']
