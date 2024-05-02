import random
from django.shortcuts import render, redirect,HttpResponse
from django.shortcuts import render
from django import forms

from app import models
from django.utils.safestring import mark_safe # 标记join()方法的字符串合法
# 导入分页类
from app.utils.pagination import Pagination
# 导入表单类
from app.utils.form import DepartmentModelForm,EditMobelForm,MobelForm,UserModelForm


# 二、用户管理
# ModelForm 与bootstrap 优化


# 靓号管理




def mobel_list(request):
    # 生成数据
    # for i in range(3000):
    #     mnum = random.randint(13000000000, 19999999999)
    #     pnum = random.randint(10,1000)
    #     lnum = random.randint(1,4)
    #     snum = random.randint(1,2)
    #
    #     models.Mobel.objects.create(mobel=mnum,price=pnum,level=lnum,status=snum)


    # 搜索靓号
    global start_page
    data_dict = {}


    search_data = request.GET.get('q','')# 有值取q值，没有q=‘’

    if search_data:

        data_dict['mobel__contains'] = search_data

    # select * from 表  order by llevel desc;
        # 导入utils.pagination工具类
    queryset = models.Mobel.objects.filter(**data_dict).order_by("-level")
    page_object = Pagination(request,queryset)
    page_queryset = page_object.page_queryset
    page_string = page_object.html()
    total_count = page_object.total_count
    context = {
        'queryset': page_queryset, # 分完页的数据
        'search_data': search_data,# 输入历史
        'page_string': page_string, # 页码
        'total_count':total_count
    }

    return render(request, 'mobel_list.html',context )


def mobel_add(request):
    if request.method == "GET":
        form = MobelForm()
        return render(request,'mobel_add.html',{"form":form})
    form = MobelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/mobel/list")
    return render(request,'mobel_add.html',{"form":form})

def mobel_edit(request,nid):

    # 获取数据
    data = models.Mobel.objects.filter(id=nid).first()

    # 页面跳转
    if request.method == 'GET':
        form = EditMobelForm(instance=data)
        return render(request,'mobel_edit.html',{'form':form})

    # 数据编辑，用户提交的 数据，更新
    form = EditMobelForm(data=request.POST,instance=data)
    if form.is_valid():
        form.save()
        return redirect('/mobel/list')

    return render(request,'mobel_edit.html',{"form":form})

def mobel_delete(request):
    """删除部门"""
    #1.获取id
    nid = request.GET.get('nid')
    #2.删除对应的数据
    models.Mobel.objects.filter(id=nid).delete()
    #3.重定向
    return redirect('/mobel/list')

