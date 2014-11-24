# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_insurance_asdf'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='insurance',
            name='asdf',
        ),
        migrations.RemoveField(
            model_name='insurance',
            name='spouse',
        ),
    ]
