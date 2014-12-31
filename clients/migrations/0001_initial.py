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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('submitted_datetime', models.DateTimeField(unique=True, verbose_name='Submitted Date')),
                ('insurance_paid_date', models.DateField(null=True, verbose_name='Insurance Paid Date', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClaimCoverage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('expected_back', models.IntegerField(default=0, verbose_name='Expected Back')),
                ('claim', models.ForeignKey(verbose_name='Claim', to='clients.Claim')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClaimItem',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0, verbose_name='Quantity')),
                ('claim_coverage', models.ForeignKey(verbose_name='Claim Coverage', to='clients.ClaimCoverage')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Coverage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('coverage_type', models.CharField(max_length=4, choices=[('o', 'Orthotics'), ('cs', 'Compression Stockings'), ('os', 'Orthopedic Shoes'), ('bs', 'Back Support')], verbose_name='Coverage Type', blank=True)),
                ('coverage_percent', models.IntegerField(default=0, verbose_name='Coverage Percent')),
                ('max_claim_amount', models.IntegerField(default=0, verbose_name='Max Claim Amount')),
                ('max_quantity', models.IntegerField(default=0, verbose_name='Max Quantity')),
                ('period', models.IntegerField(null=True, choices=[(12, '12 Rolling Months'), (24, '24 Rolling Months'), (36, '36 Rolling Months'), (1, 'Benefit Year'), (2, 'Calendar Year')], verbose_name='Period', blank=True)),
                ('period_date', models.DateField(null=True, verbose_name='Period Date', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Insurance',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('provider', models.CharField(max_length=128, verbose_name='Provider')),
                ('policy_number', models.CharField(max_length=128, verbose_name='Policy Number', blank=True)),
                ('contract_number', models.CharField(max_length=128, verbose_name='Contract Number', blank=True)),
                ('benefits', models.CharField(max_length=4, choices=[('a', 'Assignment'), ('na', 'Non-assignment')], verbose_name='Benefits', blank=True)),
                ('three_d_laser_scan', models.BooleanField(default=False, verbose_name='3D Laser Scan')),
                ('insurance_card', models.BooleanField(default=False, verbose_name='Insurance Card')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InsuranceLetter',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('practitioner_name', models.CharField(max_length=4, choices=[('dm', 'D. Mu C.Ped.'), ('ds', 'Dr. Sefcik D.P.M.')], default='dm', verbose_name='Practitioner Name', blank=True)),
                ('biomedical_and_gait_analysis_date', models.DateField(null=True, verbose_name='Biomedical and Gait Analysis Date', blank=True)),
                ('examiner', models.CharField(max_length=4, choices=[('dm', 'D. Mu C.Ped.'), ('ds', 'Dr. Sefcik D.P.M.')], default='dm', verbose_name='Examiner', blank=True)),
                ('dispensing_practitioner', models.CharField(max_length=4, choices=[('dm', 'D. Mu C.Ped.'), ('ds', 'Dr. Sefcik D.P.M.')], default='dm', verbose_name='Dispensing Practitioner', blank=True)),
                ('orthopedic_shoes', models.BooleanField(default=False, verbose_name='Orthopedic Shoes')),
                ('foot_orthotics_orthosis', models.BooleanField(default=False, verbose_name='Foot Orthotics Orthosis')),
                ('internally_modified_footwear', models.BooleanField(default=False, verbose_name='Internally Modified Orthosis')),
                ('foam_plaster', models.BooleanField(default=False, verbose_name='Foam / Plaster')),
                ('plantar_fasciitis', models.BooleanField(default=False, verbose_name='Plantar Fasciitis')),
                ('hammer_toes', models.BooleanField(default=False, verbose_name='Hammer Toes')),
                ('ligament_tear', models.BooleanField(default=False, verbose_name='Ligament Tear / Sprain')),
                ('knee_arthritis', models.BooleanField(default=False, verbose_name='Knee Arthritis')),
                ('metatarsalgia', models.BooleanField(default=False, verbose_name='Metatarsalgia')),
                ('drop_foot', models.BooleanField(default=False, verbose_name='Drop Foot')),
                ('scoliosis_with_pelvic_tilt', models.BooleanField(default=False, verbose_name='Scoliosis With Pelvic Tilt')),
                ('hip_arthritis', models.BooleanField(default=False, verbose_name='Hip Arthritis')),
                ('pes_cavus', models.BooleanField(default=False, verbose_name='Pes Cavus')),
                ('heel_spur', models.BooleanField(default=False, verbose_name='Heel Spur')),
                ('lumbar_spine_dysfunction', models.BooleanField(default=False, verbose_name='Lumbar Spine Dysfunction')),
                ('lumbar_arthritis', models.BooleanField(default=False, verbose_name='Lumbar Arthritis')),
                ('pes_planus', models.BooleanField(default=False, verbose_name='Pes Planus')),
                ('ankle_abnormal_rom', models.BooleanField(default=False, verbose_name='Ankle: Abnormal ROM')),
                ('leg_length_discrepency', models.BooleanField(default=False, verbose_name='Leg Length Discrepancy')),
                ('si_arthritis', models.BooleanField(default=False, verbose_name='SI Arthritis')),
                ('diabetes', models.BooleanField(default=False, verbose_name='Diabetes')),
                ('foot_abnormal_ROM', models.BooleanField(default=False, verbose_name='Foot: Abnormal ROM')),
                ('si_joint_dysfunction', models.BooleanField(default=False, verbose_name='SI Joint Dysfunction')),
                ('ankle_arthritis', models.BooleanField(default=False, verbose_name='Ankle Arthritis')),
                ('neuropathy', models.BooleanField(default=False, verbose_name='Neuropathy')),
                ('peroneal_dysfunction', models.BooleanField(default=False, verbose_name='Peroneal Dysfunction')),
                ('genu_valgum', models.BooleanField(default=False, verbose_name='Genu Valgum')),
                ('foot_arthritis', models.BooleanField(default=False, verbose_name='Foot Arthritis')),
                ('mtp_drop', models.BooleanField(default=False, verbose_name='MTP Drop')),
                ('interdigital_neuroma', models.BooleanField(default=False, verbose_name='Interdigital Neuroma')),
                ('genu_varum', models.BooleanField(default=False, verbose_name='Genu Varum')),
                ('first_mtp_arthritis', models.BooleanField(default=False, verbose_name='1st MTP Arthritis')),
                ('forefoot_varus', models.BooleanField(default=False, verbose_name='Forefoot Varus')),
                ('bunions_hallux_valgus', models.BooleanField(default=False, verbose_name='Bunions / Hallux Valgus')),
                ('abnormal_patellar_tracking', models.BooleanField(default=False, verbose_name='Abnormal Patellar Tracking')),
                ('rheumatoid_arthritis', models.BooleanField(default=False, verbose_name='Rheumatoid Arthritis')),
                ('forefoot_valgus', models.BooleanField(default=False, verbose_name='Forefoot Valgus')),
                ('abnormal_gait_tracking', models.BooleanField(default=False, verbose_name='Abnormal Gait Timing')),
                ('abnormal_gait_pressures', models.BooleanField(default=False, verbose_name='Abnormal Gait Pressures')),
                ('gout', models.BooleanField(default=False, verbose_name='Gout')),
                ('shin_splints', models.BooleanField(default=False, verbose_name='Shin Splints')),
                ('over_supination', models.BooleanField(default=False, verbose_name='Over Supination')),
                ('achilles_tendinitis', models.BooleanField(default=False, verbose_name='Achilles Tendinitis')),
                ('ulcers', models.BooleanField(default=False, verbose_name='Ulcers')),
                ('over_pronation', models.BooleanField(default=False, verbose_name='Over Pronation')),
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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('invoice_date', models.DateField(null=True, verbose_name='Invoice Date', blank=True)),
                ('dispensed_by', models.CharField(max_length=4, choices=[('dm', 'D. Mu C.Ped.'), ('ds', 'Dr. Sefcik D.P.M.')], verbose_name='Dispensed By', blank=True)),
                ('payment_type', models.CharField(max_length=4, choices=[('ca', 'Cash'), ('ch', 'Cheque'), ('cr', 'Credit')], verbose_name='Payment Type', blank=True)),
                ('payment_terms', models.CharField(max_length=4, choices=[('dor', 'Due On Receipt')], default='dor', verbose_name='Payment Terms', blank=True)),
                ('payment_made', models.IntegerField(default=0, verbose_name='Payment Made')),
                ('payment_date', models.DateField(null=True, verbose_name='Payment Date', blank=True)),
                ('deposit', models.IntegerField(default=0, verbose_name='Deposit')),
                ('deposit_date', models.DateField(null=True, verbose_name='Deposite Date', blank=True)),
                ('estimate', models.BooleanField(default=False, verbose_name='Estimate')),
                ('claim', models.ForeignKey(verbose_name='Claim', to='clients.Claim')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('coverage_type', models.CharField(max_length=4, choices=[('o', 'Orthotics'), ('cs', 'Compression Stockings'), ('os', 'Orthopedic Shoes'), ('bs', 'Back Support')], verbose_name='Coverage Type')),
                ('gender', models.CharField(max_length=4, choices=[('wo', "Women's"), ('me', "Men's")], verbose_name='Gender', blank=True)),
                ('product_code', models.CharField(unique=True, max_length=12, verbose_name='Product Code')),
                ('description', models.CharField(max_length=128, verbose_name='Description')),
                ('unit_price', models.IntegerField(default=0, verbose_name='Unit Price')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Laboratory',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('information', models.CharField(max_length=8, choices=[('moll', 'MA Orthotics Laboratory Ltd\n11975 W Sample Rd\nCoral Springs, FL  331000\nUSA\nPhone: (754) 206-6110\nFax: (754) 206-6109\nLaboratory Supervisor: M. Asam C.Ped.'), ('ooli', 'OOLab Inc.\n42 Niagara St\nHamilton, ON  L8L 6A2\nCanada\nToll Free: 1-888-873-3316\nPhone: (905) 521-1230\nFax: (905) 521-1210\nEmail: info@oolab.com\nLaboratory Supervisor: A. Boyle'), ('aror', 'Ares Orthotics\n107 Ave SE\nCalgary, AB  T2Z 3R7\nCanada\nPhone: (403) 398-5629\nFax: (403) 398-5635\nEmail: acct@aresorthotics.com\nLaboratory Supervisor: B. Domosky')], verbose_name='Information')),
                ('insurance_letter', models.ForeignKey(null=True, verbose_name='Insurance Letter', blank=True, to='clients.InsuranceLetter')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('first_name', models.CharField(max_length=128, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=128, verbose_name='Last Name', blank=True)),
                ('gender', models.CharField(max_length=4, choices=[('m', 'Male'), ('f', 'Female')], verbose_name='Gender', blank=True)),
                ('birth_date', models.DateField(null=True, verbose_name='Birth Date', blank=True)),
                ('health_care_number', models.CharField(max_length=20, verbose_name='Health Care Number', blank=True)),
                ('employer', models.CharField(max_length=128, verbose_name='Employer', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Dependent',
            fields=[
                ('person_ptr', models.OneToOneField(serialize=False, auto_created=True, parent_link=True, primary_key=True, to='clients.Person')),
                ('relationship', models.CharField(max_length=4, choices=[('s', 'Spouse'), ('c', 'Child')], verbose_name='Relationship', blank=True)),
            ],
            options={
            },
            bases=('clients.person',),
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('person_ptr', models.OneToOneField(serialize=False, auto_created=True, parent_link=True, primary_key=True, to='clients.Person')),
                ('address', models.CharField(max_length=128, verbose_name='Address', blank=True)),
                ('city', models.CharField(max_length=128, verbose_name='City', blank=True)),
                ('province', models.CharField(max_length=128, verbose_name='Province', blank=True)),
                ('postal_code', models.CharField(max_length=7, verbose_name='Postal Code', blank=True)),
                ('phone_number', models.CharField(max_length=14, verbose_name='Phone Number', blank=True)),
                ('cell_number', models.CharField(max_length=14, verbose_name='Cell Number', blank=True)),
                ('email', models.EmailField(null=True, max_length=254, verbose_name='Email', blank=True)),
                ('notes', models.TextField(verbose_name='Notes', blank=True)),
                ('referred_by', models.ForeignKey(null=True, related_name='referred_by', verbose_name='Referred By', blank=True, to='clients.Person')),
            ],
            options={
            },
            bases=('clients.person',),
        ),
        migrations.CreateModel(
            name='ProofOfManufacturing',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('claim', models.ForeignKey(verbose_name='Claim', to='clients.Claim')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SiteStatistics',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='insurance',
            name='claimants',
            field=models.ManyToManyField(to='clients.Person', related_name='claimants', through='clients.Coverage', verbose_name='claimants'),
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
            field=models.ManyToManyField(to='clients.Item', through='clients.ClaimItem', verbose_name='Items'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='claim',
            name='coverages',
            field=models.ManyToManyField(to='clients.Coverage', through='clients.ClaimCoverage', verbose_name='Coverages'),
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
