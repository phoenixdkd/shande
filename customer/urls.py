
from django.conf.urls import include, url
from customer import views
urlpatterns = [
    #for sale
    url(r'^customerManage$', views.customerManage, name='customerManage'),
    url(r'^queryCustomer$', views.queryCustomer, name='queryCustomer'),
    url(r'^addCustomer$', views.addCustomer, name='addCustomer'),
    url(r'^delCustomer$', views.delCustomer, name='delCustomer'),
    url(r'^delCustomerBySale$', views.delCustomerBySale, name='delCustomerBySale'),
    url(r'^checkCustomerPhone$', views.checkCustomerPhone, name='checkCustomerPhone'),
    url(r'^checkCustomerPhoneForEdit$', views.checkCustomerPhoneForEdit, name='checkCustomerPhoneForEdit'),

    #for teacher
    url(r'^customerHandle$', views.customerHandle, name='customerHandle'),
    url(r'^queryCustomerHandle$', views.queryCustomerHandle, name='queryCustomerHandle'),
    url(r'^handleCustomer$', views.handleCustomer, name='handleCustomer'),
    url(r'^handleValidCustomer$', views.handleValidCustomer, name='handleValidCustomer'),
    url(r'^handleValidCustomer$', views.handleValidCustomer, name='handleValidCustomer'),
    url(r'^editSpot$', views.editSpot, name='editSpot'),
    url(r'^handleSpotCustomer$', views.handleSpotCustomer, name='handleSpotCustomer'),

    #for bursar
    url(r'^customerPay$', views.customerPay, name='customerPay'),
    url(r'^queryCustomerPay$', views.queryCustomerPay, name='queryCustomerPay'),
    url(r'^tradePayManage$', views.tradePayManage, name='tradePayManage'),
    url(r'^queryTradePayManage$', views.queryTradePayManage, name='queryTradePayManage'),

    #for trade
    url(r'^getCustomerById$', views.getCustomerById, name='getCustomerById'),
    url(r'^getSpotCustomerById$', views.getSpotCustomerById, name='getSpotCustomerById'),

    #for report
    url(r'^noTradeCustomerReport$', views.noTradeCustomerReport, name='noTradeCustomerReport'),
    url(r'^tradeTypeReport$', views.tradeTypeReport, name='tradeTypeReport'),
    url(r'^getTeacherDetail$', views.getTeacherDetail, name='getTeacherDetail'),
    url(r'^getStockDetail$', views.getStockDetail, name='getStockDetail'),
    url(r'^dCustomerReport$', views.dCustomerReport, name='dCustomerReport'),
    url(r'^analyzeReport$', views.analyzeReport, name='analyzeReport'),
    url(r'^getStockDetailForAnalyze$', views.getStockDetailForAnalyze, name='getStockDetailForAnalyze'),
    url(r'^calcProfitByStockId$', views.calcProfitByStockId, name='calcProfitByStockId'),
    url(r'^resumeDishonestCustomer$', views.resumeDishonestCustomer, name='resumeDishonestCustomer'),



]
