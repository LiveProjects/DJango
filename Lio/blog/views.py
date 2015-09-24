from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def show(req):
    return HttpResponse('<html>123</html>')

def index(req):
    return HttpResponse('<html>234</html>')

def indexnum(req, num):
    return HttpResponse('<html>345</html>')







