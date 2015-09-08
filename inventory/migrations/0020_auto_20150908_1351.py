# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0019_auto_20150901_1419'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shoeattributes',
            options={'verbose_name_plural': 'Shoe attributes', 'permissions': (('can_lookup_shoe_attributes', 'Can Lookup Shoe Attributes'),)},
        ),
    ]
