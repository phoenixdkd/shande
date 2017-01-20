"""techsure URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from super import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^logoManage$', views.logoManage, name='logoManage'),
    url(r'^logoUpload$', views.logoUpload, name='logoUpload'),

    url(r'^accounts/login/$', views.login_view, name='login'),
    url(r'^accounts/logout/$', views.logout_view, name='logout'),

    url(r'^captcha$', views.captcha, name='captcha'),
    url(r'^siteswitch$', views.siteswitch, name='siteswitch'),
    url(r'^maintaince$', views.maintaince, name='maintaince'),
    url(r'^wap$', views.wap, name='wap'),

    url(r'^userInfo$', views.userInfo, name='userInfo'),
    url(r'^modifyPassword$', views.modifyPassword, name='modifyPassword'),

    url(r'^titleManage$', views.titleManage, name='titleManage'),
    url(r'^addTitle$', views.addTitle, name='addTitle'),
    url(r'^deleteTitle$', views.deleteTitle, name='deleteTitle'),

    url(r'^getTransmission$', views.getTransmission, name='getTransmission'),
    url(r'^demo$', views.demo, name='demo'),
]
