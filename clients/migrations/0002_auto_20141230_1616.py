# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='postal_code',
            field=models.CharField(verbose_name='Postal Code', blank=True, max_length=7),
            preserve_default=True,
        ),
    ]
