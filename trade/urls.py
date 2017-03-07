
from django.conf.urls import include, url
from trade import views
urlpatterns = [
    url(r'^queryTrade$', views.queryTrade, name='queryTrade'),
    url(r'^getNameByStockId$', views.getNameByStockId, name='getNameByStockId'),

    # for teacher
    url(r'^tradeManage$', views.tradeManage, name='tradeManage'),
    url(r'^addTrade$', views.addTrade, name='addTrade'),
    url(r'^handleTrade$', views.handleTrade, name='handleTrade'),
    url(r'^deleteTrade$', views.deleteTrade, name='deleteTrade'),
    url(r'^updateFile$', views.updateFile, name='updateFile'),
    url(r'^showFile$', views.showFile, name='showFile'),

    # for bursar
    url(r'^payManage$', views.payManage, name='payManage'),
    url(r'^payTrade$', views.payTrade, name='payTrade'),
    url(r'^backTrade$', views.backTrade, name='backTrade'),
    url(r'^backTradeAdmin$', views.backTradeAdmin, name='backTradeAdmin'),
]
