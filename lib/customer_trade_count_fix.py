# coding=utf-8
from trade.models import *
from customer.models import *
trades = Trade.objects.all()
customers = Customer.objects.all()


for customer in customers:
    customer.tradecount = trades.filter(customer_id=customer.id).count()
    customer.save()