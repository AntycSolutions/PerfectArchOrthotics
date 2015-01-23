# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoe',
            name='name',
            field=models.CharField(verbose_name='Name', max_length=32),
            preserve_default=True,
        ),
    ]
