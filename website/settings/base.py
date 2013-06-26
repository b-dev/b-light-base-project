import os
ugettext = lambda s: s

PRJ_ENV = os.environ['PRJ_ENV']
PRJ_NAME = os.environ['PRJ_NAME']
PRJ_DB = os.environ['PRJ_DB']
PRJ_USER = os.environ['PRJ_USER']
PRJ_PASS = os.environ['PRJ_PASS']

PROJECT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),'../')

DEBUG = False

ADMINS=(
    ('Marco Minutoli', 'supporto@marcominutoli.it'),
    ('Simone Cittadini', 'simone@sig-c.com'),
)
MANAGERS = ADMINS

# Email settings
EMAIL_HOST = ''
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = ''
SERVER_EMAIL = ''
EMAIL_SUBJECT_PREFIX = ""

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'Europe/Rome'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'it'
LANGUAGES = (
    ('it', ugettext('Italian')),
    ('en', ugettext('English')),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
USE_L10N = True

# Static files are for things like your applications' css files, javascript files, images, etc.
STATIC_URL = "/static/"
MEDIA_URL = "/media/"

# Media files are typically user or admin uploadable files
MEDIA_ROOT = os.path.join(PROJECT_PATH, "media/")
STATIC_ROOT = os.path.join(PROJECT_PATH, "static/")

# URL prefix for admin media -- CSS, JavaScript and images.
ADMIN_MEDIA_PREFIX = STATIC_URL + "admin/" #'/media/'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates'),
)

STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, "assets/"),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ['PRJ_SECRET_KEY']

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    "sekizai.context_processors.sekizai",
]

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
]

ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.markup',
    'django.contrib.staticfiles',

    'sekizai',
    'crispy_forms',
    'django_select2',
    'south',
    'website',
)

ANONYMOUS_USER_ID = -1
APPEND_SLASH = True

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
