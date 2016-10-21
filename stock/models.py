# coding=utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Stock(models.Model):
    stockid = models.CharField('产品ID', max_length=30, unique=True)
    stockname = models.CharField('产品名称', max_length=30, unique=True)
    stockprice = models.DecimalField('当前价格', max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.stockid.__str__()+'_'+self.stockname.__str__()