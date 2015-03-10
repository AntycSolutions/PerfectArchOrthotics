# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0017_auto_20150309_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_type',
            field=models.CharField(choices=[('o', 'Orthotics'), ('cs', 'Compression Stockings'), ('os', 'Orthopedic Shoes'), ('bs', 'Back Support'), ('s', 'Shoe'), ('a', 'Adjustment')], max_length=4, verbose_name='Order Type'),
            preserve_default=True,
        ),
    ]
