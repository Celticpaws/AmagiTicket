# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-03 12:49
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TicketsApp', '0038_auto_20160603_0820'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='group',
            new_name='m_department',
        ),
        migrations.RenameField(
            model_name='member',
            old_name='person',
            new_name='m_user',
        ),
        migrations.AddField(
            model_name='department',
            name='d_level',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='u_accesslevel',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='activity',
            name='at_timeinverted',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 3, 8, 49, 41, 448617)),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='t_reportmadeon',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 3, 8, 49, 41, 448617)),
        ),
    ]
