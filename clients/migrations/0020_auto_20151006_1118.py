# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0019_person_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='created',
            field=models.DateTimeField(verbose_name='Created', auto_now_add=True),
        ),
    ]
