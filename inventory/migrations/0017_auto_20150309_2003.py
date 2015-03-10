# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0016_auto_20150217_1451'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdjustmentOrder',
            fields=[
                ('order_ptr', models.OneToOneField(serialize=False, to='inventory.Order', primary_key=True, auto_created=True, parent_link=True)),
                ('credit_value', models.DecimalField(decimal_places=2, max_digits=3, verbose_name='Credit Value', default=Decimal('0'))),
            ],
            options={
            },
            bases=('inventory.order',),
        ),
        migrations.AlterField(
            model_name='coverageorder',
            name='vendor',
            field=models.CharField(verbose_name='Vendor', max_length=32),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shoeorder',
            name='shoe_attributes',
            field=models.ForeignKey(to='inventory.ShoeAttributes', verbose_name='Shoe', null=True, blank=True, default=None),
        ),
        migrations.AlterField(
            model_name='shoeorder',
            name='shoe_attributes',
            field=models.ForeignKey(to='inventory.ShoeAttributes', verbose_name='Shoe', default=None),
            preserve_default=False,
        ),
    ]
