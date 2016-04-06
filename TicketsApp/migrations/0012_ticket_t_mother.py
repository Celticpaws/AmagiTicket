# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-06 20:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TicketsApp', '0011_auto_20160406_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='t_mother',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='t_mother_of', to='TicketsApp.Ticket'),
        ),
    ]
