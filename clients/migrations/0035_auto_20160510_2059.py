# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0034_auto_20160510_2058'),
    ]

    operations = [
        migrations.RenameField(
            model_name='biomechanicalfoot',
            old_name='lessor_mtp_joints_2_left',
            new_name='lesser_mtp_joints_2_left',
        ),
        migrations.RenameField(
            model_name='biomechanicalfoot',
            old_name='lessor_mtp_joints_2_right',
            new_name='lesser_mtp_joints_2_right',
        ),
        migrations.RenameField(
            model_name='biomechanicalfoot',
            old_name='lessor_mtp_joints_3_left',
            new_name='lesser_mtp_joints_3_left',
        ),
        migrations.RenameField(
            model_name='biomechanicalfoot',
            old_name='lessor_mtp_joints_3_right',
            new_name='lesser_mtp_joints_3_right',
        ),
        migrations.RenameField(
            model_name='biomechanicalfoot',
            old_name='lessor_mtp_joints_4_left',
            new_name='lesser_mtp_joints_4_left',
        ),
        migrations.RenameField(
            model_name='biomechanicalfoot',
            old_name='lessor_mtp_joints_4_right',
            new_name='lesser_mtp_joints_4_right',
        ),
        migrations.RenameField(
            model_name='biomechanicalfoot',
            old_name='lessor_mtp_joints_5_left',
            new_name='lesser_mtp_joints_5_left',
        ),
        migrations.RenameField(
            model_name='biomechanicalfoot',
            old_name='lessor_mtp_joints_6_right',
            new_name='lesser_mtp_joints_6_right',
        ),
    ]
