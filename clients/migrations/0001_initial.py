# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Claim',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('submitted_date', models.DateField(verbose_name='Submitted Date', auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClaimCoverageType',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('estimated_amount_claimed', models.IntegerField(verbose_name='Estimated Amount Claimed', default=0)),
                ('actual_amount_claimed', models.IntegerField(verbose_name='Actual Amount Claimed', default=0)),
                ('estimated_expected_back', models.IntegerField(verbose_name='Estimated Expected Back', default=0)),
                ('actual_expected_back', models.IntegerField(verbose_name='Actual Expected Back', default=0)),
                ('claim', models.ForeignKey(verbose_name='Claim', to='clients.Claim')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClaimItem',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('quantity', models.IntegerField(verbose_name='Quantity', default=0)),
                ('claim', models.ForeignKey(verbose_name='Claim', to='clients.Claim')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CoverageType',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('coverage_type', models.CharField(choices=[('o', 'Orthotics'), ('cs', 'Compression Stockings'), ('os', 'Orthopedic Shoes'), ('bs', 'Back Support')], max_length=4, blank=True, verbose_name='Coverage Type')),
                ('coverage_percent', models.IntegerField(verbose_name='Coverage Percent', default=0)),
                ('max_claim_amount', models.IntegerField(verbose_name='Max Claim Amount', default=0)),
                ('total_claimed', models.IntegerField(verbose_name='Total Claimed', default=0)),
                ('quantity', models.IntegerField(verbose_name='Quantity', default=0)),
                ('period', models.IntegerField(choices=[(12, '12 Rolling Months'), (24, '24 Rolling Months'), (36, '36 Rolling Months'), (1, 'Benefit Year'), (2, 'Calendar Year')], null=True, blank=True, verbose_name='Period')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Insurance',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('provider', models.CharField(verbose_name='Provider', max_length=128)),
                ('policy_number', models.CharField(verbose_name='Policy Number', max_length=128, blank=True)),
                ('contract_number', models.CharField(verbose_name='Contract Number', max_length=128, blank=True)),
                ('benefits', models.CharField(choices=[('a', 'Assignment'), ('na', 'Non-assignment')], max_length=4, blank=True, verbose_name='Benefits')),
                ('three_d_laser_scan', models.BooleanField(verbose_name='3D Laser Scan', default=False)),
                ('insurance_card', models.BooleanField(verbose_name='Insurance Card', default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InsuranceLetter',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('practitioner_name', models.CharField(blank=True, choices=[('dm', 'D. Mu C.Ped.'), ('ds', 'Dr. Sefcik D.P.M.')], max_length=4, default='dm', verbose_name='Practitioner Name')),
                ('biomedical_and_gait_analysis_date', models.DateField(verbose_name='Biomedical and Gait Analysis Date', null=True, blank=True)),
                ('examiner', models.CharField(blank=True, choices=[('dm', 'D. Mu C.Ped.'), ('ds', 'Dr. Sefcik D.P.M.')], max_length=4, default='dm', verbose_name='Examiner')),
                ('dispensing_practitioner', models.CharField(blank=True, choices=[('dm', 'D. Mu C.Ped.'), ('ds', 'Dr. Sefcik D.P.M.')], max_length=4, default='dm', verbose_name='Dispensing Practitioner')),
                ('orthopedic_shoes', models.BooleanField(verbose_name='Orthopedic Shoes', default=False)),
                ('foot_orthotics_orthosis', models.BooleanField(verbose_name='Foot Orthotics Orthosis', default=False)),
                ('internally_modified_footwear', models.BooleanField(verbose_name='Internally Modified Orthosis', default=False)),
                ('foam_plaster', models.BooleanField(verbose_name='Foam / Plaster', default=False)),
                ('plantar_fasciitis', models.BooleanField(verbose_name='Plantar Fasciitis', default=False)),
                ('hammer_toes', models.BooleanField(verbose_name='Hammer Toes', default=False)),
                ('ligament_tear', models.BooleanField(verbose_name='Ligament Tear / Sprain', default=False)),
                ('knee_arthritis', models.BooleanField(verbose_name='Knee Arthritis', default=False)),
                ('metatarsalgia', models.BooleanField(verbose_name='Metatarsalgia', default=False)),
                ('drop_foot', models.BooleanField(verbose_name='Drop Foot', default=False)),
                ('scoliosis_with_pelvic_tilt', models.BooleanField(verbose_name='Scoliosis With Pelvic Tilt', default=False)),
                ('hip_arthritis', models.BooleanField(verbose_name='Hip Arthritis', default=False)),
                ('pes_cavus', models.BooleanField(verbose_name='Pes Cavus', default=False)),
                ('heel_spur', models.BooleanField(verbose_name='Heel Spur', default=False)),
                ('lumbar_spine_dysfunction', models.BooleanField(verbose_name='Lumbar Spine Dysfunction', default=False)),
                ('lumbar_arthritis', models.BooleanField(verbose_name='Lumbar Arthritis', default=False)),
                ('pes_planus', models.BooleanField(verbose_name='Pes Planus', default=False)),
                ('ankle_abnormal_rom', models.BooleanField(verbose_name='Ankle: Abnormal ROM', default=False)),
                ('leg_length_discrepency', models.BooleanField(verbose_name='Leg Length Discrepancy', default=False)),
                ('si_arthritis', models.BooleanField(verbose_name='SI Arthritis', default=False)),
                ('diabetes', models.BooleanField(verbose_name='Diabetes', default=False)),
                ('foot_abnormal_ROM', models.BooleanField(verbose_name='Foot: Abnormal ROM', default=False)),
                ('si_joint_dysfunction', models.BooleanField(verbose_name='SI Joint Dysfunction', default=False)),
                ('ankle_arthritis', models.BooleanField(verbose_name='Ankle Arthritis', default=False)),
                ('neuropathy', models.BooleanField(verbose_name='Neuropathy', default=False)),
                ('peroneal_dysfunction', models.BooleanField(verbose_name='Peroneal Dysfunction', default=False)),
                ('genu_valgum', models.BooleanField(verbose_name='Genu Valgum', default=False)),
                ('foot_arthritis', models.BooleanField(verbose_name='Foot Arthritis', default=False)),
                ('mtp_drop', models.BooleanField(verbose_name='MTP Drop', default=False)),
                ('interdigital_neuroma', models.BooleanField(verbose_name='Interdigital Neuroma', default=False)),
                ('genu_varum', models.BooleanField(verbose_name='Genu Varum', default=False)),
                ('first_mtp_arthritis', models.BooleanField(verbose_name='1st MTP Arthritis', default=False)),
                ('forefoot_varus', models.BooleanField(verbose_name='Forefoot Varus', default=False)),
                ('bunions_hallux_valgus', models.BooleanField(verbose_name='Bunions / Hallux Valgus', default=False)),
                ('abnormal_patellar_tracking', models.BooleanField(verbose_name='Abnormal Patellar Tracking', default=False)),
                ('rheumatoid_arthritis', models.BooleanField(verbose_name='Rheumatoid Arthritis', default=False)),
                ('forefoot_valgus', models.BooleanField(verbose_name='Forefoot Valgus', default=False)),
                ('abnormal_gait_tracking', models.BooleanField(verbose_name='Abnormal Gait Timing', default=False)),
                ('abnormal_gait_pressures', models.BooleanField(verbose_name='Abnormal Gait Pressures', default=False)),
                ('gout', models.BooleanField(verbose_name='Gout', default=False)),
                ('shin_splints', models.BooleanField(verbose_name='Shin Splints', default=False)),
                ('over_supination', models.BooleanField(verbose_name='Over Supination', default=False)),
                ('achilles_tendinitis', models.BooleanField(verbose_name='Achilles Tendinitis', default=False)),
                ('ulcers', models.BooleanField(verbose_name='Ulcers', default=False)),
                ('over_pronation', models.BooleanField(verbose_name='Over Pronation', default=False)),
                ('claim', models.ForeignKey(verbose_name='Claim', to='clients.Claim')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('dispensed_by', models.CharField(choices=[('dm', 'D. Mu C.Ped.'), ('ds', 'Dr. Sefcik D.P.M.')], max_length=4, blank=True, verbose_name='Dispensed By')),
                ('payment_type', models.CharField(choices=[('ca', 'Cash'), ('ch', 'Cheque'), ('cr', 'Credit')], max_length=4, blank=True, verbose_name='Payment Type')),
                ('payment_terms', models.CharField(blank=True, choices=[('dor', 'Due On Receipt')], max_length=4, default='dor', verbose_name='Payment Terms')),
                ('payment_made', models.IntegerField(verbose_name='Payment Made', default=0)),
                ('payment_date', models.DateField(verbose_name='Payment Date', null=True, blank=True)),
                ('deposit', models.IntegerField(verbose_name='Deposit', default=0)),
                ('deposit_date', models.DateField(verbose_name='Deposite Date', null=True, blank=True)),
                ('estimate', models.BooleanField(verbose_name='Estimate', default=False)),
                ('claim', models.ForeignKey(verbose_name='Claim', to='clients.Claim')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('coverage_type', models.CharField(choices=[('o', 'Orthotics'), ('cs', 'Compression Stockings'), ('os', 'Orthopedic Shoes'), ('bs', 'Back Support')], max_length=4, verbose_name='Coverage Type')),
                ('gender', models.CharField(choices=[('wo', "Women's"), ('me', "Men's")], max_length=4, blank=True, verbose_name='Gender')),
                ('product_code', models.CharField(verbose_name='Product Code', max_length=12, unique=True)),
                ('description', models.CharField(verbose_name='Description', max_length=128)),
                ('unit_price', models.IntegerField(verbose_name='Unit Price', default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Laboratory',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('information', models.CharField(choices=[('moll', 'MA Orthotics Laboratory Ltd\n11975 W Sample Rd\nCoral Springs, FL  331000\nUSA\nPhone: (754) 206-6110\nFax: (754) 206-6109\nLaboratory Supervisor: M. Asam C.Ped.'), ('ooli', 'OOLab Inc.\n42 Niagara St\nHamilton, ON  L8L 6A2\nCanada\nToll Free: 1-888-873-3316\nPhone: (905) 521-1230\nFax: (905) 521-1210\nEmail: info@oolab.com'), ('aror', 'Ares Orthotics\n107 Ave SE\nCalgary, AB  T2Z 3R7\nCanada\nPhone: (403) 398-5629\nFax: (403) 398-5635\nEmail: acct@aresorthotics.com\nLaboratory Supervisor: B. Domosky')], max_length=8, verbose_name='Information')),
                ('insurance_letter', models.ForeignKey(to='clients.InsuranceLetter', verbose_name='Insurance Letter', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('first_name', models.CharField(verbose_name='First Name', max_length=128)),
                ('last_name', models.CharField(verbose_name='Last Name', max_length=128, blank=True)),
                ('gender', models.CharField(choices=[('m', 'Male'), ('f', 'Female')], max_length=4, blank=True, verbose_name='Gender')),
                ('birth_date', models.DateField(verbose_name='Birth Date', null=True, blank=True)),
                ('health_care_number', models.CharField(verbose_name='Health Care Number', max_length=20, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Dependent',
            fields=[
                ('person_ptr', models.OneToOneField(parent_link=True, primary_key=True, to='clients.Person', serialize=False, auto_created=True)),
                ('relationship', models.CharField(choices=[('s', 'Spouse'), ('c', 'Child')], max_length=4, blank=True, verbose_name='Relationship')),
            ],
            options={
            },
            bases=('clients.person',),
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('person_ptr', models.OneToOneField(parent_link=True, primary_key=True, to='clients.Person', serialize=False, auto_created=True)),
                ('address', models.CharField(verbose_name='Address', max_length=128, blank=True)),
                ('city', models.CharField(verbose_name='City', max_length=128, blank=True)),
                ('postal_code', models.CharField(verbose_name='Postal Code', max_length=6, blank=True)),
                ('phone_number', models.CharField(verbose_name='Phone Number', max_length=14, blank=True)),
                ('cell_number', models.CharField(verbose_name='Cell Number', max_length=14, blank=True)),
                ('email', models.EmailField(verbose_name='Email', null=True, blank=True, max_length=254)),
                ('employer', models.CharField(verbose_name='Employer', max_length=128, blank=True)),
                ('notes', models.TextField(verbose_name='Notes', blank=True)),
                ('referred_by', models.ForeignKey(to='clients.Person', related_name='referred_by', verbose_name='Referred By', null=True, blank=True)),
            ],
            options={
            },
            bases=('clients.person',),
        ),
        migrations.CreateModel(
            name='ProofOfManufacturing',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('claim', models.ForeignKey(verbose_name='Claim', to='clients.Claim')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SiteStatistics',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='insurance',
            name='client',
            field=models.ForeignKey(verbose_name='Client', to='clients.Client'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='insurance',
            name='spouse',
            field=models.ForeignKey(to='clients.Dependent', verbose_name='Spouse', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dependent',
            name='client',
            field=models.ForeignKey(verbose_name='Client', to='clients.Client'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coveragetype',
            name='insurance',
            field=models.ForeignKey(verbose_name='Insurance', to='clients.Insurance'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='claimitem',
            name='item',
            field=models.ForeignKey(verbose_name='Item', to='clients.Item'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='claimcoveragetype',
            name='coverage_type',
            field=models.ForeignKey(verbose_name='Item', to='clients.CoverageType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='claim',
            name='client',
            field=models.ForeignKey(verbose_name='Client', to='clients.Client'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='claim',
            name='coverage_types',
            field=models.ManyToManyField(through='clients.ClaimCoverageType', verbose_name='Coverage Types', to='clients.CoverageType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='claim',
            name='insurance',
            field=models.ForeignKey(verbose_name='Insurance', to='clients.Insurance'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='claim',
            name='items',
            field=models.ManyToManyField(through='clients.ClaimItem', verbose_name='Items', to='clients.Item'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='claim',
            name='patient',
            field=models.ForeignKey(related_name='patient', verbose_name='Patient', to='clients.Person'),
            preserve_default=True,
        ),
    ]
