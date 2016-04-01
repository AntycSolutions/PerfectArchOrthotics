# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0025_claimcoverage_payment_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('notes', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(to='clients.Client')),
            ],
        ),
    ]
