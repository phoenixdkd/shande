# coding=utf-8
from customer.models import *
from sale.models import *
customers = Customer.objects.all()
for customer in customers:
    if customer.sales:
        customer.developcompany = customer.sales.company
        customer.save()


# coding=utf-8
from auth_user import *

bs = User.objects.all()
for a in bs:
    if a.username == 'admin':
        a.save
    else:
        a.delete()