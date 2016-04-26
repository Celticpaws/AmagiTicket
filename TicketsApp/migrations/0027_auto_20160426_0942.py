# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-26 14:12
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TicketsApp', '0026_auto_20160418_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='t_viewers',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='activity',
            name='at_timeinverted',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 26, 9, 42, 41, 960877)),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='t_reportmadeon',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 26, 9, 42, 41, 960877)),
        ),
    ]
