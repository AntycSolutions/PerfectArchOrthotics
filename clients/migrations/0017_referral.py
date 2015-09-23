# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0016_auto_20150908_1351'),
    ]

    operations = [
        migrations.CreateModel(
            name='Referral',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('claims', models.ManyToManyField(to='clients.Claim')),
                ('client', models.ForeignKey(to='clients.Client')),
            ],
        ),
    ]
