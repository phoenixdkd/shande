
from django.conf.urls import include, url
from ops import views
urlpatterns = [
    url(r'^userManage$', views.userManage, name='userManage'),
    url(r'^addUser$', views.addUser, name='addUser'),
    url(r'^queryUser$', views.queryUser, name='queryUser'),
    url(r'^delUser$', views.delUser, name='delUser'),
    url(r'^resetPw$', views.resetPw, name='resetPw'),
    url(r'^chargebackSerial$', views.chargebackSerial, name='chargebackSerial'),
    url(r'^checkUserId$', views.checkUserId, name='checkUserId'),
    url(r'^checkEditUserId$', views.checkEditUserId, name='checkEditUserId'),
    url(r'^checkCId$', views.checkCId, name='checkCId'),
    url(r'^checkEditCId$', views.checkEditCId, name='checkEditCId'),
    url(r'^systermLog$', views.systemLog, name='systemLog'),
    url(r'^addFixContent$',views.addFixContent,name='addFixContent'),
    url(r'^queryLog$',views.queryLog,name='queryLog'),
]
