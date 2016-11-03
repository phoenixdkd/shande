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
    password = models.CharField('密码', max_length=30, default="")
    wxname = models.CharField('微信昵称', max_length=30, )
    friend = models.IntegerField('好友数', default=0)
    bindphone = models.CharField('绑定手机', max_length=30, default="")
    bindemail = models.CharField('绑定邮件', max_length=30, default="")
    bindqq = models.CharField('绑定QQ', max_length=30, default="")
    modify = models.DateField('修改时间', null=True)
    create = models.DateField('创建时间', null=True)
    delete = models.DateField('失效时间', null=True)
    reason = models.CharField('删除理由', max_length=30, default="")
    bindsale = models.ForeignKey(Sale, null=True, blank=True)  #绑定开发

class WxFriendHis(models.Model):
    wx = models.ForeignKey(Wx)
    day = models.DateField('修改时间', null=True)
    delta = models.IntegerField('变化量', default=0)
    total = models.IntegerField('总量', default=0)

    class Meta:
        unique_together = ("wx", 'day')

class Qq(models.Model):
    qqid = models.CharField('qq号', max_length=30, unique=True)
    password = models.CharField('密码', max_length=30, default="")
    protect = models.CharField('密码', max_length=30, default="")
    qqname = models.CharField('qq昵称', max_length=30, )
    friend = models.IntegerField('好友数', default=0)
    modify = models.DateField('修改时间', null=True)
    create = models.DateField('创建时间', null=True)
    delete = models.DateField('失效时间', null=True)
    reason = models.CharField('删除理由', max_length=30, default="")
    bindsale = models.ForeignKey(Sale, null=True, blank=True)  # 绑定开发

class QqFriendHis(models.Model):
    qq = models.ForeignKey(Qq)
    day = models.DateField('修改时间', null=True)
    delta = models.IntegerField('变化量', default=0)
    total = models.IntegerField('总量', default=0)

    class Meta:
        unique_together = ("qq", 'day')