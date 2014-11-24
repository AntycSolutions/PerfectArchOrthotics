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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('submittedDate', models.DateTimeField(auto_now_add=True)),
                ('invoiceDate', models.DateTimeField(null=True, blank=True)),
                ('paidDate', models.DateTimeField(null=True, blank=True)),
                ('amountClaimed', models.IntegerField(default=0, blank=True)),
                ('expectedBack', models.IntegerField(default=0, blank=True)),
                ('paymentType', models.CharField(default='', blank=True, max_length=6, choices=[('CASH', 'Cash'), ('CHEQUE', 'Cheque'), ('CREDIT', 'Credit')])),
                ('claimType', models.CharField(default='', blank=True, max_length=21, choices=[('Orthotics', 'Orthotics'), ('Compression_stockings', 'Compression Stockings'), ('Orthopedic_shoes', 'Orthopedic Shoes')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CoverageType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('coverageType', models.CharField(default='', blank=True, max_length=21, choices=[('Orthotics', 'Orthotics'), ('Compression_stockings', 'Compression Stockings'), ('Orthopedic_shoes', 'Orthopedic Shoes')])),
                ('coveragePercent', models.IntegerField(null=True, blank=True)),
                ('maxClaimAmount', models.IntegerField(default=0, blank=True)),
                ('totalClaimed', models.IntegerField(null=True, blank=True)),
                ('quantity', models.IntegerField(null=True, blank=True)),
                ('period', models.IntegerField(default=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Insurance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('provider', models.CharField(default='', blank=True, max_length=128)),
                ('policyNumber', models.CharField(default='', blank=True, max_length=128)),
                ('contractNumber', models.CharField(default='', blank=True, max_length=128)),
                ('billing', models.CharField(default='', blank=True, max_length=8, choices=[('Direct', 'Direct'), ('Indirect', 'Indirect')])),
                ('gaitScan', models.BooleanField(default=False)),
                ('insuranceCard', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InsuranceClaim',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amountClaimed', models.IntegerField(default=0, blank=True)),
                ('claim', models.ForeignKey(to='clients.Claim')),
                ('coverageType', models.ForeignKey(to='clients.CoverageType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstName', models.CharField(default='', blank=True, max_length=128)),
                ('lastName', models.CharField(default='', blank=True, max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Dependent',
            fields=[
                ('person_ptr', models.OneToOneField(serialize=False, primary_key=True, auto_created=True, parent_link=True, to='clients.Person')),
                ('relationship', models.CharField(default='', blank=True, max_length=6, choices=[('Spouse', 'Spouse'), ('Child', 'Child')])),
                ('gender', models.CharField(default='', blank=True, max_length=6, choices=[('Male', 'Male'), ('Female', 'Female')])),
                ('birthdate', models.DateField(null=True, blank=True)),
            ],
            options={
            },
            bases=('clients.person',),
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('person_ptr', models.OneToOneField(serialize=False, primary_key=True, auto_created=True, parent_link=True, to='clients.Person')),
                ('address', models.CharField(default='', blank=True, max_length=128)),
                ('city', models.CharField(default='', blank=True, max_length=128)),
                ('postalCode', models.CharField(default='', blank=True, max_length=6)),
                ('phoneNumber', models.CharField(default='', blank=True, max_length=14)),
                ('cellNumber', models.CharField(default='', blank=True, max_length=14)),
                ('email', models.EmailField(null=True, blank=True, max_length=254)),
                ('healthcareNumber', models.CharField(default='', blank=True, max_length=20)),
                ('birthdate', models.DateField(blank=True)),
                ('gender', models.CharField(default='', blank=True, max_length=6, choices=[('Male', 'Male'), ('Female', 'Female')])),
                ('employer', models.CharField(default='', blank=True, max_length=128)),
                ('credit', models.SmallIntegerField(default=0, blank=True)),
                ('referredBy', models.CharField(default='', blank=True, max_length=128)),
                ('notes', models.TextField(default='', blank=True)),
                ('dependents', models.ManyToManyField(null=True, blank=True, to='clients.Dependent')),
            ],
            options={
            },
            bases=('clients.person',),
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateAdded', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(to='clients.Client')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='insurance',
            name='client',
            field=models.ForeignKey(to='clients.Client'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='insurance',
            name='spouse',
            field=models.ForeignKey(null=True, to='clients.Dependent', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coveragetype',
            name='insurance',
            field=models.ForeignKey(to='clients.Insurance'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='claim',
            name='client',
            field=models.ForeignKey(null=True, to='clients.Client', blank=True, related_name='uses_coverage_of'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='claim',
            name='insurance',
            field=models.ForeignKey(null=True, to='clients.Insurance', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='claim',
            name='patient',
            field=models.ForeignKey(null=True, to='clients.Person', blank=True),
            preserve_default=True,
        ),
    ]
