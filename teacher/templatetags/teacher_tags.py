# coding=utf-8
from django import template
from django.template.defaultfilters import stringfilter
from django.db.models import Sum
from teacher.models import *
from customer.models import *
from trade.models import *
import traceback
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
def getCustomerCountByTeacher(teacherid, startDate, endDate):
    try:
        customers = Customer.objects.filter(teacher_id=teacherid, trade__create__lte=endDate, trade__create__gte=startDate).distinct()
        return customers.__len__()
    except:
        return 0

@register.simple_tag()
def getNoSellTradeCountByTeacher(teacherid, startDate, endDate):
    try:
        trades = Trade.objects.filter(customer__teacher_id=teacherid, status=0,
                                      create__lte=endDate, create__gte=startDate)
        return trades.__len__()
    except:
        return 0

@register.simple_tag()
def getBuyCashTotalByTeacher(teacherid, startDate, endDate):
    try:
        trades = Trade.objects.filter(customer__teacher_id=teacherid, create__lte=endDate, create__gte=startDate)
        buycash = trades.aggregate(Sum('buycash'))
        if buycash['buycash__sum']:
            return buycash['buycash__sum']
        else:
            return 0
    except:
        return 0

@register.simple_tag()
def getPayCashTotalByTeacher(teacherid, startDate, endDate):
    try:
        trades = Trade.objects.filter(customer__teacher_id=teacherid, create__lte=endDate, create__gte=startDate)
        paycash = trades.aggregate(Sum('paycash'))
        if paycash['paycash__sum']:
            return paycash['paycash__sum']
        else:
            return 0
    except:
        return 0

@register.simple_tag()
def getSpotCustomerCountByTeacher(spotStatus, teacherid, startDate, endDate):
    try:
        customers = Customer.objects.filter(teacher_id=teacherid, spotStatus=spotStatus).distinct()
        if spotStatus != '未开发':
            customers = customers.filter(spotTime__lte=endDate, spotTime__gte=startDate).distinct()
        else:
            customers = customers.filter(create__lte=endDate, create_gte=startDate).distinct()
        return customers.__len__()
    except:
        traceback.print_exc()
        return 0

@register.simple_tag()
def getDCustomerCountByTeacher(teacherid, startDate, endDate):
    try:
        customers = Customer.objects.filter(teacher_id=teacherid, spotStatus='D', spotTime__lte=endDate,
                                            spotTime__gte=startDate)
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
