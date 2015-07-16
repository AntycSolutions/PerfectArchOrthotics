# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0012_claim_claim_package_multifile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='claim',
            name='claim_package',
        ),
    ]
