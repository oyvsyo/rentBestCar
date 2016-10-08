# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20161008_1724'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='manufacture',
            field=models.IntegerField(default=2000),
        ),
    ]
