# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-03 14:23
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TicketsApp', '0040_auto_20160603_0922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='at_timeinverted',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 3, 10, 23, 2, 755092)),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='t_reportmadeon',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 3, 10, 23, 2, 755092)),
        ),
    ]