# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-09 18:04
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TicketsApp', '0056_auto_20160609_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='ttype',
            name='ty_icon',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='at_timeinverted',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 9, 14, 4, 27, 112962)),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='t_reportmadeon',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 9, 14, 4, 27, 112962)),
        ),
    ]
