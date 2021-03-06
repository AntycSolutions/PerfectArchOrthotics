# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2019-01-27 23:11
from __future__ import unicode_literals

from django.db import migrations
from django.db import models


def forwards_copy_invoice_number(apps, schema_editor):
    Invoice = apps.get_model('clients', 'Invoice')
    db_alias = schema_editor.connection.alias
    Invoice.objects.using(db_alias).update(invoice_number=models.F('claim_id'))


def backwards_copy_invoice_number(apps, schema_editor):
    Invoice = apps.get_model('clients', 'Invoice')
    db_alias = schema_editor.connection.alias
    Invoice.objects.using(db_alias).update(invoice_number=None)


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0052_invoice_invoice_number'),
    ]

    operations = [
        migrations.RunPython(
            forwards_copy_invoice_number, backwards_copy_invoice_number
        )
    ]
