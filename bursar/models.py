# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Bursar(models.Model):
    bursarId = models.CharField('财务ID', max_length=20, unique=True)
    company = models.CharField('公司', max_length=30, )
    department = models.CharField('部门', max_length=30, )
    binduser = models.ForeignKey(User, default=1)