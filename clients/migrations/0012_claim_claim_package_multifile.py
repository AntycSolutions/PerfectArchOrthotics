# -*- coding: utf-8 -*-
from django.db import migrations


def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Claim = apps.get_model("clients", "Claim")
    ClaimAttachment = apps.get_model("clients", "ClaimAttachment")
    db_alias = schema_editor.connection.alias
    for claim in Claim.objects.using(db_alias):
        if claim.claim_package:
            ClaimAttachment.objects.create(attachment=claim.claim_package,
                                           claim=claim)


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0011_auto_20150713_2117'),
    ]

    operations = [
        migrations.RunPython(
            forwards_func,
        ),
    ]
