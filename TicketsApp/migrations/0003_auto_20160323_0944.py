# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-23 14:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TicketsApp', '0002_auto_20160323_0943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='u_email',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
