# -*- coding: utf-8 -*-
import os

# Constants for RangeSlot.type
TRANSACTION_STATES = (
    ('0', u'Zero'),              # description
    ('1', u'One'),    # description
    ('2', u'Two'),          # description
    ('3', u'Tree'),   # description
)

# DateTime format
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# for api gateway workers
RUN_ENV = os.environ.get('RUN_ENV')

# Rabbit credential
RABBITMQ_USER = os.environ.get('RABBITMQ_DEFAULT_USER')
RABBITMQ_PASS = os.environ.get('RABBITMQ_DEFAULT_PASS')
RABBITMQ_HOST = 'api.preply.org'

if RUN_ENV == 'PROD':
    prefix = 'prod_'
    RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST')
elif RUN_ENV == 'STAGE':
    prefix = 'stage_'
elif RUN_ENV == 'TEST':
    prefix = 'test_'
else:
    prefix = 'dev_'

SERVICE_NAME_TIMESLOT = prefix + 'timeslot'
SERVICE_NAME_TIMESLOT_SEARCH = prefix + 'timeslot_search'
