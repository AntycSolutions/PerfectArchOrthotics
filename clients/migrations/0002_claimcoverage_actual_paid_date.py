# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='claimcoverage',
            name='actual_paid_date',
            field=models.DateField(verbose_name='Actual Paid Date', null=True, blank=True),
            preserve_default=True,
        ),
    ]
