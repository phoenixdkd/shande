
from django.conf.urls import include, url
from spot import views
urlpatterns = [
    url(r'^teacherManage$', views.teacherManage, name='teacherManage'),
    url(r'^queryTeacher$', views.queryTeacher, name='queryTeacher'),
    url(r'^addTeacher$', views.addTeacher, name='addTeacher'),
    url(r'^addTeacherGroup$', views.addTeacherGroup, name='addTeacherGroup'),
    url(r'^delTeacher$', views.delTeacher, name='delTeacher'),

    url(r'^spotCustomer$', views.spotCustomer, name='spotCustomer'),
    url(r'^querySpotCustomer$', views.querySpotCustomer, name='querySpotCustomer'),

    url(r'^spotManage$', views.spotManage, name='spotManage'),
    url(r'^querySpot$', views.querySpot, name='querySpot'),
    url(r'^addSpot$', views.addSpot, name='addSpot'),
    url(r'^handleSpot$', views.handleSpot, name='handleSpot'),

    url(r'^spotReport$', views.spotReport, name='spotReport'),
    url(r'^getSpotTeacherDetail$', views.getSpotTeacherDetail, name='getSpotTeacherDetail'),


]
