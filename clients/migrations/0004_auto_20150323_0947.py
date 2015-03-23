# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_claimcoverage_actual_paid_date_same_as_insurance_paid_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insurance',
            name='contract_number',
            field=models.CharField(max_length=128, blank=True, verbose_name='ID Number'),
            preserve_default=True,
        ),
    ]
