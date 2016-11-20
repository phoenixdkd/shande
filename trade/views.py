# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models import Q
from django.utils import timezone

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
from sale.models import *
from customer.models import *
from trade.models import *

@login_required()
def tradeManage(request):
    if (not request.user.userprofile.title.role_name in ['admin', 'ops', 'teacher', 'teachermanager', 'teacherboss']):
        return HttpResponseRedirect("/")
    customerId = request.GET.get("customerId")
    customer = Customer.objects.get(id=customerId)
    data = {
        "customer": customer,
    }
    return render(request, 'trade/tradeManage.html', data)

@login_required()
def queryTrade(request):
    customerId = request.GET.get("customerid")
    trades = Trade.objects.filter(customer_id=customerId)

    # 分页
    p = Paginator(trades, 20)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        tradePage = p.page(page)
    except (EmptyPage, InvalidPage):
        tradePage = p.page(p.num_pages)
    data = {
        "tradePage": tradePage,
        "requestArgs": getArgsExcludePage(request),
    }
    return render(request, 'trade/queryTrade.html', data)

@login_required()
def addTrade(request):
    data = {}
    firstTrade = False
    secondTrade = False
    try:
        if float(request.POST.get('buycount')) == 0:
            raise Exception("buycountzero")
        customer = Customer.objects.get(id=request.POST.get('customerid'))
        # 判断是否首笔交易
        existTrade = Trade.objects.filter(customer=customer)
        if existTrade.__len__() == 0:
            firstTrade = True
        elif existTrade.__len__() == 1:
            secondTrade = True
        stock, created = Stock.objects.get_or_create(stockid=request.POST.get('stockid'), stockname=request.POST.get('stockname'))
        if stock:
            newTrade = Trade.objects.create(customer=customer, stock=stock, create=timezone.now())
        else:
            raise Exception("stockerror")
        newTrade.status = 0
        newTrade.stockid = request.POST.get('stockid')
        newTrade.stockname = request.POST.get('stockname')
        buyprice = float(request.POST.get('buyprice'))
        buycount = int(request.POST.get('buycount'))
        newTrade.buyprice = buyprice
        newTrade.buycount = buycount
        buycash = buyprice * buycount
        newTrade.buycash = buycash
        customer.modify = timezone.now()
        # 判断是否VIP和10W+
        if buycash >= 100000:
            customer.vip = True
            customer.crude = True

        #如果是首笔交易标记客户状态为有效客户
        if firstTrade:
            customer.status = 40
            customer.first_trade_cash = buycash
            customer.first_trade = timezone.now()
            #绑定开发的真实用户有效客户数加1
            customer.sales.binduser.userprofile.grade += 1
            customer.sales.binduser.userprofile.save()
            #历史有效客户数加1
            userGradeHis, created = customer.sales.binduser.usergradehis_set.get_or_create(user=customer.sales.binduser,
                                                                                  day=datetime.date.today())
            userGradeHis.delta += 1
            userGradeHis.total = customer.sales.binduser.userprofile.grade
            userGradeHis.save()
            #同时建立历史提交数记录
            userCommitHis, created = customer.sales.binduser.usercommithis_set.get_or_create(user=customer.sales.binduser, day=datetime.date.today())
            userCommitHis.total = customer.sales.binduser.userprofile.commit
            userCommitHis.save()
        elif secondTrade:
            customer.vip = True

        # newTrade.income = request.POST.get('income', 0)
        newTrade.share = request.POST.get('share')
        # newTrade.sellprice = request.POST.get('sellprice', '0')
        # newTrade.commission = request.get('commission', 0)
        newTrade.save()
        customer.save()

        data['msg'] = "操作成功"
        data['msgLevel'] = "info"
    except Exception as e:
        traceback.print_exc()
        print(e.__str__())
        if e.__str__() == 'stockerror':
            data['msg'] = "操作失败, 产品id或者产品名称不正确"
        elif e.__str__() == 'buycountzero':
            data['msg'] = "操作失败, 购买数量不能为零"
        else:
            data['msg'] = "操作失败, %s" % e.__str__()
        data['msgLevel'] = "error"
    return HttpResponse(json.dumps(data))

@login_required()
def handleTrade(request):
    data = {}
    try:
        customer = Customer.objects.get(id=request.POST.get('htcustomerid'))
        # 判断是否首笔交易
        firstTrade = Trade.objects.filter(customer=customer).earliest('create')
        if int(request.POST.get('htid')) == firstTrade.id:
            firstTrade = True
        newTrade = Trade.objects.get(id=request.POST.get("htid"))
        stock, created = Stock.objects.get_or_create(stockid=request.POST.get('htstockid'),
                                                     stockname=request.POST.get('htstockname'))
        if stock:
            newTrade.stock = stock
        else:
            raise Exception("stockerror")
        newTrade.stockid = request.POST.get('htstockid')
        newTrade.stockname = request.POST.get('htstockname')
        newTrade.status = request.POST.get('htstatus')
        buyprice = float(request.POST.get('htbuyprice'))
        buycount = int(request.POST.get('htbuycount'))
        newTrade.buyprice = buyprice
        newTrade.buycount = buycount
        buycash = buyprice * buycount
        newTrade.buycash = buycash
        customer.modify = timezone.now()
        #判断是否VIP
        if buycash >= 100000:
            customer.vip = True
            customer.crude = True

        newTrade.share = request.POST.get('htshare')
        newTrade.sellprice = request.POST.get('htsellprice', '0')
        newTrade.income = request.POST.get('htincome', 0)
        newTrade.commission = request.POST.get('htcommission', 0)
        newTrade.save()
        customer.save()
        data['msg'] = "操作成功"
        data['msgLevel'] = "info"
    except Exception as e:
        print(e.__str__())
        if e.__str__() == 'stockerror':
            data['msg'] = "操作失败, 产品ID或者产品名称不正确"
        elif str(e.__str__()).__contains__('stock_stock_stockid'):
            data['msg'] = "操作失败, 产品ID或者产品名称不正确"
        elif str(e.__str__()).__contains__('stock_stock_stockname'):
            data['msg'] = "操作失败, 产品ID或者产品名称不正确"
        else:
            data['msg'] = "操作失败, %s" % e.__str__()
        data['msgLevel'] = "error"
    return HttpResponse(json.dumps(data))

@login_required()
def payManage(request):
    if (not request.user.userprofile.title.role_name in ['admin', 'ops', 'bursar', 'bursarmanager']):
        return HttpResponseRedirect("/")
    customerId = request.GET.get("customerId")
    customer = Customer.objects.get(id=customerId)
    data = {
        "customer": customer,
    }
    return render(request, 'trade/payManage.html', data)

@login_required()
def payTrade(request):
    data = {}
    try:
        trade = Trade.objects.get(id=request.POST.get("ptid"))
        trade.status = 30
        trade.paytime = timezone.now()
        trade.paytype = request.POST.get('ptpaytype')
        trade.paycash = request.POST.get('ptpaycash')
        trade.save()
        data['msg'] = "操作成功"
        data['msgLevel'] = "info"
    except Exception as e:
        print(e.__str__())
        data['msg'] = "操作失败, %s" % e.__str__()
        data['msgLevel'] = "error"
    return HttpResponse(json.dumps(data))