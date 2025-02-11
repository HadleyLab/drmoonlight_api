"""
Django settings for drmoonlight project.

Generated by 'django-admin startproject' using Django 1.11.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os, sys
import dj_database_url


# Celery settings
from celery.schedules import crontab

CELERY_BROKER_URL = os.environ.get('BROKER_URL', 'redis://redis/1')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


CELERY_BEAT_SCHEDULE = {
    'daily-make-confirmed-applications-completed': {
        'task': 'apps.shifts.tasks.'
                'daily_make_confirmed_applications_completed_for_ended_shifts',
        'schedule': crontab(minute='0', hour='0'),
    },
}

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'exk2#v+-54&bux=80=$zpfn8xa8-=2n+s9$ood3ja^i!)!!swo'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
DEBUG_EMAIL = os.environ.get('DEBUG_EMAIL', 'False') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# EMAIL settings
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '25'))
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == "True"
DEFAULT_FROM_EMAIL = os.environ.get(
    "DEFAULT_FROM_EMAIL", "no-reply@example.com")

POSTMARK_API_KEY = os.environ.get('POSTMARK_API_KEY')
POSTMARK_SENDER = os.environ.get('POSTMARK_SENDER')

if DEBUG_EMAIL:  # pragma: no cover
    EMAIL_BACKEND = 'db_email_backend.backend.DBEmailBackend'  # pragma: no cover
elif POSTMARK_API_KEY:  # pragma: no cover
    EMAIL_BACKEND = 'postmark.django_backend.EmailBackend'  # pragma: no cover
    DEFAULT_FROM_EMAIL = POSTMARK_SENDER  # pragma: no cover
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Application definition

# APP CONFIGURATION
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

PROJECT_APPS = [
    'apps.accounts',
    'apps.shifts',
    'apps.main',
]

THIRD_PARTY_APPS = [
    'dbmail',
    'contrib.dbmail_patch',
    'ckeditor',
    'channels',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'storages',
    'django_extensions',
    'django_filters',
    'django_fsm',
    'fsm_admin',
    'constance',
    'constance.backends.database',
    'raven.contrib.django.raven_compat',
    'corsheaders',
    'sorl.thumbnail',
]

if DEBUG_EMAIL:  # pragma: no cover
    THIRD_PARTY_APPS.append('db_email_backend')

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIGRATION_MODULES = {
    'dbmail': 'contrib.external_migrations.dbmail',
}

# MIDDLEWARE CONFIGURATION
MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
]

ROOT_URLCONF = 'drmoonlight.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(BASE_DIR, 'templates')],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
},
]

WSGI_APPLICATION = 'drmoonlight.wsgi.application'

# CUSTOM USER ACCOUNT MODEL
AUTH_USER_MODEL = 'accounts.User'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(),
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# DRF SETTINGS
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'libs.drf_kebab_case.renderers.KebabCaseJSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'libs.drf_kebab_case.parsers.KebabCaseJSONParser',
        'libs.drf_kebab_case.parsers.KebabCaseFormParser',
        'libs.drf_kebab_case.parsers.KebabCaseMultiPartParser',
    ),
}

DOMAIN = os.environ.get('DOMAIN', 'localhost:3000')
if os.environ.get('HTTPS', 'False') == 'True':
    PROTOCOL = 'https'  # pragma: no cover
else:
    PROTOCOL = 'http'  # pragma: no cover

SITE_NAME = os.environ.get('SITE_NAME', 'Dr. Moonlight')
SITE_ID = 1

DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': os.environ.get(
        'DJOSER_PASSWORD_RESET_CONFIRM_URL',
        '#/confirm/{uid}/{token}'),
    'ACTIVATION_URL': os.environ.get(
        'DJOSER_ACTIVATION_URL',
        '#/activate/{uid}/{token}'),
    'SEND_ACTIVATION_EMAIL': True,
}

CHANNEL_REDIS_URL = os.environ.get('REDIS_URL', 'redis://redis/2')
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [CHANNEL_REDIS_URL],
        },
        "ROUTING": "drmoonlight.routing.channel_routing",
    },
}


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake'
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
STATIC_ROOT = os.path.join(os.path.dirname(PROJECT_ROOT), 'static')

RAVEN_CONFIG = {
    'dsn': os.environ.get('SENTRY_DSN', '')
}

# LOGGING SETTINGS
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'factory': {
            'handlers': ['null'],
            'propagate': False,
            'level': 'DEBUG',
        },
    }
}

# TESTING SETTINGS
RUN_TESTS = 'test' in sys.argv
IS_CI = os.environ.get('IS_CI', 'False') == 'True'

if RUN_TESTS:
    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
    NOSE_ARGS = ['--with-doctest', '--rednose']

    if not IS_CI:
        NOSE_ARGS += [
            '--nocapture',
        ]

    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True

    CHANNEL_LAYERS['default']['BACKEND'] = "asgiref.inmemory.ChannelLayer"
    CHANNEL_LAYERS['default']['CONFIG'] = {
        'capacity': 10000,
    }

    DATABASES = {
        'default': dj_database_url.config(
            engine='libs.postgresql_psycopg2_for_tests')
    }


AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', None)
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', None)


USE_S3 = AWS_ACCESS_KEY_ID is not None and \
         AWS_SECRET_ACCESS_KEY is not None and \
         AWS_STORAGE_BUCKET_NAME is not None

if USE_S3:
    DEFAULT_FILE_STORAGE = 'drmoonlight.awsstorage.MediaStorage'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# CONSTANCE SETTINGS
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CONSTANCE_CONFIG = {

}

FSM_ADMIN_FORCE_PERMIT = True

CORS_ORIGIN_ALLOW_ALL = DEBUG
