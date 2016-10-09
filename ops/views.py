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

from shande.settings import BASE_DIR
from shande.util import *
from ops.models import *
from super.models import *

@login_required()
def userManage(request):
    if (not request.user.userprofile.title.role_name in ['admin' ,'ops'] ):
        return HttpResponseRedirect("/")
    titles = Title.objects.all()
    data = {
        "titles": titles,
    }
    return render(request, 'ops/userManage.html', data)

@login_required()
def addUser(request):
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
        newUser.save()
        newUser.userprofile.save()
        data['msg'] = "操作成功"
        data['msgLevel'] = "info"
    except Exception as e:
        print(e.__str__())
        data['msg'] = "操作失败"
        data['msgLevel'] = "error"
    return HttpResponse(json.dumps(data))

@login_required()
def queryUser(request):
    users = User.objects.all().order_by('-username')
    users = users.filter(~Q(username='admin'))
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
    return render(request, 'ops/queryUser.html', data)

@login_required()
def delUser(request):
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
    return HttpResponse(json.dumps(data))

@login_required()
def resetPw(request):
    data = {}
    try:
        tmpUser = User.objects.get(id=request.POST['userid'])
        tmpUser.set_password("123456")
        tmpUser.save()
        data['msg'] = "操作成功"
        data['msgLevel'] = "info"
    except Exception as e:
        print(e.__str__())
        data['msg'] = "操作失败"
        data['msgLevel'] = "error"
    return HttpResponse(json.dumps(data))