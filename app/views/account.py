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
from app.utils.code import check_code
from app.utils.countdown import CountdownTimer
from io import BytesIO

def login(request):

    # 检查用户是否已经登录，已经登录继续，未登录跳转回登录页面
    # 1.用户发来请求，获取cookie随机字符串，与浏览器的session中有没有
    info = request.session.get('info')
    print('info',info)
    # if not info:
    #     print(info)
    #     return redirect('/account/login')
    # if info:
    #     return redirect('/user/list')

    if request.method == 'GET':
        form = LoginForm()
        return render(request,'login.html',{'form':form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 0.验证码校验
        user_input_code = form.cleaned_data.pop('code')

        code = request.session.get('image_code','')
        if code.upper() != user_input_code.upper():
            form.add_error('code', '验证码错误！')
            flag = 'none'
            return render(request, 'login.html', {'form': form,'error':flag})

        # 1.用户输入正确验证成功获取用户名密码 form.cleaned_data,form模型定义钩子
        # 2.去数据库校验用户名和密码
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error('password','用户名或密码错误！')
            return render(request,'login.html', {'form':form})
        # 3.验证通过，网站生成随机字符串；写到用户浏览器的cookie中，写到session中

        request.session['info']= {'id':admin_object.id,'username':admin_object.username}
        # 签名修改时间,七天免登录
        request.session.set_expiry(60*60*24*7)

        # 4.请求相应终止后，重定向
        return redirect('/admin/list')
    return render(request,'login.html', {'form':form})

def logout(request):
    request.session.clear()
    return redirect('/account/login')

def image_code(request):
    # 调用pillow，生成图片
    img,code_string = check_code()
    #存储到浏览器session中
    request.session['image_code']=code_string
    #设置六十秒超时
    request.session.set_expiry(60)

    # 生成的验证码图片保存的电脑存储中
    stream = BytesIO()
    img.save(stream,'png')
    stream.getvalue()
    # 图片渲染到前端
    return HttpResponse(stream.getvalue())

