# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-27 19:07
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TicketsApp', '0028_auto_20160426_1301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='at_timeinverted',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 27, 14, 37, 31, 790203)),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='t_reportmadeon',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 27, 14, 37, 31, 774580)),
        ),
    ]
