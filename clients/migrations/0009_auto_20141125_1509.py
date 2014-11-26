# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0008_insuranceletter_laboratory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insuranceletter',
            name='abnormal_gait_pressures',
            field=models.BooleanField(help_text='Abnormal Gait Pressures', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='abnormal_gait_tracking',
            field=models.BooleanField(help_text='Abnormal Gait Timing', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='abnormal_patellar_tracking',
            field=models.BooleanField(help_text='Abnormal Patellar Tracking', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='achilles_tendinitis',
            field=models.BooleanField(help_text='Achilles Tendinitis', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='ankle_abnormal_rom',
            field=models.BooleanField(help_text='Ankle: Abnormal ROM', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='ankle_arthritis',
            field=models.BooleanField(help_text='Ankle Arthritis', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='bunions_hallux_valgus',
            field=models.BooleanField(help_text='Bunions / Hallux Valgus', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='diabetes',
            field=models.BooleanField(help_text='Diabetes', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='drop_foot',
            field=models.BooleanField(help_text='Drop Foot', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='first_mtp_arthritis',
            field=models.BooleanField(help_text='1st MTP Arthritis', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='foot_abnormal_ROM',
            field=models.BooleanField(help_text='Foot: Abnormal ROM', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='foot_arthritis',
            field=models.BooleanField(help_text='Foot Arthritis', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='forefoot_valgus',
            field=models.BooleanField(help_text='Forefoot Valgus', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='forefoot_varus',
            field=models.BooleanField(help_text='Forefoot Varus', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='genu_valgum',
            field=models.BooleanField(help_text='Genu Valgum', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='genu_varum',
            field=models.BooleanField(help_text='Genu Varum', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='gout',
            field=models.BooleanField(help_text='Gout', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='hammer_toes',
            field=models.BooleanField(help_text='Hammer Toes', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='heel_spur',
            field=models.BooleanField(help_text='Heel Spur', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='hip_arthritis',
            field=models.BooleanField(help_text='Hip Arthritis', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='interdigital_neuroma',
            field=models.BooleanField(help_text='Interdigital Neuroma', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='knee_arthritis',
            field=models.BooleanField(help_text='Knee Arthritis', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='leg_length_discrepency',
            field=models.BooleanField(help_text='Leg Length Discrepancy', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='ligament_tear',
            field=models.BooleanField(help_text='Ligament Tear / Sprain', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='lumbar_arthritis',
            field=models.BooleanField(help_text='Lumbar Arthritis', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='lumbar_spine_dysfunction',
            field=models.BooleanField(help_text='Lumbar Spine Dysfunction', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='metatarsalgia',
            field=models.BooleanField(help_text='Metatarsalgia', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='mtp_drop',
            field=models.BooleanField(help_text='MTP Drop', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='neuropathy',
            field=models.BooleanField(help_text='Neuropathy', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='over_pronation',
            field=models.BooleanField(help_text='Over Pronation', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='over_supination',
            field=models.BooleanField(help_text='Over Supination', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='peroneal_dysfunction',
            field=models.BooleanField(help_text='Peroneal Dysfunction', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='pes_cavus',
            field=models.BooleanField(help_text='Pes Cavus', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='pes_planus',
            field=models.BooleanField(help_text='Pes Planus', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='plantar_fasciitis',
            field=models.BooleanField(help_text='Plantar Fasciitis', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='rheumatoid_arthritis',
            field=models.BooleanField(help_text='Rheumatoid Arthritis', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='scoliosis_with_pelvic_tilt',
            field=models.BooleanField(help_text='Scoliosis With Pelvic Tilt', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='shin_splints',
            field=models.BooleanField(help_text='Shin Splints', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='si_arthritis',
            field=models.BooleanField(help_text='SI Arthritis', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='si_joint_dysfunction',
            field=models.BooleanField(help_text='SI Joint Dysfunction', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='insuranceletter',
            name='ulcers',
            field=models.BooleanField(help_text='Ulcers', default=False),
            preserve_default=True,
        ),
    ]
