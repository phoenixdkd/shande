# coding=utf-8
from django import template
from django.template.defaultfilters import stringfilter
from django.db.models import Sum
from customer.models import *
from trade.models import *
register = template.Library()

@register.simple_tag
def getLowBuypriceByStockAndUser(stockid, userid, startDate, endDate):
    try:
        user = User.objects.get(id=userid)
        trades = Trade.objects.filter(status=0, stock_id=stockid, create__gte=startDate, create__lte=endDate)
        if user.userprofile.title.role_name == 'teachermanager':
            trades = trades.filter(customer__teacher__company=user.userprofile.company,
                                   customer__teacher__department=user.userprofile.department)
        elif user.userprofile.title.role_name == 'teacherboss':
            trades = trades.filter(customer__teacher__company=user.userprofile.company)
        else:
            trades = trades
        trade = trades.earliest('buyprice')
        return trade.buyprice
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag
def getHighBuypriceByStockAndUser(stockid, userid):
    try:
        user = User.objects.get(id=userid)
        trades = Trade.objects.filter(status=0, stock_id=stockid)
        if user.userprofile.title.role_name == 'teachermanager':
            trades = trades.filter(customer__teacher__company=user.userprofile.company,
                                   customer__teacher__department=user.userprofile.department)
        elif user.userprofile.title.role_name == 'teacherboss':
            trades = trades.filter(customer__teacher__company=user.userprofile.company)
        else:
            trades = trades
        trade = trades.latest('buyprice')
        return trade.buyprice
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag
def getBuyCashTotalByStockAndUser(stockid, userid):
    try:
        user = User.objects.get(id=userid)
        trades = Trade.objects.filter(status=0, stock_id=stockid)
        if user.userprofile.title.role_name == 'teachermanager':
            trades = trades.filter(customer__teacher__company=user.userprofile.company,
                                   customer__teacher__department=user.userprofile.department)
        elif user.userprofile.title.role_name == 'teacherboss':
            trades = trades.filter(customer__teacher__company=user.userprofile.company)
        else:
            trades = trades
        cashTotal = trades.aggregate(Sum('buycash'))
        if cashTotal['buycash__sum']:
            return cashTotal['buycash__sum']
        else:
            return 0
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag
def getCustomerCountByStockAndUser(stockid, userid):
    try:
        user = User.objects.get(id=userid)
        customers = Customer.objects.filter(trade__stock_id=stockid, trade__status=0)
        if user.userprofile.title.role_name == 'teachermanager':
            customers = customers.filter(teacher__company=user.userprofile.company,
                                   teacher__department=user.userprofile.department)
        elif user.userprofile.title.role_name == 'teacherboss':
            customers = customers.filter(teacher__company=user.userprofile.company)
        else:
            customers = customers
        customers = customers.distinct()
        return customers.__len__()
    except Exception as e:
        print(e.__str__())
        return 0
