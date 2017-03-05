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
import time

import logging
logger = logging.getLogger("django")

from shande.settings import BASE_DIR
from shande.util import *
from ops.models import *
from super.models import *

@login_required()
def userManage(request):
    # t1 = time.clock()
    if (not request.user.userprofile.title.role_name in ['admin' ,'ops', 'saleboss'] ):
        return HttpResponseRedirect("/")
    titles = Title.objects.all()
    data = {
        "titles": titles,
    }
    # t2 = time.clock()
    # logger.error("bursarMange cost time: %f s, start: %f, end: %f"%((t2-t1),t1,t2))
    return render(request, 'ops/userManage.html', data)

@login_required()
def addUser(request):
    # t1 = time.clock()
    data = {}
    try:
        if request.POST['userid'] == "":
            newUser = User.objects.create(username=request.POST['username'])
            newUser.set_password("123456")
            newUserProfile, created = UserProfile.objects.get_or_create(user=newUser,
                                                               title=Title.objects.get(id=int(request.POST['title'])) )
        else:
            newUser = User.objects.get(id=request.POST['userid'])
            newUser.username = request.POST['username']
            newUser.userprofile.title = Title.objects.get(id=int(request.POST['title']))
        newUser.username = request.POST['username']
        newUser.userprofile.nick = request.POST['nick']
        newUser.userprofile.cid = request.POST['cid']
        newUser.userprofile.company = request.POST['company']
        newUser.userprofile.department = request.POST['department']
        newUser.userprofile.group = request.POST['group']
        newUser.userprofile.faillocktime = None
        newUser.save()
        newUser.userprofile.save()
        data['msg'] = "操作成功"
        data['msgLevel'] = "info"
    except Exception as e:
        print(e.__str__())
        data['msg'] = "操作失败"
        data['msgLevel'] = "error"
    # t2 = time.clock()
    # logger.error("addUser cost time: %f" % (t2 - t1))
    return HttpResponse(json.dumps(data))

@login_required()
def queryUser(request):
    # t1 = time.clock()
    users = User.objects.all().order_by('-username')
    users = users.filter(~Q(username='admin'))
    if request.user.userprofile.title.role_name == 'saleboss':
        users = users.filter(userprofile__company=request.user.userprofile.company)
    users = users.filter(userprofile__company__icontains=request.GET.get('company', ''))
    users = users.filter(userprofile__department__icontains=request.GET.get('department', ''))
    if 'title' in request.GET:
        users = users.filter(userprofile__title__role_desc__icontains=request.GET.get('title'))
    users = users.filter(username__icontains=request.GET.get('username', ''))
    users = users.filter(userprofile__nick__icontains=request.GET.get('nick', ''))
    users = users.filter(userprofile__cid__icontains=request.GET.get('cid', ''))

    p = Paginator(users, 20)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        userpage = p.page(page)
    except (EmptyPage, InvalidPage):
        userpage = p.page(p.num_pages)
    data = {
        "userpage": userpage,
        "requestArgs": getArgsExcludePage(request),
    }
    # t2 = time.clock()
    # logger.error("queryUser cost time: %f" % (t2 - t1))
    return render(request, 'ops/queryUser.html', data)

@login_required()
def delUser(request):
    # t1 = time.clock()
    data = {}
    try:
        tmpUser = User.objects.get(id=request.POST['userid'])
        tmpUser.delete()
        data['msg'] = "操作成功"
        data['msgLevel'] = "info"
    except Exception as e:
        print(e.__str__())
        data['msg'] = "操作失败"
        data['msgLevel'] = "error"
    # t2 = time.clock()
    # logger.error("delUser cost time: %f" % (t2 - t1))
    return HttpResponse(json.dumps(data))

@login_required()
def resetPw(request):
    # t1 = time.clock()
    data = {}
    try:
        tmpUser = User.objects.get(id=request.POST['userid'])
        tmpUser.set_password("123456")
        tmpUser.userprofile.faillocktime = None
        tmpUser.userprofile.save()
        tmpUser.save()
        data['msg'] = "操作成功"
        data['msgLevel'] = "info"
    except Exception as e:
        print(e.__str__())
        data['msg'] = "操作失败"
        data['msgLevel'] = "error"
    # t2 = time.clock()
    # logger.error("reserPw cost time: %f" % (t2 - t1))
    return HttpResponse(json.dumps(data))

@login_required()
def chargebackSerial(request):
    # t1 = time.clock()
    u = User.objects.get(id=request.GET.get('userid'))
    userCommitHis = u.usercommithis_set.all().order_by('-day')[0:30]
    userGradeHis = u.usergradehis_set.all().order_by('-day')[0:30]
    userCommitDeltaData = []
    userGradeDeltaData = []
    chargebackData = []
    dayData = []
    for index in range(0, userCommitHis.__len__(), 1):
        chargebackData.insert(0, 100 - float(userGradeHis[index].total) / float(userCommitHis[index].total) * 100)
        userCommitDeltaData.insert(0, userCommitHis[index].delta)
        userGradeDeltaData.insert(0, userGradeHis[index].delta)
        dayData.insert(0, userGradeHis[index].day)
    data = {
        "chargebackData": chargebackData,
        "userCommitDeltaData": userCommitDeltaData,
        "userGradeDeltaData": userGradeDeltaData,
        "dayData": dayData,
    }
    # t2 = time.clock()
    # logger.error("chargebackSerial cost time: %f" % (t2 - t1))
    return render(request, "ops/chargebackSerial.html", data)

@login_required()
def checkUserId(request):
    # t1 = time.clock()
    username = request.POST.get('username')
    try:
        user = User.objects.get(username=username)
        valid = False
    except:
        valid = True
    data = {
        'valid': valid,
    }
    # t2 = time.clock()
    # logger.error("checkUserId cost time: %f" % (t2 - t1))
    return HttpResponse(json.dumps(data))

@login_required()
def checkCId(request):
    # t1 = time.clock()
    cid = request.POST.get('cid')
    valid = False
    try:
        user = User.objects.filter(userprofile__cid=cid)
        if user.__len__() == 0:
            valid = True
    except:
        traceback.print_exc()
    data = {
        'valid': valid,
    }
    # t2 = time.clock()
    # logger.error("checkId cost time: %f" % (t2 - t1))
    return HttpResponse(json.dumps(data))

@login_required()
def checkEditUserId(request):
    # t1 = time.clock()
    username = request.POST.get('username')
    try:
        user = User.objects.filter(username=username)
        if user.__len__() > 1:
            valid = False
        else:
            valid = True
    except:
        valid = True
    data = {
        'valid': valid,
    }
    # t2 = time.clock()
    # logger.error("checkEditUserId cost time: %f" % (t2 - t1))
    return HttpResponse(json.dumps(data))

@login_required()
def checkEditCId(request):
    # t1 = time.clock()
    cid = request.POST.get('cid')
    valid = False
    try:
        user = User.objects.filter(userprofile__cid=cid)
        if user.__len__() <= 1:
            valid = True
    except:
        traceback.print_exc()
    data = {
        'valid': valid,
    }
    # t2 = time.clock()
    # logger.error("checkEditCId cost time: %f" % (t2 - t1))
    return HttpResponse(json.dumps(data))

@login_required()
def systemLog(request):
    # t1 = time.clock()

    logs = Ops.objects.all()
    logs = logs.order_by("-create")
    # startDate = request.GET.get('startDate','')
    # endDate = request.GET.get('endDate','')

    # if startDate == '':
    #     startDate = request.POST.get('startDate', datetime.date.today() - datetime.timedelta(days=7))
    #     endDate = request.POST.get('endDate', datetime.date.today() + datetime.timedelta(days=1))

    # logs = logs.filter(create__lte=endDate,create__gte=startDate).distinct()

    p = Paginator(logs,20)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        logPage = p.page(page)
    except (EmptyPage, InvalidPage):
        logPage = p.page(p.num_pages)
    data = {
        "logPage": logPage,
        # "startDate": str(startDate),
        # "endDate": str(endDate),
    }
    # t2 = time.clock()
    # logger.error("systermLog cost time: %f" % (t2 - t1))
    return render(request, "ops/systemLog.html", data)

#编辑和修改维护信息
@login_required()
def addFixContent(request):
    # t1 = time.clock()
    data = {}
    try:
       if request.POST['id'] == '':

           #新增记录
           newRecord = Ops.objects.create(create=timezone.now())
           newRecord.fixContent = request.POST.get('content','')
       else:
           newRecord = Ops.objects.get(id=int(request.POST['id']))
           newRecord.create = timezone.now()
           newRecord.fixContent = request.POST['content']
       newRecord.save()

       data['msg'] = "操作成功"
       data['msgLevel'] = "info"
    except Exception as e:
        traceback.print_exc()
        data['msg'] = "操作失败"
        data['msgLevel'] = "error"
    # t2 = time.clock()
    # logger.error("addFixcontent cost time: %f" % (t2 - t1))
    return HttpResponse(json.dumps(data))

@login_required()
def queryLog(request):
    # if not request.user.userprofile.title.role_name in ['admin', 'ops']:
    #     return HttpResponseRedirect("/")
    # t1 = time.clock()
    logs = Ops.objects.all()
    logs = logs.order_by("-create")

    p = Paginator(logs,20)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        logPage = p.page(page)
    except (EmptyPage, InvalidPage):
        logPage = p.page(p.num_pages)
    data = {
        "logPage": logPage,
    }
    # t2 = time.clock()
    # logger.error("queryLog cost time: %f" % (t2 - t1))
    return render(request, "ops/queryLog.html", data)