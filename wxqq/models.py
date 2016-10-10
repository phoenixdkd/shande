# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from sale.models import Sale
# Create your models here.
from django.contrib.auth.models import User

# Create your models here.
class Wx(models.Model):
    wxid = models.CharField('微信号', max_length=30, unique=True)
    wxname = models.CharField('微信昵称', max_length=30, )
    bindsale = models.ForeignKey(Sale, null=True, blank=True)  #绑定开发

class Qq(models.Model):
    qqid = models.CharField('qq号', max_length=30, unique=True)
    qqname = models.CharField('qq昵称', max_length=30, )
    bindsale = models.ForeignKey(Sale, null=True, blank=True)  # 绑定开发