# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2022-02-10 23:57
from __future__ import unicode_literals

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0060_auto_20220127_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='deposit',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=6, verbose_name='Deposit'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='payment_made',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=6, verbose_name='Payment Made'),
        ),
    ]
