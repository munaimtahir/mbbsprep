import os

def config(key, default=None, cast=None):
    """Simple replacement for python-decouple config function"""
    value = os.environ.get(key, default)
    if cast and value is not None:
        if cast == bool:
            return str(value).lower() in ('true', '1', 'yes', 'on')
        elif cast == lambda v: [s.strip() for s in v.split(',')]:
            return [s.strip() for s in str(value).split(',')]
        else:
            return cast(value)
    return value