# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0033_biomechanicalfoot'),
    ]

    operations = [
        migrations.RenameField(
            model_name='biomechanicalfoot',
            old_name='first_ray',
            new_name='first_ray_left',
        ),
        migrations.AddField(
            model_name='biomechanicalfoot',
            name='first_ray_right',
            field=models.CharField(blank=True, choices=[('D', 'DOR'), ('P', 'PLN')], max_length=2),
        ),
    ]
