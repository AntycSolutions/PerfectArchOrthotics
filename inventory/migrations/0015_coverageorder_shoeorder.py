# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0014_auto_20150217_1409'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoverageOrder',
            fields=[
                ('order_ptr', models.OneToOneField(auto_created=True, to='inventory.Order', serialize=False, parent_link=True, primary_key=True)),
                ('order_type', models.CharField(max_length=4, choices=[('o', 'Orthotics'), ('cs', 'Compression Stockings'), ('os', 'Orthopedic Shoes'), ('bs', 'Back Support')], verbose_name='Order Type')),
                ('quantity', models.IntegerField(default=0, verbose_name='Quantity')),
                ('credit_value', models.IntegerField(default=0, verbose_name='Credit Value')),
                ('vendor', models.CharField(max_length=32, verbose_name='Vendor', blank=True)),
            ],
            options={
            },
            bases=('inventory.order',),
        ),
        migrations.CreateModel(
            name='ShoeOrder',
            fields=[
                ('order_ptr', models.OneToOneField(auto_created=True, to='inventory.Order', serialize=False, parent_link=True, primary_key=True)),
                ('order_type', models.CharField(default='s', max_length=4, choices=[('s', 'Shoe')], verbose_name='Order Type')),
                ('shoe_attributes', models.ForeignKey(verbose_name='Shoe', null=True, to='inventory.ShoeAttributes', blank=True)),
            ],
            options={
            },
            bases=('inventory.order',),
        ),
    ]
