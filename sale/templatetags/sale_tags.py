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
def getVipCountBySale(saleid):
    try:
        customers = Customer.objects.filter(status=40, vip=True, sales__id=saleid)
        return customers.__len__()
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag()
def getTotalBuyCashBySale( saleid ):
    try:
        trades = Trade.objects.filter(customer__status=40, customer__sales__id=saleid).aggregate(Sum('buycash'))
        if trades['buycash__sum']:
            return trades['buycash__sum']
        else:
            return 0
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag()
def getWxFriendDeltaBySale( saleid ):
    try:
        wx = WxFriendHis.objects.filter(wx__bindsale__id=saleid, day=datetime.date.today()).aggregate(Sum('delta'))
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
def getQqFriendDeltaBySale( saleid ):
    try:
        qq = QqFriendHis.objects.filter(qq__bindsale__id=saleid, day=datetime.date.today()).aggregate(
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
def getChargebackBySale( saleid ):
    try:
        userCommits = UserProfile.objects.filter(user__sale__id=saleid, title__role_name='sale').aggregate(Sum('commit'))
        userGrade = UserProfile.objects.filter(user__sale__id=saleid, title__role_name='sale').aggregate(Sum('grade'))
        chargeback = 100 - float(userGrade['grade__sum']) / float(userCommits['commit__sum'])  *100
        return "%s / %s (%.2f"%(userGrade['grade__sum'], userCommits['commit__sum'], chargeback)+'%)'
    except Exception as e:
        print(e.__str__())
        return 0

@register.simple_tag()
def getDishonestBySale( saleid ):
    try:
        customers = Customer.objects.filter(sales__id=saleid, honest=False)
        return customers.__len__()
    except Exception as e:
        print(e.__str__())
        return 0