# coding=utf-8
from django import template
from django.template.defaultfilters import stringfilter
from django.db.models import Sum
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
def getLatestStockByCustomerId(customerId):
    try:
        trade = Trade.objects.filter(customer=Customer.objects.get(id=customerId)).order_by('-create')
        if trade.__len__() != 0:
           return "%s %s" % (trade[0].stock.stockid , trade[0].stock.stockname)
        else:
           return None
    except Exception as e:
        print(e.__str__())
        return ""

@register.simple_tag
def getLatestTradeIDByCustomerId(customerId):
    try:
        trade = Trade.objects.filter(customer=Customer.objects.get(id=customerId)).order_by('-create')
        if trade.__len__() !=0:
            return trade[0].id
        else:
            return None
    except Exception as e:
        traceback.print_exc()
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

@register.simple_tag()
def getTotalBuycashByCustomerId( customerId ):
    try:
        trades = Trade.objects.filter(customer_id=customerId).values('customer').annotate(dcount=Sum('buycash'))[0]
        if trades['dcount']:
            return trades['dcount']
        else:
            return 0
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag()
def getCrudeColorByCustomerId( customerId ):
    try:
        customer = Customer.objects.get(id=customerId)
        if customer.crude:
            return "red"
        else:
            return "default"
    except Exception as e:
        print(e.__str__())
        return "red"


@register.filter(name="maskphone")
@stringfilter
def maskphone(phone):
    if phone.__len__() < 5:
        return '***'
    return phone[0:-4]+'****'+phone[8:]


@register.filter(name="maskname")
@stringfilter
def maskname(name):
    return name[0:1]+'**'

@register.filter(name="mask8")
@stringfilter
def mask8(name):
    if name.__len__() <= 8:
        return name
    return name[0:8]+'...'

@register.filter(name="masklast4")
@stringfilter
def masklast4(name):
    if name.__len__() < 4:
        return "****"
    return name[0:-4]+'****'
