# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal
import utils.model_utils


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0021_auto_20151130_2017'),
    ]

    operations = [
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('card_type', models.CharField(default='c', choices=[('d', 'Debit'), ('c', 'Credit')], max_length=1)),
                ('card_company', models.CharField(default='v', choices=[('v', 'VISA'), ('m', 'MASTERCARD'), ('i', 'INTERAC')], max_length=1)),
                ('card_method', models.CharField(default='c', choices=[('c', 'Chip'), ('m', 'Manual CP')], max_length=1)),
                ('MID', models.CharField(max_length=11)),
                ('TID', models.CharField(max_length=22)),
                ('REF', models.CharField(max_length=8)),
                ('batch', models.CharField(max_length=3)),
                ('RRN', models.CharField(blank=True, max_length=12)),
                ('APPR', models.CharField(max_length=6)),
                ('trace', models.CharField(max_length=1)),
                ('card_number', models.CharField(max_length=4)),
                ('amount', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=6)),
                ('AID', models.CharField(blank=True, max_length=14)),
                ('TVR', models.CharField(blank=True, max_length=14)),
                ('TSI', models.CharField(blank=True, max_length=5)),
                ('claim', models.ForeignKey(to='clients.Claim')),
            ],
            bases=(models.Model, utils.model_utils.FieldList),
        ),
    ]
