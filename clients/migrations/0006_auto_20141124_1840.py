# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0005_invoice_item'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoice',
            old_name='payment',
            new_name='payment_made',
        ),
    ]
