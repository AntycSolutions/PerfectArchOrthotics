# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0039_receipt_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receipt',
            name='date',
        ),
        migrations.AddField(
            model_name='receipt',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 28, 2, 42, 32, 731688, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
