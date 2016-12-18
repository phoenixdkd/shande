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
def getVipCountByGroup( company, department, group ):
    try:
        groups = Customer.objects.filter(status=40, vip=True, sales__company=company, sales__department=department, sales__group=group)
        return groups.__len__()
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag()
def getCrudeCountByGroup( company, department, group ):
    try:
        groups = Customer.objects.filter(status=40, crude=True, sales__company=company, sales__department=department, sales__group=group)
        return groups.__len__()
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag()
def getTotalBuyCashByGroup( company, department, group ):
    try:
        trades = Trade.objects.filter(customer__status=40, customer__sales__company=company, customer__sales__department=department,
                                      customer__sales__group=group).aggregate(Sum('buycash'))
        if trades['buycash__sum']:
            return trades['buycash__sum']
        else:
            return 0
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag()
def getWxFriendDeltaByGroup( company, department, group ):
    try:
        wx = WxFriendHis.objects.filter(wx__bindsale__company=company, wx__bindsale__department=department,
                                        wx__bindsale__group=group, day=datetime.date.today()).aggregate(Sum('delta'))
        if wx['delta__sum']:
            return wx['delta__sum']
        else:
            return 0
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag()
def getWxFriendTotalByGroup( company, department, group ):
    try:
        wx = Wx.objects.filter(bindsale__company=company, bindsale__department=department,
            bindsale__group=group).aggregate(Sum('friend'))
        if wx['friend__sum']:
            return wx['friend__sum']
        else:
            return 0
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag()
def getQqFriendDeltaByGroup( company, department, group ):
    try:
        qq = QqFriendHis.objects.filter(qq__bindsale__company=company, qq__bindsale__department=department,
                                        qq__bindsale__group=group, day=datetime.date.today()).aggregate(
            Sum('delta'))
        if qq['delta__sum']:
            return qq['delta__sum']
        else:
            return 0
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag()
def getQqFriendTotalByGroup( company, department, group ):
    try:
        qq = Qq.objects.filter(bindsale__company=company, bindsale__department=department,
                               bindsale__group=group).aggregate(Sum('friend'))
        if qq['friend__sum']:
            return qq['friend__sum']
        else:
            return 0
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag()
def getChargebackByGroup( company, department, group ):
    try:
        userCommits = UserProfile.objects.filter(user__sale__company=company, user__sale__department=department,
                                                user__sale__group=group, title__role_name='sale').aggregate(Sum('commit'))
        userGrade = UserProfile.objects.filter(user__sale__company=company, user__sale__department=department,
                                                user__sale__group=group, title__role_name='sale').aggregate(Sum('grade'))
        chargeback = 100 - float(userGrade['grade__sum']) / float(userCommits['commit__sum'])  *100
        return "%s / %s (%.2f"%(userGrade['grade__sum'], userCommits['commit__sum'], chargeback)+'%)'
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag()
def getDishonestByGroup( company, department, group ):
    try:
        customers = Customer.objects.filter(sales__company=company, sales__department=department, sales__group=group, honest=False)
        return customers.__len__()
    except Exception as e:
        print(e.__str__())
        return 0