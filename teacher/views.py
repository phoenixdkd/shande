# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models import Q

import os, time, logging
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
from sale.models import *
logger = logging.getLogger("django")

@login_required()
def teacherManage(request):
    # t1 = time.clock()
    if (not request.user.userprofile.title.role_name in ['admin', 'ops']):
        return HttpResponseRedirect("/")
    bindUsers = User.objects.filter(userprofile__title__role_name='teacher').order_by("username")
    bindBursars = Bursar.objects.all()
    bindspotteachers = SpotTeacher.objects.all().order_by('teacherId')
    data = {
        "bindusers": bindUsers,
        "bindBursars": bindBursars,
        "bindspotteachers": bindspotteachers,
    }
    # t2 = time.clock()
    # logger.error("teacherManage cost time: %f"%(t2-t1))
    return render(request, 'teacher/teacherManage.html', data)

@login_required()
def queryTeacher(request):
    # t1 = time.clock()
    if(request.GET.get('teacherid') or request.GET.get('company') or request.GET.get('department') or request.GET.get('group') or request.GET.get('binduser')):
        teachers = Teacher.objects.all().order_by('teacherId')
        teachers = teachers.filter(teacherId__icontains=request.GET.get('teacherid', ''))
        teachers = teachers.filter(company__icontains=request.GET.get('company', ''))
        teachers = teachers.filter(department__icontains=request.GET.get('department', ''))
        teachers = teachers.filter(group__icontains=request.GET.get('group', ''))

        if 'binduser' in request.GET and request.GET['binduser'] != '':
          teachers = teachers.filter(binduser__userprofile__nick__icontains=request.GET.get('binduser'))
        p = Paginator(teachers, 15)
        try:
           page = int(request.GET.get('page', '1'))
        except ValueError:
           page = 1
        try:
           teacherPage = p.page(page)
        except (EmptyPage, InvalidPage):
           teacherPage = p.page(p.num_pages)

        showContent = "True"
        showContent = json.dumps(showContent)
        data = {
          "teacherPage": teacherPage,
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
    # logger.error("queryTeacher cost time: %f"%(t2-t1))
    return render(request, 'teacher/queryTeacher.html', data)

@login_required()
def addTeacher(request):
    # t1 = time.clock()
    data = {}
    try:

        if request.POST['id'] == "":
            newTeacher = Teacher.objects.create(teacherId=request.POST['teacherid'])
        else:
            newTeacher = Teacher.objects.get(id=request.POST['id'])
            newTeacher.teacherId = request.POST['teacherid']

        # binduserid = request.POST.get('binduser', '无')
        if request.POST.get('bindusername', '无'):
            if User.objects.get(username=request.POST.get('bindusername')):
                user = User.objects.get(username=request.POST.get('bindusername'))
                binduserid = str(user.id)
        else:
            binduserid = '无'

        if binduserid.isdigit():
            try:
                oldTeacher = Teacher.objects.get(binduser_id=binduserid)
                oldTeacher.binduser = None
                oldTeacher.save()
            except Exception as e:
                # print(e.message)
                # print(e.__str__())
                pass
            newTeacher.binduser = User.objects.get(id=binduserid)
        else:
            newTeacher.binduser = None


        # bindbursarid = request.POST.get('bindbursar', '无')
        if request.POST.get('bindbursarId', '无'):
            if Bursar.objects.get(bursarId=request.POST.get('bindbursarId')):
                bursar = Bursar.objects.get(bursarId=request.POST.get('bindbursarId'))
                bindbursarid = str(bursar.id)
        else:
            bindbursarid = '无'
        if bindbursarid.isdigit():
            newTeacher.bindbursar = Bursar.objects.get(id=bindbursarid)
        else:
            newTeacher.bindbursar = None

        # 如果绑定的财务变化，需要将该老师所有未收款的客户都切换对应的财务
        customers = newTeacher.customer_set.filter(~Q(status=40) & ~Q(status=98))
        for customer in customers:
            customer.bursar = newTeacher.bindbursar
            customer.save()
        bindspotteacherid = request.POST.get('bindspotteacher', '无')
        if bindspotteacherid.isdigit():
            newTeacher.bindspotteacher = SpotTeacher.objects.get(id=bindspotteacherid)
        else:
            newTeacher.bindspotteacher = None
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
    # t2 = time.clock()
    # logger.error("addTeacher cost time: %f"%(t2-t1))
    return HttpResponse(json.dumps(data))

@login_required()
def addTeacherGroup(request):
    # t1 = time.clock()
    data = {}
    try:
        company = request.POST.get('teacherCompany')
        department = request.POST.get('teacherDepartment')
        group = request.POST.get('teacherGroup')
        teacherCount = request.POST.get('teacherCount')
        for i in range(1, int(teacherCount) + 1):
            if i < 10:
                index = '0' + str(i)
            else:
                index = str(i)
            teacherId = company + group + department + index
            teacher, created = Teacher.objects.get_or_create(teacherId=teacherId)
            teacher.company = company
            teacher.department = department
            teacher.group = group
            teacher.save()
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
    # t2 = time.clock()
    # logger.error("addTeacherGroup cost time: %f"%(t2-t1))

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