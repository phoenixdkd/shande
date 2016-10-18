# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from bursar.models import Bursar


# Create your models here.
class SpotTeacher(models.Model):
    teacherId = models.CharField('老师ID', max_length=20, unique=True)
    company = models.CharField('公司', max_length=30, )
    department = models.CharField('部门', max_length=30, )
    group = models.CharField('组', max_length=30, null=True, blank=True)
    binduser = models.ForeignKey(User, null=True, blank=True)

    def getTeacherList( self ):
        teachers = self.teacher_set.all()
        return teachers

class Teacher(models.Model):
    teacherId = models.CharField('老师ID', max_length=20, unique=True)
    company = models.CharField('公司', max_length=30, )
    department = models.CharField('部门', max_length=30, )
    group = models.CharField('组', max_length=30, null=True, blank=True)
    binduser = models.ForeignKey(User, null=True, blank=True)
    bindbursar = models.ForeignKey(Bursar, null=True, blank=True)
    bindspotteacher = models.ForeignKey(SpotTeacher, null=True, blank=True)

    def getSaleList(self):
        sales = self.sale_set.all()
        return sales


