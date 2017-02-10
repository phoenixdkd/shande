# coding=utf-8
from __future__ import unicode_literals
import traceback
from django.db import models
from django.utils import timezone

# Create your models here.
class Systemlog(models.Model):
    name = models.CharField('维护人员', max_length=30)
    fixTime = models.DateTimeField('维护时间', null=True)
    fixContent = models.CharField('维护内容', max_length=300)

    def __str__(self):
        return self.name.__str__()
