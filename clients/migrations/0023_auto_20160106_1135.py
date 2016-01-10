# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0022_receipt'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='credit2',
            field=models.DecimalField(default=Decimal('0'), max_digits=5, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='laboratory',
            name='information',
            field=models.CharField(verbose_name='Information', choices=[('moll', 'MA Orthotics Laboratory Ltd\n11975 W Sample Rd\nCoral Springs, FL  331000\nUSA\nPhone: (754) 206-6110\nFax: (754) 206-6109\n\nLaboratory Supervisor: M. Asam C.Ped.'), ('ooli', 'OOLab Inc.\n42 Niagara St\nHamilton, ON  L8L 6A2\nCanada\nToll Free: 1-888-873-3316\nPhone: (905) 521-1230\nFax: (905) 521-1210\nEmail: info@oolab.com\nLaboratory Supervisor: A. Boyle'), ('aror', 'Ares Orthotics\n107 Ave SE\nCalgary, AB  T2Z 3R7\nCanada\nPhone: (403) 398-5629\nFax: (403) 398-5635\nEmail: acct@aresorthotics.com\nLaboratory Supervisor: B. Domosky'), ('paoi', 'The Perfect Arch Orthotics Inc.\n10540 - 169 ST\nEdmonton, AB  T5P 3X6\nCanada\nPhone: (587) 400-4588\nFax: (587) 400-4566\nEmail: danny@perfectarch.ca\nLaboratory Supervisor: Danny Mu')], max_length=8),
        ),
        migrations.AlterField(
            model_name='proofofmanufacturing',
            name='laboratory',
            field=models.CharField(choices=[('moll', 'MA Orthotics Laboratory Ltd\n11975 W Sample Rd\nCoral Springs, FL  331000\nUSA\nPhone: (754) 206-6110\nFax: (754) 206-6109\n\nLaboratory Supervisor: M. Asam C.Ped.'), ('ooli', 'OOLab Inc.\n42 Niagara St\nHamilton, ON  L8L 6A2\nCanada\nToll Free: 1-888-873-3316\nPhone: (905) 521-1230\nFax: (905) 521-1210\nEmail: info@oolab.com\nLaboratory Supervisor: A. Boyle'), ('aror', 'Ares Orthotics\n107 Ave SE\nCalgary, AB  T2Z 3R7\nCanada\nPhone: (403) 398-5629\nFax: (403) 398-5635\nEmail: acct@aresorthotics.com\nLaboratory Supervisor: B. Domosky'), ('paoi', 'The Perfect Arch Orthotics Inc.\n10540 - 169 ST\nEdmonton, AB  T5P 3X6\nCanada\nPhone: (587) 400-4588\nFax: (587) 400-4566\nEmail: danny@perfectarch.ca\nLaboratory Supervisor: Danny Mu')], max_length=4),
        ),
    ]
