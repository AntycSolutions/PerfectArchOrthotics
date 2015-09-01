# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0013_remove_claim_claim_package'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dependent',
            name='relationship',
            field=models.CharField(verbose_name='Relationship', max_length=4, choices=[('s', 'Spouse'), ('c', 'Child')]),
        ),
    ]
