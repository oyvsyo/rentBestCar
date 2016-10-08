# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='price',
            field=models.IntegerField(default=30),
        ),
        migrations.AlterField(
            model_name='car',
            name='description',
            field=models.CharField(max_length=5048),
        ),
    ]
