# coding=utf-8
import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models import Q, Count
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import datetime
from sale.models import *
from customer.models import *
from shande.util import *


@login_required()
def saleManage(request):
    if (not request.user.userprofile.title.role_name in ['admin', 'ops', 'saleboss']):
        return HttpResponseRedirect("/")
    bindUsers = User.objects.filter(userprofile__title__role_name='sale').order_by("userprofile__nick")
    if request.user.userprofile.title.role_name == 'saleboss':
        bindUsers = bindUsers.filter(userprofile__company=request.user.userprofile.company)
    bindTeachers = Teacher.objects.all().order_by("teacherId")
    # for sale in Sale.objects.all():
    #     bindUsers = bindUsers.filter(~Q(id=sale.binduser.id))
    data = {
        "bindusers": bindUsers,
        "bindteachers": bindTeachers,
    }
    return render(request, 'sale/saleManage.html', data)

@login_required()
def querySale(request):
    sales = Sale.objects.all().order_by('saleId')
    #不同的用户看到不同的列表
    if request.user.userprofile.title.role_name == 'saleboss':
        sales = sales.filter(company=request.user.userprofile.company)
    sales = sales.filter(saleId__icontains=request.GET.get('saleid', ''))
    sales = sales.filter(company__icontains=request.GET.get('company', ''))
    sales = sales.filter(department__icontains=request.GET.get('department', ''))
    if 'binduser' in request.GET and request.GET['binduser'] != '':
        sales = sales.filter(binduser__userprofile__nick__icontains=request.GET.get('binduser'))
    if 'bindteacher' in request.GET and request.GET['bindteacher'] != '':
        sales = sales.filter(bindteacher__teacherId__icontains=request.GET.get('bindteacher'))
    if 'bindbursar' in request.GET and request.GET['bindbursar'] != '':
        sales = sales.filter(bindteacher__bindbursar__bursarId__icontains=request.GET.get('bindbursar'))

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
        if request.POST['id'] == "":
            newSale = Sale.objects.create(saleId=request.POST['saleid'])
        else:
            newSale = Sale.objects.get(id=request.POST['id'])
            newSale.saleId = request.POST['saleid']

        binduserid = request.POST.get('binduser', '无')
        if binduserid.isdigit():
            try:
                oldSale = Sale.objects.get(binduser_id=binduserid)
                oldSale.binduser = None
                oldSale.save()
            except Exception as e:
                # print(e.message)
                # print(e.__str__())
                pass
            newSale.binduser = User.objects.get(id=binduserid)
        else:
            newSale.binduser = None
        #newSale.bindteacher = getTeacherBySaleId(request.POST['saleid'])
        # newSale.company = request.POST['company']
        # newSale.department = request.POST['department']
        bindteacher = request.POST.get('bindteacher', '无')
        if bindteacher.isdigit():
            teacher = Teacher.objects.get(id=request.POST.get('bindteacher'))
            newSale.bindteacher = teacher
        else:
            newSale.bindteacher = None
        newSale.save()
        data['msg'] = "操作成功"
        data['msgLevel'] = "info"
    except Exception as e:
        print(e.__str__())
        print(e.message)
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
            if i<10:
                index = '0' +str(i)
            else:
                index = str(i)
            saleId = company + group + department + index
            sale, created = Sale.objects.get_or_create(saleId=saleId)
            sale.company = company
            sale.department = department
            sale.group = group
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

@login_required()
def saleKpiReport(request):
    if (not request.user.userprofile.title.role_name in ['admin', 'ops', 'salemanager', 'saleboss']):
        return HttpResponseRedirect("/")
    sql = """
        SELECT s.company, IFNULL(COUNT(c.id),0) as dcount
        FROM  sale_sale s
        LEFT JOIN customer_customer c ON c.sales_id = s.id and c.status = 40
        GROUP BY s.company
        ORDER by dcount desc
    """
    cursor = connection.cursor()
    cursor.execute(sql)
    companys = []
    for row in cursor.fetchall():
        company = {}
        company['company'] = row[0]
        company['dcount'] = row[1]
        companys.append(company)
    data = {
        "companys": companys,
    }
    return render(request, 'sale/saleKpiReport.html', data)

@login_required()
def getCompanyDetail(request):
    company = request.POST.get('company')
    cursor = connection.cursor()
    cursor.execute("""
            SELECT s.department, IFNULL(COUNT(c.id),0) as dcount
            FROM  sale_sale s
            LEFT JOIN customer_customer c ON c.sales_id = s.id and c.status = 40
            WHERE s.company = %s
            GROUP BY s.department
            ORDER by dcount desc
        """, [company])
    departments = []
    for row in cursor.fetchall():
        department = {}
        department['department'] = row[0]
        department['dcount'] = row[1]
        departments.append(department)
    data = {
        "departments": departments,
        "company": company,
    }
    return render(request, 'sale/getCompanyDetail.html', data)

@login_required()
def getDepartmentDetail(request):
    company = request.POST.get('company')
    department = request.POST.get('department')
    cursor = connection.cursor()
    cursor.execute("""
                SELECT s.group, IFNULL(COUNT(c.id),0) as dcount
                FROM  sale_sale s
                LEFT JOIN customer_customer c ON c.sales_id = s.id and c.status =40
                WHERE s.company = %s and s.department = %s
                GROUP BY s.group
                ORDER by dcount desc
            """, [company, department])
    groups = []
    for row in cursor.fetchall():
        group = {}
        group['group'] = row[0]
        group['dcount'] = row[1]
        groups.append(group)
    data = {
        "groups": groups,
        "company": company,
        "department": department,
    }
    return render(request, 'sale/getDepartmentDetail.html', data)

@login_required()
def getGroupDetail(request):
    company = request.POST.get('company')
    department = request.POST.get('department')
    group = request.POST.get('group')
    cursor = connection.cursor()
    cursor.execute("""
                SELECT s.id, s.saleid, IFNULL(COUNT(c.id),0) as dcount
                FROM  sale_sale s
                LEFT JOIN customer_customer c ON c.sales_id = s.id and c.status = 40
                WHERE s.company = %s and s.department = %s and s.group = %s
                GROUP BY s.saleid
                ORDER by dcount desc
            """, [company, department, group])
    sales = []
    for row in cursor.fetchall():
        sale = {}
        sale['id'] = row[0]
        sale['sale'] = row[1]
        sale['dcount'] = row[2]
        sales.append(sale)
    data = {
        "sales": sales,
        "group": group,
        "company": company,
        "department": department,
    }
    return render(request, 'sale/getGroupDetail.html', data)

@login_required()
def getSaleDetail(request):
    company = request.POST.get('company')
    department = request.POST.get('department')
    group = request.POST.get('group')
    sale = request.POST.get('sale')
    customers = Customer.objects.filter(sales_id=sale, status=40).order_by('-first_trade')
    data = {
        "customers": customers,
        "sale": sale,
        "group": group,
        "company": company,
        "department": department,
    }
    return render(request, 'sale/getSaleDetail.html', data)

@login_required()
def dishonestCustomerReport(request):
    if not request.user.userprofile.title.role_name in ['admin', 'ops', 'saleboss']:
        return HttpResponseRedirect("/")
    endDate = request.POST.get('endDate', "")
    if endDate == '':
        endDate = datetime.date.today()
    else:
        endDate = datetime.datetime.strptime(endDate, "%Y-%m-%d").date()
    startDate = request.POST.get('startDate', "")
    if startDate == "":
        startDate = datetime.date.today() - datetime.timedelta(days=30)
    else:
        startDate = datetime.datetime.strptime(startDate, "%Y-%m-%d").date()
    companys = Sale.objects.values('company').distinct()
    if request.user.userprofile.title.role_name == 'saleboss':
        companys = companys.filter(company=request.user.userprofile.company)
    days = []
    tmpDay = startDate
    while tmpDay <= endDate:
        days.append(tmpDay)
        tmpDay = tmpDay + datetime.timedelta(days=1)
    print(days)
    data = {
        "startDate": str(startDate),
        "endDate": str(endDate),
        "days": days,
        "companys": companys,
    }
    return render(request, 'sale/dishonestCustomerReport.html', data)

@login_required()
def saleKpiReportSerial(request):
    if not request.user.userprofile.title.role_name in ['admin', 'ops', 'saleboss']:
        return HttpResponseRedirect("/")
    endDate = request.POST.get('endDate', "")
    if endDate == '':
        endDate = datetime.date.today()
    else:
        endDate = datetime.datetime.strptime(endDate, "%Y-%m-%d").date()
    startDate = request.POST.get('startDate', "")
    if startDate == "":
        startDate = datetime.date.today() - datetime.timedelta(days=30)
    else:
        startDate = datetime.datetime.strptime(startDate, "%Y-%m-%d").date()
    companys = Sale.objects.values('company').distinct()
    if request.user.userprofile.title.role_name == 'saleboss':
        companys = companys.filter(company=request.user.userprofile.company)
    days = []
    tmpDay = startDate
    while tmpDay <= endDate:
        days.append(tmpDay)
        tmpDay = tmpDay + datetime.timedelta(days=1)
    print(days)
    data = {
        "startDate": str(startDate),
        "endDate": str(endDate),
        "days": days,
        "companys": companys,
    }
    return render(request, 'sale/saleKpiReportSerial.html', data)