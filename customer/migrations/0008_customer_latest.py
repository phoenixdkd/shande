# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-12 10:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0007_customer_realuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='latest',
            field=models.DateTimeField(null=True, verbose_name='\u6700\u8fd1\u5408\u4f5c\u65f6\u95f4'),
        ),
    ]
