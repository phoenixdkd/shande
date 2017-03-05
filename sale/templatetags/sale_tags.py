# coding=utf-8
from django import template
from django.template.defaultfilters import stringfilter
from django.db.models import Sum
from sale.models import *
from customer.models import *
from trade.models import *
from wxqq.models import *
from super.models import *
register = template.Library()

#
# @register.filter(name="maskphone")
# @stringfilter
# def maskphone(phone):
#     if phone.__len__() < 5:
#         return '***'
#     return phone[0:3]+'****'+phone[7:]

@register.simple_tag
def getSaleIdByUserId(uid):
    try:
        sale = Sale.objects.get(binduser__id=uid)
        # print sale.saleId
        return sale.saleId
    except:
        return "未找到绑定的开发ID"

@register.simple_tag
def getSaleCompanyByUserId(uid):
    try:
        sale = Sale.objects.get(binduser__id=uid)
        return sale.company
    except:
        return "未找到绑定的开发ID"

@register.simple_tag
def getSaleDepartmentByUserId(uid):
    try:
        sale = Sale.objects.get(binduser__id=uid)
        return sale.department
    except:
        return "未找到绑定的开发ID"

@register.simple_tag
def getChargebackByUserId(uid):
    try:
        user = User.objects.get(id=uid)
        commit = user.userprofile.commit
        grade = user.userprofile.grade

        x = float(grade)/float(commit) *100
        return "%s / %s (%.2f" % (grade, commit, x) + '%)'
    except Exception as e:
        print("str"+ e.message)
        return 0

@register.simple_tag()
def getVipCountBySale(saleid, startDate, endDate):
    try:
        customers = Customer.objects.filter(status=40, vip=True, sales__id=saleid,
                                            first_trade__lte = endDate, first_trade__gte = startDate)
        return customers.__len__()
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag()
def getCrudeCountBySale(saleid, startDate, endDate):
    try:
        customers = Customer.objects.filter(status=40, crude=True, sales__id=saleid,
                                            first_trade__lte = endDate, first_trade__gte = startDate)
        return customers.__len__()
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag()
def getTotalBuyCashBySale( saleid, startDate, endDate ):
    try:
        trades = Trade.objects.filter(customer__status=40, customer__first_trade__lte=endDate, customer__first_trade__gte=startDate,
                                      customer__sales__id=saleid).aggregate(Sum('buycash'))
        if trades['buycash__sum']:
            return trades['buycash__sum']
        else:
            return 0
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag()
def getWxFriendDeltaBySale( saleid, startDate, endDate ):
    try:
        wx = WxFriendHis.objects.filter(wx__bindsale__id=saleid, day__lte=endDate, day__gte=startDate).aggregate(Sum('delta'))
        if wx['delta__sum']:
            return wx['delta__sum']
        else:
            return 0
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag()
def getWxFriendTotalBySale( saleid ):
    try:
        wx = Wx.objects.filter(bindsale__id=saleid).aggregate(Sum('friend'))
        if wx['friend__sum']:
            return wx['friend__sum']
        else:
            return 0
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag()
def getQqFriendDeltaBySale( saleid, startDate, endDate ):
    try:
        qq = QqFriendHis.objects.filter(qq__bindsale__id=saleid, day__lte=endDate, day__gte=startDate).aggregate(
            Sum('delta'))
        if qq['delta__sum']:
            return qq['delta__sum']
        else:
            return 0
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag()
def getQqFriendTotalBySale( saleid ):
    try:
        qq = Qq.objects.filter(bindsale__id=saleid).aggregate(Sum('friend'))
        if qq['friend__sum']:
            return qq['friend__sum']
        else:
            return 0
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag()
def getChargebackBySale( saleid, startDate, endDate ):
    try:
        # userCommits = UserProfile.objects.filter(user__sale__id=saleid, title__role_name='sale').aggregate(Sum('commit'))
        # userGrade = UserProfile.objects.filter(user__sale__id=saleid, title__role_name='sale').aggregate(Sum('grade'))
        userCommitToday = UserCommitHis.objects.filter(user__sale__id=saleid, user__userprofile__title__role_name='sale',
                                                       day__lte=endDate,
                                                        day__gte=startDate,
                                                       ).aggregate(Sum('delta'))
        userGradeToday = UserGradeHis.objects.filter(user__sale__id=saleid,
                                                     user__userprofile__title__role_name='sale', day__lte=endDate,
                                                     day__gte=startDate).aggregate(Sum('delta'))
        chargeback = 100 - float(userGradeToday['delta__sum']) / float(userCommitToday['delta__sum'])  *100
        return "%s / %s (%.2f"%(userGradeToday['delta__sum'], userCommitToday['commit__sum'], delta__sum)+'%)'
    except Exception as e:
        print(e.__str__())
        return '0/0 (0%)'

@register.simple_tag()
def getDishonestBySale( saleid ):
    try:
        customers = Customer.objects.filter(sales__id=saleid, honest=False)
        return customers.__len__()
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag()
def getDishonestCustomerByCompanyAndDay(company, day):
    try:
        y, m, d = str(day).split('-')
        customers = Customer.objects.filter(modify__year=y, modify__month=m, modify__day=d, status=98, sales__company=company)
        return customers.__len__()
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag()
def getEffectCustomerByCompanyAndDay(company, day):
    try:
        y, m, d = str(day).split('-')
        customers = Customer.objects.filter(first_trade__year=y, first_trade__month=m, first_trade__day=d, status=40, sales__company=company)
        return customers.__len__()
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag()
def getEffectCustomerBySaleAndDay( sale, day ):
    try:
        y, m, d = str(day).split('-')
        customers = Customer.objects.filter(first_trade__year=y, first_trade__month=m, first_trade__day=d,
                                            status=40, sales_id=sale)
        return customers.__len__()
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag()
def getNickBySaleId(saleid):
    try:
        sale = Sale.objects.get(id=saleid)
        return sale.binduser.userprofile.nick
    except Exception as e:
        print(e.__str__())
        return ""