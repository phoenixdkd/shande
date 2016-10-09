# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-04 11:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wxqq', '0006_auto_20161004_0254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qq',
            name='bindsale',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sale.Sale'),
        ),
        migrations.AlterField(
            model_name='wx',
            name='bindsale',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sale.Sale'),
        ),
    ]
