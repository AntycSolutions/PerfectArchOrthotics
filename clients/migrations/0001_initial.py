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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('submitted_date', models.DateField(verbose_name='Submitted Date', auto_now_add=True)),
                ('paid_date', models.DateField(blank=True, verbose_name='Paid Date', null=True)),
                ('amount_claimed', models.IntegerField(verbose_name='Amount Claimed', default=0)),
                ('expected_back', models.IntegerField(verbose_name='Expected Back', default=0)),
                ('payment_type', models.CharField(blank=True, verbose_name='Payment Type', max_length=4, choices=[('ca', 'Cash'), ('ch', 'Cheque'), ('cr', 'Credit')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CoverageType',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('coverage_type', models.CharField(blank=True, verbose_name='Coverage Type', max_length=4, choices=[('o', 'Orthotics'), ('cs', 'Compression Stockings'), ('os', 'Orthopedic Shoes')])),
                ('coverage_percent', models.IntegerField(verbose_name='Coverage Percent', default=0)),
                ('max_claim_amount', models.IntegerField(verbose_name='Max Claim Amount', default=0)),
                ('total_claimed', models.IntegerField(verbose_name='Total Claimed', default=0)),
                ('quantity', models.IntegerField(verbose_name='Quantity', default=0)),
                ('period', models.IntegerField(blank=True, verbose_name='Period', choices=[(12, '12 Rolling Months'), (24, '24 Rolling Months'), (36, '36 Rolling Months'), (1, 'Benefit Year'), (2, 'Calendar Year')], null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Insurance',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('provider', models.CharField(blank=True, verbose_name='Provider', max_length=128)),
                ('policy_number', models.CharField(blank=True, verbose_name='Policy Number', max_length=128)),
                ('contract_number', models.CharField(blank=True, verbose_name='Contract Number', max_length=128)),
                ('billing', models.CharField(blank=True, verbose_name='Billing', max_length=4, choices=[('d', 'Direct'), ('i', 'Indirect')])),
                ('gait_scan', models.BooleanField(verbose_name='Gait Scan', default=False)),
                ('insurance_card', models.BooleanField(verbose_name='Insurance Card', default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InsuranceLetter',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('practitioner_name', models.CharField(blank=True, verbose_name='Practitioner Name', max_length=128, choices=[('dm', 'Danny Mu')], default='dm')),
                ('biomedical_and_gait_analysis_date', models.DateField(blank=True, verbose_name='Biomedical and Gait Analysis Date', null=True)),
                ('examiner', models.CharField(blank=True, verbose_name='Examiner', max_length=128)),
                ('dispensing_practitioner', models.CharField(blank=True, verbose_name='Dispensing Practitioner', max_length=128)),
                ('dispense_date', models.DateField(blank=True, verbose_name='Dispense Date', null=True)),
                ('orthopedic_shoes', models.BooleanField(verbose_name='Orthopedic Shoes', default=False)),
                ('foot_orthotics_orthosis', models.BooleanField(verbose_name='Foot Orthotics Orthosis', default=False)),
                ('internally_modified_footwear', models.BooleanField(verbose_name='Internally Modified Orthosis', default=False)),
                ('foam_plaster', models.BooleanField(verbose_name='Foam / Plaster', default=False)),
                ('gaitscan', models.BooleanField(verbose_name='Gait Scan(TM)', default=False)),
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
                ('claim', models.ForeignKey(to='clients.Claim', verbose_name='Claim')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('dispensed_by', models.CharField(blank=True, verbose_name='Dispensed By', max_length=128)),
                ('payment_type', models.CharField(blank=True, verbose_name='Payment Type', max_length=4, choices=[('a', 'Assignment'), ('na', 'Non-assignment')])),
                ('payment_terms', models.CharField(blank=True, verbose_name='Payment Terms', max_length=256)),
                ('payment_made', models.IntegerField(verbose_name='Payment Made', default=0)),
                ('claim', models.ForeignKey(to='clients.Claim', verbose_name='Claim')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('description', models.CharField(blank=True, verbose_name='Description', max_length=512)),
                ('unit_price', models.IntegerField(verbose_name='Unit Price', default=0)),
                ('quantity', models.IntegerField(verbose_name='Quantity', default=0)),
                ('invoice', models.ForeignKey(to='clients.Invoice', verbose_name='Invoice')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Laboratory',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('information', models.CharField(verbose_name='Information', max_length=8, choices=[('moll', 'MA Orthotics Laboratory Ltd\n11975 W Sample Rd\nCoral Springs, FL  331000\nUSA\nPhone: (754) 206-6110\nFax: (754) 206-6109'), ('ooli', 'OOLab Inc.\n42 Niagara St\nHamilton, ON  L8L 6A2\nCanada\nToll Free: 1-888-873-3316\nPhone: (905) 521-1230\nFax: (905) 521-1210\nEmail: info@oolab.com'), ('aror', 'Ares Orthotics\n107 Ave SE\nCalgary, AB  T2Z 3R7\nCanada\nPhone: (403) 398-5629\nFax: (403) 398-5635\nEmail: acct@aresorthotics.com')])),
                ('insurance_letter', models.ForeignKey(blank=True, verbose_name='Insurance Letter', to='clients.InsuranceLetter', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('first_name', models.CharField(verbose_name='First Name', max_length=128)),
                ('last_name', models.CharField(blank=True, verbose_name='Last Name', max_length=128)),
                ('gender', models.CharField(blank=True, verbose_name='Gender', max_length=4, choices=[('m', 'Male'), ('f', 'Female')])),
                ('birth_date', models.DateField(blank=True, verbose_name='Birth Date', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Dependent',
            fields=[
                ('person_ptr', models.OneToOneField(serialize=False, primary_key=True, to='clients.Person', parent_link=True, auto_created=True)),
                ('relationship', models.CharField(blank=True, verbose_name='Relationship', max_length=4, choices=[('s', 'Spouse'), ('c', 'Child')])),
            ],
            options={
            },
            bases=('clients.person',),
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('person_ptr', models.OneToOneField(serialize=False, primary_key=True, to='clients.Person', parent_link=True, auto_created=True)),
                ('address', models.CharField(blank=True, verbose_name='Address', max_length=128)),
                ('city', models.CharField(blank=True, verbose_name='City', max_length=128)),
                ('postal_code', models.CharField(blank=True, verbose_name='Postal Code', max_length=6)),
                ('phone_number', models.CharField(blank=True, verbose_name='Phone Number', max_length=14)),
                ('cell_number', models.CharField(blank=True, verbose_name='Cell Number', max_length=14)),
                ('email', models.EmailField(blank=True, verbose_name='Email', max_length=254, null=True)),
                ('health_care_number', models.CharField(blank=True, verbose_name='Health Care Number', max_length=20)),
                ('employer', models.CharField(blank=True, verbose_name='Employer', max_length=128)),
                ('notes', models.TextField(blank=True, verbose_name='Notes')),
                ('referred_by', models.ForeignKey(blank=True, verbose_name='Referred By', related_name='referred_by', to='clients.Person', null=True)),
            ],
            options={
            },
            bases=('clients.person',),
        ),
        migrations.CreateModel(
            name='ProofOfManufacturing',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('invoice_date', models.DateField(blank=True, verbose_name='Invoice Date', null=True)),
                ('product', models.CharField(blank=True, verbose_name='Product', max_length=256)),
                ('quantity', models.IntegerField(verbose_name='Quantity', default=0)),
                ('laboratory_supervisor', models.CharField(blank=True, verbose_name='Laboratory Supervisor', max_length=128)),
                ('raw_materials', models.TextField(blank=True, verbose_name='Raw Materials')),
                ('manufacturing', models.TextField(blank=True, verbose_name='Manufacturing')),
                ('casting_technique', models.TextField(blank=True, verbose_name='Casting Technique')),
                ('claim', models.ForeignKey(to='clients.Claim', verbose_name='Claim')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SiteStatistics',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('home_page_views', models.IntegerField(verbose_name='Home Page Views', default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='laboratory',
            name='proof_of_manufacturing',
            field=models.ForeignKey(blank=True, verbose_name='Proof of Manufacturing', to='clients.ProofOfManufacturing', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='insurance',
            name='client',
            field=models.ForeignKey(to='clients.Client', verbose_name='Client'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='insurance',
            name='spouse',
            field=models.ForeignKey(blank=True, verbose_name='Spouse', to='clients.Dependent', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dependent',
            name='client',
            field=models.ForeignKey(to='clients.Client', verbose_name='Client'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coveragetype',
            name='insurance',
            field=models.ForeignKey(to='clients.Insurance', verbose_name='Insurance'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='claim',
            name='client',
            field=models.ForeignKey(to='clients.Client', verbose_name='Client'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='claim',
            name='coverage_types',
            field=models.ManyToManyField(to='clients.CoverageType', blank=True, verbose_name='Coverage Types', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='claim',
            name='patient',
            field=models.ForeignKey(blank=True, verbose_name='Patient', related_name='patient', to='clients.Person', null=True),
            preserve_default=True,
        ),
    ]
