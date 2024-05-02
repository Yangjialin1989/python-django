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

# 一、部门管理


def depart_list(request):
    """部门列表"""
    # 去数据库中获取所有部门的列表
    # queryset类型,传递给前端页面,前端直接用queryset变量
    queryset = models.Department.objects.all()
    # print(queryset)
    page_obj = Pagination(request, queryset)

    context = {
        'queryset': page_obj.page_queryset,
        'page_string': page_obj.html()
    }


    return render(request,'depart_list.html',context)

def depart_add(request):
    # 判断，get形式，则是网页跳转
    if request.method == 'GET':
        return render(request,'depart_add.html')
    # 判断，post形式，则是后台交互
    title = request.POST.get('title')
    #print(title)
    # 存储到数据库
    # modes.Department.objects.create(title=title)
    models.Department.objects.create(title=title)
    # 重定向回到部门列表
    return redirect('/depart/list')

def depart_delete(request):
    """删除部门"""
    #1.获取id
    nid = request.GET.get('nid')
    #2.删除对应的数据
    models.Department.objects.filter(id=nid).delete()
    #3.重定向
    return redirect('/depart/list')

def depart_edit(request,nid):
    """修改部门"""
    if request.method == 'GET':
        row_object = models.Department.objects.filter(id=nid).first()

        return render(request,'depart_edit.html',{'row_object':row_object})
    #POST存储数据
    title = request.POST.get('title')
    models.Department.objects.filter(id=nid).update(title=title)
    # 跳转
    return redirect('/depart/list')
