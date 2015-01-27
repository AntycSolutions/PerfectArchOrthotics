# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from utils import model_utils


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_auto_20150122_0206'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShoeAttributes',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('size', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('3.5', '3.5'), ('4', '4'), ('4.5', '4.5'), ('5', '5'), ('5.5', '5.5'), ('6', '6'), ('6.5', '6.5'), ('7', '7'), ('7.5', '7.5'), ('8', '8'), ('8.5', '8.5'), ('9', '9'), ('9.5', '9.5'), ('10', '10'), ('10.5', '10.5'), ('11', '11'), ('11.5', '11.5'), ('12', '12'), ('12.5', '12.5'), ('13', '13'), ('13.5', '13.5'), ('14', '14')], verbose_name='Size', max_length=4)),
                ('quantity', models.IntegerField(verbose_name='Quantity', default=0)),
                ('shoe', models.ForeignKey(verbose_name='Shoe', to='inventory.Shoe')),
            ],
            options={
            },
            bases=(models.Model, model_utils.FieldList),
        ),
        migrations.RemoveField(
            model_name='shoe',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='shoe',
            name='size',
        ),
    ]
