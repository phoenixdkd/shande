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

import logging
import time
logger = logging.getLogger("django")

@login_required()
def bursarManage(request):
    # t1 = time.clock()
    if (not request.user.userprofile.title.role_name in ['admin', 'ops']):
        return HttpResponseRedirect("/")
    bindUsers = User.objects.filter(userprofile__title__role_name='bursar').order_by("userprofile__nick")
    # for bursar in Bursar.objects.all():
    #     bindUsers = bindUsers.filter(~Q(id=bursar.binduser.id))
    data = {
        "bindusers": bindUsers,
    }
    # t2 = time.clock()
    # logger.error("bursarMangae cost time: %f %f %f s" % ((t2-t1),t1,t2))
    return render(request, 'bursar/bursarManage.html', data)

@login_required()
def queryBursar(request):
    # t1 = time.clock()
    if (request.GET.get('bursarid') or request.GET.get('binduser')):
        bursars = Bursar.objects.all().order_by('bursarId')
        bursars = bursars.filter(bursarId__icontains=request.GET.get('bursarid', ''))
        # bursars = bursars.filter(company__icontains=request.GET.get('company', ''))
        # bursars = bursars.filter(department__icontains=request.GET.get('department', ''))
        if 'binduser' in request.GET and request.GET['binduser'] != '':
            bursars = bursars.filter(binduser__userprofile__nick__icontains=request.GET.get('binduser'))
        p = Paginator(bursars, 20)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        try:
            bursarPage = p.page(page)
        except (EmptyPage, InvalidPage):
            bursarPage = p.page(p.num_pages)
        showContent = "True"
        showContent = json.dumps(showContent)
        data = {
            "bursarPage": bursarPage,
            "requestArgs": getArgsExcludePage(request),
            "showContent": showContent,
        }
    else:
        showContent = "False"
        showContent = json.dumps(showContent)
        data = {
           "showContent": showContent,
        }
    # t2 = time.clock()
    # logger.error("queryBursar cost time: %f"%(t2-t1))
    return render(request, 'bursar/queryBursar.html', data)

@login_required()
def addBursar(request):
    data = {}
    try:
        if request.POST['id'] == "":
            newBursar = Bursar.objects.create(bursarId=request.POST['bursarid'])
        else:
            newBursar = Bursar.objects.get(id=request.POST['id'])


        # binduserid = request.POST.get('binduser', '无')
        if request.POST.get('bindusername'):
            # binduserid = request.POST.get('binduser', '无')
            if User.objects.get(username=request.POST.get('bindusername','')):
                user = User.objects.get(username=request.POST.get('bindusername',''))
                binduserid = str(user.id)
        else:
            binduserid = '无'


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
        # bursarCount = request.POST.get('bursarCount')
        bursarCode = request.POST.get('bursarCode')
        departmentID = request.POST.get('departmentID')
        groupID = request.POST.get('groupID')
        bursarID = str(bursarCode)+str(groupID)+str(departmentID)
        bursar,created = Bursar.objects.get_or_create(bursarId=bursarID)
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
    # t1 = time.clock()
    if (not request.user.userprofile.title.role_name in ['admin', 'ops', 'bursar', 'bursarmanager', 'teacher', 'teachermanager', 'saleboss', 'salemanager']):
        return HttpResponseRedirect("/")
    # trades = Trade.objects.filter(paytime__isnull=False,status=30).order_by('-paytime')

    if request.POST.get("startDate",'') == '':
        startDate = request.GET.get('startDate','')
        endDate = request.GET.get('endDate','')
        company = request.GET.get('company','')
        bursarID = request.GET.get('bursarID','')
        phone = request.GET.get('phone','')
        paytype = request.GET.get('paytype','')
    else:
        startDate = request.POST.get('startDate')
        endDate = request.POST.get('endDate')
        bursarID = request.POST.get('bursarID')
        company = request.POST.get('company')
        phone = request.POST.get('phone')
        paytype = request.POST.get('paytype')

    if endDate == '':
        endDate = datetime.date.today() + datetime.timedelta(days=1)
    else:
        endDate = datetime.datetime.strptime(endDate, "%Y-%m-%d").date()

    if startDate == "":
        if request.user.userprofile.title.role_name == 'teacher':
            startDate = datetime.date.today()
        else:
            startDate = datetime.date.today() - datetime.timedelta(days=0)
    else:
        startDate = datetime.datetime.strptime(startDate, "%Y-%m-%d").date()
    # trades = trades.filter(paytime__lte=endDate, paytime__gte=startDate)
    bursars = Bursar.objects.all()

    # #按条件筛选
    # if bursarID != '':
    #     trades = trades.filter(customer__bursar__bursarId__icontains=str(bursarID))
    # if company != '':
    #     trades = trades.filter(customer__sales__company=str(company))
    #
    # if request.user.userprofile.title.role_name == 'bursar':
    #     trades = trades.filter(customer__bursar__binduser=request.user)
    # if request.user.userprofile.title.role_name == 'teacher':
    #     trades = trades.filter(customer__teacher__binduser=request.user)
    #
    # if request.user.userprofile.title.role_name == 'teachermanager':
    #     # trades = trades.filter(customer__teacher__company=request.user.userprofile.company,
    #     #                        customer__teacher__department=request.user.userprofile.department,
    #     #                        customer__teacher__group=request.user.userprofile.group)
    #     user = request.user
    #     bursarID = 'CW'+user.userprofile.group+user.userprofile.department
    #     trades = trades.filter(customer__bursar__bursarId__icontains=str(bursarID))
    #
    # if request.user.userprofile.title.role_name == 'saleboss':
    #     trades = trades.filter(customer__sales__company=request.user.userprofile.company)
    # if request.user.userprofile.title.role_name == 'salemanager':
    #     trades = trades.filter(customer__sales__company=request.user.userprofile.company,
    #                            customer__sales__department=request.user.userprofile.department).order_by('customer__sales')
    #
    # p = Paginator(trades, 100)
    # try:
    #     page = int(request.GET.get('page', '1'))
    # except ValueError:
    #     page = 1
    # try:
    #     tradePage = p.page(page)
    # except (EmptyPage, InvalidPage):
    #     tradePage = p.page(p.num_pages)
    #
    #
    # payCashTotal = 0
    # for tradeObj in tradePage :
    #     payCashTotal = payCashTotal + tradeObj.paycash

    data = {
        # "tradePage": tradePage,
        # "requestArgs": getArgsExcludePage(request),
        # "payCashTotal": payCashTotal,
        "startDate": str(startDate),
        "endDate": str(endDate),
        "bursarID": bursarID,
        "company": company,
        "bursars": bursars,
        "phone": phone,
        "paytype": paytype,
    }
    # t2 = time.clock()
    # logger.error("bursar/payReport cost time: %f"%(t2-t1))
    return render(request, 'bursar/payReport.html', data)

@login_required()
def queryPayReport(request):

    trades = Trade.objects.filter(paytime__isnull=False,status=30).order_by('-paytime')
    if request.user.userprofile.title.role_name == 'salemanager':
        company = request.user.userprofile.company
        bursarID = ''
        paytype=''
        phone=''
    else:
        company = request.GET.get('company', '')
        bursarID = request.GET.get('bursarID', '')
        paytype = request.GET.get('paytype', '')
        phone = request.GET.get('phone', '')
    startDate = request.GET.get('startDate', '')
    endDate = request.GET.get('endDate', '')


    trades = Trade.objects.filter(paytime__isnull=False, status=30,paytime__gt=startDate).order_by('-paytime')

    if endDate == '':
        endDate = datetime.date.today() + datetime.timedelta(days=1)
    else:
        endDate = datetime.datetime.strptime(endDate, "%Y-%m-%d").date()

    if startDate == "":
        if request.user.userprofile.title.role_name == 'teacher':
            startDate = datetime.date.today()
        else:
            startDate = datetime.date.today() - datetime.timedelta(days=0)
    else:
        startDate = datetime.datetime.strptime(startDate, "%Y-%m-%d").date()
    trades = trades.filter(paytime__lte=endDate, paytime__gte=startDate)

    # #按条件筛选
    if phone :
        trades = trades.filter(customer__phone=str(phone))
    if bursarID :
        trades = trades.filter(customer__bursar__bursarId__icontains=str(bursarID))
    if company :
        trades = trades.filter(customer__sales__company=str(company))
    if paytype :
        trades = trades.filter(paytype=paytype)


    if request.user.userprofile.title.role_name == 'bursar':
        trades = trades.filter(customer__bursar__binduser=request.user)
    if request.user.userprofile.title.role_name == 'teacher':
        # trades = trades.filter(customer__teacher__binduser=request.user)
        trades = trades.filter(realteacheruser=request.user)
    if request.user.userprofile.title.role_name == 'teachermanager':
        # trades = trades.filter(customer__teacher__company=request.user.userprofile.company,
        #                        customer__teacher__department=request.user.userprofile.department,
        #                        customer__teacher__group=request.user.userprofile.group)
        user = request.user
        bursarID = 'CW'+user.userprofile.group+user.userprofile.department
        trades = trades.filter(customer__bursar__bursarId__icontains=str(bursarID))

    if request.user.userprofile.title.role_name == 'saleboss':
        trades = trades.filter(customer__sales__company=request.user.userprofile.company)
    if request.user.userprofile.title.role_name == 'salemanager':
        trades = trades.filter(customer__sales__company=request.user.userprofile.company,
                               customer__sales__department=request.user.userprofile.department).order_by('customer__sales')

    payCashTotal = 0
    for tradeObj in trades:
        payCashTotal = payCashTotal + tradeObj.paycash

    p = Paginator(trades, 50)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        tradePage = p.page(page)
    except (EmptyPage, InvalidPage):
        tradePage = p.page(p.num_pages)


    # payCashTotal = 0
    # for tradeObj in tradePage :
    #     payCashTotal = payCashTotal + tradeObj.paycash

    data = {
        "tradePage": tradePage,
        "requestArgs": getArgsExcludePage(request),
        "payCashTotal": payCashTotal,
    }
    return render(request, 'bursar/queryPayReport.html', data)


@login_required()
def payTypeReport(request):
    # t1 = time.clock()
    if (not request.user.userprofile.title.role_name in ['admin', 'ops', 'bursar', 'bursarmanager']):
        return HttpResponseRedirect("/")
    trades = Trade.objects.filter(paytime__isnull=False)
    endDate = request.POST.get('endDate', "")
    if endDate == '':
        endDate = datetime.date.today() + datetime.timedelta(days=1)
    else:
        endDate = datetime.datetime.strptime(endDate, "%Y-%m-%d").date()
    startDate = request.POST.get('startDate', "")
    if startDate == "":
        startDate = datetime.date.today()
    else:
        startDate = datetime.datetime.strptime(startDate, "%Y-%m-%d").date()
    trades = trades.filter(paytime__lte=endDate, paytime__gte=startDate)
    if request.user.userprofile.title.role_name == 'bursar':
        trades=trades.filter(customer__bursar__binduser=request.user)
    company = request.POST.get('company', "")
    if company != '':
        trades=trades.filter(realteacheruser__teacher__company=company)

    tradePayTypeSum = trades.values('paytype').annotate(dcount=Sum('paycash'))
    total = tradePayTypeSum.aggregate(Sum('dcount'))
    data = {
        "tradePayTypeSum": tradePayTypeSum,
        "total": total,
        "startDate": str(startDate),
        "endDate": str(endDate),
        "company": company,
    }
    # t2 = time.clock()
    # logger.error("bursar/payTypeReport cost time: %f"%(t2-t1))
    return render(request, 'bursar/payTypeReport.html', data)

@login_required()
def payCompanyReport(request):
    # t1 = time.clock()
    if (not request.user.userprofile.title.role_name in ['admin', 'ops', 'bursar', 'bursarmanager', 'saleboss']):
        return HttpResponseRedirect("/")
    data = { }
    startDate = request.GET.get('startDate', '')
    endDate = request.GET.get('endDate', '')
    if startDate =='':
        startDate = datetime.date.today()
    if endDate == '':
        endDate = datetime.date.today() + datetime.timedelta(days=1)

    data = {
        "startDate": str(startDate),
        "endDate": str(endDate),
    }
    # t2 = time.clock()
    # logger.error("bursar/payCompanyReport cost time: %f"%(t2-t1))
    return render(request, 'bursar/payCompanyReport.html', data)

def queryPayCompany(request):
    # t1 = time.clock()
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
    elif request.user.userprofile.title.role_name == 'saleboss':
        company = request.user.userprofile.company
        sql = """
            SELECT s.company,IFNULL(SUM(t.paycash),0) FROM sale_sale s
            LEFT JOIN customer_customer c ON c.sales_id = s.id
            LEFT JOIN trade_trade t ON t.customer_id = c.id AND t.paytime IS NOT NULL AND t.paytime > '%s' and t.paytime < '%s'
            WHERE s.company = '%s'
            GROUP BY s.company
        """ % (startDate, endDate, company)
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
    # t2 = time.clock()
    # logger.error("bursar/queryPayCompany cost time: %f"%(t2-t1))
    return render(request, 'bursar/queryPayCompany.html', data)

@login_required()
def payStockReport(request):
    if (not request.user.userprofile.title.role_name in ['admin', 'ops', 'bursar', 'bursarmanager']):
        return HttpResponseRedirect("/")
    endDate = request.POST.get('endDate', "")
    if endDate == '':
        endDate = datetime.date.today() + datetime.timedelta(days=1)
    else:
        endDate = datetime.datetime.strptime(endDate, "%Y-%m-%d").date()
    startDate = request.POST.get('startDate', "")
    if startDate == "":
        startDate = datetime.date.today()
    else:
        startDate = datetime.datetime.strptime(startDate, "%Y-%m-%d").date()
    trades = Trade.objects.filter(paytime__isnull=False)
    trades = trades.filter(paytime__lte=endDate, paytime__gte=startDate)
    tradeStockPaySum = trades.values('stock_id', 'stock__stockid', 'stock__stockname').annotate(Sum('paycash'))
    total = tradeStockPaySum.aggregate(Sum('paycash__sum'))
    data = {
        "tradeStockPaySum": tradeStockPaySum,
        "total": total,
        "startDate": str(startDate),
        "endDate": str(endDate),
    }
    return render(request, 'bursar/payStockReport.html', data)

@login_required()
def payCompanySerialReport(request):
    # t1 = time.clock()
    endDate = request.POST.get('endDate', "")
    if endDate == '':
        endDate = datetime.date.today() + datetime.timedelta(days=1)
    else:
        endDate = datetime.datetime.strptime(endDate, "%Y-%m-%d").date()
    startDate = request.POST.get('startDate', "")
    if startDate == "":
        startDate = datetime.date.today()
    else:
        startDate = datetime.datetime.strptime(startDate, "%Y-%m-%d").date()
    companys = Sale.objects.values('company').distinct()
    companys = companys.filter(company=request.user.userprofile.company)
    days = []
    tmpDay = startDate
    while tmpDay <= endDate:
        days.append(tmpDay)
        tmpDay = tmpDay + datetime.timedelta(days=1)
    data = {
        "companys": companys,
        "days": days,
        "startDate": startDate,
        "endDate": endDate,
    }
    # t2 = time.clock()
    # logger.error("bursar/payCompanySerialReport cost time: %f"%(t2-t1))
    return render(request, 'bursar/payCompanySerialReport.html', data)