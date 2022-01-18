# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2022-01-15 21:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0058_auto_20220115_1414'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='company',
            field=models.CharField(choices=[('pa', 'Perfect Arch'), ('pc', 'PC Medical'), ('bb', 'Brace and Body')], default='pa', max_length=2),
        ),
    ]
