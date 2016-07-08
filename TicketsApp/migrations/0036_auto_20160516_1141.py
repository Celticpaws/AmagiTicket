# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-16 15:41
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TicketsApp', '0035_auto_20160516_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='at_timeinverted',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 16, 11, 41, 39, 296926)),
        ),
        migrations.AlterField(
            model_name='department',
            name='d_management',
            field=models.ForeignKey(default=0, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='d_superior', to='TicketsApp.Department'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='t_reportmadeon',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 16, 11, 41, 39, 296926)),
        ),
    ]