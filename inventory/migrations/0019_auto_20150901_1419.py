# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0018_auto_20150309_2013'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shoeattributes',
            options={'verbose_name_plural': 'Shoe attributes'},
        ),
    ]
