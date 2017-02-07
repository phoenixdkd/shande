# coding=utf-8
from customer.models import *
customers = Customer.objects.all()
for customer in customers:
    if customer.first_trade:
        trades = customer.trade_set
        trade = trades.latest('create')
        if trade:
            customer.latest = trade.create
            customer.save()

