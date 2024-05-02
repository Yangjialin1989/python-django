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


def user_list(request):
    search_data = request.GET.get('q', '')  # 有值取q值，没有q=‘’
    data_dict = {}
    if search_data:
        data_dict['name__contains'] = search_data

    # select * from 表  order by llevel desc;
    # 导入utils.pagination工具类
    queryset = models.UserInfo.objects.filter(**data_dict)

    page_obj = Pagination(request,queryset)

    context = {
        'queryset':page_obj.page_queryset,
        'page_string':page_obj.html()
    }

    # 部门元组，通过数字找到对应的文字
    for obj in queryset:
        print(obj.get_gender_display())# 语法obj.get_字段_display()
                                       # 取到对应的文字。

    return render(request,'user_list.html',context)

def user_add(request):

    # 页面默认get请求跳转，
    if request.method == 'GET':
        form = UserModelForm()
        return render(request,'user_add.html',{'form':form})

    # 其他情况post，提交表单数据
    # 效验
    # 不允许为空
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # 校验成功获取的数据 form.cleaned_data;
        #print(form.cleaned_data)
        # {'name': 'ya', 'password': '45682', 'age': 44,
        #  'create_time': datetime.datetime(1989, 11, 30, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')), 'gender': 2,
        #  'depart': < Department: 售后部 >}
        # form.save()自动保持
        form.save()

        return redirect('/user/list')
    else:
        # 错误的信息 form.errors
        #print(form.errors)
        return render(request,'user_add.html',{'form':form})

# 编辑用户
def user_edit(request,nid):

    # 获取数据
    data = models.UserInfo.objects.filter(id=nid).first()

    # 页面跳转
    if request.method == 'GET':
        form = UserModelForm(instance=data)
        return render(request,'user_edit.html',{'form':form})

    # 数据编辑，用户提交的 数据，更新
    form = UserModelForm(data=request.POST,instance=data)
    if form.is_valid():
        form.save()
        return redirect('/user/list')

# 删除
def user_delete(request):
    """删除部门"""
    #1.获取id
    nid = request.GET.get('nid')
    #2.删除对应的数据
    models.UserInfo.objects.filter(id=nid).delete()
    #3.重定向
    return redirect('/user/list')
