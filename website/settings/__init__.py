import os
from os.path import abspath, dirname

# Absolute filesystem path to the Django project directory:
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# Absolute filesystem path to the top-level project folder:
SITE_ROOT = dirname(DJANGO_ROOT)

from _set_local_env_vars import import_env_vars
import_env_vars(SITE_ROOT)

ENVIRONMENT = os.getenv("PRJ_ENV")

if not ENVIRONMENT:
    ENVIRONMENT = 'dev'

if ENVIRONMENT == 'production':
    from .production import *
elif ENVIRONMENT == 'dev':
    from .dev import *
elif ENVIRONMENT == 'staging':
    from .staging import *
elif ENVIRONMENT == 'test':
    from .test import *
