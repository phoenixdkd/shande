# coding=utf-8
from django import template
from django.template.defaultfilters import stringfilter
from django.db.models import Sum, Count
from customer.models import *
from trade.models import *
from spot.models import *
register = template.Library()

@register.simple_tag
def getPayCashTotalByDayAndCompany(company, day):
    try:
        y, m, d = str(day).split('-')
        trades = Trade.objects.filter(paytime__isnull=False, customer__sales__company=company,
                                      paytime__year=y, paytime__month=m, paytime__day=d)
        cashTotal = trades.aggregate(Sum('paycash'))
        if cashTotal['paycash__sum']:
            return cashTotal['paycash__sum']
        else:
            return 0
    except Exception as e:
        print(e.__str__())
        return 0


@register.simple_tag
def getSequenceNumber(number, start_index):
    try:
        result = number + start_index - 1
        return result
    except Exception as e:
        print(e.__str__())
        return 0