# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_auto_20150206_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='credit_value',
            field=models.IntegerField(default=0, verbose_name='Credit Value'),
            preserve_default=True,
        ),
    ]
