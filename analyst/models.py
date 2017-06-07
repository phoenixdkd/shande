# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Analyst(models.Model):
    analystId = models.CharField('技术分析师ID', max_length=20, unique=True)
    company = models.CharField('公司', max_length=2, null=True, blank=True)
    department = models.CharField('部门', max_length=30, null=True, blank=True)
    binduser = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    # def getTeacherList(self):
    #     return self.teacher_set.all()
