# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2018-11-03 20:31
from __future__ import unicode_literals

from django.db import migrations


def copy_insurance(apps, schema_editor):
    Claim = apps.get_model('clients', 'Claim')  # get migration model
    for claim in Claim.objects.all():
        claim.insurances.add(claim.insurance)
        claim.save()


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0049_auto_20181103_1429'),
    ]

    operations = [
        migrations.RunPython(copy_insurance),
    ]