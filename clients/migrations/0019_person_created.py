# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0018_referral_credit_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 10, 6, 17, 16, 56, 646649, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
