# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import utils.model_utils


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0032_auto_20160509_1522'),
    ]

    operations = [
        migrations.CreateModel(
            name='BiomechanicalFoot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('exam_date', models.DateField()),
                ('angle_of_gait_left', models.CharField(choices=[('D', 'ADD'), ('B', 'ABD')], blank=True, max_length=1)),
                ('angle_of_gait_right', models.CharField(choices=[('D', 'ADD'), ('B', 'ABD')], blank=True, max_length=1)),
                ('base_of_gait', models.CharField(blank=True, max_length=5)),
                ('contact_period', models.CharField(choices=[('T', 'Toe Heel Gait'), ('FO', 'Forefoot Slap'), ('E', 'Equinus (Uncomp.)'), ('S', 'Steppage Gait'), ('FE', 'Festination')], blank=True, max_length=2)),
                ('midstance_period', models.CharField(choices=[('EX', 'Extensor Substitution'), ('AB', 'Abductory Twist'), ('EA', 'Early Heel Off'), ('S', 'Scissors Gait'), ('AT', 'Ataxic Gait'), ('T', 'Trendelenburg Gait')], blank=True, max_length=2)),
                ('propulsive_period', models.CharField(choices=[('A', 'Antalgia'), ('CE', 'Cerebellar Gait'), ('CA', 'Calcaneus Gait'), ('L', 'Lack of 1st MPJ Dorsiflexion')], blank=True, max_length=2)),
                ('postural_considerations', models.CharField(blank=True, max_length=64)),
                ('subtalar_joint_left', models.CharField(choices=[('S', 'SUP'), ('P', 'PRO')], blank=True, max_length=2)),
                ('subtalar_joint_right', models.CharField(choices=[('S', 'SUP'), ('P', 'PRO')], blank=True, max_length=2)),
                ('subtalar_joint_comments', models.CharField(max_length=64)),
                ('midtarsal_joint_left', models.CharField(choices=[('I', 'INV'), ('E', 'EV')], blank=True, max_length=2)),
                ('midtarsal_joint_right', models.CharField(choices=[('I', 'INV'), ('E', 'EV')], blank=True, max_length=2)),
                ('midtarsal_joint_comments', models.CharField(max_length=64)),
                ('ankle_joint_knee_extended_left', models.CharField(choices=[('Y', 'Y'), ('N', 'N')], blank=True, max_length=2)),
                ('ankle_joint_knee_extended_right', models.CharField(choices=[('Y', 'Y'), ('N', 'N')], blank=True, max_length=2)),
                ('ankle_joint_knee_flexed_left', models.CharField(choices=[('Y', 'Y'), ('N', 'N')], blank=True, max_length=2)),
                ('ankle_joint_knee_flexed_right', models.CharField(choices=[('Y', 'Y'), ('N', 'N')], blank=True, max_length=2)),
                ('first_ray', models.CharField(choices=[('D', 'DOR'), ('P', 'PLN')], blank=True, max_length=2)),
                ('first_ray_comments', models.CharField(max_length=64)),
                ('first_mtp_joint_left', models.CharField(choices=[('F', 'FULL'), ('L', 'LIM')], blank=True, max_length=2)),
                ('first_mtp_joint_right', models.CharField(choices=[('F', 'FULL'), ('L', 'LIM')], blank=True, max_length=2)),
                ('first_mtp_joint_comments', models.CharField(max_length=64)),
                ('lessor_mtp_joints_2_left', models.CharField(choices=[('F', 'FULL'), ('L', 'LIM')], blank=True, max_length=2)),
                ('lessor_mtp_joints_2_right', models.CharField(choices=[('F', 'FULL'), ('L', 'LIM')], blank=True, max_length=2)),
                ('lessor_mtp_joints_3_left', models.CharField(choices=[('F', 'FULL'), ('L', 'LIM')], blank=True, max_length=2)),
                ('lessor_mtp_joints_3_right', models.CharField(choices=[('F', 'FULL'), ('L', 'LIM')], blank=True, max_length=2)),
                ('lessor_mtp_joints_4_left', models.CharField(choices=[('F', 'FULL'), ('L', 'LIM')], blank=True, max_length=2)),
                ('lessor_mtp_joints_4_right', models.CharField(choices=[('F', 'FULL'), ('L', 'LIM')], blank=True, max_length=2)),
                ('lessor_mtp_joints_5_left', models.CharField(choices=[('F', 'FULL'), ('L', 'LIM')], blank=True, max_length=2)),
                ('lessor_mtp_joints_6_right', models.CharField(choices=[('F', 'FULL'), ('L', 'LIM')], blank=True, max_length=2)),
                ('lesser_mtp_joints_comments', models.CharField(max_length=64)),
                ('treatment_recommendations', models.TextField(blank=True)),
                ('claim', models.OneToOneField(to='clients.Claim')),
            ],
            bases=(models.Model, utils.model_utils.FieldList),
        ),
    ]
