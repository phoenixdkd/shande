
from django.conf.urls import include, url
from trade import views
urlpatterns = [
    url(r'^queryTrade$', views.queryTrade, name='queryTrade'),
    url(r'^getNameByStockId$', views.getNameByStockId, name='getNameByStockId'),

    # for teacher
    url(r'^tradeManage$', views.tradeManage, name='tradeManage'),
    url(r'^addTrade$', views.addTrade, name='addTrade'),
    url(r'^handleTrade$', views.handleTrade, name='handleTrade'),

    # for bursar
    url(r'^payManage$', views.payManage, name='payManage'),
    url(r'^payTrade$', views.payTrade, name='payTrade'),

]
