# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2016-11-11 02:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reminders', '0005_auto_20161110_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claimreminder',
            name='created',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='orderreminder',
            name='created',
            field=models.DateField(),
        ),
    ]