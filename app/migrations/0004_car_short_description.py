# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_car_manufacture'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='short_description',
            field=models.CharField(default=b'short_description', max_length=200),
        ),
    ]
