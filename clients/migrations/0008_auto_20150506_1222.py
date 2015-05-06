# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0007_delete_sitestatistics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insurance',
            name='benefits',
            field=models.CharField(verbose_name='Benefits', max_length=4, choices=[('a', 'Assignment'), ('na', 'Non-assignment')]),
        ),
    ]
