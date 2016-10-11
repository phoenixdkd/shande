# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-11 09:08
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0018_auto_20161010_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='create',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 11, 9, 8, 36, 763000), verbose_name='\u521b\u5efa\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='modify',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 11, 9, 8, 36, 763000), verbose_name='\u66f4\u65b0\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='sales',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sale.Sale'),
        ),
    ]
