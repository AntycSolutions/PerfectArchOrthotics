# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_auto_20150323_0947'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='cost',
            field=models.IntegerField(verbose_name='Cost', default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='unit_price',
            field=models.IntegerField(verbose_name='Retail', default=0),
            preserve_default=True,
        ),
    ]
