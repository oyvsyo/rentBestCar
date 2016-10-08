import os
from raven.handlers.logging import SentryHandler
from raven.conf import setup_logging
DEBUG = False
ALLOWED_HOSTS = ['54.194.144.54']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'scheduling_stage',
        'USER': 'scheduling_stage',
        'PASSWORD': 'scheduling_stage',
        'HOST': 'postgres_stage',
        'PORT': '5432',
        'unicode_results': True,
        # 'OPTIONS': {'client_encoding': 'UTF8','default_transaction_isolation': 'read committed',}
    },
}
BROKER_URL = "redis_stage"
REDIS_HOST = "redis_stage"

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
