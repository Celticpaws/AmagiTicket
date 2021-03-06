# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-13 19:39
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TicketsApp', '0019_auto_20160411_0927'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='u_cancreatetickets',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='activity',
            name='at_timeinverted',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 13, 15, 9, 40, 167739)),
        ),
        migrations.AlterField(
            model_name='archive',
            name='a_route',
            field=models.FileField(upload_to=''),
        ),
    ]
