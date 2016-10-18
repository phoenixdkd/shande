# coding=utf-8

from super.models import *
from django.contrib.auth.models import User
def __main__():
    # title表
    Title.objects.create(role_name='admin', role_desc='超级管理员')
    Title.objects.create(role_name='ops', role_desc='管理员')
    Title.objects.create(role_name='sale', role_desc='客户开发专员')
    Title.objects.create(role_name='salemanager', role_desc='客户开发经理')
    Title.objects.create(role_name='saleboss', role_desc='客户开发总经理')
    Title.objects.create(role_name='teacher', role_desc='客户管理专员')
    Title.objects.create(role_name='teachermanager', role_desc='客户管理经理')
    Title.objects.create(role_name='teacherboss', role_desc='客户管理总经理')
    Title.objects.create(role_name='spotteacher', role_desc='现货老师')
    Title.objects.create(role_name='bursar', role_desc='财务专员')
    Title.objects.create(role_name='bursarmanager', role_desc='财务经理')

    #创建管理员和超级管理员
    user = User.objects.create(username='admin', is_superuser=1)
    user.password = '123456'
    user.userprofile.nick = '超级管理员'
    user.userprofile.title = Title.objects.get(role_name='admin')
    user.save()
    user.userprofile.save()

    user = User.objects.create(username='ops')
    user.password = '123456'
    user.userprofile.nick = '管理员'
    user.userprofile.title = Title.objects.get(role_name='ops')
    user.save()
    user.userprofile.save()

    #Config表
    Config.objects.create(key='维护模式', value='0')
    Config.objects.create(key='维护公告', value='网站维护中')



