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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('submitted_datetime', models.DateTimeField(verbose_name='Submitted Date', auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClaimCoverage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('expected_back', models.IntegerField(verbose_name='Expected Back', default=0)),
                ('claim', models.ForeignKey(verbose_name='Claim', to='clients.Claim')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClaimItem',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('quantity', models.IntegerField(verbose_name='Quantity', default=0)),
                ('claim_coverage', models.ForeignKey(verbose_name='Claim Coverage', to='clients.ClaimCoverage')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Coverage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('coverage_type', models.CharField(max_length=4, verbose_name='Coverage Type', choices=[('o', 'Orthotics'), ('cs', 'Compression Stockings'), ('os', 'Orthopedic Shoes'), ('bs', 'Back Support')], blank=True)),
                ('coverage_percent', models.IntegerField(verbose_name='Coverage Percent', default=0)),
                ('max_claim_amount', models.IntegerField(verbose_name='Max Claim Amount', default=0)),
                ('max_quantity', models.IntegerField(verbose_name='Max Quantity', default=0)),
                ('period', models.IntegerField(verbose_name='Period', null=True, choices=[(12, '12 Rolling Months'), (24, '24 Rolling Months'), (36, '36 Rolling Months'), (1, 'Benefit Year'), (2, 'Calendar Year')], blank=True)),
                ('period_date', models.DateField(verbose_name='Period Date', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Insurance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('provider', models.CharField(max_length=128, verbose_name='Provider')),
                ('policy_number', models.CharField(max_length=128, verbose_name='Policy Number', blank=True)),
                ('contract_number', models.CharField(max_length=128, verbose_name='Contract Number', blank=True)),
                ('benefits', models.CharField(max_length=4, verbose_name='Benefits', choices=[('a', 'Assignment'), ('na', 'Non-assignment')], blank=True)),
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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('practitioner_name', models.CharField(max_length=4, verbose_name='Practitioner Name', default='dm', choices=[('dm', 'D. Mu C.Ped.'), ('ds', 'Dr. Sefcik D.P.M.')], blank=True)),
                ('biomedical_and_gait_analysis_date', models.DateField(verbose_name='Biomedical and Gait Analysis Date', null=True, blank=True)),
                ('examiner', models.CharField(max_length=4, verbose_name='Examiner', default='dm', choices=[('dm', 'D. Mu C.Ped.'), ('ds', 'Dr. Sefcik D.P.M.')], blank=True)),
                ('dispensing_practitioner', models.CharField(max_length=4, verbose_name='Dispensing Practitioner', default='dm', choices=[('dm', 'D. Mu C.Ped.'), ('ds', 'Dr. Sefcik D.P.M.')], blank=True)),
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
                ('other', models.CharField(max_length=64, verbose_name='Other', blank=True)),
                ('claim', models.ForeignKey(verbose_name='Claim', to='clients.Claim')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('dispensed_by', models.CharField(max_length=4, verbose_name='Dispensed By', choices=[('dm', 'D. Mu C.Ped.'), ('ds', 'Dr. Sefcik D.P.M.')], blank=True)),
                ('payment_type', models.CharField(max_length=4, verbose_name='Payment Type', choices=[('ca', 'Cash'), ('ch', 'Cheque'), ('cr', 'Credit')], blank=True)),
                ('payment_terms', models.CharField(max_length=4, verbose_name='Payment Terms', default='dor', choices=[('dor', 'Due On Receipt')], blank=True)),
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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('coverage_type', models.CharField(max_length=4, verbose_name='Coverage Type', choices=[('o', 'Orthotics'), ('cs', 'Compression Stockings'), ('os', 'Orthopedic Shoes'), ('bs', 'Back Support')])),
                ('gender', models.CharField(max_length=4, verbose_name='Gender', choices=[('wo', "Women's"), ('me', "Men's")], blank=True)),
                ('product_code', models.CharField(max_length=12, unique=True, verbose_name='Product Code')),
                ('description', models.CharField(max_length=128, verbose_name='Description')),
                ('unit_price', models.IntegerField(verbose_name='Unit Price', default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Laboratory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('information', models.CharField(max_length=8, verbose_name='Information', choices=[('moll', 'MA Orthotics Laboratory Ltd\n11975 W Sample Rd\nCoral Springs, FL  331000\nUSA\nPhone: (754) 206-6110\nFax: (754) 206-6109\nLaboratory Supervisor: M. Asam C.Ped.'), ('ooli', 'OOLab Inc.\n42 Niagara St\nHamilton, ON  L8L 6A2\nCanada\nToll Free: 1-888-873-3316\nPhone: (905) 521-1230\nFax: (905) 521-1210\nEmail: info@oolab.com\nLaboratory Supervisor: A. Boyle'), ('aror', 'Ares Orthotics\n107 Ave SE\nCalgary, AB  T2Z 3R7\nCanada\nPhone: (403) 398-5629\nFax: (403) 398-5635\nEmail: acct@aresorthotics.com\nLaboratory Supervisor: B. Domosky')])),
                ('insurance_letter', models.ForeignKey(verbose_name='Insurance Letter', blank=True, null=True, to='clients.InsuranceLetter')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('first_name', models.CharField(max_length=128, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=128, verbose_name='Last Name', blank=True)),
                ('gender', models.CharField(max_length=4, verbose_name='Gender', choices=[('m', 'Male'), ('f', 'Female')], blank=True)),
                ('birth_date', models.DateField(verbose_name='Birth Date', null=True, blank=True)),
                ('health_care_number', models.CharField(max_length=20, verbose_name='Health Care Number', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Dependent',
            fields=[
                ('person_ptr', models.OneToOneField(serialize=False, parent_link=True, auto_created=True, primary_key=True, to='clients.Person')),
                ('relationship', models.CharField(max_length=4, verbose_name='Relationship', choices=[('s', 'Spouse'), ('c', 'Child')], blank=True)),
            ],
            options={
            },
            bases=('clients.person',),
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('person_ptr', models.OneToOneField(serialize=False, parent_link=True, auto_created=True, primary_key=True, to='clients.Person')),
                ('address', models.CharField(max_length=128, verbose_name='Address', blank=True)),
                ('city', models.CharField(max_length=128, verbose_name='City', blank=True)),
                ('postal_code', models.CharField(max_length=6, verbose_name='Postal Code', blank=True)),
                ('phone_number', models.CharField(max_length=14, verbose_name='Phone Number', blank=True)),
                ('cell_number', models.CharField(max_length=14, verbose_name='Cell Number', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='Email', null=True, blank=True)),
                ('employer', models.CharField(max_length=128, verbose_name='Employer', blank=True)),
                ('notes', models.TextField(verbose_name='Notes', blank=True)),
                ('referred_by', models.ForeignKey(verbose_name='Referred By', blank=True, related_name='referred_by', null=True, to='clients.Person')),
            ],
            options={
            },
            bases=('clients.person',),
        ),
        migrations.CreateModel(
            name='ProofOfManufacturing',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('claim', models.ForeignKey(verbose_name='Claim', to='clients.Claim')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SiteStatistics',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='insurance',
            name='claimants',
            field=models.ManyToManyField(through='clients.Coverage', verbose_name='claimants', to='clients.Person', related_name='claimants'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='insurance',
            name='main_claimant',
            field=models.ForeignKey(verbose_name='Claimant', to='clients.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dependent',
            name='client',
            field=models.ForeignKey(verbose_name='Client', to='clients.Client'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coverage',
            name='claimant',
            field=models.ForeignKey(verbose_name='Claimant', to='clients.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coverage',
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
            model_name='claimcoverage',
            name='coverage',
            field=models.ForeignKey(verbose_name='Coverage', to='clients.Coverage'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='claimcoverage',
            name='items',
            field=models.ManyToManyField(through='clients.ClaimItem', verbose_name='Items', to='clients.Item'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='claim',
            name='coverages',
            field=models.ManyToManyField(through='clients.ClaimCoverage', verbose_name='Coverages', to='clients.Coverage'),
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
            name='patient',
            field=models.ForeignKey(verbose_name='Patient', to='clients.Person'),
            preserve_default=True,
        ),
    ]
