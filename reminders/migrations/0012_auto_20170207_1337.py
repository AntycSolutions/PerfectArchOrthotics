# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-02-07 20:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reminders', '0011_auto_20170203_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderarrivedmessagelog',
            name='msg_type',
            field=models.CharField(choices=[('t', 'Text'), ('e', 'Email'), ('c', 'Call')], max_length=1),
        ),
        migrations.AlterField(
            model_name='unpaidclaimmessagelog',
            name='msg_type',
            field=models.CharField(choices=[('t', 'Text'), ('e', 'Email'), ('c', 'Call')], max_length=1),
        ),
    ]
