# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_auto_20150126_1447'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='shoeattributes',
            unique_together=set([('shoe', 'size')]),
        ),
    ]
