# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-11-29 14:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0010_trade_dealtime'),
    ]

    operations = [
        migrations.AddField(
            model_name='trade',
            name='message',
            field=models.CharField(blank=True, default='', max_length=30, null=True, verbose_name='\u9000\u56de\u539f\u56e0'),
        ),
    ]
