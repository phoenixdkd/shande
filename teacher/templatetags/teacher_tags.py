# coding=utf-8
from django import template
from django.template.defaultfilters import stringfilter
from teacher.models import *
register = template.Library()

#
# @register.filter(name="maskphone")
# @stringfilter
# def maskphone(phone):
#     if phone.__len__() < 5:
#         return '***'
#     return phone[0:3]+'****'+phone[7:]

@register.simple_tag
def getTeacherIdByUserId(uid):
    try:
        teacher = Teacher.objects.get(binduser__id=uid)
        return teacher.teacherId
    except:
        return "未找到绑定的老师ID"

@register.simple_tag
def getTeacherCompanyByUserId(uid):
    try:
        teacher = Teacher.objects.get(binduser__id=uid)
        return teacher.company
    except:
        return "未找到绑定的老师ID"

@register.simple_tag
def getTeacherDepartmentByUserId(uid):
    try:
        teacher = Teacher.objects.get(binduser__id=uid)
        return teacher.department
    except:
        return "未找到绑定的老师ID"


