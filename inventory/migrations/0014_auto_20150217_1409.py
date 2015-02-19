# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0013_auto_20150213_1212'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='credit_value',
        ),
        migrations.RemoveField(
            model_name='order',
            name='order_type',
        ),
        migrations.RemoveField(
            model_name='order',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shoe_attributes',
        ),
        migrations.RemoveField(
            model_name='order',
            name='vendor',
        ),
    ]
