# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from teacher.models import *

# Create your models here.
class Sale(models.Model):
    saleId = models.CharField('开发ID', max_length=20, unique=True)
    company = models.CharField('公司', max_length=30, )
    department = models.CharField('部门', max_length=30, )
    group = models.CharField('组', max_length=30, default="")
    binduser = models.ForeignKey(User, default=1)
    bindteacher = models.ForeignKey(Teacher, default=1)


class SaleManagerPassword(models.Model):
    company = models.CharField('公司', max_length=30, )
    department = models.CharField('部门', max_length=30, )
    password = models.CharField('密码', max_length=30, )