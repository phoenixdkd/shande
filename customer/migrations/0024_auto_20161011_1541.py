# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-11 15:41
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0023_auto_20161011_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='create',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 11, 15, 41, 56, 759000), verbose_name='\u521b\u5efa\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='modify',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 11, 15, 41, 56, 759000), verbose_name='\u66f4\u65b0\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='sales',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sale.Sale'),
        ),
    ]
