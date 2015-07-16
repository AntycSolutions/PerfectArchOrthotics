# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0008_auto_20150506_1222'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClaimAttachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attachment', models.FileField(upload_to='clients/claim_packages/%Y/%m/%d', verbose_name='Attachment')),
                ('claim', models.ForeignKey(to='clients.Claim')),
            ],
        ),
    ]
