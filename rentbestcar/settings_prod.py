import os
from raven.handlers.logging import SentryHandler
from raven.conf import setup_logging

SCHEDUL_DB_PASS = os.environ.get('SCHEDUL_DB_PASS')
SCHEDUL_DB_HOST = os.environ.get('SCHEDUL_DB_HOST')
DEBUG = False
ALLOWED_HOSTS = ['54.229.178.168']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'scheduling',
        'USER': 'postgres',
        'PASSWORD': SCHEDUL_DB_PASS,
        'HOST': SCHEDUL_DB_HOST,
        'PORT': '5432',
    }
}
BROKER_URL = "redis"
REDIS_HOST = "redis"
SCHEDUL_SENTRY_URL = os.getenv('SCHEDUL_SENTRY_URL', '')

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
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',  # all messages
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'sentry': {
            'level': 'INFO',  # only Info, Warning and Error messages
            'class': 'raven.handlers.logging.SentryHandler',
            'dsn': SCHEDUL_SENTRY_URL,
            'formatter': 'verbose',
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
            'handlers': ['console', 'sentry'],
            'propagate': True,
            'level': 'DEBUG',
        },
    }
}

SCHEDUL_SENTRY_URL = os.getenv('SCHEDUL_SENTRY_URL', '')

handler = SentryHandler(SCHEDUL_SENTRY_URL)
setup_logging(handler)
RAVEN_CONFIG = {
    'dsn': SCHEDUL_SENTRY_URL,
}

