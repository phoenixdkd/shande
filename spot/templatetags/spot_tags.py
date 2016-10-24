# coding=utf-8
from django import template
from django.template.defaultfilters import stringfilter
from django.db.models import Sum, Count
from customer.models import *
from trade.models import *
from spot.models import *
register = template.Library()

@register.simple_tag
def getCashTotalByCustomerId(customerId):
    try:
        spots = Spot.objects.filter(customer_id=customerId).aggregate(dcount=Sum('cash'))
        return spots['dcount']
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag
def getAddCountByCustomerId(customerId):
    try:
        spots = Spot.objects.filter(customer_id=customerId, cash__gt=0).aggregate(dcount=Count('id'))
        return spots['dcount']
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag
def getProfitTotalByCustomerId( customerId ):
    try:
        spots = Spot.objects.filter(customer_id=customerId).aggregate(dcount=Sum('profit'))
        return spots['dcount']
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag
def getTaxTotalByCustomerId( customerId ):
    try:
        spots = Spot.objects.filter(customer_id=customerId).aggregate(dcount=Sum('tax'))
        return spots['dcount']
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag
def getCustomerCountBySpotTeacher( teacherid ):
    try:
        customers = Customer.objects.filter(spotTeacher_id=teacherid)
        return customers.__len__()
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag
def getFirstCashTotalBySpotTeacher( teacherid ):
    try:
        cashTotal = Spot.objects.filter(customer__spotTeacher_id=teacherid, type=0).aggregate(Sum('cash'))
        if cashTotal['cash__sum']:
            return cashTotal['cash__sum']
        else:
            return 0
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag
def getCashTotalBySpotTeacher( teacherid ):
    try:
        cashTotal = Spot.objects.filter(customer__spotTeacher_id=teacherid).aggregate(Sum('cash'))
        if cashTotal['cash__sum']:
            return cashTotal['cash__sum']
        else:
            return 0
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag
def getProfitTotalBySpotTeacher( teacherid ):
    try:
        profitTotal = Spot.objects.filter(customer__spotTeacher_id=teacherid).aggregate(Sum('profit'))
        if profitTotal['profit__sum']:
            return profitTotal['profit__sum']
        else:
            return 0
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag
def getTaxTotalBySpotTeacher( teacherid ):
    try:
        taxTotal = Spot.objects.filter(customer__spotTeacher_id=teacherid).aggregate(Sum('tax'))
        if taxTotal['tax__sum']:
            return taxTotal['tax__sum']
        else:
            return 0
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag
def getSpotTotalBySpotTeacher( teacherid ):
    try:
        cashTotal = Spot.objects.filter(customer__spotTeacher_id=teacherid).aggregate(Sum('cash'))
        if cashTotal['cash__sum']:
            cash = cashTotal['cash__sum']
        else:
            cash = 0
        profitTotal = Spot.objects.filter(customer__spotTeacher_id=teacherid).aggregate(Sum('profit'))
        if profitTotal['profit__sum']:
            profit = profitTotal['profit__sum']
        else:
            profit = 0
        taxTotal = Spot.objects.filter(customer__spotTeacher_id=teacherid).aggregate(Sum('tax'))
        if taxTotal['tax__sum']:
            tax = taxTotal['tax__sum']
        else:
            tax = 0
        return cash + profit - tax
    except Exception as e:
        print(e.__str__())
        return 0