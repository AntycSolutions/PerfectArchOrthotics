# -*- coding: utf-8 -*-
from django.db import migrations


def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    ClaimCoverage = apps.get_model("clients", "ClaimCoverage")
    db_alias = schema_editor.connection.alias
    for claim_coverage in ClaimCoverage.objects.using(db_alias):
        claim_coverage.actual_paid_date = claim_coverage.claim.insurance_paid_date
        claim_coverage.save()


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_claimcoverage_actual_paid_date'),
    ]

    operations = [
        migrations.RunPython(
            forwards_func,
        ),
    ]
