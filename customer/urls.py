
from django.conf.urls import include, url
from customer import views
urlpatterns = [
    #for sale
    url(r'^customerManage$', views.customerManage, name='customerManage'),
    url(r'^queryCustomer$', views.queryCustomer, name='queryCustomer'),
    url(r'^addCustomer$', views.addCustomer, name='addCustomer'),
    url(r'^delCustomer$', views.delCustomer, name='delCustomer'),

    #for teacher
    url(r'^customerHandle$', views.customerHandle, name='customerHandle'),
    url(r'^queryCustomerHandle$', views.queryCustomerHandle, name='queryCustomerHandle'),
    url(r'^handleCustomer$', views.handleCustomer, name='handleCustomer'),
    url(r'^handleValidCustomer$', views.handleValidCustomer, name='handleValidCustomer'),
    url(r'^handleValidCustomer$', views.handleValidCustomer, name='handleValidCustomer'),

    #for bursar
    url(r'^customerPay$', views.customerPay, name='customerPay'),
    url(r'^queryCustomerPay$', views.queryCustomerPay, name='queryCustomerPay'),

    #for trade
    url(r'^getCustomerById$', views.getCustomerById, name='getCustomerById'),


]
