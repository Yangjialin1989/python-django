import random
from django.shortcuts import render, redirect,HttpResponse
from django.shortcuts import render
from django import forms

from app import models
from django.utils.safestring import mark_safe # 标记join()方法的字符串合法
# 导入分页类
from app.utils.pagination import Pagination
# 导入表单类
from app.utils.form import LoginForm,AdminResetModelForm,EditAdminModelForm,AdminModelForm,DepartmentModelForm,EditMobelForm,MobelForm,UserModelForm

from django.shortcuts import render


def login(request):

    if request.method == 'GET':
        form = LoginForm()
        return render(request,'login.html',{'form':form})
    form = LoginForm(data=request.POST)
    if form.is_valid():

        # 1.用户输入正确验证成功获取用户名密码 form.cleaned_data,form模型定义钩子
        # 2.去数据库校验用户名和密码
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error('password','用户名或密码错误！')
            return render(request,'login.html', {'form':form})
        # 3.验证通过，网站生成随机字符串；写到用户浏览器的cookie中，写到session中
        request.session['info']= {'id':admin_object.id,'username':admin_object.username}
        # 4.请求相应终止后，重定向
        return redirect('/admin/list')
    return render(request,'login.html', {'form':form})





