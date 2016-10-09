from django.test import TestCase
import re
# Create your tests here.
def substr():
    str = '0123456789'
    print(str[1:3])

def replaystr():
    str = 'A001'
    str = re.sub(r'^[^\d]+', 'CW', str)
    print("str:"+str)

replaystr()