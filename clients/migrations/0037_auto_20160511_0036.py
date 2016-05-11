# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0036_auto_20160510_2059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biomechanicalfoot',
            name='first_mtp_joint_comments',
            field=models.CharField(max_length=64, blank=True),
        ),
        migrations.AlterField(
            model_name='biomechanicalfoot',
            name='first_ray_comments',
            field=models.CharField(max_length=64, blank=True),
        ),
        migrations.AlterField(
            model_name='biomechanicalfoot',
            name='lesser_mtp_joints_comments',
            field=models.CharField(max_length=64, blank=True),
        ),
        migrations.AlterField(
            model_name='biomechanicalfoot',
            name='midtarsal_joint_comments',
            field=models.CharField(max_length=64, blank=True),
        ),
        migrations.AlterField(
            model_name='biomechanicalfoot',
            name='subtalar_joint_comments',
            field=models.CharField(max_length=64, blank=True),
        ),
    ]
