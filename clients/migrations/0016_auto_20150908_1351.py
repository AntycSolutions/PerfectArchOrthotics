# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0015_auto_20150901_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insuranceletter',
            name='claim',
            field=models.OneToOneField(verbose_name='Claim', to='clients.Claim'),
        ),
        migrations.AlterField(
            model_name='proofofmanufacturing',
            name='claim',
            field=models.OneToOneField(verbose_name='Claim', to='clients.Claim'),
        ),
    ]
