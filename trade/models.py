# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from customer.models import *
from django.utils import timezone
from stock.models import *

# Create your models here.
class Trade(models.Model):
    customer = models.ForeignKey(Customer)
    # 0 未出货(新录入); 10 亏损; 11 已补亏;  20 盈利 提交财务收款; 30 已收款;

    status = models.IntegerField('交易状态', default=0)
    stock = models.ForeignKey(Stock, null=True, blank=True)
    stockid = models.CharField('产品ID', max_length=30, null=True, blank=True)
    stockname = models.CharField('产品名称', max_length=30, null=True, blank=True)
    buyprice = models.DecimalField('购入价格', max_digits=10, decimal_places=2, default=0)
    buycount = models.IntegerField('购入数量', default=0)
    buycash = models.DecimalField('购入总价',  max_digits=10, decimal_places=2, default=0)
    share = models.CharField('分成比例', max_length=5, default='5|5')
    sellprice = models.DecimalField('卖出价格',  max_digits=10, decimal_places=2, default=0)
    income = models.DecimalField('盈利', max_digits=10, decimal_places=2, default=0)
    commission = models.DecimalField('手续费', max_digits=10, decimal_places=2, default=0)
    # 支付宝
    paytype = models.CharField('收款类型', max_length=30, default="")
    create = models.DateTimeField('交易时间')
    paytime = models.DateTimeField('收款时间', default=None, null=True)
    paycash = models.DecimalField('收款金额', max_digits=10, decimal_places=2, default=0)


