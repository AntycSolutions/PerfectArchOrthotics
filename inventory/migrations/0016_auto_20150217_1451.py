# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0015_coverageorder_shoeorder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coverageorder',
            name='order_type',
        ),
        migrations.RemoveField(
            model_name='shoeorder',
            name='order_type',
        ),
        migrations.AddField(
            model_name='order',
            name='order_type',
            field=models.CharField(default='o', choices=[('o', 'Orthotics'), ('cs', 'Compression Stockings'), ('os', 'Orthopedic Shoes'), ('bs', 'Back Support'), ('s', 'Shoe')], max_length=4, verbose_name='Order Type'),
            preserve_default=False,
        ),
    ]
