import random
from django.shortcuts import render, redirect,HttpResponse
from django.shortcuts import render
from django import forms

from app import models
from django.utils.safestring import mark_safe # 标记join()方法的字符串合法
# 导入分页类
from app.utils.pagination import Pagination
# 导入表单类
from app.utils.form import AdminResetModelForm,EditAdminModelForm,AdminModelForm,DepartmentModelForm,EditMobelForm,MobelForm,UserModelForm

# 一、管理员管理
def admin_list(request):
    # 一、搜索功能
    data_dict = {}
    search_data = request.GET.get('q','')
    if search_data:
        data_dict['username__contains'] = search_data
    #
    queryset = models.Admin.objects.filter(**data_dict)

    # 二、分页功能
    page_obj = Pagination(request,queryset)
    page_string = page_obj.html()
    context = {
        'queryset':queryset,
        'page_string':page_string,
        'search_data':search_data
    }
    return render(request,'admin_list.html',context)

def admin_add(request):
    title = '新建管理员'
    # 页面默认get请求跳转，
    if request.method == 'GET':
        form = AdminModelForm()
        return render(request, 'change.html', {'form': form,'title':title})
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        # 数据保存到数据库
        form.save()
        return redirect('/admin/list')
    else:
        return render(request,'change.html',{'form':form,'title':title})


def admin_edit(request,nid):
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request,'error.html',{'msg':'数据不存在'})
    title = '编辑管理员'

    if request.method == 'GET':
        form = EditAdminModelForm(instance=row_object)# 表默认值
        return render(request, 'change.html', {'form':form,'title': title})

    form = EditAdminModelForm(data= request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list')
    return render(request,'change.html',{'form':form,'title':title})

def admin_delete(request):
    """删除部门"""
    #1.获取id
    nid = request.GET.get('nid')
    #2.删除对应的数据
    models.Admin.objects.filter(id=nid).delete()
    #3.重定向
    return redirect('/admin/list')

def admin_reset(request,nid):
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request, 'error.html', {'msg': '数据不存在'})
    title = '重置密码- {}'.format(row_object.username)

    if request.method == 'GET':
        form = AdminResetModelForm()
        context = {
            'form': form,
            'title': title
        }
        return render(request, 'change.html', context)

    form = AdminResetModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list')
    return render(request,'change.html',{'form':form,'title':title})







