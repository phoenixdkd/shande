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
from teacher.models import *
from teacher.models import *

@login_required()
def teacherManage(request):
    if (not request.user.userprofile.title.role_name in ['admin', 'ops']):
        return HttpResponseRedirect("/")
    bindUsers = User.objects.filter(userprofile__title__role_name='teacher').order_by("userprofile__nick")
    for teacher in Teacher.objects.all():
        bindUsers = bindUsers.filter(~Q(id=teacher.binduser.id))
    bindBursars = Bursar.objects.all()
    data = {
        "bindusers": bindUsers,
        "bindBursars": bindBursars,
    }
    return render(request, 'teacher/teacherManage.html', data)

@login_required()
def queryTeacher(request):
    teachers = Teacher.objects.all().order_by('teacherId')
    teachers = teachers.filter(teacherId__icontains=request.GET.get('teacherid', ''))
    teachers = teachers.filter(company__icontains=request.GET.get('company', ''))
    teachers = teachers.filter(department__icontains=request.GET.get('department', ''))
    if 'binduser' in request.GET and request.GET['binduser'] != '':
        teachers = teachers.filter(binduser__userprofile__nick__icontains=request.GET.get('binduser'))
    p = Paginator(teachers, 20)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        teacherPage = p.page(page)
    except (EmptyPage, InvalidPage):
        teacherPage = p.page(p.num_pages)
    data = {
        "teacherPage": teacherPage,
        "requestArgs": getArgsExcludePage(request),
    }
    return render(request, 'teacher/queryTeacher.html', data)

@login_required()
def addTeacher(request):
    data = {}
    try:
        binduserid = request.POST.get('binduser', '无可用用户')
        if binduserid.isdigit():
            existTeacher = Teacher.objects.filter(binduser__id=binduserid)
            if binduserid != '1' and existTeacher and str(existTeacher[0].id) != request.POST.get('id', '1'):
                raise Exception("binduser exists")
        if request.POST['id'] == "":
            if binduserid.isdigit():
                existTeacher = Teacher.objects.filter(binduser__id=binduserid)
                newTeacher = Teacher.objects.create(teacherId=request.POST['teacherid'],
                                              binduser=User.objects.get(id=int(request.POST['binduser'])))
            else:
                newTeacher = Teacher.objects.create(teacherId=request.POST['teacherid'],)
        else:
            newTeacher = Teacher.objects.get(id=request.POST['id'])
            newTeacher.teacherId = request.POST['teacherid']
            if binduserid.isdigit():
                newTeacher.binduser = User.objects.get(id=int(request.POST['binduser']))
        newTeacher.bindbursar = Bursar.objects.get(id=int(request.POST['bindbursar']))
        newTeacher.company = request.POST['company']
        newTeacher.department = request.POST['department']
        newTeacher.save()
        data['msg'] = "操作成功"
        data['msgLevel'] = "info"
    except Exception as e:
        print(e.__str__())
        print(e.message)
        if str(e.__str__()).__contains__('teacherId'):
            data['msg'] = "操作失败,老师ID已存在"
        elif str(e.__str__()).__contains__('binduser'):
            data['msg'] = "操作失败,用户已绑定老师，请刷新页面重试"
        else:
            data['msg'] = "操作失败,请联系管理员。错误信息:%s" % e.__str__()
        data['msgLevel'] = "error"
    return HttpResponse(json.dumps(data))

@login_required()
def delTeacher(request):
    data = {}
    try:
        tmpTeacher = Teacher.objects.get(id=request.POST['id'])
        tmpTeacher.delete()
        data['msg'] = "操作成功"
        data['msgLevel'] = "info"
    except Exception as e:
        print(e.__str__())
        data['msg'] = "操作失败"
        data['msgLevel'] = "error"
    return HttpResponse(json.dumps(data))