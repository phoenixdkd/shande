# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from customer.models import *

# Create your models here.

class Spot(models.Model):
    customer = models.ForeignKey(Customer)
    create = models.DateTimeField('交易时间')
    # 0 首次入金; 10 加仓; 20 减仓;  30 盈; 40 亏; 99 其他
    type = models.IntegerField('交易动作', default=0)
    cash = models.DecimalField('净入金', max_digits=15, decimal_places=2, default=0)
    profit = models.DecimalField('盈亏', max_digits=15, decimal_places=2, default=0)
    tax = models.DecimalField('手续费', max_digits=15, decimal_places=2, default=0)
