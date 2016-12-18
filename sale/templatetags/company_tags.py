# coding=utf-8
import datetime
from django import template
from django.template.defaultfilters import stringfilter
from django.db.models import Count, Sum
from customer.models import *
from trade.models import *
from wxqq.models import *
from super.models import *
register = template.Library()


@register.simple_tag()
def getVipCountByCompany( company, startDate, endDate ):
    try:
        companys = Customer.objects.filter(status=40, vip=True, sales__company=company, first_trade__lte=endDate, first_trade__gte=startDate)
        return companys.__len__()
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag()
def getCrudeCountByCompany( company, startDate, endDate ):
    try:
        companys = Customer.objects.filter(status=40, crude=True, sales__company=company, first_trade__lte=endDate, first_trade__gte=startDate)
        return companys.__len__()
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag()
def getTotalBuyCashByCompany( company, startDate, endDate ):
    try:
        trades = Trade.objects.filter(customer__status=40, customer__first_trade__lte=endDate, customer__first_trade__gte=startDate,
                                      customer__sales__company=company).aggregate(Sum('buycash'))
        if trades['buycash__sum']:
            return trades['buycash__sum']
        else:
            return 0
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag()
def getWxFriendDeltaByCompany( company, startDate, endDate ):
    try:
        wx = WxFriendHis.objects.filter(wx__bindsale__company=company, day__lte=endDate, day__gte=startDate).aggregate(Sum('delta'))
        if wx['delta__sum']:
            return wx['delta__sum']
        else:
            return 0
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag()
def getWxFriendTotalByCompany( company ):
    try:
        wx = Wx.objects.filter(bindsale__company=company).aggregate(Sum('friend'))
        if wx['friend__sum']:
            return wx['friend__sum']
        else:
            return 0
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag()
def getQqFriendDeltaByCompany( company, startDate, endDate ):
    try:
        qq = QqFriendHis.objects.filter(qq__bindsale__company=company, day__gte=startDate, day__lte=endDate).aggregate(
            Sum('delta'))
        if qq['delta__sum']:
            return qq['delta__sum']
        else:
            return 0
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag()
def getQqFriendTotalByCompany( company ):
    try:
        qq = Qq.objects.filter(bindsale__company=company).aggregate(Sum('friend'))
        if qq['friend__sum']:
            return qq['friend__sum']
        else:
            return 0
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag()
def getChargebackByCompany( company ):
    try:
        userCommits = UserProfile.objects.filter(user__sale__company=company, title__role_name='sale').aggregate(Sum('commit'))
        userGrade = UserProfile.objects.filter(user__sale__company=company, title__role_name='sale').aggregate(Sum('grade'))
        chargeback = 100- float(userGrade['grade__sum']) / float(userCommits['commit__sum'])  *100
        return "%s / %s (%.2f"%(userGrade['grade__sum'], userCommits['commit__sum'], chargeback)+'%)'
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag()
def getDishonestByCompany( company, startDate, endDate ):
    try:
        customers = Customer.objects.filter(sales__company=company, honest=False, modify__lte=endDate, modify__gte=startDate)
        return customers.__len__()
    except Exception as e:
        print(e.__str__())
        return 0