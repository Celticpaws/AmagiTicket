# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-09 15:28
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TicketsApp', '0048_auto_20160609_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='at_timeinverted',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 9, 11, 28, 29, 418326)),
        ),
        migrations.AlterField(
            model_name='state',
            name='s_workflow',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='TicketsApp.Workflow'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='t_reportmadeon',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 9, 11, 28, 29, 415325)),
        ),
    ]
