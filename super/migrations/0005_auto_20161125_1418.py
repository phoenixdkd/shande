# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-11-25 14:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('super', '0004_auto_20161113_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='title',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='super.Title'),
        ),
    ]
