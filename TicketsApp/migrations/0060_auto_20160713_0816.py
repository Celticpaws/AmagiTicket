# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-13 12:16
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TicketsApp', '0059_auto_20160621_0817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='at_timeinverted',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 13, 8, 16, 25, 152951)),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='t_reportmadeon',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 13, 8, 16, 25, 150949)),
        ),
    ]
