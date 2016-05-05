# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0029_biomechanical'),
    ]

    operations = [
        migrations.AddField(
            model_name='insuranceletter',
            name='signature_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
