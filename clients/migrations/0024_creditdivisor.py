# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0023_auto_20160106_1135'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreditDivisor',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('value', models.DecimalField(default=Decimal('0'), decimal_places=2, max_digits=5)),
                ('created', models.DateTimeField()),
            ],
        ),
    ]
