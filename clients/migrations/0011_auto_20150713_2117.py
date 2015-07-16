# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0010_auto_20150713_1854'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='claim',
            name='claim_package2',
        ),
        migrations.AddField(
            model_name='claimattachment',
            name='claim',
            field=models.ForeignKey(to='clients.Claim', default=63),
            preserve_default=False,
        ),
    ]
