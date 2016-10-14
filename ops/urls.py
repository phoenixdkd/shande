
from django.conf.urls import include, url
from ops import views
urlpatterns = [
    url(r'^userManage$', views.userManage, name='userManage'),
    url(r'^addUser$', views.addUser, name='addUser'),
    url(r'^queryUser$', views.queryUser, name='queryUser'),
    url(r'^delUser$', views.delUser, name='delUser'),
    url(r'^resetPw$', views.resetPw, name='resetPw'),
    url(r'^chargebackSerial$', views.chargebackSerial, name='chargebackSerial'),
]
