# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0006_auto_20141124_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='payment_type',
            field=models.CharField(choices=[('Assignment', 'Assignment'), ('Non-assignment', 'Non-assignment')], max_length=15),
            preserve_default=True,
        ),
    ]
