# coding=utf-8
from customer.models import *
from sale.models import *
customers = Customer.objects.all()
for customer in customers:
    if customer.sales:
        customer.developcompany = customer.sales.company
        customer.save()