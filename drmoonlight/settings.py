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

BROKER_URL = os.environ.get('BROKER_URL', 'amqp://guest:guest@localhost//')

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

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
]

PROJECT_APPS = [
    'apps.accounts',
    'apps.shifts',
    'apps.main',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'djoser',
    'storages',
    'django_extensions',
    'django_filters',
    'django_fsm',
    'fsm_admin',
    'constance',
    'constance.backends.database',
    'raven.contrib.django.raven_compat',
]

if DEBUG_EMAIL:  # pragma: no cover
    THIRD_PARTY_APPS.append('db_email_backend')

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

# MIDDLEWARE CONFIGURATION
MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
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
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
        'djangorestframework_camel_case.parser.CamelCaseFormParser',
        'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
    ),
}

DJOSER = {
    'DOMAIN': os.environ.get('DJOSER_DOMAIN', 'localhost:8000'),
    'SITE_NAME': 'SkinIQ',
    'PASSWORD_RESET_CONFIRM_URL': os.environ.get(
        # TODO: change this url
        'DJOSER_PASSWORD_RESET_CONFIRM_URL',
        '/confirm/{uid}/{token}'),
    'ACTIVATION_URL': os.environ.get(
        'DJOSER_ACTIVATION_URL',
        # TODO: change this url
        '/activate/{uid}/{token}'),
    'SEND_ACTIVATION_EMAIL': True,
    # 'SERIALIZERS': {
    #     'user_registration': 'apps.accounts.serializers.doctor.RegisterDoctorSerializer',
    # },
}

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

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
            '--ipdb',
            '--ipdb-failures',
            '--nocapture',
        ]

    CELERY_ALWAYS_EAGER = True
    CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# CONSTANCE SETTINGS
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CONSTANCE_CONFIG = {

}

FSM_ADMIN_FORCE_PERMIT = True
