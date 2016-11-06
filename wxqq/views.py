# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models import Q

import os
import random
import string
import datetime
import traceback
import json

from shande.util import *
from shande.settings import BASE_DIR
from ops.models import *
from super.models import *
from sale.models import *
from wxqq.models import *

@login_required()
def wxManage(request):
    if (not request.user.userprofile.title.role_name in ['admin', 'ops', 'sale', 'salemanager', 'saleboss']):
        return HttpResponseRedirect("/")
    bindsales = Sale.objects.all().order_by("saleId")
    data = {
        "bindsales": bindsales,
    }
    return render(request, 'wxqq/wxManage.html', data)

@login_required()
def queryWx(request):
    data = {}
    wxs = Wx.objects.all().order_by('delete', 'wxid')

    #不同角色看到的范围不同
    if request.user.userprofile.title.role_name in ['salemanager']:
        company = request.user.userprofile.company
        department = request.user.userprofile.department
        wxs = wxs.filter(company=company, bindsale__company=company, bindsale__department=department)
    elif request.user.userprofile.title.role_name in ['saleboss']:
        company = request.user.userprofile.company
        wxs = wxs.filter(company=company)
    elif request.user.userprofile.title.role_name in ['sale']:
        sale = Sale.objects.get(binduser=request.user)
        wxs = wxs.filter(bindsale=sale)
        wxs = wxs.exclude(delete__isnull=False)
    else:
        wxs = wxs

    #根据查询筛选
    wxs = wxs.filter(wxid__icontains=request.GET.get('wxid', ''))
    wxs = wxs.filter(wxname__icontains=request.GET.get('wxname', ''))
    if 'bindsale' in request.GET and request.GET['bindsale'] != '':
        wxs = wxs.filter(bindsale__saleId__icontains=request.GET.get('bindsale'))
    if request.GET.get('delete', '') != '':
        isDelete = request.GET.get('delete')
        if isDelete == '1':
            wxs = wxs.filter(delete__isnull=False)
        else:
            wxs = wxs.filter(delete__isnull=True)
    p = Paginator(wxs, 20)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        wxPage = p.page(page)
    except (EmptyPage, InvalidPage):
        wxPage = p.page(p.num_pages)
    data = {
        "wxPage": wxPage,
        "requestArgs": getArgsExcludePage(request),
    }
    return render(request, 'wxqq/queryWx.html', data)

@login_required()
def addWx(request):
    data = {}
    try:
        bindsaleid = request.POST.get('bindsale', '无')
        if request.POST['id'] == "":
            newWx = Wx.objects.create(wxid=request.POST['wxid'])
            newWx.create = datetime.date.today()
        else:
            newWx = Wx.objects.get(id=int(request.POST['id']))
            newWx.wxid = request.POST['wxid']
        if bindsaleid.isdigit():
            newWx.bindsale = Sale.objects.get(id=bindsaleid)
        else:
            newWx.bindsale = None
        newWx.password = request.POST['password']
        newWx.company = request.POST['company']
        newWx.wxname = request.POST['wxname']
        newWx.bindphone = request.POST.get('bindphone', '')
        newWx.bindemail = request.POST.get('bindemail', '')
        newWx.bindqq = request.POST.get('bindqq', '')
        newWx.save()
        data['msg'] = "操作成功"
        data['msgLevel'] = "info"
    except Exception as e:
        print(e.__str__())
        print(e.message)
        if str(e.__str__()).__contains__('wxid'):
            data['msg'] = "操作失败,微信ID已存在"
        else:
            data['msg'] = "操作失败,请联系管理员。错误信息:%s,%s" % (e.__str__(), e.message)
        data['msgLevel'] = "error"
    return HttpResponse(json.dumps(data))

@login_required()
def delWx(request):
    data = {}
    try:
        tmpWx = Wx.objects.get(id=request.POST['dwid'])
        tmpWx.delete = datetime.date.today()
        tmpWx.reason = request.POST.get('reason')
        tmpWx.bindsale = None
        tmpWx.save()
        data['msg'] = "操作成功"
        data['msgLevel'] = "info"
    except Exception as e:
        print(e.__str__())
        data['msg'] = "操作失败"
        data['msgLevel'] = "error"
    return HttpResponse(json.dumps(data))

@login_required()
def resetWx(request):
    data = {}
    try:
        tmpWx = Wx.objects.get(id=request.POST['id'])
        tmpWx.delete = None
        tmpWx.reason = ""
        tmpWx.save()
        data['msg'] = "操作成功"
        data['msgLevel'] = "info"
    except Exception as e:
        print(e.__str__())
        data['msg'] = "操作失败"
        data['msgLevel'] = "error"
    return HttpResponse(json.dumps(data))

@login_required()
def editWxFriend(request):
    data = {}
    try:
        id = request.POST.get('ewid')
        wx = Wx.objects.get(id=id)
        lastDayFriend = wx.friend
        todayFriend = request.POST.get('friend')
        delta = int(todayFriend) - int(lastDayFriend)
        wx.friend = todayFriend
        wx.modify = datetime.date.today()
        wfh = WxFriendHis.objects.create(wx=wx, day =datetime.date.today(), total=todayFriend, delta=delta)
        wfh.save()
        wx.save()
        data['msg'] = '操作成功'
        data['msgLevel'] = 'info'
    except Exception as e:
        print(e.__str__())
        print(e.message)
        if(str(e.__str__()).__contains__('wxfriendhis_day')):
            data['msg'] = '操作失败,当天已经录入过好友数'
        else:
            data['msg'] = '操作失败'
        data['msgLevel'] = 'error'
    return HttpResponse(json.dumps(data))

@login_required()
def wxFriendSerial(request):
    wx = Wx.objects.get(id=request.GET.get('id'))
    friendHis = wx.wxfriendhis_set.all().order_by('-day')[0:30]
    totalData = []
    deltaData = []
    dayData = []
    for friend in friendHis:
        deltaData.insert(0, friend.delta)
        totalData.insert(0, friend.total)
        dayData.insert(0, friend.day)
    data = {
        "totalData": totalData,
        "deltaData": deltaData,
        "dayData": dayData,
    }

    return render(request, "wxqq/wxFriendSerial.html", data)

@login_required()
def qqManage(request):
    if (not request.user.userprofile.title.role_name in ['admin', 'ops', 'sale', 'salemanager', 'saleboss']):
        return HttpResponseRedirect("/")
    bindsales = Sale.objects.all().order_by("saleId")
    data = {
        "bindsales": bindsales,
    }
    return render(request, 'wxqq/qqManage.html', data)

@login_required()
def queryQq(request):
    data = {}
    qqs = Qq.objects.all().order_by('delete','qqid')
    # 不同角色看到的范围不同
    if request.user.userprofile.title.role_name in ['salemanager']:

        company = request.user.userprofile.company
        department = request.user.userprofile.department
        print(company)
        qqs = qqs.filter(company=company, bindsale__company=company, bindsale__department=department)
    elif request.user.userprofile.title.role_name in ['saleboss']:
        company = request.user.userprofile.company
        qqs = qqs.filter(company=company)
    elif request.user.userprofile.title.role_name in ['sale']:
        sale = Sale.objects.get(binduser=request.user)
        qqs = qqs.filter(bindsale=sale)
        qqs = qqs.exclude(delete__isnull=False)
    else:
        qqs = qqs

    # 根据查询筛选
    qqs = qqs.filter(qqid__icontains=request.GET.get('qqid', ''))
    qqs = qqs.filter(qqname__icontains=request.GET.get('qqname', ''))
    if 'bindsale' in request.GET and request.GET['bindsale'] != '':
        qqs = qqs.filter(bindsale__saleId__icontains=request.GET.get('bindsale'))
    if request.GET.get('delete', '') != '':
        isDelete = request.GET.get('delete')
        if isDelete == '1':
            qqs = qqs.filter(delete__isnull=False)
        else:
            qqs = qqs.filter(delete__isnull=True)
    p = Paginator(qqs, 20)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        qqPage = p.page(page)
    except (EmptyPage, InvalidPage):
        qqPage = p.page(p.num_pages)
    data = {
        "qqPage": qqPage,
        "requestArgs": getArgsExcludePage(request),
    }
    return render(request, 'wxqq/queryQq.html', data)

@login_required()
def addQq(request):
    data = {}
    try:
        bindsaleid = request.POST.get('bindsale', '无')
        if request.POST['id'] == "":
            newQq = Qq.objects.create(qqid=request.POST['qqid'])
            newQq.create = datetime.date.today()
        else:
            newQq = Qq.objects.get(id=request.POST['id'])
            newQq.qqid = request.POST['qqid']
        if bindsaleid.isdigit():
            newQq.bindsale = Sale.objects.get(id=bindsaleid)
        else:
            newQq.bindsale = None
        newQq.password = request.POST['password']
        newQq.company = request.POST['company']
        newQq.protect = request.POST['protect']
        newQq.qqname = request.POST['qqname']
        newQq.save()
        data['msg'] = "操作成功"
        data['msgLevel'] = "info"
    except Exception as e:
        print(e.__str__())
        print(e.message)
        if str(e.__str__()).__contains__('qqid'):
            data['msg'] = "操作失败,QQ已存在"
        else:
            data['msg'] = "操作失败,请联系管理员。错误信息:%s,%s" % (e.__str__(), e.message)
        data['msgLevel'] = "error"
    return HttpResponse(json.dumps(data))

@login_required()
def delQq(request):
    data = {}
    try:
        tmpQq = Qq.objects.get(id=request.POST['dqid'])
        tmpQq.delete = datetime.date.today()
        tmpQq.reason = request.POST.get("reason", "")
        tmpQq.bindsale = None
        tmpQq.save()
        data['msg'] = "操作成功"
        data['msgLevel'] = "info"
    except Exception as e:
        print(e.__str__())
        data['msg'] = "操作失败"
        data['msgLevel'] = "error"
    return HttpResponse(json.dumps(data))

@login_required()
def resetQq(request):
    data = {}
    try:
        tmpQq = Qq.objects.get(id=request.POST['id'])
        tmpQq.delete = None
        tmpQq.reason = ""
        tmpQq.save()
        data['msg'] = "操作成功"
        data['msgLevel'] = "info"
    except Exception as e:
        print(e.__str__())
        data['msg'] = "操作失败"
        data['msgLevel'] = "error"
    return HttpResponse(json.dumps(data))

@login_required()
def editQqFriend(request):
    data = {}
    try:
        id = request.POST.get('eqid')
        qq = Qq.objects.get(id=id)
        lastDayFriend = qq.friend
        todayFriend = request.POST.get('friend')
        delta = int(todayFriend) - int(lastDayFriend)
        qq.friend = todayFriend
        qq.modify = datetime.date.today()
        qfh = QqFriendHis.objects.create(qq=qq, day =datetime.date.today(), total=todayFriend, delta=delta)
        qfh.save()
        qq.save()
        data['msg'] = '操作成功'
        data['msgLevel'] = 'info'
    except Exception as e:
        print(e.__str__())
        print(e.message)
        if(str(e.__str__()).__contains__('qqfriendhis_day')):
            data['msg'] = '操作失败,当天已经录入过好友数'
        else:
            data['msg'] = '操作失败'
        data['msgLevel'] = 'error'
    return HttpResponse(json.dumps(data))

@login_required()
def qqFriendSerial(request):
    qq = Qq.objects.get(id=request.GET.get('id'))
    friendHis = qq.qqfriendhis_set.all().order_by('-day')[0:30]
    totalData = []
    deltaData = []
    dayData = []
    for friend in friendHis:
        deltaData.insert(0, friend.delta)
        totalData.insert(0, friend.total)
        dayData.insert(0, friend.day)
    data = {
        "totalData": totalData,
        "deltaData": deltaData,
        "dayData": dayData,
    }

    return render(request, "wxqq/qqFriendSerial.html", data)