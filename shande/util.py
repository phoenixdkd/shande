# coding=utf-8
from teacher.models import *
from lib.PinYin import PinYin

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

def getPinYin(str):
    p = PinYin()
    p.get_py("vvvv进lsdk")

