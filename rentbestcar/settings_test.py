DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'scheduling_test',
        'USER': 'scheduling_test',
        'PASSWORD': 'scheduling_test',
        'HOST': 'postgres_test',
        'PORT': '5432',
        'unicode_results': True,
        # 'OPTIONS': {'client_encoding': 'UTF8','default_transaction_isolation': 'read committed',}
    },
}
BROKER_URL = "redis_test"
REDIS_HOST = "redis_test"
