# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_insurance_spouse'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dispensed_by', models.CharField(max_length=128)),
                ('payment_type', models.CharField(choices=[('Assignment', 'Assignment'), ('Non-assignment', 'Non-assignment')], max_length=6)),
                ('payment_terms', models.CharField(max_length=256)),
                ('payment', models.IntegerField(default=0)),
                ('claim', models.ForeignKey(to='clients.Claim')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=512)),
                ('unit_price', models.IntegerField(default=0)),
                ('quantity', models.IntegerField(default=0)),
                ('invoice', models.ForeignKey(to='clients.Invoice')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
