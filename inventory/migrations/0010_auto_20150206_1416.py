# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_coverageorder_shoeorder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coverageorder',
            name='order_ptr',
        ),
        migrations.DeleteModel(
            name='CoverageOrder',
        ),
        migrations.RemoveField(
            model_name='shoeorder',
            name='order_ptr',
        ),
        migrations.RemoveField(
            model_name='shoeorder',
            name='shoe',
        ),
        migrations.DeleteModel(
            name='ShoeOrder',
        ),
        migrations.AddField(
            model_name='order',
            name='quantity',
            field=models.IntegerField(verbose_name='Quantity', default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='shoe',
            field=models.ForeignKey(to='inventory.Shoe', blank=True, verbose_name='Shoe', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='where',
            field=models.CharField(verbose_name='Where', default='', blank=True, max_length=32),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='order_type',
            field=models.CharField(choices=[('o', 'Orthotics'), ('cs', 'Compression Stockings'), ('os', 'Orthopedic Shoes'), ('bs', 'Back Support'), ('s', 'Shoes')], verbose_name='Order Type', max_length=4),
            preserve_default=True,
        ),
    ]
