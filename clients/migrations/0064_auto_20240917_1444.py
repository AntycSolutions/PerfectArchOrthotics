# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2024-09-17 20:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0063_auto_20240915_1546'),
    ]

    operations = [
        migrations.AddField(
            model_name='insuranceletter',
            name='company',
            field=models.CharField(choices=[('pa', 'Perfect Arch'), ('op', 'Orthotics Pros')], default='pa', max_length=2),
        ),
        migrations.AlterField(
            model_name='laboratory',
            name='information',
            field=models.CharField(choices=[('moll', 'MA Orthotics Laboratory Ltd\n11975 W Sample Rd\nCoral Springs, FL  331000\nUSA\n\nPhone: (754) 206-6110\nFax: (754) 206-6109\n\nLaboratory Supervisor: M. Asam C.Ped.'), ('aror', 'Ares Orthotics\n107 Ave SE\nCalgary, AB  T2Z 3R7\nCanada\n\nPhone: (403) 398-5629\nFax: (403) 398-5635\nEmail: acct@aresorthotics.com\nLaboratory Supervisor: B. Domosky'), ('iorl', 'International Orthotics Lab\n6777 Fairmount Drive SE\nCalgary, AB  T2H 0X6\nCanada\n\nPhone: (403) 236-8540\nFax: (403) 236-8539\nEmail: info@orthotic.ca\nLaboratory Supervisor: Lou-Anne Knopp'), ('paoi', 'The Perfect Arch Orthotics Inc.\n10540 - 169 St.\nEdmonton, AB  T5P 3X6\nCanada\n\nPhone: (587) 400-4588\nFax: (587) 400-4566\nEmail: info@perfectarch.ca\nLaboratory Supervisor: Danny Mu'), ('porl', 'Paragon Orthotic Laboratory\n1650 Cedar Hill Cross Road\nVictoria, BC  V8P 2P6\nCanada\n\nPhone: (250) 721-1112\nFax: (250) 721-1160\nEmail: info@paragonorthotic.com\nLaboratory Supervisor: Eve Podolsky'), ('orpr', 'Orthotics Pros\nSuite 201, 9426 51 Ave NW\nEdmoton, AB  T6E 5A6\nCanada\n\nPhone: (780) 556-8686\n\nEmail: info@orthoticspros.ca\nLaboratory Supervisor: Danny Mu')], max_length=8, verbose_name='Information'),
        ),
        migrations.AlterField(
            model_name='proofofmanufacturing',
            name='laboratory',
            field=models.CharField(choices=[('moll', 'MA Orthotics Laboratory Ltd\n11975 W Sample Rd\nCoral Springs, FL  331000\nUSA\n\nPhone: (754) 206-6110\nFax: (754) 206-6109\n\nLaboratory Supervisor: M. Asam C.Ped.'), ('aror', 'Ares Orthotics\n107 Ave SE\nCalgary, AB  T2Z 3R7\nCanada\n\nPhone: (403) 398-5629\nFax: (403) 398-5635\nEmail: acct@aresorthotics.com\nLaboratory Supervisor: B. Domosky'), ('iorl', 'International Orthotics Lab\n6777 Fairmount Drive SE\nCalgary, AB  T2H 0X6\nCanada\n\nPhone: (403) 236-8540\nFax: (403) 236-8539\nEmail: info@orthotic.ca\nLaboratory Supervisor: Lou-Anne Knopp'), ('paoi', 'The Perfect Arch Orthotics Inc.\n10540 - 169 St.\nEdmonton, AB  T5P 3X6\nCanada\n\nPhone: (587) 400-4588\nFax: (587) 400-4566\nEmail: info@perfectarch.ca\nLaboratory Supervisor: Danny Mu'), ('porl', 'Paragon Orthotic Laboratory\n1650 Cedar Hill Cross Road\nVictoria, BC  V8P 2P6\nCanada\n\nPhone: (250) 721-1112\nFax: (250) 721-1160\nEmail: info@paragonorthotic.com\nLaboratory Supervisor: Eve Podolsky'), ('orpr', 'Orthotics Pros\nSuite 201, 9426 51 Ave NW\nEdmoton, AB  T6E 5A6\nCanada\n\nPhone: (780) 556-8686\n\nEmail: info@orthoticspros.ca\nLaboratory Supervisor: Danny Mu')], max_length=4),
        ),
    ]
