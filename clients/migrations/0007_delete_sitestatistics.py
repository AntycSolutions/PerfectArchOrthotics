# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0006_claim_claim_package'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SiteStatistics',
        ),
    ]
