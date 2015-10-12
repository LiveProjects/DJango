#!/usr/bin/python
#coding:utf-8

import os
import json
import time,datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response

from crawl_data.djangosite.resys.models.profile import ShowProfile
from crawl_data.djangosite.resys.models.profile import Tag
# Create your views here.；

# def showBlogList(request):
#     t = loader.get_template('blog_list.html')
#     blogs = Blog.objects.all()
#     context = {'blog':blogs}
#     html = t.render(context)
#     return HttpResponse(html)
#
# dicts = {}
def fen_lei(list, pid=0):
    res=ShowProfile.objects.filter(parent_id=pid, version=0)
    arr=[]
    if len(res)>0:
        for x in res:
            data = {}
            data['zh_name'] = x.zh_name
            data['en_name'] = x.en_name
            data['profile_type'] = x.profile_type
            arr.append(data)
            fen_lei(arr, x.id)

        list.append(arr)
    return list

def showProfile(request):
    connect = []
    which=[]
    context=dict(
        tab_list = ['内容主题','文章质量','地理位置','其他'],
        search = Tag.objects.all(),
        search_show_profile = ShowProfile.objects.all().filter(version=0),
    )
    #exchange Tag
    def exchange(req):
        maxnum=1
        for x in context['search']:
            length = len(x.path.split('/'))
            if maxnum < length:
                maxnum = length
        for x in context['search']:
            #which.append(x.path)
            if len(x.path.split('/'))==1:
                ShowProfile.objects.create(zh_name=x.cn_name,
                                           en_name=x.en_name,
                                           parent_id=0,
                                           definition='',
                                           regulation='',
                                           product_use=00000,
                                           achieve_method=x.source,
                                           output_method=0000,
                                           version=0,
                                           profile_type=0,)
        startx=0
        while startx <= maxnum+4:
            for x in context['search']:
                if len(x.path.split('/'))==startx+2:
                    parent_name = x.path.split('/')[startx].strip()
                    try:
                        parent_id = ShowProfile.objects.get(en_name=parent_name, version=0).id
                        ShowProfile.objects.create( zh_name=x.cn_name,
                                                    en_name=x.en_name,
                                                    parent_id=parent_id,
                                                    definition='',
                                                    regulation='',
                                                    product_use=00000,
                                                    achieve_method=x.source,
                                                    output_method=0000,
                                                    version=0,
                                                    profile_type=0,)
                    except:
                        #ll =  err.message
                        which.append(x.path)

                    # parent_id = ShowProfile.objects.get(en_name=parent_name, version=0).id
                    #
                    # ShowProfile.objects.create( zh_name=x.cn_name,
                    #                             en_name=x.en_name,
                    #                             parent_id=parent_id,
                    #                             definition='',
                    #                             regulation='',
                    #                             product_use=00000,
                    #                             achieve_method=x.source,
                    #                             output_method=0000,
                    #                             version=0,)

            startx=startx+1
    #exchange(1)

    #概念实体词
    def read_concept(req):
        f = open('djangosite/resys/models/concept.Feature.Data.txt', 'r+')
        # arr = {}
        # arr['object']=f.readlines()
        arr = f.readlines()
        for x in arr:
            #return HttpResponse(len(json.loads(x)['TAG']))
            array = []
            try:
                for y in json.loads(x)['TAG']:
                    zh_name = y
                    #return HttpResponse(zh_name)
                    parent_id = ShowProfile.objects.get(zh_name=zh_name, version=0).id

                    ShowProfile.objects.create( zh_name=json.loads(x)['TITLE'],
                                                en_name=json.loads(x)['ID'],
                                                parent_id=parent_id,
                                                definition='',
                                                regulation='',
                                                product_use=00000,
                                                achieve_method=0000,
                                                output_method=0000,
                                                version=0,
                                                profile_type=1,)
            except:
                zh_name = "无"
                array.append(zh_name)
        f.close()
        return HttpResponse(array)
    #read_concept(1)

    list=[]
    #lists = fen_lei(list)

    # def fist_grade(list):
    #     for x in context['search_show_profile']:
    #         if x.parent_id==0:
    #             list.append(x)
    # fist_grade(list)


    # 生成二维list
    # def make_dict(dicts, pid=0):
    #     res = ShowProfile.objects.filter(parent_id=pid, version=0)
    #     if pid==0:
    #         chinese_name = "first_grade"
    #     elif pid!=0:
    #         chinese_name= ShowProfile.objects.get(id=pid, version=0).en_name
    #     arr=[]
    #     for x in res:
    #         arr.append(x)
    #         #temporary
    #         dicts[chinese_name] = arr
    #         make_dict(dicts, x.id)
    #
    #     return dicts
    # make_dict(dicts)

    response = render_to_response('profile/profile.html', {
        'tab_list':context['tab_list'],'which':which,
    })
    return response

#异步获取树叶子
def ajax_fun(request):
    dictval = {}
    if request.is_ajax():
        #dictval['value']=request.REQUEST.get('value','default')
        data=request.REQUEST.get('value','default')
        if dicts[data]:
            dictval['list'] = []
            dd= {}
            for x in dicts[data]:
                dd[x.zh_name]=x.en_name
            dictval['list'].append(dd)
            jsons=json.dumps(dictval)
        return HttpResponse(jsons)


#profile_detail page
def show_profile_detail(req, item):
    tab_list = ['内容主题','文章质量','地理位置','其他']
    res= ShowProfile.objects.filter(en_name=item, version=0)[0]
    history_res = ShowProfile.objects.filter(en_name=item, version=1).order_by("modify_time")
    if res.parent_id!=0:
        try:
            parent_res_id = res.parent_id
            parent_res = ShowProfile.objects.get(id=parent_res_id)
            common_name = parent_res.en_name
            parent_res_new = ShowProfile.objects.get(en_name=common_name, version=0)
        except:
            parent_res_new = ShowProfile.objects.filter(en_name=common_name, version=0).order_by("-modify_time")[0]
    else:
        parent_res_new = ''
    try:
        # sons = dicts[item]
        sones = ShowProfile.objects.filter(parent_id=res.id, version=0)
        sons=[]
        for x in sones:
            sons.append(x)
    except:
        sons = [123]
    response = render_to_response('profile/profile_detail.html', {'tab_list':tab_list,'item':res,'parent_res':parent_res_new,'sons': sons,'history_res': history_res})
    return response

#定义修改
def profile_detail_changedefine(request, item):
    if request.is_ajax():
        data=request.REQUEST.get('value','default')
        try:
            history = ShowProfile.objects.get(en_name=item,version=0)
            ShowProfile.objects.filter(en_name=item,version=0).update(version=1)

            ShowProfile.objects.create( zh_name=history.zh_name,
                                        en_name=history.en_name,
                                        parent_id=history.parent_id,
                                        definition=data,
                                        regulation=history.regulation,
                                        product_use=history.product_use,
                                        achieve_method=history.achieve_method,
                                        output_method=history.output_method,
                                        version=0,)
            return HttpResponse(1)
        except:
            return HttpResponse(0)

#规则修改
def profile_detail_changeregular(request, item):
    if request.is_ajax():
        data=request.REQUEST.get('value','default')
        try:
            history = ShowProfile.objects.get(en_name=item,version=0)
            ShowProfile.objects.filter(en_name=item,version=0).update(version=1)
            ShowProfile.objects.create( zh_name=history.zh_name,
                                        en_name=history.en_name,
                                        parent_id=history.parent_id,
                                        definition=history.definition,
                                        regulation=data,
                                        product_use=history.product_use,
                                        achieve_method=history.achieve_method,
                                        output_method=history.output_method,
                                        version=0,)
            return HttpResponse(1)
        except:
            return HttpResponse(0)


#添加新词,没有历史记录
def add_new(request):
    if request.is_ajax():
        data=request.REQUEST.get('value','default')
        jsons=json.loads(data)
        try:
            parent = ShowProfile.objects.get(zh_name=jsons['parent_name'],version=0)
        except:
            return HttpResponse(0)
        en_names=parent.en_name
        try:
            ShowProfile.objects.create( zh_name=jsons['zh_name'],
                                        en_name=jsons['en_name'],
                                        parent_id=parent.id,
                                        definition=jsons['defination'],
                                        regulation=jsons['regulation'],
                                        product_use='%05d' % jsons['product_use'],
                                        achieve_method=0000,
                                        output_method=0000,
                                        version=0,)
            return HttpResponse(en_names)
        except:
            return HttpResponse(0)

#修改父级
def profile_detail_fixparent(request, item):
    if request.is_ajax():
        data=request.REQUEST.get('value','default')
        try:
            newparent_id = ShowProfile.objects.get(zh_name=data, version=0).id
            newparnet_name = ShowProfile.objects.get(zh_name=data, version=0).en_name
            history = ShowProfile.objects.get(en_name=item, version=0)
            ShowProfile.objects.filter(en_name=item, version=0).update(version=1)
            ShowProfile.objects.create( zh_name=history.zh_name,
                                        en_name=history.en_name,
                                        parent_id=newparent_id,
                                        definition=history.definition,
                                        regulation=history.regulation,
                                        product_use=history.product_use,
                                        achieve_method=history.achieve_method,
                                        output_method=history.output_method,
                                        version=0,)
            return HttpResponse(newparnet_name)
        except:
            return HttpResponse(0)


#撤回历史记录
def drawback_history(request, item):
    if request.is_ajax():
        data = request.REQUEST.get('value', 'default')
        try:
            ShowProfile.objects.filter(en_name=item, version=0).update(version=1)
            ShowProfile.objects.filter(en_name=item, modify_time= data).update(version=0)
            return HttpResponse(1)
        except:
            return HttpResponse(0)


#加载实现数据异步传输
def profile_ajax(request):
    if request.is_ajax():
        data = request.REQUEST.get('value','default')
        list= []
        val = fen_lei(list, pid=0)
        val = json.dumps(val)
        return HttpResponse(val)



