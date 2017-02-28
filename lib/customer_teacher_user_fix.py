# coding=utf-8
from customer.models import *
from teacher.models import *
customers = Customer.objects.all()
for customer in customers:
    if customer.teacher:
        if customer.teacher.binduser:
            customer.teacheruser = customer.teacher.binduser.id
            customer.save()