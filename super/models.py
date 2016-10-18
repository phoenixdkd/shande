# coding=utf-8
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Title(models.Model):
    role_name = models.CharField(max_length=30, unique=True)
    role_desc = models.CharField(max_length=30, )

    def __str__(self):
        return self.role_name


class UserProfile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.CharField('公司', max_length=10, blank=True, null=True)
    commit = models.IntegerField('提交数', default=0)
    grade = models.IntegerField('有效客户数', default=0)
    department = models.CharField('部门', max_length=10, blank=True, null=True)
    cid = models.CharField('身份证号', max_length=18, blank=True, null=True)
    nick = models.CharField('真实姓名', max_length=10, blank=True, null=True)
    title = models.ForeignKey(Title)
    failcount = models.IntegerField('失败次数', default=-1)
    faillocktime = models.DateTimeField('失败锁定时间', null=True)

    def __str__(self):
        return self.user.username

class UserCommitHis(models.Model):
    user = models.ForeignKey(User)
    day = models.DateField('修改时间', null=True)
    delta = models.IntegerField('变化量', default=0)
    total = models.IntegerField('总量', default=0)

    class Meta:
        unique_together = ("user", 'day')

class UserGradeHis(models.Model):
    user = models.ForeignKey(User)
    day = models.DateField('修改时间', null=True)
    delta = models.IntegerField('变化量', default=0)
    total = models.IntegerField('总量', default=0)

    class Meta:
        unique_together = ("user", 'day')

class Config(models.Model):
    key = models.CharField(max_length=30)
    value = models.CharField(max_length=300)

    def __str__(self):
        return self.key

class Transmission(models.Model):
    user = models.OneToOneField(User)
    transmission = models.CharField(max_length=300)
    checked = models.BooleanField(default=False)