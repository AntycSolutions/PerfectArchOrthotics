# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0037_auto_20160511_0036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='biomechanicalgait',
            name='claim',
        ),
        migrations.AddField(
            model_name='biomechanicalgait',
            name='patient',
            field=models.ForeignKey(default=1, to='clients.Person'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='biomechanicalgait',
            name='provider',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
    ]
