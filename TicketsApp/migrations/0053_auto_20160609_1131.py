# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-09 15:31
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TicketsApp', '0052_auto_20160609_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='at_timeinverted',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 9, 11, 31, 26, 992350)),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='t_reportmadeon',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 9, 11, 31, 26, 989349)),
        ),
    ]