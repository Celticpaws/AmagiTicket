# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-16 15:49
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TicketsApp', '0036_auto_20160516_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='at_timeinverted',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 16, 11, 49, 52, 381709)),
        ),
        migrations.AlterField(
            model_name='department',
            name='d_management',
            field=models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='d_superior', to='TicketsApp.Department'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='t_reportmadeon',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 16, 11, 49, 52, 381709)),
        ),
    ]
