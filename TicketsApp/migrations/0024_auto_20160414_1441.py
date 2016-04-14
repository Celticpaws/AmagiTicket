# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-14 19:11
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TicketsApp', '0023_auto_20160414_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='at_timeinverted',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 14, 14, 41, 7, 322318)),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='t_isincident',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='t_reportmadeon',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 14, 14, 41, 7, 322318)),
        ),
    ]