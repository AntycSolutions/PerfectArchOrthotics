# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import utils.model_utils


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
        ('inventory', '0006_auto_20150128_2036'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('order_type', models.CharField(verbose_name='Order Type', choices=[('o', 'Orthotics'), ('cs', 'Compression Stockings'), ('os', 'Orthopedic Shoes'), ('bs', 'Back Support'), ('s', 'Shoes')], max_length=4, blank=True)),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('ordered_date', models.DateField(null=True, verbose_name='Ordered Date', blank=True)),
                ('arrived_date', models.DateField(null=True, verbose_name='Arrived Date', blank=True)),
                ('dispensed_date', models.DateField(null=True, verbose_name='Dispensed Date', blank=True)),
                ('where', models.CharField(verbose_name='Where', max_length=32, blank=True)),
                ('quantity', models.IntegerField(verbose_name='Quantity', default=0)),
                ('claimant', models.ForeignKey(to='clients.Person', verbose_name='Claimant')),
                ('shoe', models.ForeignKey(null=True, to='inventory.Shoe', verbose_name='Shoe', blank=True)),
            ],
            options={
            },
            bases=(models.Model, utils.model_utils.FieldList),
        ),
    ]
