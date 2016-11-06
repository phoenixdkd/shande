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
from sale.models import *
from customer.models import *
from spot.models import *

@login_required()
def teacherManage(request):
    if (not request.user.userprofile.title.role_name in ['admin', 'ops']):
        return HttpResponseRedirect("/")
    bindUsers = User.objects.filter(userprofile__title__role_name__in=["spotteacher", "spotmanager"]).order_by("userprofile__nick")
    data = {
        "bindusers": bindUsers,
    }
    return render(request, 'spot/teacherManage.html', data)

@login_required()
def queryTeacher(request):
    teachers = SpotTeacher.objects.all().order_by('teacherId')
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
    return render(request, 'spot/queryTeacher.html', data)

@login_required()
def addTeacher(request):
    data = {}
    try:

        if request.POST['id'] == "":
            newTeacher = SpotTeacher.objects.create(teacherId=request.POST['teacherid'])
        else:
            newTeacher = SpotTeacher.objects.get(id=request.POST['id'])
            newTeacher.teacherId = request.POST['teacherid']
        binduserid = request.POST.get('binduser', '无')
        if binduserid.isdigit():
            try:
                oldTeacher = SpotTeacher.objects.get(binduser_id=binduserid)
                oldTeacher.binduser = None
                oldTeacher.save()
            except Exception as e:
                # print(e.message)
                # print(e.__str__())
                pass
            newTeacher.binduser = User.objects.get(id=binduserid)
        else:
            newTeacher.binduser = None
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
def addTeacherGroup(request):
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
            teacherId = company + department + group + index
            spotTeacher, created = SpotTeacher.objects.get_or_create(teacherId=teacherId)
            spotTeacher.company = company
            spotTeacher.department = department
            spotTeacher.group = group
            spotTeacher.save()
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
        tmpTeacher = SpotTeacher.objects.get(id=request.POST['id'])
        tmpTeacher.delete()
        data['msg'] = "操作成功"
        data['msgLevel'] = "info"
    except Exception as e:
        print(e.__str__())
        data['msg'] = "操作失败"
        data['msgLevel'] = "error"
    return HttpResponse(json.dumps(data))

@login_required()
def spotCustomer(request):
    if (not request.user.userprofile.title.role_name in ['admin', 'ops', 'spotteacher', 'spotmanager','teacher', 'teachermanager', 'teacherboss']):
        return HttpResponseRedirect("/")
    data = {}
    return render(request, 'spot/spotCustomer.html', data)

@login_required()
def querySpotCustomer(request):
    customers = Customer.objects.all().order_by('-modify')
    # 不同角色看到不同的列表
    if request.user.userprofile.title.role_name in ['spotteacher', 'spotmanager']:
        spotTeacher = SpotTeacher.objects.get(binduser=request.user)
        customers = customers.filter(spotTeacher=spotTeacher)
        customers = customers.exclude(status=99)
    elif request.user.userprofile.title.role_name in ['teacher']:
        teacher = Teacher.objects.get(binduser=request.user)
        customers = customers.filter(teacher=teacher)
        customers = customers.exclude(status=99)
    elif request.user.userprofile.title.role_name in ['teacherboss']:
        company = request.user.userprofile.company
        customers = customers.filter(teacher__company=company)
        customers = customers.exclude(status=99)
    elif request.user.userprofile.title.role_name in ['teachermanager']:
        company = request.user.userprofile.company
        department = request.user.userprofile.department
        customers = customers.filter(teacher__company=company, teacher__department=department)
        customers = customers.exclude(status=99)
    else:
        customers = customers

    # 去掉退回状态的客户
    customers = customers.exclude(status=10)
    customers = customers.exclude(status=30)

    # 按条件查询
    customers = customers.filter(teacher__teacherId__icontains=request.GET.get('teacherid', ''))
    customers = customers.filter(name__icontains=request.GET.get('name', ''))
    customers = customers.filter(phone__icontains=request.GET.get('phone', ''))
    if request.GET.get('wxid', '') != '':
        customers = customers.filter(wxid__icontains=request.GET.get('wxid', ''))
    if request.GET.get('wxname', '') != '':
        customers = customers.filter(wxname__icontains=request.GET.get('wxname', ''))
    if request.GET.get('qqid', '') != '':
        customers = customers.filter(qqid__icontains=request.GET.get('qqid', ''))
    if request.GET.get('qqname', '') != '':
        customers = customers.filter(qqname__icontains=request.GET.get('qqname', ''))
    if request.GET.get('startDate', '') != '':
        customers = customers.filter(create__gte=request.GET.get('startDate'))
    if request.GET.get('endDate', '') != '':
        customers = customers.filter(create__lte=request.GET.get('endDate'))
    p = Paginator(customers, 20)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        customerPage = p.page(page)
    except (EmptyPage, InvalidPage):
        customerPage = p.page(p.num_pages)
    data = {
        "customerPage": customerPage,
        "requestArgs": getArgsExcludePage(request),
    }
    return render(request, 'spot/querySpotCustomer.html', data)

@login_required()
def spotManage(request):
    if (not request.user.userprofile.title.role_name in ['admin', 'ops', 'spotteacher', 'spotmanager', 'teacher', 'teachermanager', 'teacherboss']):
        return HttpResponseRedirect("/")
    customerId = request.GET.get("customerId")
    customer = Customer.objects.get(id=customerId)
    data = {
        "customer": customer,
    }
    return render(request, 'spot/spotManage.html', data)

@login_required()
def querySpot(request):
    customerId = request.GET.get("customerid")
    spots = Spot.objects.filter(customer_id=customerId)
    cashTotal = 0
    profitTotal = 0
    taxTotal = 0
    for spot in spots:
        cashTotal += spot.cash
        profitTotal += spot.profit
        taxTotal += spot.tax

    sumTotal = cashTotal + profitTotal - taxTotal

    # 分页
    p = Paginator(spots, 20)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        spotPage = p.page(page)
    except (EmptyPage, InvalidPage):
        spotPage = p.page(p.num_pages)
    data = {
        "spotPage": spotPage,
        "requestArgs": getArgsExcludePage(request),
        "cashTotal": cashTotal,
        "profitTotal": profitTotal,
        "taxTotal": taxTotal,
        "sumTotal": sumTotal,
    }
    return render(request, 'spot/querySpot.html', data)

@login_required()
def addSpot(request):
    data = {}
    try:
        customer = Customer.objects.get(id=request.POST.get('customerid'))
        newSpot = Spot.objects.create(customer=customer)
        newSpot.create = timezone.now()
        cash = request.POST.get('cash')
        newSpot.cash = cash
        if cash > 0:
            newSpot.type = 10
        elif cash < 0:
            newSpot.type = 20
        else:
            newSpot.type = 99
        newSpot.profit = request.POST.get('profit')
        newSpot.tax = request.POST.get('tax')
        newSpot.save()
        data['msg'] = "操作成功"
        data['msgLevel'] = "info"
    except Exception as e:
        print(e.__str__())
        data['msg'] = "操作失败, %s" % e.__str__()
        data['msgLevel'] = "error"
    return HttpResponse(json.dumps(data))

@login_required()
def handleSpot(request):
    data = {}
    try:
        spot = Spot.objects.get(id=request.POST.get("hsid"))
        cash = request.POST.get('hscash')
        if cash > 0:
            spot.type = 10
        elif cash < 0:
            spot.type = 20
        else:
            spot.type = 99
        spot.cash = cash
        spot.profit = request.POST.get('hsprofit')
        spot.tax = request.POST.get('hstax')
        spot.save()
        data['msg'] = "操作成功"
        data['msgLevel'] = "info"
    except Exception as e:
        print(e.__str__())
        data['msg'] = "操作失败, %s" % e.__str__()
        data['msgLevel'] = "error"
    return HttpResponse(json.dumps(data))

@login_required()
def spotReport(request):
    spotTeachers = SpotTeacher.objects.all()
    data = {
        "spotTeachers": spotTeachers,
    }
    return render(request, 'spot/spotReport.html', data)

@login_required()
def getSpotTeacherDetail(request):
    spotTeacherId = request.POST.get('spotteacherid')
    customers = Customer.objects.filter(spotTeacher_id=spotTeacherId)
    data = {
        "customers": customers,
        "spotTeacherId": spotTeacherId,
    }
    return render(request, 'spot/getSpotTeacherDetail.html', data)