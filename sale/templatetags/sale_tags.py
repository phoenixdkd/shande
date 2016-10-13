# coding=utf-8
from django import template
from django.template.defaultfilters import stringfilter
from sale.models import *
register = template.Library()

#
# @register.filter(name="maskphone")
# @stringfilter
# def maskphone(phone):
#     if phone.__len__() < 5:
#         return '***'
#     return phone[0:3]+'****'+phone[7:]

@register.simple_tag
def getSaleIdByUserId(uid):
    try:
        sale = Sale.objects.get(binduser__id=uid)
        return sale.saleId
    except:
        return "未找到绑定的开发ID"

@register.simple_tag
def getSaleCompanyByUserId(uid):
    try:
        sale = Sale.objects.get(binduser__id=uid)
        return sale.company
    except:
        return "未找到绑定的开发ID"

@register.simple_tag
def getSaleDepartmentByUserId(uid):
    try:
        sale = Sale.objects.get(binduser__id=uid)
        return sale.department
    except:
        return "未找到绑定的开发ID"

@register.simple_tag
def getChargebackByUserId(uid):
    try:
        user = User.objects.get(id=uid)
        commit = user.userprofile.commit
        grade = user.userprofile.grade
        return str(grade/commit *100) + '%'
    except:
        return 0

