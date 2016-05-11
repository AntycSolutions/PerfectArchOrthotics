# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0035_auto_20160510_2059'),
    ]

    operations = [
        migrations.RenameField(
            model_name='biomechanicalfoot',
            old_name='lesser_mtp_joints_6_right',
            new_name='lesser_mtp_joints_5_right',
        ),
    ]
