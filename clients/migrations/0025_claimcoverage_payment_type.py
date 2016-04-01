# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0024_creditdivisor'),
    ]

    operations = [
        migrations.AddField(
            model_name='claimcoverage',
            name='payment_type',
            field=models.CharField(blank=True, choices=[('cas', 'Cash'), ('che', 'Cheque'), ('vis', 'VISA'), ('mas', 'MasterCard'), ('deb', 'Interac Debit')], max_length=3),
        ),
    ]
