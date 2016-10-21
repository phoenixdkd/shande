
from django.conf.urls import include, url
from sale import views
urlpatterns = [
    url(r'^saleManage$', views.saleManage, name='saleManage'),
    url(r'^querySale$', views.querySale, name='querySale'),
    url(r'^addSale$', views.addSale, name='addSale'),
    url(r'^addSaleGroup$', views.addSaleGroup, name='addSaleGroup'),
    url(r'^delSale$', views.delSale, name='delSale'),

    url(r'^saleManagerPasswordManage$', views.saleManagerPasswordManage, name='saleManagerPasswordManage'),
    url(r'^addSaleManagerPassword$', views.addSaleManagerPassword, name='addSaleManagerPassword'),
    url(r'^delSaleManagerPassword$', views.delSaleManagerPassword, name='delSaleManagerPassword'),

    url(r'^saleKpiReport$', views.saleKpiReport, name='saleKpiReport'),
    url(r'^getCompanyDetail$', views.getCompanyDetail, name='getCompanyDetail'),
    url(r'^getDepartmentDetail$', views.getDepartmentDetail, name='getDepartmentDetail'),
    url(r'^getGroupDetail$', views.getGroupDetail, name='getGroupDetail'),
    url(r'^getSaleDetail$', views.getSaleDetail, name='getSaleDetail'),


]
