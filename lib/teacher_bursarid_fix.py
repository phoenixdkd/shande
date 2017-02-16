from teacher.models import *
from customer.models import *
teachers = Teacher.objects.all()
for teacher in teachers:
   customers = Customer.objects.filter(teacher=teacher.id)
   for customer in customers:
       customer.bursar = teacher.bindbursar
       customer.save()