#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from celery import task
from datetime import datetime

import logging
logger = logging.getLogger(__name__)


@task()
def every_day():
    """
    Every day celery worker for creating periodic RangeSlots and BinSlots.
    :return: None
    """
    logger.info('[ EVERY_DAY ] [ %s ]' % str(datetime.now().time()))
