# coding=utf-8
import datetime
import traceback
from django import template
from django.template.defaultfilters import stringfilter
from django.db.models import Count, Sum
from customer.models import *
from trade.models import *
from wxqq.models import *
from super.models import *

register = template.Library()


@register.simple_tag()
def getVipCountByDepartment( company, department, startDate, endDate ):
    try:
        departments = Customer.objects.filter(status=40, vip=True, first_trade__gte=startDate, first_trade__lte=endDate,
                                              sales__company=company, sales__department=department)
        return departments.__len__()
    except Exception as e:
        traceback.print_exc()
        print(e.__str__())
        return 0

@register.simple_tag()
def getCrudeCountByDepartment( company, department, startDate, endDate ):
    try:
        departments = Customer.objects.filter(status=40, crude=True, first_trade__gte=startDate,
                                              first_trade__lte=endDate,
                                              sales__company=company, sales__department=department)
        return departments.__len__()
    except Exception as e:
        traceback.print_exc()
        print(e.__str__())
        return 0

@register.simple_tag()
def getTotalBuyCashByDepartment( company, department, startDate, endDate ):
    try:
        trades = Trade.objects.filter(customer__status=40, customer__first_trade__lte=endDate, customer__first_trade__gte=startDate,
                                      customer__sales__company=company, customer__sales__department=department).aggregate(Sum('buycash'))
        if trades['buycash__sum']:
            return trades['buycash__sum']
        else:
            return 0
    except Exception as e:
        traceback.print_exc()
        print(e.__str__())
        return 0

@register.simple_tag()
def getWxFriendDeltaByDepartment( company, department, startDate, endDate ):
    try:
        wx = WxFriendHis.objects.filter(wx__bindsale__company=company, wx__bindsale__department=department,
                                        day__lte=endDate, day__gte=startDate).aggregate(Sum('delta'))
        if wx['delta__sum']:
            return wx['delta__sum']
        else:
            return 0
    except Exception as e:
        traceback.print_exc()
        print(e.__str__())
        return 0

@register.simple_tag()
def getWxFriendTotalByDepartment( company, department ):
    try:
        wx = Wx.objects.filter(bindsale__company=company, bindsale__department=department).aggregate(Sum('friend'))
        if wx['friend__sum']:
            return wx['friend__sum']
        else:
            return 0
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag()
def getQqFriendDeltaByDepartment( company, department, startDate, endDate ):
    try:
        qq = QqFriendHis.objects.filter(qq__bindsale__company=company, qq__bindsale__department=department,
                                        day__lte=endDate, day__gte=startDate).aggregate(Sum('delta'))
        if qq['delta__sum']:
            return qq['delta__sum']
        else:
            return 0
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag()
def getQqFriendTotalByDepartment( company, department ):
    try:
        qq = Qq.objects.filter(bindsale__company=company, bindsale__department=department).aggregate(Sum('friend'))
        if qq['friend__sum']:
            return qq['friend__sum']
        else:
            return 0
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag()
def getChargebackByDepartment( company, department, startDate, endDate ):
    try:
        # userCommits = UserProfile.objects.filter(user__sale__company=company, user__sale__department=department, title__role_name='sale').aggregate(Sum('commit'))
        # userGrade = UserProfile.objects.filter(user__sale__company=company, user__sale__department=department, title__role_name='sale').aggregate(Sum('grade'))
        userCommitsToday = UserCommitHis.objects.filter(user__sale__company=company,
                                                        user__sale__department=department,
                                                        user__userprofile__title__role_name='sale', day__lte=endDate,
                                                        day__gte=startDate).aggregate(Sum('delta'))
        userGradeToday = UserGradeHis.objects.filter(user__sale__company=company,
                                                     user__sale__department=department,
                                                     user__userprofile__title__role_name='sale', day__lte=endDate,
                                                     day__gte=startDate).aggregate(Sum('delta'))

        if userCommitsToday['delta__sum'] & userGradeToday['delta_sum']:
            chargeback = 100 -float(userGradeToday['delta__sum']) / float(userCommitsToday['delta__sum'])  *100
        return "%s / %s (%.2f"%(userGradeToday['delta__sum'], userCommitsToday['delta__sum'], chargeback)+'%)'
    except Exception as e:
        traceback.print_exc()
        return '0/0 (0%)'

@register.simple_tag()
def getDishonestByDepartment( company, department ):
    try:
        customers = Customer.objects.filter(sales__company=company, sales__department=department, honest=False)
        return customers.__len__()
    except Exception as e:
        print(e.__str__())
        return 0