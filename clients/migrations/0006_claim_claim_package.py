# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0005_auto_20150325_2322'),
    ]

    operations = [
        migrations.AddField(
            model_name='claim',
            name='claim_package',
            field=models.FileField(upload_to='clients/claim_packages/%Y/%m/%d', null=True, verbose_name='Claim Package', blank=True),
            preserve_default=True,
        ),
    ]
