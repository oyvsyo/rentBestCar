"""
Django settings for scheduling project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import djcelery
djcelery.setup_loader()
from celery.schedules import crontab
from datetime import timedelta
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1!vgz*)s(2rofl*qrj-2kqz6=vxm__fij$_uv)ok(8h#=5i8*4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'djsupervisor',
    'tastypie',
    'django_extensions',
    'raven.contrib.django.raven_compat',
    'djcelery',
)

MIDDLEWARE_CLASSES = (
    'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
    'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'rentbestcar.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'scheduling.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'rentbestcar_dev',
        'USER': 'rentbestcar_dev',
        'PASSWORD': 'rentbestcar_dev',
        'HOST': 'postgres_dev',
        'PORT': '5432',
        'unicode_results': True,
        # 'OPTIONS': {'client_encoding': 'UTF8','default_transaction_isolation': 'read committed',}
    },
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

BROKER_URL = "redis_dev"
BROKER_BACKEND = "redis"
REDIS_HOST = "redis_dev"
REDIS_PORT = 6379

CELERYBEAT_SCHEDULE = {
    # Executes everyday morning at 6:30 A.M
    'add-every-day-morning': {
        'task': 'app.tasks.every_day',
        'schedule': crontab(hour=6, minute=30),
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join("static/")
# STATICFILES_DIRS = (
#     # os.path.join(BASE_DIR, "static_in_pro", "our_static"),
#     # os.path.join(BASE_DIR, "app", "static"),
#     # '/var/www/static/',
# )

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },

    'handlers': {
        'null': {
            'level': 'INFO',
            'class': 'logging.NullHandler',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO', # all messages
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },

    },
    'loggers': {
        'django': {
            'handlers': ['null', 'console'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'app': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
    }
}

SERVER_ENVIRONMENT = os.getenv('RUN_ENV', '')
if SERVER_ENVIRONMENT == 'PROD':
    from settings_prod import *

if SERVER_ENVIRONMENT == 'STAGE':
    from settings_stage import *

if SERVER_ENVIRONMENT == 'TEST':
    from settings_test import *