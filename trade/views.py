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

from PIL import Image

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
    buyprice = float(request.POST.get('buyprice'))
    buycount = int(request.POST.get('buycount'))
    buycash = buyprice * buycount
    try:
        if float(request.POST.get('buycount')) == 0:
            raise Exception("buycountzero")
        customer = Customer.objects.get(id=request.POST.get('customerid'))
        # 判断是否首笔交易
        existTrade = Trade.objects.filter(customer=customer)
        if existTrade.__len__() == 0:
            firstTrade = True
            if buycash < 20000:
                raise Exception("buycashlow")
        elif existTrade.__len__() == 1:
            secondTrade = True

        #判断是否存在该产品
        stock = Stock.objects.get(stockid=request.POST.get('stockid'), stockname=request.POST.get('stockname'))
        # stock, created = Stock.objects.get_or_create(stockid=request.POST.get('stockid'), stockname=request.POST.get('stockname'))
        if stock:
            newTrade = Trade.objects.create(customer=customer, stock=stock, create=timezone.now())
        else:
            raise Exception("stockerror")
        newTrade.status = 0
        newTrade.stockid = request.POST.get('stockid')
        newTrade.stockname = request.POST.get('stockname')

        newTrade.buyprice = buyprice
        newTrade.buycount = buycount

        newTrade.buycash = buycash
        customer.modify = timezone.now()
        # 判断是否VIP和10W+
        if buycash >= 100000:
            customer.tcrude = True

        customer.status = 40
        #如果是首笔交易标记客户状态为有效客户
        if firstTrade:

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
            if buycash >= 100000:
                customer.crude = True

        elif secondTrade:
            customer.vip = True


        # newTrade.income = request.POST.get('income', 0)
        newTrade.share = request.POST.get('share')
        customer.latest = timezone.now()
        # newTrade.sellprice = request.POST.get('sellprice', '0')
        # newTrade.commission = request.get('commission', 0)
        tradeid = newTrade.id
        newTrade.save()
        customer.save()

        #上传交割单据
        tradefile = request.FILES['file']
        filename = str(tradeid)+'.jpg'
        filejpg = "trade/static/trade/images/"+filename
        file = open(filejpg, "wb+")

        for chunk in tradefile.chunks():
            file.write(chunk)
        file.close()

        data['msg'] = "操作成功"
        data['msgLevel'] = "info"
    except Exception as e:
        traceback.print_exc()
        print(e.__str__())
        if e.__str__() == 'stockerror':
            data['msg'] = "操作失败, 输入错误，或产品库中无此产品，请联系管理员"
        elif str(e.__str__()).__contains__('stock_stock_stockid'):
            data['msg'] = "操作失败, 输入错误，或产品库中无此产品，请联系管理员"
        elif str(e.__str__()).__contains__('Stock matching'):
            data['msg'] = "操作失败, 输入错误，或产品库中无此产品，请联系管理员"
        elif str(e.__str__()).__contains__('stock_stock_stockname'):
            data['msg'] = "操作失败, 输入错误，或产品库中无此产品，请联系管理员"
        elif e.__str__() == 'buycountzero':
            data['msg'] = "操作失败, 购买数量不能为零"
        elif e.__str__() == 'buycashlow':
            data['msg'] = "客户买入资金不足，无法提交"
        else:
            data['msg'] = "操作失败, %s" % e.__str__()
        data['msgLevel'] = "error"
    return HttpResponse(json.dumps(data))

@login_required()
def handleTrade(request):
    data = {}
    firstTrade = False
    try:
        a=request.POST.get('htcustomerid')

        customer = Customer.objects.get(id=request.POST.get('htcustomerid'))
        # 判断是否首笔交易
        firstTradeObj = Trade.objects.filter(customer=customer).earliest('create')
        if int(request.POST.get('htid')) == firstTradeObj.id:
            firstTrade = True

        newTrade = Trade.objects.get(id=request.POST.get("htid"))
        # 判断是否存在该产品
        stock = Stock.objects.get(stockid=request.POST.get('htstockid'), stockname=request.POST.get('htstockname'))
        # stock, created = Stock.objects.get_or_create(stockid=request.POST.get('htstockid'),
        #                                              stockname=request.POST.get('htstockname'))
        if stock:
            newTrade.stock = stock
        else:
            raise Exception("stockerror")
        newTrade.stockid = request.POST.get('htstockid')
        newTrade.stockname = request.POST.get('htstockname')
        tradeStatus = request.POST.get('htstatus')
        newTrade.status = tradeStatus
        if tradeStatus == '20':
            newTrade.dealtime = timezone.now()
        buyprice = float(request.POST.get('htbuyprice'))
        buycount = int(request.POST.get('htbuycount'))
        newTrade.buyprice = buyprice
        newTrade.buycount = buycount
        buycash = buyprice * buycount
        if firstTrade:
            if buycash < 20000:
                raise Exception("buycashlow")
            customer.first_trade_cash = buycash
            if buycash >= 100000:
                customer.crude = True
            else:
                customer.crude = False
            # customer.first_trade = timezone.now()

        newTrade.buycash = buycash
        customer.modify = timezone.now()
        #判断是否VIP
        if buycash >= 100000:
            customer.vip = True
            customer.tcrude = True


        newTrade.share = request.POST.get('htshare')
        newTrade.sellprice = request.POST.get('htsellprice', '0')
        newTrade.income = request.POST.get('htincome', 0)
        newTrade.commission = request.POST.get('htcommission', 0)
        newTrade.save()
        customer.save()

        # #上传交割单据
        # tradefile = request.FILES['htfile']
        # filename = str(newTrade.id)+'.jpg'
        # filejpg = "trade/static/trade/images/"+filename
        # file = open(filejpg, "wb+")

        # for chunk in tradefile.chunks():
        #     file.write(chunk)
        # file.close()

        data['msg'] = "操作成功"
        data['msgLevel'] = "info"
    except Exception as e:
        print(e.__str__())
        if e.__str__() == 'stockerror':
            data['msg'] = "操作失败, 输入错误，或产品库中无此产品，请联系管理员"
        elif str(e.__str__()).__contains__('stock_stock_stockid'):
            data['msg'] = "操作失败, 输入错误，或产品库中无此产品，请联系管理员"
        elif str(e.__str__()).__contains__('stock_stock_stockname'):
            data['msg'] = "操作失败, 输入错误，或产品库中无此产品，请联系管理员"
        elif str(e.__str__()).__contains__('Stock matching'):
            data['msg'] = "操作失败, 输入错误，或产品库中无此产品，请联系管理员"
        elif e.__str__() == 'buycashlow':
            data['msg'] = "客户买入资金不足，无法提交"
        else:
            data['msg'] = "操作失败, %s" % e.__str__()
        traceback.print_exc()
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

@login_required()
def deleteTrade(request):
    data = {}
    try:
        trade = Trade.objects.get(id=request.POST.get("id"))
        tradeid = trade.id
        customer = trade.customer
        trade.delete()
        trades = Trade.objects.filter(customer=customer)
        #删除交易时，更新客户的最近合作时间
        customer.latest = customer.getLatestTradeDate()
        if trades.__len__() == 0:  #如果是唯一一笔交易
            customer.latest = None
            #历史有效客户数-1
            firstTradeDate = customer.first_trade
            userGradeHis = customer.sales.binduser.usergradehis_set.get(user=customer.sales.binduser,
                                                                                           day=firstTradeDate)
            userGradeHis.delta -= 1
            userGradeHis.save()
            #有效客户总数-1
            customer.sales.binduser.userprofile.grade -= 1
            customer.sales.binduser.userprofile.save()
            #客户状态改变
            customer.status = 20
            customer.crude = 0
            customer.vip = 0
            customer.modify = timezone.now()
            customer.first_trade_cash = 0
            customer.first_trade = None
            customer.save()
        else:#如果非首笔交易，但其他交易金额都小于100000，则去掉客户的10W+标记
            customer.latest = customer.getLatestTradeDate()
            crudeTrades = trades.filter(buycash__gte=100000)
            if crudeTrades.__len__() == 0:
                customer.crude = 0
                customer.save()

        #删除图片
        jpgfile = "trade/static/trade/images/"+str(tradeid)+'.jpg'
        if os.path.isfile(jpgfile):
               os.remove(jpgfile)

        data['msg'] = "操作成功"
        data['msgLevel'] = "info"
    except Exception as e:
        data['msg'] = "操作失败, %s" % e.__str__()
        data['msgLevel'] = "error"
        traceback.print_exc()
    return HttpResponse(json.dumps(data))

@login_required()
def backTrade(request):
    data = {}
    try:
        trade = Trade.objects.get(id=request.POST.get("btid"))
        trade.status = 1
        trade.message = request.POST.get('btmessage')
        trade.save()
        data['msg'] = "操作成功"
        data['msgLevel'] = "info"
    except Exception as e:
        traceback.print_exc()
        data['msg'] = "操作失败, %s" % e.__str__()
        data['msgLevel'] = "error"
    return HttpResponse(json.dumps(data))

def getNameByStockId(request):
    stockid = request.POST.get("stockid")
    try:
        stock = Stock.objects.get(stockid=stockid)
        return HttpResponse(stock.stockname)
    except Exception as e:
        traceback.print_exc()
        return HttpResponse("无此代码，请联系管理员")

@login_required()
def pictureshow(request):
    return render(request, 'trade/pictureshow.html', locals())

@login_required()
def updateFile(request):
    data = {}
    try:
        #上传交割单据
        tradeid=request.POST.get('tradeid')
        tradefile = request.FILES['file']
        filename = str(tradeid)+'.jpg'
        jpgfile = "trade/static/trade/images/"+filename
        file = open(jpgfile, "wb+")

        for chunk in tradefile.chunks():
            file.write(chunk)
        file.close()

        data['msg'] = "操作成功"
        data['msgLevel'] = "info"
    except Exception as e:
        traceback.print_exc()
        data['msg'] = "操作失败, %s" % e.__str__()
        data['msgLevel'] = "error"
    return HttpResponse(json.dumps(data))

@login_required()
def showFile(request):
    data = {}
    try:
        tradeid = request.POST.get('tradeid')
        dpath = 'trade/static/trade/images/'
        filename = str(tradeid)+'.jpg'
        existfile = "trade/static/trade/images/"+filename
        if os.path.isfile(existfile):
            data["filename"] = "/static/trade/images/"+filename
            data["msg"] = " "
            data['msgLevel'] = "info"
        else:
            data["filename"] = ''
            data["msg"] = "文件不存在"
            data['msgLevel'] = "error"
    except:
            traceback.print_exc()
            data['msg'] = "文件不存在"
            data['msgLevel'] = "error"
            data['filename'] = " "
    return HttpResponse(json.dumps(data))
