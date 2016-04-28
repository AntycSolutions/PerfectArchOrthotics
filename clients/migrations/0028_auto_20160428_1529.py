# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0027_itemhistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coverage',
            name='period',
            field=models.IntegerField(choices=[(12, '12 Rolling Months'), (24, '24 Rolling Months'), (36, '36 Rolling Months'), (1, 'Benefit Year'), (2, 'Calendar Year')], verbose_name='Period'),
        ),
    ]
