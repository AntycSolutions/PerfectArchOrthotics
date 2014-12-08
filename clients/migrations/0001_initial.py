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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('submitted_date', models.DateField(verbose_name='Submitted Date', auto_now_add=True)),
                ('paid_date', models.DateField(verbose_name='Paid Date', blank=True, null=True)),
                ('amount_claimed', models.IntegerField(verbose_name='Amount Claimed', default=0)),
                ('expected_back', models.IntegerField(verbose_name='Expected Back', default=0)),
                ('payment_type', models.CharField(verbose_name='Payment Type', blank=True, choices=[('ca', 'Cash'), ('ch', 'Cheque'), ('cr', 'Credit')], max_length=4)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CoverageType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('coverage_type', models.CharField(verbose_name='Coverage Type', blank=True, choices=[('o', 'Orthotics'), ('cs', 'Compression Stockings'), ('os', 'Orthopedic Shoes')], max_length=4)),
                ('coverage_percent', models.IntegerField(verbose_name='Coverage Percent', default=0)),
                ('max_claim_amount', models.IntegerField(verbose_name='Max Claim Amount', default=0)),
                ('total_claimed', models.IntegerField(verbose_name='Total Claimed', default=0)),
                ('quantity', models.IntegerField(verbose_name='Quantity', default=0)),
                ('period', models.IntegerField(verbose_name='Period', blank=True, choices=[(12, '12 Rolling Months'), (24, '24 Rolling Months'), (36, '36 Rolling Months'), (1, 'Benefit Year'), (2, 'Calendar Year')], null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Insurance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('provider', models.CharField(verbose_name='Provider', blank=True, max_length=128)),
                ('policy_number', models.CharField(verbose_name='Policy Number', blank=True, max_length=128)),
                ('contract_number', models.CharField(verbose_name='Contract Number', blank=True, max_length=128)),
                ('billing', models.CharField(verbose_name='Billing', blank=True, choices=[('d', 'Direct'), ('i', 'Indirect')], max_length=4)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('practitioner_name', models.CharField(verbose_name='Practitioner Name', blank=True, choices=[('dm', 'Danny Mu')], max_length=128, default='dm')),
                ('biomedical_and_gait_analysis_date', models.DateField(verbose_name='Biomedical and Gait Analysis Date', blank=True, null=True)),
                ('examiner', models.CharField(verbose_name='Examiner', blank=True, max_length=128)),
                ('dispensing_practitioner', models.CharField(verbose_name='Dispensing Practitioner', blank=True, max_length=128)),
                ('dispense_date', models.DateField(verbose_name='Dispense Date', blank=True, null=True)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('dispensed_by', models.CharField(verbose_name='Dispensed By', blank=True, max_length=128)),
                ('payment_type', models.CharField(verbose_name='Payment Type', blank=True, choices=[('a', 'Assignment'), ('na', 'Non-assignment')], max_length=4)),
                ('payment_terms', models.CharField(verbose_name='Payment Terms', blank=True, max_length=256)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('description', models.CharField(verbose_name='Description', blank=True, max_length=512)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('information', models.CharField(verbose_name='Information', choices=[('moll', 'MA Orthotics Laboratory Ltd\n11975 W Sample Rd\nCoral Springs, FL  331000\nPhone: (754) 206-6110\nFax: (754) 206-6109')], max_length=8)),
                ('insurance_letter', models.ForeignKey(blank=True, null=True, verbose_name='Insurance Letter', to='clients.InsuranceLetter')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('first_name', models.CharField(verbose_name='First Name', max_length=128)),
                ('last_name', models.CharField(verbose_name='Last Name', blank=True, max_length=128)),
                ('gender', models.CharField(verbose_name='Gender', blank=True, choices=[('m', 'Male'), ('f', 'Female')], max_length=4)),
                ('birth_date', models.DateField(verbose_name='Birth Date', blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Dependent',
            fields=[
                ('person_ptr', models.OneToOneField(primary_key=True, parent_link=True, auto_created=True, serialize=False, to='clients.Person')),
                ('relationship', models.CharField(verbose_name='Relationship', blank=True, choices=[('s', 'Spouse'), ('c', 'Child')], max_length=4)),
            ],
            options={
            },
            bases=('clients.person',),
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('person_ptr', models.OneToOneField(primary_key=True, parent_link=True, auto_created=True, serialize=False, to='clients.Person')),
                ('address', models.CharField(verbose_name='Address', blank=True, max_length=128)),
                ('city', models.CharField(verbose_name='City', blank=True, max_length=128)),
                ('postal_code', models.CharField(verbose_name='Postal Code', blank=True, max_length=6)),
                ('phone_number', models.CharField(verbose_name='Phone Number', blank=True, max_length=14)),
                ('cell_number', models.CharField(verbose_name='Cell Number', blank=True, max_length=14)),
                ('email', models.EmailField(verbose_name='Email', blank=True, null=True, max_length=254)),
                ('health_care_number', models.CharField(verbose_name='Health Care Number', blank=True, max_length=20)),
                ('employer', models.CharField(verbose_name='Employer', blank=True, max_length=128)),
                ('credit', models.SmallIntegerField(verbose_name='Credit', default=0)),
                ('referred_by', models.CharField(verbose_name='Referred By', blank=True, max_length=128)),
                ('notes', models.TextField(verbose_name='Notes', blank=True)),
                ('dependents', models.ManyToManyField(verbose_name='Dependents', blank=True, null=True, to='clients.Dependent')),
            ],
            options={
            },
            bases=('clients.person',),
        ),
        migrations.CreateModel(
            name='ProofOfManufacturing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('invoice_date', models.DateField(verbose_name='Invoice Date', blank=True, null=True)),
                ('product', models.CharField(verbose_name='Product', blank=True, max_length=256)),
                ('quantity', models.IntegerField(verbose_name='Quantity', default=0)),
                ('laboratory_supervisor', models.CharField(verbose_name='Laboratory Supervisor', blank=True, max_length=128)),
                ('raw_materials', models.TextField(verbose_name='Raw Materials', blank=True)),
                ('manufacturing', models.TextField(verbose_name='Manufacturing', blank=True)),
                ('casting_technique', models.TextField(verbose_name='Casting Technique', blank=True)),
                ('claim', models.ForeignKey(to='clients.Claim', verbose_name='Claim')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SiteStatistics',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('home_page_views', models.IntegerField(default=0)),
                ('outstanding_fees', models.IntegerField(default=0)),
                ('number_of_clients_with_outstanding_fees', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='laboratory',
            name='proof_of_manufacturing',
            field=models.ForeignKey(blank=True, null=True, verbose_name='Proof of Manufacturing', to='clients.ProofOfManufacturing'),
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
            field=models.ForeignKey(blank=True, null=True, verbose_name='Spouse', to='clients.Dependent'),
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
            field=models.ManyToManyField(verbose_name='Coverage Types', blank=True, null=True, to='clients.CoverageType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='claim',
            name='patient',
            field=models.ForeignKey(blank=True, related_name='patient', null=True, verbose_name='Patient', to='clients.Person'),
            preserve_default=True,
        ),
    ]
