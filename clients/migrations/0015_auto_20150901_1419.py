# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0014_auto_20150831_1648'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='laboratory',
            options={'verbose_name_plural': 'Laboratories'},
        ),
        migrations.AlterModelOptions(
            name='proofofmanufacturing',
            options={'verbose_name_plural': 'Proofs of manufacturing'},
        ),
        migrations.AlterField(
            model_name='invoice',
            name='claim',
            field=models.OneToOneField(verbose_name='Claim', to='clients.Claim'),
        ),
    ]
