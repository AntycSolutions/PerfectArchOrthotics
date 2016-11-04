# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2016-11-03 21:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0041_auto_20161103_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='referred_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='referred_set', to='clients.Person', verbose_name='Referred By'),
        ),
        migrations.AlterField(
            model_name='dependent',
            name='primary',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.Client'),
        ),
        migrations.AlterField(
            model_name='laboratory',
            name='information',
            field=models.CharField(choices=[('moll', 'MA Orthotics Laboratory Ltd\n11975 W Sample Rd\nCoral Springs, FL  331000\nUSA\nPhone: (754) 206-6110\nFax: (754) 206-6109\nLaboratory Supervisor: M. Asam C.Ped.'), ('ooli', 'OOLab Inc.\n42 Niagara St\nHamilton, ON  L8L 6A2\nCanada\nToll Free: 1-888-873-3316\nPhone: (905) 521-1230\nFax: (905) 521-1210\nEmail: info@oolab.com\nLaboratory Supervisor: A. Boyle'), ('aror', 'Ares Orthotics\n107 Ave SE\nCalgary, AB  T2Z 3R7\nCanada\nPhone: (403) 398-5629\nFax: (403) 398-5635\nEmail: acct@aresorthotics.com\nLaboratory Supervisor: B. Domosky'), ('paoi', 'The Perfect Arch Orthotics Inc.\n10540 - 169 St.\nEdmonton, AB  T5P 3X6\nCanada\nPhone: (587) 400-4588\nFax: (587) 400-4566')], max_length=8, verbose_name='Information'),
        ),
        migrations.AlterField(
            model_name='proofofmanufacturing',
            name='laboratory',
            field=models.CharField(choices=[('moll', 'MA Orthotics Laboratory Ltd\n11975 W Sample Rd\nCoral Springs, FL  331000\nUSA\nPhone: (754) 206-6110\nFax: (754) 206-6109\nLaboratory Supervisor: M. Asam C.Ped.'), ('ooli', 'OOLab Inc.\n42 Niagara St\nHamilton, ON  L8L 6A2\nCanada\nToll Free: 1-888-873-3316\nPhone: (905) 521-1230\nFax: (905) 521-1210\nEmail: info@oolab.com\nLaboratory Supervisor: A. Boyle'), ('aror', 'Ares Orthotics\n107 Ave SE\nCalgary, AB  T2Z 3R7\nCanada\nPhone: (403) 398-5629\nFax: (403) 398-5635\nEmail: acct@aresorthotics.com\nLaboratory Supervisor: B. Domosky'), ('paoi', 'The Perfect Arch Orthotics Inc.\n10540 - 169 St.\nEdmonton, AB  T5P 3X6\nCanada\nPhone: (587) 400-4588\nFax: (587) 400-4566')], max_length=4),
        ),
    ]
