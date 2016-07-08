# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-09 13:06
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TicketsApp', '0042_auto_20160609_0901'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ac_name', models.CharField(max_length=50)),
                ('ac_next_state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ac_s_next', to='TicketsApp.State')),
                ('ac_state_apply', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ac_s_actual', to='TicketsApp.State')),
            ],
        ),
        migrations.AlterField(
            model_name='activity',
            name='at_timeinverted',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 9, 9, 6, 16, 750278)),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='t_reportmadeon',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 9, 9, 6, 16, 748277)),
        ),
    ]