# coding=utf-8
from teacher.models import *

def getArgsExcludePage(request):
    requestArgs = ""
    for arg in request.GET:
        if arg == 'page':
            continue
        if requestArgs == "":
            requestArgs = requestArgs + arg + "=" + request.GET[arg]
        else:
            requestArgs = requestArgs + "&" + arg + "=" + request.GET[arg]
    return requestArgs

def getTeacherBySaleId(saleid):
    teacherId = saleid[1:3]
    teacher = Teacher.objects.get(teacherId=teacherId)
    return teacher