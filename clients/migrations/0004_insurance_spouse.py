# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_auto_20141123_1841'),
    ]

    operations = [
        migrations.AddField(
            model_name='insurance',
            name='spouse',
            field=models.ForeignKey(blank=True, to='clients.Dependent', null=True),
            preserve_default=True,
        ),
    ]
