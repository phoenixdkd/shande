
from django.conf.urls import include, url
from wxqq import views
urlpatterns = [
    url(r'^wxManage$', views.wxManage, name='wxManage'),
    url(r'^queryWx$', views.queryWx, name='queryWx'),
    url(r'^addWx$', views.addWx, name='addWx'),
    url(r'^delWx$', views.delWx, name='delWx'),
    url(r'^editWxFriend$', views.editWxFriend, name='editWxFriend'),
    url(r'^wxFriendSerial$', views.wxFriendSerial, name='wxFriendSerial'),


    url(r'^qqManage$', views.qqManage, name='qqManage'),
    url(r'^queryQq$', views.queryQq, name='queryQq'),
    url(r'^addQq$', views.addQq, name='addQq'),
    url(r'^delQq$', views.delQq, name='delQq'),
    url(r'^editQqFriend$', views.editQqFriend, name='editQqFriend'),
    url(r'^qqFriendSerial$', views.qqFriendSerial, name='qqFriendSerial'),

]
