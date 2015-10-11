# -*- coding: UTF-8 -*-
import json
from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader,Context

# Create your views here.

def show(req):
    return HttpResponse('<html>123</html>')

def index(req):
    t = loader.get_template('blog/index.html')
    
    tab_list = ['内容主题','文章质量','地理位置','其他']
    c = Context({'tab_list':tab_list})
    return HttpResponse(t.render(c)) 

def indexnum(req, num):
    return HttpResponse('<html>345</html>')

def aajax(request):
    if request.is_ajax() and request.method == 'POST':
        dict = {}
        for key in request.POST:
            dict['key'] = key
            json=simplejson.dumps(dict)
        return HttpResponse(json)

def ajax(request):
    dict = {}
    if request.is_ajax():
        dict['name']='lio'
        dict['name']=request.REQUEST.get('name','default')
      
        jsons=json.dumps(dict)
        return HttpResponse(jsons) 
        









