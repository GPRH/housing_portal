"""
Django settings for housing-portal-prototype project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
import environ
from datetime import timedelta

from .base import *  # noqa

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'

# This ensures that Django will be able to detect a secure connection
# properly on Heroku.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# SECURITY CONFIGURATION
# ------------------------------------------------------------------------------
# See https://docs.djangoproject.com/en/dev/ref/middleware/#module-django.middleware.security
# and https://docs.djangoproject.com/en/dev/howto/deployment/checklist/#run-manage-py-check-deploy

# set this to 60 seconds and then to 518400 when you can prove it works
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    'DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
    'DJANGO_SECURE_CONTENT_TYPE_NOSNIFF', default=True)
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = env.bool('DJANGO_SECURE_SSL_REDIRECT', default=False)
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_SECURE = True

INSTALLED_APPS += ['gunicorn', ]


# STORAGE CONFIGURATION
# ------------------------------------------------------------------------------
# Uploaded Media Files
# ------------------------
# See: http://django-storages.readthedocs.io/en/latest/index.html
INSTALLED_APPS += ['storages', ]

AWS_ACCESS_KEY_ID = env('DJANGO_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('DJANGO_AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('DJANGO_AWS_STORAGE_BUCKET_NAME')
AWS_S3_ENDPOINT_URL = env('DJANGO_AWS_S3_ENDPOINT_URL')
AWS_AUTO_CREATE_BUCKET = False
AWS_QUERYSTRING_AUTH = False
S3_USE_SIGV4 = True
AWS_S3_REGION_NAME = 'nyc3'

# AWS cache settings, don't change unless you know what you're doing:
AWS_EXPIRY = 60 * 60 * 24 * 7

# TODO See: https://github.com/jschneier/django-storages/issues/47
# Revert the following and use str after the above-mentioned bug is fixed in
# either django-storage-redux or boto
control = 'max-age=%d, s-maxage=%d, must-revalidate' % (AWS_EXPIRY, AWS_EXPIRY)

AWS_HEADERS = {
    'Cache-Control': bytes(control, encoding='latin-1')
}

# URL that handles the media served from MEDIA_ROOT, used for managing
# stored files.
MEDIA_URL = (
    '%s/%s/' % (AWS_S3_ENDPOINT_URL, AWS_STORAGE_BUCKET_NAME)
)
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# EMAIL
# ------------------------------------------------------------------------------
# DEFAULT_FROM_EMAIL = env('DJANGO_DEFAULT_FROM_EMAIL', default='')

# EMAIL_SUBJECT_PREFIX = env(
#     'DJANGO_EMAIL_SUBJECT_PREFIX', default='Housing Portal')
# SERVER_EMAIL = env('DJANGO_SERVER_EMAIL', default=DEFAULT_FROM_EMAIL)

# INSTALLED_APPS += ['django_ses', ]
# EMAIL_BACKEND = 'django_ses.SESBackend'
# AWS_SES_ACCESS_KEY_ID = env('DJANGO_AWS_SES_ACCESS_KEY_ID')
# AWS_SES_SECRET_ACCESS_KEY = env('DJANGO_AWS_SES_SECRET_ACCESS_KEY')
# AWS_SES_REGION_NAME = env('DJANGO_AWS_SES_REGION_NAME', default='')
# AWS_SES_REGION_ENDPOINT = env("DJANGO_AWS_SES_REGION_ENDPOINT", default='')

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See:
# https://docs.djangoproject.com/en/dev/ref/templates/api/#django.template.loaders.cached.Loader
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader', ]),
]

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------

# Use the Heroku-style specification
# Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
DATABASES['default']['CONN_MAX_AGE'] = env.int('CONN_MAX_AGE', default=0)


# CACHING
# ------------------------------------------------------------------------------
REDIS_LOCATION = '{0}/{1}'.format(env('REDIS_URL',
                                      default='redis://redis:6379'), 0)

# Heroku URL does not pass the DB number, so we parse it in
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_LOCATION,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'IGNORE_EXCEPTIONS': True,  # mimics memcache behavior.
                                        # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
        }
    }
}

# raven sentry client
# See https://docs.sentry.io/clients/python/integrations/django/
INSTALLED_APPS += ['raven.contrib.django.raven_compat']
RAVEN_MIDDLEWARE = [
    'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware']
MIDDLEWARE = RAVEN_MIDDLEWARE + MIDDLEWARE

# Sentry Configuration
SENTRY_DSN = env.str('SENTRY_DSN')
SENTRY_CLIENT = 'raven.contrib.django.raven_compat.DjangoClient'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
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
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'django.security.DisallowedHost': {
            'level': 'ERROR',
            'handlers': ['console', 'sentry'],
            'propagate': False,
        },
    },
}

RAVEN_CONFIG = {
    'DSN': SENTRY_DSN
}

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
    'rest_framework.renderers.JSONRenderer'
]
