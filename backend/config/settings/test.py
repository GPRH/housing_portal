"""
Test settings housing portal project.

- Used to run tests fast on the continuous integration server and locally
"""

from .base import *  # noqa


# DEBUG
# ------------------------------------------------------------------------------
# Turn debug off so tests run faster
DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = True

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env.str('DJANGO_SECRET_KEY', default='CHANGEME!!!')

DOMAIN = env.str('DOMAIN', default='http://localhost:8000')

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': env.str('POSTGRES_DB'),
        'USER': env.str('POSTGRES_USER'),
        'PASSWORD': env.str('POSTGRES_PASS'),
        'HOST': env.str('POSTGRES_HOST', 'postgres'),
        'PORT': 5432,
    },
}
# Mail settings
# ------------------------------------------------------------------------------
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025

# In-memory email backend stores messages in django.core.mail.outbox
# for unit testing purposes
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# CACHING
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
}

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'


# PASSWORD HASHING
# ------------------------------------------------------------------------------
# Use fast password hasher so tests run faster
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# TEMPLATE LOADERS
# ------------------------------------------------------------------------------
# Keep templates in memory so tests run faster
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ['django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ], ],
]

MEDIA_ROOT = str(APPS_DIR('media/test'))


EXPORTS_DIR = 'media/test/exports/'

LANGUAGE_CODE = 'en'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['console'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        }
    },
}

CONTACT_FORM_AUTH_TOKEN = 'test_auth_token'
CONTACT_FORM_RECIPIENTS = ['test1@test.org', 'test2@test.org']

LOCAL_EPSG = 3857
