# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20150122_0152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoe',
            name='size',
            field=models.CharField(blank=True, max_length=4, verbose_name='Size', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('3.5', '3.5'), ('4', '4'), ('4.5', '4.5'), ('5', '5'), ('5.5', '5.5'), ('6', '6'), ('6.5', '6.5'), ('7', '7'), ('7.5', '7.5'), ('8', '8'), ('8.5', '8.5'), ('9', '9'), ('9.5', '9.5'), ('10', '10'), ('10.5', '10.5'), ('11', '11'), ('11.5', '11.5'), ('12', '12'), ('12.5', '12.5'), ('13', '13'), ('13.5', '13.5'), ('14', '14')]),
            preserve_default=True,
        ),
    ]
