# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0007_auto_20141124_1847'),
    ]

    operations = [
        migrations.CreateModel(
            name='InsuranceLetter',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('practitioner_name', models.CharField(max_length=128)),
                ('diagnosis', models.CharField(max_length=512)),
                ('biomedical_and_gait_analysis_date', models.DateTimeField()),
                ('examiner', models.CharField(max_length=128)),
                ('dispensing_practitioner', models.CharField(max_length=128)),
                ('dispense_date', models.DateTimeField()),
                ('orthopedic_shoes', models.BooleanField(default=False)),
                ('foot_orthotics_orthosis', models.BooleanField(default=False)),
                ('internally_modified_footwear', models.BooleanField(default=False)),
                ('foam_plaster', models.BooleanField(default=False)),
                ('gaitscan', models.BooleanField(default=False)),
                ('plantar_fasciitis', models.BooleanField(default=False)),
                ('hammer_toes', models.BooleanField(default=False)),
                ('ligament_tear', models.BooleanField(default=False)),
                ('knee_arthritis', models.BooleanField(default=False)),
                ('metatarsalgia', models.BooleanField(default=False)),
                ('drop_foot', models.BooleanField(default=False)),
                ('scoliosis_with_pelvic_tilt', models.BooleanField(default=False)),
                ('hip_arthritis', models.BooleanField(default=False)),
                ('pes_cavus', models.BooleanField(default=False)),
                ('heel_spur', models.BooleanField(default=False)),
                ('lumbar_spine_dysfunction', models.BooleanField(default=False)),
                ('lumbar_arthritis', models.BooleanField(default=False)),
                ('pes_planus', models.BooleanField(default=False)),
                ('ankle_abnormal_rom', models.BooleanField(default=False)),
                ('leg_length_discrepency', models.BooleanField(default=False)),
                ('si_arthritis', models.BooleanField(default=False)),
                ('diabetes', models.BooleanField(default=False)),
                ('foot_abnormal_ROM', models.BooleanField(default=False)),
                ('si_joint_dysfunction', models.BooleanField(default=False)),
                ('ankle_arthritis', models.BooleanField(default=False)),
                ('neuropathy', models.BooleanField(default=False)),
                ('peroneal_dysfunction', models.BooleanField(default=False)),
                ('genu_valgum', models.BooleanField(default=False)),
                ('foot_arthritis', models.BooleanField(default=False)),
                ('mtp_drop', models.BooleanField(default=False)),
                ('interdigital_neuroma', models.BooleanField(default=False)),
                ('genu_varum', models.BooleanField(default=False)),
                ('first_mtp_arthritis', models.BooleanField(default=False)),
                ('forefoot_varus', models.BooleanField(default=False)),
                ('bunions_hallux_valgus', models.BooleanField(default=False)),
                ('abnormal_patellar_tracking', models.BooleanField(default=False)),
                ('rheumatoid_arthritis', models.BooleanField(default=False)),
                ('forefoot_valgus', models.BooleanField(default=False)),
                ('abnormal_gait_tracking', models.BooleanField(default=False)),
                ('abnormal_gait_pressures', models.BooleanField(default=False)),
                ('gout', models.BooleanField(default=False)),
                ('shin_splints', models.BooleanField(default=False)),
                ('over_supination', models.BooleanField(default=False)),
                ('achilles_tendinitis', models.BooleanField(default=False)),
                ('ulcers', models.BooleanField(default=False)),
                ('over_pronation', models.BooleanField(default=False)),
                ('claim', models.ForeignKey(to='clients.Claim')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Laboratory',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('description', models.CharField(max_length=512)),
                ('insurance_letter', models.ForeignKey(to='clients.InsuranceLetter')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
