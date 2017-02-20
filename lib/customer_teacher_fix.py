# coding=utf-8
from customer.models import  *

customers = Customer.objects.filter(sales__isnull=False, teacher__isnull=True)
for customer in customers:
    customer.teacher = customer.sales.bindteacher
    customer.save()

noBursarCustomers = Customer.objects.filter(teacher__isnull=False, bursar__isnull=True)
for customer in noBursarCustomers:
    customer.bursar = customer.teacher.bindbursar
    customer.save()

