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
    wxs = Wx.objects.all().order_by('wxid')

    #不同角色看到的范围不同
    if request.user.userprofile.title.role_name in ['salemanager']:
        company = request.user.userprofile.company
        department = request.user.userprofile.department
        wxs = wxs.filter(bindsale__company=company, bindsale__department=department)
    elif request.user.userprofile.title.role_name in ['saleboss']:
        company = request.user.userprofile.company
        wxs = wxs.filter(bindsale__company=company)
    elif request.user.userprofile.title.role_name in ['sale']:
        sale = Sale.objects.get(binduser=request.user)
        wxs = wxs.filter(bindsale=sale)
    else:
        wxs = wxs

    #根据查询筛选
    wxs = wxs.filter(wxid__icontains=request.GET.get('wxid', ''))
    wxs = wxs.filter(wxname__icontains=request.GET.get('wxname', ''))
    if 'bindsale' in request.GET and request.GET['bindsale'] != '':
        wxs = wxs.filter(bindsale__saleId__icontains=request.GET.get('bindsale'))
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
        bindsaleid = int(request.POST.get('bindsale', '1'))
        if request.POST['id'] == "":
            newWx = Wx.objects.create(wxid=request.POST['wxid'], bindsale=Sale.objects.get(id=int(bindsaleid)))
        else:
            newWx = Wx.objects.get(id=int(request.POST['id']))
            newWx.wxid = request.POST['wxid']
            newWx.bindsale = Sale.objects.get(id=int(bindsaleid))
        newWx.wxname = request.POST['wxname']
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
        tmpWx = Wx.objects.get(id=request.POST['id'])
        tmpWx.delete()
        data['msg'] = "操作成功"
        data['msgLevel'] = "info"
    except Exception as e:
        print(e.__str__())
        data['msg'] = "操作失败"
        data['msgLevel'] = "error"
    return HttpResponse(json.dumps(data))

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
    qqs = Qq.objects.all().order_by('qqid')
    # 不同角色看到的范围不同
    if request.user.userprofile.title.role_name in ['salemanager']:
        company = request.user.userprofile.company
        department = request.user.userprofile.department
        qqs = qqs.filter(bindsale__company=company, bindsale__department=department)
    elif request.user.userprofile.title.role_name in ['saleboss']:
        company = request.user.userprofile.company
        qqs = qqs.filter(bindsale__company=company)
    elif request.user.userprofile.title.role_name in ['sale']:
        sale = Sale.objects.get(binduser=request.user)
        qqs = qqs.filter(bindsale=sale)
    else:
        qqs = qqs

    # 根据查询筛选
    qqs = qqs.filter(qqid__icontains=request.GET.get('qqid', ''))
    qqs = qqs.filter(qqname__icontains=request.GET.get('qqname', ''))
    if 'bindsale' in request.GET and request.GET['bindsale'] != '':
        qqs = qqs.filter(bindsale__saleId__icontains=request.GET.get('bindsale'))
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
        bindsaleid = int(request.POST.get('bindsale', '1'))
        if request.POST['id'] == "":
            newQq = Qq.objects.create(qqid=request.POST['qqid'], bindsale=Sale.objects.get(id=int(bindsaleid)))
        else:
            newQq = Qq.objects.get(id=int(request.POST['id']))
            newQq.qqid = request.POST['qqid']
            newQq.bindsale = Sale.objects.get(id=int(bindsaleid))
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
        tmpQq = Qq.objects.get(id=request.POST['id'])
        tmpQq.delete()
        data['msg'] = "操作成功"
        data['msgLevel'] = "info"
    except Exception as e:
        print(e.__str__())
        data['msg'] = "操作失败"
        data['msgLevel'] = "error"
    return HttpResponse(json.dumps(data))