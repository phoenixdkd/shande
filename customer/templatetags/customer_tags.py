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
