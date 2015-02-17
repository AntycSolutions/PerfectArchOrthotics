# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0012_auto_20150210_1629'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='shoe',
        ),
        migrations.AddField(
            model_name='order',
            name='shoe_attributes',
            field=models.ForeignKey(verbose_name='Shoe', blank=True, null=True, to='inventory.ShoeAttributes'),
            preserve_default=True,
        ),
    ]
