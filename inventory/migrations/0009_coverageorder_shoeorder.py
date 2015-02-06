# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_auto_20150206_1323'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoverageOrder',
            fields=[
                ('order_ptr', models.OneToOneField(to='inventory.Order', primary_key=True, serialize=False, auto_created=True, parent_link=True)),
                ('where', models.CharField(verbose_name='Where', blank=True, max_length=32)),
                ('quantity', models.IntegerField(verbose_name='Quantity', default=0)),
            ],
            options={
            },
            bases=('inventory.order',),
        ),
        migrations.CreateModel(
            name='ShoeOrder',
            fields=[
                ('order_ptr', models.OneToOneField(to='inventory.Order', primary_key=True, serialize=False, auto_created=True, parent_link=True)),
                ('shoe', models.ForeignKey(to='inventory.Shoe', blank=True, verbose_name='Shoe', null=True)),
            ],
            options={
            },
            bases=('inventory.order',),
        ),
    ]
