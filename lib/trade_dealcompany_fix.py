# coding=utf-8
from trade.models import *
from sale.models import *
trades = Trade.objects.all()
for trade in trades:
    if trade.customer.sales:
        trade.dealcompany = trade.customer.sales.company
        trade.save()