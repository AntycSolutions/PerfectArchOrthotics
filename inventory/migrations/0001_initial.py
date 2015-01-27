# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal
from utils import model_utils


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shoe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('image', models.ImageField(verbose_name='Image', blank=True, upload_to='inventory/shoes/%Y/%m/%d', null=True)),
                ('category', models.CharField(max_length=4, verbose_name='Category', blank=True, choices=[('wo', "Women's"), ('me', "Men's"), ('ju', 'Junior'), ('ki', 'Kids')])),
                ('size', models.CharField(max_length=4, verbose_name='Size', blank=True, choices=[(1, 1), (2, 2), (3.0, 3.0), (3.5, 3.5), (4.0, 4.0), (4.5, 4.5), (5.0, 5.0), (5.5, 5.5), (6.0, 6.0), (6.5, 6.5), (7.0, 7.0), (7.5, 7.5), (8.0, 8.0), (8.5, 8.5), (9.0, 9.0), (9.5, 9.5), (10.0, 10.0), (10.5, 10.5), (11.0, 11.0), (11.5, 11.5), (12.0, 12.0), (12.5, 12.5), (13.0, 13.0), (13.5, 13.5)])),
                ('availability', models.CharField(max_length=4, verbose_name='Availability', blank=True, choices=[('or', 'Orderable'), ('di', 'Discontinued')])),
                ('brand', models.CharField(max_length=32, verbose_name='Brand', blank=True)),
                ('style', models.CharField(max_length=32, verbose_name='Style', blank=True)),
                ('name', models.CharField(max_length=32, verbose_name='Name', blank=True)),
                ('sku', models.CharField(max_length=32, verbose_name='SKU', blank=True)),
                ('colour', models.CharField(max_length=32, verbose_name='Colour', blank=True)),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('credit_value', models.IntegerField(verbose_name='Credit Value', default=0)),
                ('quantity', models.IntegerField(verbose_name='Quantity', default=0)),
                ('cost', models.DecimalField(verbose_name='Cost', default=Decimal('0'), max_digits=6, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model, model_utils.FieldList),
        ),
    ]
