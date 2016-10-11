# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from sale.models import Sale
# Create your models here.
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Wx(models.Model):
    wxid = models.CharField('微信号', max_length=30, unique=True)
    wxname = models.CharField('微信昵称', max_length=30, )
    friend = models.IntegerField('好友数', default=0)
    modify = models.DateField('修改时间', null=True)
    create = models.DateField('创建时间', default=datetime.date.today())
    delete = models.DateField('失效时间', null=True)
    bindsale = models.ForeignKey(Sale, null=True, blank=True)  #绑定开发

class WxFriendHis(models.Model):
    wx = models.ForeignKey(Wx)
    day = models.DateField('修改时间', null=True, unique=True)
    delta = models.IntegerField('变化量', default=0)
    total = models.IntegerField('总量', default=0)

class Qq(models.Model):
    qqid = models.CharField('qq号', max_length=30, unique=True)
    qqname = models.CharField('qq昵称', max_length=30, )
    friend = models.IntegerField('好友数', default=0)
    modify = models.DateField('修改时间', null=True)
    create = models.DateField('创建时间', null=True)
    delete = models.DateField('失效时间', null=True)
    bindsale = models.ForeignKey(Sale, null=True, blank=True)  # 绑定开发

class QqFriendHis(models.Model):
    qq = models.ForeignKey(Qq)
    day = models.DateField('修改时间', null=True, unique=True)
    delta = models.IntegerField('变化量', default=0)
    total = models.IntegerField('总量', default=0)