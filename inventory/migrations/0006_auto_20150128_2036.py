# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import utils.model_utils


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_auto_20150127_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoe',
            name='image',
            field=utils.model_utils.ImageField(blank=True, verbose_name='Image', upload_to='inventory/shoes/%Y/%m/%d', null=True),
            preserve_default=True,
        ),
    ]
