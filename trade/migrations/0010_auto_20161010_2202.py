# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-10 22:02
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0009_auto_20161010_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='create',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 10, 22, 2, 26, 651000), verbose_name='\u6536\u6b3e\u65f6\u95f4'),
        ),
    ]
