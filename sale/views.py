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
import re

from shande.settings import BASE_DIR
from shande.util import *
from ops.models import *
from super.models import *
from sale.models import *


@login_required()
def saleManage(request):
    if (not request.user.userprofile.title.role_name in ['admin', 'ops']):
        return HttpResponseRedirect("/")
    bindUsers = User.objects.filter(userprofile__title__role_name='sale').order_by("userprofile__nick")
    for sale in Sale.objects.all():
        bindUsers = bindUsers.filter(~Q(id=sale.binduser.id))
    data = {
        "bindusers": bindUsers,
    }
    return render(request, 'sale/saleManage.html', data)

@login_required()
def querySale(request):
    sales = Sale.objects.all().order_by('saleId')
    sales = sales.filter(~Q(id=1))
    sales = sales.filter(saleId__icontains=request.GET.get('saleid', ''))
    sales = sales.filter(company__icontains=request.GET.get('company', ''))
    sales = sales.filter(department__icontains=request.GET.get('department', ''))
    if 'binduser' in request.GET and request.GET['binduser'] != '':
        sales = sales.filter(binduser__userprofile__nick__icontains=request.GET.get('binduser'))
    p = Paginator(sales, 20)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        salePage = p.page(page)
    except (EmptyPage, InvalidPage):
        salePage = p.page(p.num_pages)
    data = {
        "salePage": salePage,
        "requestArgs": getArgsExcludePage(request),
    }
    return render(request, 'sale/querySale.html', data)

@login_required()
def addSale(request):
    data = {}
    try:
        binduserid = request.POST.get('binduser', '无可用用户')
        if binduserid.isdigit():
            existSale = Sale.objects.filter(binduser__id=binduserid)
            if binduserid != '1' and existSale and str(existSale[0].id) != request.POST.get('id', '1'):
                raise Exception("binduser exists")
        if request.POST['id'] == "":
            if binduserid.isdigit():
                existSale = Sale.objects.filter(binduser__id=binduserid)
                newSale = Sale.objects.create(saleId=request.POST['saleid'],
                                              binduser=User.objects.get(id=int(request.POST['binduser'])),)
            else:
                newSale = Sale.objects.create(saleId=request.POST['saleid'],)
        else:
            newSale = Sale.objects.get(id=request.POST['id'])
            newSale.saleId = request.POST['saleid']
            if binduserid.isdigit():
                newSale.binduser = User.objects.get(id=int(request.POST['binduser']))
        newSale.bindteacher = getTeacherBySaleId(request.POST['saleid'])
        newSale.company = request.POST['company']
        newSale.department = request.POST['department']
        newSale.save()
        data['msg'] = "操作成功"
        data['msgLevel'] = "info"
    except Exception as e:
        print(e.__str__())
        if str(e.__str__()).__contains__('saleId'):
            data['msg'] = "操作失败,开发ID已存在"
        elif str(e.__str__()).__contains__('binduser'):
            data['msg'] = "操作失败,用户已绑定开发，请刷新页面重试"
        else:
            data['msg'] = "操作失败,请联系管理员。错误信息:%s" % e.__str__()
        data['msgLevel'] = "error"
    return HttpResponse(json.dumps(data))

@login_required()
def addSaleGroup(request):
    data = {}
    try:
        company = request.POST.get('saleCompany')
        department = request.POST.get('saleDepartment')
        group = request.POST.get('saleGroup')
        saleCount = request.POST.get('saleCount')
        for i in range(1, int(saleCount)+1):
            saleId = company + group + department + str(i)
            teacherId = company + group
            bursarId = re.sub(r'^[^\d]+', 'CW', teacherId)
            bursar, created = Bursar.objects.get_or_create(bursarId=bursarId)
            bursar.company = company
            bursar.department = department
            bursar.save()
            teacher, created = Teacher.objects.get_or_create(teacherId=teacherId)
            teacher.company = company
            teacher.department = department
            teacher.bindbursar = bursar
            teacher.save()
            sale, created = Sale.objects.get_or_create(saleId=saleId)
            sale.company = company
            sale.department = department
            sale.group = group
            sale.bindteacher = teacher
            sale.save()

        data['msg'] = "操作成功"
        data['msgLevel'] = "info"
    except Exception as e:
        print(e.__str__())
        if str(e.__str__()).__contains__('saleId'):
            data['msg'] = "操作失败,开发ID已存在"
        elif str(e.__str__()).__contains__('binduser'):
            data['msg'] = "操作失败,用户已绑定开发，请刷新页面重试"
        else:
            data['msg'] = "操作失败,请联系管理员。错误信息:%s" % e.__str__()
        data['msgLevel'] = "error"
    return HttpResponse(json.dumps(data))

@login_required()
def delSale(request):
    data = {}
    try:
        tmpSale = Sale.objects.get(id=request.POST['id'])
        tmpSale.delete()
        data['msg'] = "操作成功"
        data['msgLevel'] = "info"
    except Exception as e:
        print(e.__str__())
        data['msg'] = "操作失败"
        data['msgLevel'] = "error"
    return HttpResponse(json.dumps(data))

@login_required()
def saleManagerPasswordManage(request):
    if (not request.user.userprofile.title.role_name in ['admin', 'ops', 'salemanager', 'saleboss']):
        return HttpResponseRedirect("/")
    passwordList = SaleManagerPassword.objects.all()
    if request.user.userprofile.title.role_name in ['saleboss']:
        company = request.user.userprofile.company
        passwordList = passwordList.filter(company=company)
    elif request.user.userprofile.title.role_name in ['salemanager']:
        company = request.user.userprofile.company
        department = request.user.userprofile.department
        passwordList = passwordList.filter(company=company, department=department)
    else:
        passwordList = passwordList

    data = {
        "passwordList": passwordList,
    }
    return render(request, 'sale/saleManagerPasswordManage.html', data)

@login_required()
def addSaleManagerPassword(request):
    try:
        SaleManagerPassword.objects.create(company=request.POST.get('company'),
                                           department=request.POST.get('department'),
                                           password=request.POST.get('password'))
    except Exception as e:
        print(e.__str__())
        print(e.message)
    return HttpResponseRedirect('/sale/saleManagerPasswordManage')

@login_required()
def delSaleManagerPassword(request):
    try:
        SaleManagerPassword.objects.get(id=request.GET.get("id")).delete()
    except Exception as e:
        print(e.__str__())
        print(e.message)
    return HttpResponseRedirect('/sale/saleManagerPasswordManage')