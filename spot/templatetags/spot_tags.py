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