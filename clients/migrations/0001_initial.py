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
                ('submitted_date', models.DateField(auto_now_add=True, verbose_name='Submitted Date')),
                ('paid_date', models.DateField(null=True, blank=True, verbose_name='Paid Date')),
                ('amount_claimed', models.IntegerField(default=0, blank=True, verbose_name='Amount Claimed')),
                ('expected_back', models.IntegerField(default=0, blank=True, verbose_name='Expected Back')),
                ('payment_type', models.CharField(choices=[('ca', 'Cash'), ('ch', 'Cheque'), ('cr', 'Credit')], default='', max_length=6, blank=True, verbose_name='Payment Type')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CoverageType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('coverage_type', models.CharField(choices=[('o', 'Orthotics'), ('cs', 'Compression Stockings'), ('os', 'Orthopedic Shoes')], default='', max_length=21, blank=True, verbose_name='Coverage Type')),
                ('coverage_percent', models.IntegerField(default=0, null=True, blank=True, verbose_name='Coverage Percent')),
                ('max_claim_amount', models.IntegerField(default=0, blank=True, verbose_name='Max Claim Amount')),
                ('total_claimed', models.IntegerField(default=0, null=True, blank=True, verbose_name='Total Claimed')),
                ('quantity', models.IntegerField(default=0, null=True, blank=True, verbose_name='Quantity')),
                ('period', models.IntegerField(default=1, verbose_name='Period')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Insurance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('provider', models.CharField(default='', max_length=128, blank=True, verbose_name='Provider')),
                ('policy_number', models.CharField(default='', max_length=128, blank=True, verbose_name='Policy Number')),
                ('contract_number', models.CharField(default='', max_length=128, blank=True, verbose_name='Contract Number')),
                ('billing', models.CharField(choices=[('d', 'Direct'), ('i', 'Indirect')], default='', max_length=8, blank=True, verbose_name='Billing')),
                ('gait_scan', models.BooleanField(default=False, verbose_name='Gait Scan')),
                ('insurance_card', models.BooleanField(default=False, verbose_name='Insurance Card')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InsuranceLetter',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('practitioner_name', models.CharField(choices=[('dm', 'Danny Mu')], default=('dm', 'Danny Mu'), max_length=128, verbose_name='Practitioner Name')),
                ('biomedical_and_gait_analysis_date', models.DateField(verbose_name='Biomedical and Gait Analysis Date')),
                ('examiner', models.CharField(max_length=128, verbose_name='Examiner')),
                ('dispensing_practitioner', models.CharField(max_length=128, verbose_name='Dispensing Practitioner')),
                ('dispense_date', models.DateField(verbose_name='Dispense Date')),
                ('orthopedic_shoes', models.BooleanField(default=False, verbose_name='Orthopedic Shoes')),
                ('foot_orthotics_orthosis', models.BooleanField(default=False, verbose_name='Foot Orthotics Orthosis')),
                ('internally_modified_footwear', models.BooleanField(default=False, verbose_name='Internally Modified Orthosis')),
                ('foam_plaster', models.BooleanField(default=False, verbose_name='Foam / Plaster')),
                ('gaitscan', models.BooleanField(default=False, verbose_name='Gait Scan(TM)')),
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
                ('claim', models.ForeignKey(to='clients.Claim', verbose_name='Claim')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('dispensed_by', models.CharField(max_length=128, verbose_name='Dispensed By')),
                ('payment_type', models.CharField(choices=[('a', 'Assignment'), ('na', 'Non-assignment')], max_length=15, verbose_name='Payment Type')),
                ('payment_terms', models.CharField(max_length=256, verbose_name='Payment Terms')),
                ('payment_made', models.IntegerField(default=0, verbose_name='Payment Made')),
                ('claim', models.ForeignKey(to='clients.Claim', verbose_name='Claim')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('description', models.CharField(max_length=512, verbose_name='Description')),
                ('unit_price', models.IntegerField(default=0, verbose_name='Unit Price')),
                ('quantity', models.IntegerField(default=0, verbose_name='Quantity')),
                ('invoice', models.ForeignKey(to='clients.Invoice', verbose_name='Invoice')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Laboratory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('information', models.CharField(choices=[('moll', 'MA Orthotics Laboratory Ltd\n11975 W Sample Rd\nCoral Springs, FL  331000\nPhone: (754) 206-6110\nFax: (754) 206-6109')], max_length=512, verbose_name='Information')),
                ('insurance_letter', models.ForeignKey(null=True, to='clients.InsuranceLetter', blank=True, verbose_name='Insurance Letter')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=128, blank=True, verbose_name='First Name')),
                ('last_name', models.CharField(default='', max_length=128, blank=True, verbose_name='Last Name')),
                ('gender', models.CharField(choices=[('m', 'Male'), ('f', 'Female')], default='', max_length=6, blank=True, verbose_name='Gender')),
                ('birth_date', models.DateField(null=True, blank=True, verbose_name='Birth Date')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Dependent',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, serialize=False, parent_link=True, primary_key=True, to='clients.Person')),
                ('relationship', models.CharField(choices=[('s', 'Spouse'), ('c', 'Child')], default='', max_length=6, blank=True, verbose_name='Relationship')),
            ],
            options={
            },
            bases=('clients.person',),
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, serialize=False, parent_link=True, primary_key=True, to='clients.Person')),
                ('address', models.CharField(default='', max_length=128, blank=True, verbose_name='Address')),
                ('city', models.CharField(default='', max_length=128, blank=True, verbose_name='City')),
                ('postal_code', models.CharField(default='', max_length=6, blank=True, verbose_name='Postal Code')),
                ('phone_number', models.CharField(default='', max_length=14, blank=True, verbose_name='Phone Number')),
                ('cell_number', models.CharField(default='', max_length=14, blank=True, verbose_name='Cell Number')),
                ('email', models.EmailField(verbose_name='Email', null=True, blank=True, max_length=254)),
                ('health_care_number', models.CharField(default='', max_length=20, blank=True, verbose_name='Health Care Number')),
                ('employer', models.CharField(default='', max_length=128, blank=True, verbose_name='Employer')),
                ('credit', models.SmallIntegerField(default=0, blank=True, verbose_name='Credit')),
                ('referred_by', models.CharField(default='', max_length=128, blank=True, verbose_name='Referred By')),
                ('notes', models.TextField(default='', blank=True, verbose_name='Notes')),
                ('dependents', models.ManyToManyField(to='clients.Dependent', null=True, blank=True, verbose_name='Dependents')),
            ],
            options={
            },
            bases=('clients.person',),
        ),
        migrations.CreateModel(
            name='ProofOfManufacturing',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('invoice_date', models.DateField(verbose_name='Invoice Date')),
                ('product', models.CharField(max_length=256, verbose_name='Product')),
                ('quantity', models.IntegerField(default=0, verbose_name='Quantity')),
                ('laboratory_supervisor', models.CharField(max_length=128, verbose_name='Laboratory Supervisor')),
                ('raw_materials', models.TextField(verbose_name='Raw Materials')),
                ('manufacturing', models.TextField(verbose_name='Manufacturing')),
                ('casting_technique', models.TextField(verbose_name='Casting Technique')),
                ('claim', models.ForeignKey(to='clients.Claim', verbose_name='Claim')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='laboratory',
            name='proof_of_manufacturing',
            field=models.ForeignKey(null=True, to='clients.ProofOfManufacturing', blank=True, verbose_name='Proof of Manufacturing'),
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
            field=models.ForeignKey(null=True, to='clients.Dependent', blank=True, verbose_name='Spouse'),
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
            field=models.ForeignKey(null=True, to='clients.Client', blank=True, verbose_name='Client'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='claim',
            name='coverage_types',
            field=models.ManyToManyField(to='clients.CoverageType', null=True, blank=True, verbose_name='Coverage Types'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='claim',
            name='patient',
            field=models.ForeignKey(null=True, related_name='patient', to='clients.Person', blank=True, verbose_name='Patient'),
            preserve_default=True,
        ),
    ]
