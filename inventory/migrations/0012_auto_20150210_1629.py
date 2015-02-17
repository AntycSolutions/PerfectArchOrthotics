# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0011_order_credit_value'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='where',
        ),
        migrations.AddField(
            model_name='order',
            name='vendor',
            field=models.CharField(default='', blank=True, max_length=32, verbose_name='Vendor'),
            preserve_default=False,
        ),
    ]
