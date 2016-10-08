# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1024)),
                ('description', models.CharField(max_length=2048)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(default=b'0', max_length=64, choices=[(b'0', 'Zero'), (b'1', 'One'), (b'2', 'Two'), (b'3', 'Tree')])),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=1024)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('userprofile_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='app.UserProfile')),
                ('insurance', models.CharField(max_length=1024)),
            ],
            bases=('app.userprofile',),
        ),
        migrations.CreateModel(
            name='Renter',
            fields=[
                ('userprofile_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='app.UserProfile')),
                ('field', models.CharField(max_length=1024)),
            ],
            bases=('app.userprofile',),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='transaction',
            name='owner',
            field=models.ForeignKey(to='app.Owner'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='renter',
            field=models.ForeignKey(to='app.Renter'),
        ),
        migrations.AddField(
            model_name='car',
            name='owner',
            field=models.ForeignKey(to='app.Owner'),
        ),
    ]
