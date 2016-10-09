# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-04 01:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0001_initial'),
        ('sale', '0006_auto_20161002_2350'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='bindteacher',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='teacher.Teacher'),
            preserve_default=False,
        ),
    ]
