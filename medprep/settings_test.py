# ruff: noqa: I001
from .settings import *  # noqa: F403


PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
MEDIA_ROOT = BASE_DIR / 'test_media'  # noqa: F405
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']
