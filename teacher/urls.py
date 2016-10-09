
from django.conf.urls import include, url
from teacher import views
urlpatterns = [
    url(r'^teacherManage$', views.teacherManage, name='teacherManage'),
    url(r'^queryTeacher$', views.queryTeacher, name='queryTeacher'),
    url(r'^addTeacher$', views.addTeacher, name='addTeacher'),
    url(r'^delTeacher$', views.delTeacher, name='delTeacher'),
]
