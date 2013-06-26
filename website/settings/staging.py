from base import *

# IMPORT CMS SETTINGS
if CMS_ENABLED:
    from django_cms import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'ctmdbdj',                      # Or path to database file if using sqlite3.
        'USER': 'ctmdbuser',                      # Not used with sqlite3.
        'PASSWORD': 'ctmdb',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
}


MEDIA_URL = 'YOUR MEDIA URL'

SSL_ENABLED = True
SEND_BROKEN_LINK_EMAILS = False

# Local Cache Settings
# Enable for memcache backend
#CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
#CACHE_MIDDLEWARE_SECONDS = 300

INSTALLED_APPS += (
    'debug_toolbar',
    'django_extensions',
    #'product',#'prodotti',
    'main',
    'jumbo_product',
)