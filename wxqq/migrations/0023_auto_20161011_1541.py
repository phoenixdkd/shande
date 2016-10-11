# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-11 15:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wxqq', '0022_auto_20161011_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qq',
            name='bindsale',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sale.Sale'),
        ),
        migrations.AlterField(
            model_name='wx',
            name='bindsale',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sale.Sale'),
        ),
        migrations.AlterField(
            model_name='wx',
            name='modify',
            field=models.DateField(null=True, unique=True, verbose_name='\u4fee\u6539\u65f6\u95f4'),
        ),
    ]
