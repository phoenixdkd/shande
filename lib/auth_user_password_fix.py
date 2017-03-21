from django.contrib.auth.models import User
from teacher.models import *

teachers = Teacher.objects.all()
nums = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15']
for num in nums:
        for teacher in teachers:
            #1组4部
            if teacher.teacherId == 'Z0104'+num:
                teacher.binduser.set_password('u000000')
                teacher.binduser.save()
                print(teacher.binduser.username)
            #3组3部
            if teacher.teacherId == 'Z0303'+num:
                teacher.binduser.set_password('u000000')
                teacher.binduser.save()
                print(teacher.binduser.username)
            #3组1部
            if teacher.teacherId == 'Z0301'+num:
                teacher.binduser.set_password('u000000')
                teacher.binduser.save()
                print(teacher.binduser.username)
            #2组2部
            if teacher.teacherId == 'Z0202'+num:
                teacher.binduser.set_password('u000000')
                teacher.binduser.save()
                print(teacher.binduser.username)