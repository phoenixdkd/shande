# coding=utf-8
from django import template
from django.template.defaultfilters import stringfilter
from customer.models import *
from trade.models import *
register = template.Library()

@register.simple_tag
def getNoPayTradeCountByCustomerId(customerId):
    try:
        trades = Trade.objects.filter(customer_id=customerId, status=20)
        return trades.__len__()
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag
def getLatestProductByCustomerId(customerId):
    try:
        trade = Trade.objects.filter(customer=Customer.objects.get(id=customerId)).order_by('-create')
        return "%s-%s" % (trade[0].stockid , trade[0].stockname)
    except Exception as e:
        print(e.__str__())
        return ""

@register.simple_tag()
def getCommissionTotalByCustomerId(customerId):
    try:
        trades = Trade.objects.filter(customer=Customer.objects.get(id=customerId), paytime__isnull=False)
        total = 0
        for trade in trades:
            total += trade.paycash
        return total
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag()
def getTradeTotalByCustomerId( customerId ):
    try:
        trades = Trade.objects.filter(customer=Customer.objects.get(id=customerId))
        return trades.__len__()
    except Exception as e:
        print(e.__str__())
        return 0
