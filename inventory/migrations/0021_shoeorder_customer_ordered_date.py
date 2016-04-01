# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0020_auto_20150908_1351'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoeorder',
            name='customer_ordered_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
