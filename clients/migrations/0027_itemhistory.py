# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0026_note'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('cost', models.IntegerField()),
                ('unit_price', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(to='clients.Item')),
            ],
        ),
    ]
