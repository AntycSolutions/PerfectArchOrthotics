# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0038_auto_20160512_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='date',
            field=models.DateField(default=datetime.datetime(2016, 5, 28, 2, 36, 44, 474225, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
