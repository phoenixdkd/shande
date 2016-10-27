# coding=utf-8
from django import template
from django.template.defaultfilters import stringfilter
from django.db.models import Sum
from teacher.models import *
from customer.models import *
from trade.models import *
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

@register.simple_tag()
def getCustomerCountByTeacher(teacherid):
    try:
        customers = Customer.objects.filter(teacher_id=teacherid)
        return customers.__len__()
    except:
        return 0

@register.simple_tag()
def getNoSellTradeCountByTeacher(teacherid):
    try:
        trades = Trade.objects.filter(customer__teacher_id=teacherid, status=0)
        return trades.__len__()
    except:
        return 0

@register.simple_tag()
def getBuyCashTotalByTeacher(teacherid):
    try:
        trades = Trade.objects.filter(customer__teacher_id=teacherid)
        buycash = trades.aggregate(Sum('buycash'))
        if buycash['buycash__sum']:
            return buycash['buycash__sum']
        else:
            return 0
    except:
        return 0

@register.simple_tag()
def getPayCashTotalByTeacher(teacherid):
    try:
        trades = Trade.objects.filter(customer__teacher_id=teacherid)
        paycash = trades.aggregate(Sum('paycash'))
        if paycash['paycash__sum']:
            return paycash['paycash__sum']
        else:
            return 0
    except:
        return 0

@register.simple_tag()
def getDCustomerCountByTeacher(teacherid):
    try:
        customers = Customer.objects.filter(teacher_id=teacherid, spotStatus='D')
        return customers.__len__()
    except:
        return 0

@register.simple_tag()
def getDCustomerCountByTeacherAndDay(teacherid, day):
    try:
        y, m, d = day.split('-')
        customers = Customer.objects.filter(teacher_id=teacherid, spotStatus='D',
                                            spotTime__year=y, spotTime__month=m, spotTime__day=d)
        return customers.__len__()
    except:
        return 0

@register.simple_tag()
def getCustomerCountByStock(teacherid, stockid):
    try:
        customers = Customer.objects.filter(teacher_id=teacherid, trade__stock_id=stockid)
        return customers.__len__()
    except:
        return 0

@register.simple_tag()
def getMaxPriceByStock( teacherid, stockid ):
    try:
        trades = Trade.objects.filter(customer__teacher_id=teacherid, stock_id=stockid)
        trade = trades.latest('buyprice')
        return trade.buyprice
    except:
        return 0

@register.simple_tag()
def getMinPriceByStock( teacherid, stockid ):
    try:
        trades = Trade.objects.filter(customer__teacher_id=teacherid, stock_id=stockid)
        trade = trades.earliest('buyprice')
        return trade.buyprice
    except:
        return 0
