
from django.conf.urls import include, url
from bursar import views
urlpatterns = [
    url(r'^bursarManage$', views.bursarManage, name='bursarManage'),
    url(r'^queryBursar$', views.queryBursar, name='queryBursar'),
    url(r'^addBursar$', views.addBursar, name='addBursar'),
    url(r'^addBursarGroup$', views.addBursarGroup, name='addBursarGroup'),
    url(r'^delBursar$', views.delBursar, name='delBursar'),

    url(r'^payReport$', views.payReport, name='payReport'),
    url(r'^queryPayReport$', views.queryPayReport, name='queryPayReport'),
    url(r'^payTypeReport$', views.payTypeReport, name='payTypeReport'),
    url(r'^payCompanyReport$', views.payCompanyReport, name='payCompanyReport'),
    url(r'^queryPayCompany$', views.queryPayCompany, name='queryPayCompany'),
    url(r'^payStockReport$', views.payStockReport, name='payStockReport'),
    url(r'^payCompanySerialReport$', views.payCompanySerialReport, name='payCompanySerialReport'),
]
