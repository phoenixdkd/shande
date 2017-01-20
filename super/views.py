# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from PIL import Image, ImageDraw, ImageFont
import os
import random
import string
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO
import datetime
import traceback
import json

from shande.settings import BASE_DIR
from super.models import *


# Create your views here.
def index(request):
    if request.user.is_authenticated():
        return render(request, 'super/index.html', locals())
    else:
        redirect_to = 'accounts/login/'
        return HttpResponseRedirect(redirect_to)

def login_view(request):
    data = {
        "accept": request.META['HTTP_ACCEPT'],
    }
    failed = False
    if 'next' in request.GET:
        redirect_to = request.GET['next']
    else:
        redirect_to = '/ops/userManage/'
    if request.method == 'POST':
        if 'captcha' not in request.session:
            redirect_to = '/'
            return HttpResponseRedirect(redirect_to)
        if 'ident' in request.POST and string.upper(request.POST['ident']) == string.upper(request.session['captcha']):
            user = None
            try:
                user = User.objects.get(username=request.POST['username'])
            except Exception as e:
                print(e.__str__())
                print(request.POST['username'])
                error_msg = "用户不存在"
            if user:
                faillocktime = user.userprofile.faillocktime
                if faillocktime:
                    deltatime = (datetime.datetime.now() - faillocktime).total_seconds() - 900
                    if deltatime < 0:
                        error_msg = "用户已锁定，解锁倒计时 %s 秒" % int(deltatime)
                        return render(request, 'super/login_view.html', locals())
                userauth = authenticate(username=request.POST['username'], password=request.POST['password'])
                if userauth is not None:
                    login(request, userauth)
                    if userauth.userprofile.title.role_name in ['sale', 'saleboss', 'salemanager']:
                        redirect_to = '/customer/customerManage'
                    elif userauth.userprofile.title.role_name in ['teacher', 'teacherboss', 'teachermanager']:
                        redirect_to = '/customer/customerHandle'
                    elif userauth.userprofile.title.role_name in ['spotteacher', 'spotmanager']:
                        redirect_to = '/spot/spotCustomer'
                    elif userauth.userprofile.title.role_name in ['bursar', 'bursarmanager']:
                        redirect_to = '/customer/tradePayManage'
                    elif userauth.userprofile.title.role_name in ['admin', 'ops']:
                        redirect_to = '/ops/userManage'
                    else:
                        redirect_to = '/'
                    userauth.userprofile.failcount = 0
                    userauth.userprofile.faillocktime = None
                    userauth.userprofile.save()
                    return HttpResponseRedirect(redirect_to)
                else:
                    failcount = user.userprofile.failcount
                    failcount += 1
                    if failcount > 3:
                        error_msg = "登陆失败超过三次，十五分钟内无法登陆"
                        user.userprofile.failcount = failcount
                        user.userprofile.faillocktime = datetime.datetime.now()
                    else:
                        error_msg = "用户密码错误，登陆失败三次后，将锁定十五分钟"
                        user.userprofile.failcount = failcount
                    user.userprofile.save()
            else:
                error_msg = "用户%s不存在" % request.POST['username']
        else:
            error_msg = "验证码错误"
    return render(request, 'super/login_view.html', locals())

def logout_view(request):
    logout(request)
    redirect_to = '/'
    return HttpResponseRedirect(redirect_to)

def captcha(request):
    image = Image.new('RGB', (147, 49), color=(255, 255, 255))
    # model, size, background color
    font_file = os.path.join(BASE_DIR, 'static/assets/fonts/simsun.ttc')
    font = ImageFont.truetype(font_file, 30)
    # the font object
    draw = ImageDraw.Draw(image)
    rand_str = ''.join(random.sample(string.letters + string.digits, 4))
    # The random string
    draw.text((7, 0), rand_str, fill=(0, 0, 0), font=font)
    # position, content, color, font
    del draw
    request.session['captcha'] = rand_str.lower()
    # store the content in Django's session store
    buf = StringIO()
    # a memory buffer used to store the generated image
    image.save(buf, 'jpeg')
    return HttpResponse(buf.getvalue(), 'image/jpeg')
    # return the image data stream as image/jpeg format, browser will treat it as an image

def siteswitch(request):
    maintaince = Config.objects.get(key="维护模式");
    return HttpResponse(maintaince.value)

def maintaince(request):
    message = Config.objects.get(key="维护公告")
    data = {
        "message": message.value,
    }
    return render(request, 'maintaince.html', data)

def wap(request):
    data = {
        "message": "手机网页暂时无法查看。",
    }
    return render(request, 'wap.html', data)

@login_required()
def userInfo(request):
    return render(request, 'super/userInfo.html', locals())

def modifyPassword(request):
    data = {}
    user = authenticate(username=request.user.username, password=request.POST['currentPassword'])
    if user is not None:
        user.set_password(request.POST['password'])
        try:
            user.save()
            logout(request)
            data['msg'] = "密码更新成功，请重新登陆"
            data['msgLevel'] = "info"
        except Exception as e:
            print(e.__str__)
            data['msg'] = "更新密码失败"
            data['msgLevel'] = "error"
    else:
        data['msg'] = "当前密码错误"
        data['msgLevel'] = "error"
    return HttpResponse(json.dumps(data))

@login_required()
def titleManage(request):
    if (request.user.userprofile.title.role_name != 'admin'):
        return HttpResponseRedirect("/")
    titles = Title.objects.all()
    data = {
        "titles": titles,
    }
    return render(request, 'super/titleManage.html', locals())

@login_required()
def demo(request):
    if (request.user.userprofile.title.role_name != 'admin'):
        return HttpResponseRedirect("/")
    titles = 'It is my demo'
    data = {
        "titles": titles,
    }
    return render(request, 'super/demo.html', locals())

@login_required()
def addTitle(request):
    data = {}
    title = Title()
    title.role_name = request.POST['role_name']
    title.role_desc = request.POST['role_desc']
    try:
        title.save()
        data['msg'] = "新增职位成功"
        data['msgLevel'] = "info"
    except Exception as e:
        print(e.__str__())
        data['msg'] = "新增职位失败"
        data['msgLevel'] = "error"
    return HttpResponse(json.dumps(data))

@login_required()
def deleteTitle(request):
    data = {}
    titleId = request.POST['titleId']
    try:
        title = Title.objects.get(id=titleId)
        title.delete()
        data['msg'] = "删除职位成功"
        data['msgLevel'] = "info"
    except Exception as e:
        print(e.__str__)
        data['msg'] = "删除职位失败"
        data['msgLevel'] = "error"
    return HttpResponse(json.dumps(data))

@login_required()
def logoManage(request):
    if (request.user.userprofile.title.role_name != 'admin'):
        return HttpResponseRedirect("/")
    return render(request, 'super/logoManage.html')

@login_required
def logoUpload(request):
    data = {}
    try:
        logofile = request.FILES['file']
        file = open("super/static/super/images/header.jpg", "wb+")
        for chunk in logofile.chunks():
            file.write(chunk)
        file.close()
        data['msg'] = "修改LOGO成功"
        data['msgLevel'] = "info"
    except Exception as e:
        print(e.__str__)
        data['msg'] = "删除职位失败"
        data['msgLevel'] = "error"
    return HttpResponse(json.dumps(data))

@login_required()
def getTransmission(request):
    msg = ""
    try:
        transmission = Transmission.objects.get(user=request.user, checked=False)
        msg = transmission.transmission
        transmission.checked = True
        transmission.save()

    except Exception as e:
        hasMessage = False
    if msg:
        hasMessage = True
    else:
        hasMessage = False
    data = {
        "hasMessage": hasMessage,
        "msg": msg,
    }
    return HttpResponse(json.dumps(data))