# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-11 14:43
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0012_auto_20161011_0909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='create',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 11, 14, 43, 39, 469000), verbose_name='\u6536\u6b3e\u65f6\u95f4'),
        ),
    ]
