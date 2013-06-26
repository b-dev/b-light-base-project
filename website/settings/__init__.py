import os

ENVIRONMENT = os.getenv("PRJ_ENV")

if not ENVIRONMENT:
    ENVIRONMENT = 'dev'

if ENVIRONMENT == 'production':
    from production import *
elif ENVIRONMENT == 'dev':
    from dev import *
elif ENVIRONMENT == 'staging':
    from staging import *
elif ENVIRONMENT == 'staging':
    from staging import *
elif ENVIRONMENT == 'test':
    from test import *
