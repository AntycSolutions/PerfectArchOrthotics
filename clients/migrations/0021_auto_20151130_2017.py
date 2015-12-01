# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0020_auto_20151006_1118'),
    ]

    operations = [
        migrations.AddField(
            model_name='proofofmanufacturing',
            name='laboratory',
            field=models.CharField(choices=[('moll', 'MA Orthotics Laboratory Ltd\n11975 W Sample Rd\nCoral Springs, FL  331000\nUSA\nPhone: (754) 206-6110\nFax: (754) 206-6109\nLaboratory Supervisor: M. Asam C.Ped.'), ('ooli', 'OOLab Inc.\n42 Niagara St\nHamilton, ON  L8L 6A2\nCanada\nToll Free: 1-888-873-3316\nPhone: (905) 521-1230\nFax: (905) 521-1210\nEmail: info@oolab.com\nLaboratory Supervisor: A. Boyle'), ('aror', 'Ares Orthotics\n107 Ave SE\nCalgary, AB  T2Z 3R7\nCanada\nPhone: (403) 398-5629\nFax: (403) 398-5635\nEmail: acct@aresorthotics.com\nLaboratory Supervisor: B. Domosky'), ('paoi', 'The Perfect Arch Orthotics Inc.\n10540 - 169 ST\nEdmonton, AB  T5P 3X6\nCanada\nPhone: (587) 400-4588\nFax: (587) 400-4566\nEmail: danny@perfectarch.ca\nLaboratory Supervisor: Danny Mu')], default='moll', max_length=4),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='laboratory',
            name='information',
            field=models.CharField(choices=[('moll', 'MA Orthotics Laboratory Ltd\n11975 W Sample Rd\nCoral Springs, FL  331000\nUSA\nPhone: (754) 206-6110\nFax: (754) 206-6109\nLaboratory Supervisor: M. Asam C.Ped.'), ('ooli', 'OOLab Inc.\n42 Niagara St\nHamilton, ON  L8L 6A2\nCanada\nToll Free: 1-888-873-3316\nPhone: (905) 521-1230\nFax: (905) 521-1210\nEmail: info@oolab.com\nLaboratory Supervisor: A. Boyle'), ('aror', 'Ares Orthotics\n107 Ave SE\nCalgary, AB  T2Z 3R7\nCanada\nPhone: (403) 398-5629\nFax: (403) 398-5635\nEmail: acct@aresorthotics.com\nLaboratory Supervisor: B. Domosky'), ('paoi', 'The Perfect Arch Orthotics Inc.\n10540 - 169 ST\nEdmonton, AB  T5P 3X6\nCanada\nPhone: (587) 400-4588\nFax: (587) 400-4566\nEmail: danny@perfectarch.ca\nLaboratory Supervisor: Danny Mu')], verbose_name='Information', max_length=8),
        ),
    ]
