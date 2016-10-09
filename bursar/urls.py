
from django.conf.urls import include, url
from bursar import views
urlpatterns = [
    url(r'^bursarManage$', views.bursarManage, name='bursarManage'),
    url(r'^queryBursar$', views.queryBursar, name='queryBursar'),
    url(r'^addBursar$', views.addBursar, name='addBursar'),
    url(r'^delBursar$', views.delBursar, name='delBursar'),
]
