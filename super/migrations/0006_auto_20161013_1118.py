# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-13 11:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('super', '0005_auto_20161002_1327'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='commit',
            field=models.IntegerField(default=0, verbose_name='\u63d0\u4ea4\u6570'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='grade',
            field=models.IntegerField(default=0, verbose_name='\u6709\u6548\u5ba2\u6237\u6570'),
        ),
    ]
