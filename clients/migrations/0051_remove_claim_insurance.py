# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2018-11-03 21:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0050_auto_20181103_1431'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='claim',
            name='insurance',
        ),
    ]
