"""
URL configuration for pydjango1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import depart,user,mobel,admin,account,task




urlpatterns = [
    #部门管理
    path('depart/list',depart.depart_list),
    path('depart/add',depart.depart_add),
    path('depart/delete',depart.depart_delete),
    path('depart/<int:nid>/edit',depart.depart_edit),

    # 用户管理
    path('user/list',user.user_list),
    path('user/add',user.user_add),
    path('user/<int:nid>/edit',user.user_edit),
    path('user/delete',user.user_delete),

    # 靓号管理
    path('mobel/list',mobel.mobel_list),
    path('mobel/add',mobel.mobel_add),
    path('mobel/<int:nid>/edit',mobel.mobel_edit),
    path('mobel/delete',mobel.mobel_delete),

    # 管理员管理
    path('admin/list',admin.admin_list),
    path('admin/add',admin.admin_add),
    path('admin/<int:nid>/edit',admin.admin_edit),
    path('admin/delete',admin.admin_delete),
    path('admin/<int:nid>/reset',admin.admin_reset),

    # 登录
    path('account/login',account.login),
    path('account/logout',account.logout),
    path('image/code',account.image_code),

    # 任务
    path('task/list',task.task_list),
    path('task/ajax/',task.task_ajax),
    path('task/add/',task.task_add),

]
