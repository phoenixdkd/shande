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
from analyst.models import *

import logging
import time
logger = logging.getLogger("django")

@login_required()
def analystManage(request):
    # t1 = time.clock()
    if (not request.user.userprofile.title.role_name in ['admin', 'ops']):
        return HttpResponseRedirect("/")
    bindUsers = User.objects.filter(userprofile__title__role_name='analyst').order_by("userprofile__nick")
    # for analyst in Analyst.objects.all():
    #     bindUsers = bindUsers.filter(~Q(id=analyst.binduser.id))
    data = {
        "bindusers": bindUsers,
    }
    # t2 = time.clock()
    # logger.error("analystMangae cost time: %f %f %f s" % ((t2-t1),t1,t2))
    return render(request, 'analyst/analystManage.html', data)

@login_required()
def queryAnalyst(request):
    # t1 = time.clock()
    if (request.GET.get('analystid') or request.GET.get('binduser')):
        analysts = Analyst.objects.all().order_by('analystId')
        analysts = analysts.filter(analystId__icontains=request.GET.get('analystid', ''))
        # analysts = analysts.filter(company__icontains=request.GET.get('company', ''))
        if 'binduser' in request.GET and request.GET['binduser'] != '':
            analysts = analysts.filter(binduser__userprofile__nick__icontains=request.GET.get('binduser'))
        p = Paginator(analysts, 20)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        try:
            analystPage = p.page(page)
        except (EmptyPage, InvalidPage):
            analystPage = p.page(p.num_pages)
        showContent = "True"
        showContent = json.dumps(showContent)
        data = {
            "analystPage": analystPage,
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
    # logger.error("queryAnalyst cost time: %f"%(t2-t1))
    return render(request, 'analyst/queryAnalyst.html', data)


@login_required()
def addAnalyst(request):
    data = {}
    try:
        if request.POST['id'] == "":
            analysts = Analyst.objects.filter(analystId=request.POST['analystid']).count()
            if analysts:
                raise Exception("分析师ID已存在")
            else:
                newAnalyst = Analyst.objects.create(analystId=request.POST['analystid'],company=request.POST['company'])
        else:
            newAnalyst = Analyst.objects.get(id=request.POST['id'])


        if request.POST.get('bindusername'):
            # binduserid = request.POST.get('binduser', '无')
            if User.objects.get(username=request.POST.get('bindusername','')):
                user = User.objects.get(username=request.POST.get('bindusername',''))
                binduserid = str(user.id)
        else:
            binduserid = '无'


        if binduserid.isdigit():
            newAnalyst.binduser = User.objects.get(id=binduserid)
        else:
            newAnalyst.binduser = None
        newAnalyst.company = request.POST['company']
        # newAnalyst.department = request.POST['department']
        newAnalyst.save()
        data['msg'] = "操作成功"
        data['msgLevel'] = "info"
    except Exception as e:
        print(e.__str__())
        if str(e.__str__()).__contains__('analystId'):
            data['msg'] = "操作失败,分析师ID已存在"
        elif str(e.__str__()).__contains__('binduser'):
            data['msg'] = "操作失败,用户已绑定财务，请刷新页面重试"
        else:
            data['msg'] = "操作失败,请联系管理员。错误信息:%s" % e.__str__()
        data['msgLevel'] = "error"
    return HttpResponse(json.dumps(data))

@login_required()
def addAnalystGroup(request):
    data = {}
    try:
        # analystCount = request.POST.get('analystCount')
        analystCode = request.POST.get('analystCode')
        departmentID = request.POST.get('departmentID')
        groupID = request.POST.get('groupID')
        analystID = str(analystCode)+str(groupID)+str(departmentID)
        analyst,created = Analyst.objects.get_or_create(analystId=analystID)
        data['msg'] = "操作成功"
        data['msgLevel'] = "info"

    except Exception as e:
        print(e.__str__())
        if str(e.__str__()).__contains__('analystId'):
            data['msg'] = "操作失败,财务ID已存在"
        elif str(e.__str__()).__contains__('binduser'):
            data['msg'] = "操作失败,用户已绑定财务，请刷新页面重试"
        else:
            data['msg'] = "操作失败,请联系管理员。错误信息:%s" % e.__str__()
        data['msgLevel'] = "error"
    return HttpResponse(json.dumps(data))

@login_required()
def delAnalyst(request):
    data = {}
    try:
        tmpAnalyst = Analyst.objects.get(id=request.POST['id'])
        tmpAnalyst.delete()
        data['msg'] = "操作成功"
        data['msgLevel'] = "info"
    except Exception as e:
        print(e.__str__())
        data['msg'] = "操作失败"
        data['msgLevel'] = "error"
    return HttpResponse(json.dumps(data))