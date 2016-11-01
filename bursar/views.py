# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models import Q, Sum
from django.db import connection

import os
import random
import string
import datetime
import traceback
import json

from shande.settings import BASE_DIR
from shande.util import *
from ops.models import *
from super.models import *
from bursar.models import *
from trade.models import *

@login_required()
def bursarManage(request):
    if (not request.user.userprofile.title.role_name in ['admin', 'ops']):
        return HttpResponseRedirect("/")
    bindUsers = User.objects.filter(userprofile__title__role_name='bursar').order_by("userprofile__nick")
    # for bursar in Bursar.objects.all():
    #     bindUsers = bindUsers.filter(~Q(id=bursar.binduser.id))
    data = {
        "bindusers": bindUsers,
    }
    return render(request, 'bursar/bursarManage.html', data)

@login_required()
def queryBursar(request):
    bursars = Bursar.objects.all().order_by('bursarId')
    bursars = bursars.filter(bursarId__icontains=request.GET.get('bursarid', ''))
    # bursars = bursars.filter(company__icontains=request.GET.get('company', ''))
    # bursars = bursars.filter(department__icontains=request.GET.get('department', ''))
    if 'binduser' in request.GET and request.GET['binduser'] != '':
        bursars = bursars.filter(binduser__userprofile__nick__icontains=request.GET.get('binduser'))
    p = Paginator(bursars, 5)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        bursarPage = p.page(page)
    except (EmptyPage, InvalidPage):
        bursarPage = p.page(p.num_pages)
    data = {
        "bursarPage": bursarPage,
        "requestArgs": getArgsExcludePage(request),
    }
    return render(request, 'bursar/queryBursar.html', data)

@login_required()
def addBursar(request):
    data = {}
    try:
        if request.POST['id'] == "":
            newBursar = Bursar.objects.create(bursarId=request.POST['bursarid'])
        else:
            newBursar = Bursar.objects.get(id=request.POST['id'])
        binduserid = request.POST.get('binduser', '无')
        if binduserid.isdigit():
            newBursar.binduser = User.objects.get(id=binduserid)
        else:
            newBursar.binduser = None
        # newBursar.company = request.POST['company']
        # newBursar.department = request.POST['department']
        newBursar.save()
        data['msg'] = "操作成功"
        data['msgLevel'] = "info"
    except Exception as e:
        print(e.__str__())
        if str(e.__str__()).__contains__('bursarId'):
            data['msg'] = "操作失败,财务ID已存在"
        elif str(e.__str__()).__contains__('binduser'):
            data['msg'] = "操作失败,用户已绑定财务，请刷新页面重试"
        else:
            data['msg'] = "操作失败,请联系管理员。错误信息:%s" % e.__str__()
        data['msgLevel'] = "error"
    return HttpResponse(json.dumps(data))

@login_required()
def addBursarGroup(request):
    data = {}
    try:
        bursarCount = request.POST.get('bursarCount')
        for i in range(1, int(bursarCount) + 1):
            if i < 10:
                index = '0' + str(i)
            else:
                index = str(i)
            bursarId = "CW" + index
            bursar, created = Bursar.objects.get_or_create(bursarId=bursarId)
            bursar.save()
        data['msg'] = "操作成功"
        data['msgLevel'] = "info"
    except Exception as e:
        print(e.__str__())
        if str(e.__str__()).__contains__('bursarId'):
            data['msg'] = "操作失败,财务ID已存在"
        elif str(e.__str__()).__contains__('binduser'):
            data['msg'] = "操作失败,用户已绑定财务，请刷新页面重试"
        else:
            data['msg'] = "操作失败,请联系管理员。错误信息:%s" % e.__str__()
        data['msgLevel'] = "error"
    return HttpResponse(json.dumps(data))

@login_required()
def delBursar(request):
    data = {}
    try:
        tmpBursar = Bursar.objects.get(id=request.POST['id'])
        tmpBursar.delete()
        data['msg'] = "操作成功"
        data['msgLevel'] = "info"
    except Exception as e:
        print(e.__str__())
        data['msg'] = "操作失败"
        data['msgLevel'] = "error"
    return HttpResponse(json.dumps(data))

@login_required()
def payReport(request):
    if (not request.user.userprofile.title.role_name in ['admin', 'ops', 'bursar', 'bursarmanager']):
        return HttpResponseRedirect("/")
    trades = Trade.objects.filter(paytime__isnull=False)

    if request.user.userprofile.title.role_name == 'bursar':
        trades.filter(customer__bursar__binduser=request.user)
    tradePayCashSum = trades.aggregate(Sum('paycash'))
    if tradePayCashSum['paycash__sum']:
        payCashTotal = tradePayCashSum['paycash__sum']
    else:
        payCashTotal = 0
    data = {
        "trades": trades,
        "payCashTotal": payCashTotal,
    }
    return render(request, 'bursar/payReport.html', data)

@login_required()
def payTypeReport(request):
    if (not request.user.userprofile.title.role_name in ['admin', 'ops', 'bursar', 'bursarmanager']):
        return HttpResponseRedirect("/")
    trades = Trade.objects.filter(paytime__isnull=False)
    if request.user.userprofile.title.role_name == 'bursar':
        trades.filter(customer__bursar__binduser=request.user)
    tradePayTypeSum = trades.values('paytype').annotate(dcount=Sum('paycash'))
    total = tradePayTypeSum.aggregate(Sum('dcount'))
    data = {
        "tradePayTypeSum": tradePayTypeSum,
        "total": total,
    }
    return render(request, 'bursar/payTypeReport.html', data)

@login_required()
def payCompanyReport(request):
    if (not request.user.userprofile.title.role_name in ['admin', 'ops', 'bursar', 'bursarmanager']):
        return HttpResponseRedirect("/")
    data = { }
    return render(request, 'bursar/payCompanyReport.html', data)

def queryPayCompany(request):
    startDate = request.GET.get('startDate', '')
    endDate = request.GET.get('endDate', '')
    if startDate =='':
        startDate = datetime.date.today()
    if endDate == '':
        endDate = datetime.date.today() + datetime.timedelta(days=1)
    if request.user.userprofile.title.role_name == 'bursar':
        bursar = request.user.bursar_set[0]
        bursarid = bursar.id
        sql = """
            SELECT s.company,IFNULL(SUM(t.paycash),0) FROM sale_sale s
            LEFT JOIN customer_customer c ON c.sales_id = s.id and c.bursar_id = %s
            LEFT JOIN trade_trade t ON t.customer_id = c.id AND t.paytime IS NOT NULL AND t.paytime > '%s' and t.paytime < '%s'
            GROUP BY s.company
        """ % (bursarid, startDate, endDate)
    else:
        sql = """
            SELECT s.company,IFNULL(SUM(t.paycash),0) FROM sale_sale s
            LEFT JOIN customer_customer c ON c.sales_id = s.id
            LEFT JOIN trade_trade t ON t.customer_id = c.id AND t.paytime IS NOT NULL AND t.paytime > '%s' and t.paytime < '%s'
            GROUP BY s.company
        """ % (startDate, endDate)
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        tradePayCompanySum = []
        total = 0
        for row in cursor.fetchall():
            company = {}
            company['company'] = row[0]
            company['dcount'] = row[1]
            total += row[1]
            tradePayCompanySum.append(company)
    except Exception as e:
        print(e.__str__())
        tradePayCompanySum = None
        total = 0
    data = {
        "tradePayCompanySum": tradePayCompanySum,
        "total": total,
        "startDate": startDate,
        "endDate": endDate,
    }
    return render(request, 'bursar/queryPayCompany.html', data)

@login_required()
def payStockReport(request):
    if (not request.user.userprofile.title.role_name in ['admin', 'ops', 'bursarmanager']):
        return HttpResponseRedirect("/")
    trades = Trade.objects.filter(paytime__isnull=False)
    tradeStockPaySum = trades.values('stock_id', 'stock__stockid', 'stock__stockname').annotate(Sum('paycash'))
    total = tradeStockPaySum.aggregate(Sum('paycash__sum'))
    data = {
        "tradeStockPaySum": tradeStockPaySum,
        "total": total,
    }
    return render(request, 'bursar/payStockReport.html', data)

@login_required()
def payCompanySerialReport(request):

    companys = Sale.objects.values('company').distinct()
    days = []
    for i in range(0,30):
        day = datetime.date.today()-datetime.timedelta(days=i)
        days.insert(0, day)
    data = {
        "companys": companys,
        "days": days,
    }
    return render(request, 'bursar/payCompanySerialReport.html', data)