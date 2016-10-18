# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from sale.models import *
from teacher.models import *
from bursar.models import Bursar
from wxqq.models import Wx, Qq

from django.utils import timezone


# Create your models here.
class Customer(models.Model):
    name = models.CharField('姓名', max_length=30)
    phone = models.CharField('电话', max_length=30, null=True)
    wxid = models.CharField('微信号', max_length=30, null=True, default="")
    wxname = models.CharField('微信昵称', max_length=30, null=True, default="")
    qqid = models.CharField('QQ', max_length=30, null=True, default="")
    qqname = models.CharField('QQ昵称', max_length=30, null=True, default="")
    startup = models.IntegerField('初始资金', default=0)
    gem = models.BooleanField('创业板', default=False)
    crude = models.BooleanField('原油10W+', default=False)
    spotStatus = models.CharField('现货客户状态', max_length=5, default="未开发")
    spotTime = models.DateTimeField('现货输送时间', null=True)
    spotDay = models.IntegerField('开发周期', null=True)
    spotTeacher = models.ForeignKey(SpotTeacher, null=True)
    spotCash = models.DecimalField('现货资金', max_digits=20, decimal_places=2, default=50000)
    vip = models.BooleanField('大客户', default=False)
    honest = models.BooleanField('诚信客户', default=True)
    # message list
    # 1 客户不回消息
    # 2 给票不买 
    # 3 分成太高 
    # 4 要看票 
    # 5 今天不买，下次再买 
    # 6 不发截图 
    # 7 合作资金不足 
    # 8 买错票 
    # 9 客户信息有误,需再核实 
    message = models.CharField('说明', max_length=30, default="")
    # 0 新客户；10 待跟进 ；20 无交易； 30 退回； 40 有效；98 不诚信删除; 99 删除；
    status = models.IntegerField('状态', default=0)
    sales = models.ForeignKey(Sale)
    saleswx = models.ForeignKey(Wx, null=True, blank=True)
    salesqq = models.ForeignKey(Qq, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, null=True, blank=True)
    bursar = models.ForeignKey(Bursar, null=True, blank=True)
    receivable = models.IntegerField('盈利总额', default=0)
    first_trade_cash = models.DecimalField('首笔资金', max_digits=20, decimal_places=2, default=0)
    first_trade = models.DateTimeField('首单时间', null=True)
    create = models.DateTimeField('创建时间')
    modify = models.DateTimeField('更新时间')