# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sitestatistics',
            name='number_of_clients_with_outstanding_fees',
        ),
        migrations.RemoveField(
            model_name='sitestatistics',
            name='outstanding_fees',
        ),
    ]
