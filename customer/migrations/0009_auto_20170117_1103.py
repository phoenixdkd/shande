# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-17 11:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0008_customer_latest'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='tcrude',
            field=models.BooleanField(default=False, verbose_name='\u8001\u5e0810W+'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='crude',
            field=models.BooleanField(default=False, verbose_name='\u5f00\u53d110W+'),
        ),
    ]