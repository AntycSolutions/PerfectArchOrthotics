# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0009_claimattachment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='claimattachment',
            name='claim',
        ),
        migrations.AddField(
            model_name='claim',
            name='claim_package2',
            field=models.ManyToManyField(to='clients.ClaimAttachment'),
        ),
    ]
