# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-11 13:26
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TicketsApp', '0017_ticket_t_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='at_timeinverted',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 11, 8, 56, 59, 288351)),
        ),
    ]