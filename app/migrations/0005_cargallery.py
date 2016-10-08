# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_car_short_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarGallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image_description', models.CharField(default=b'image', max_length=100)),
                ('image', models.ImageField(default=b'', max_length=1024, upload_to=b'cargallery/')),
                ('car_id', models.ForeignKey(to='app.Car')),
            ],
        ),
    ]
