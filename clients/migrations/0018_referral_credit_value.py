# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0017_referral'),
    ]

    operations = [
        migrations.AddField(
            model_name='referral',
            name='credit_value',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=3, verbose_name='Credit Value'),
        ),
    ]
