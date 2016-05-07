# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0030_insuranceletter_signature_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='biomechanical',
            name='signature_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
