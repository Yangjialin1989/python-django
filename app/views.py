import random
from django.shortcuts import render, redirect,HttpResponse
from django.shortcuts import render
from django import forms

from app import models
from django.utils.safestring import mark_safe # 标记join()方法的字符串合法
# 导入分页类
from app.utils.pagination import Pagination
# 导入表单类
from app.utils.form import EditMobelForm,MobelForm,BootStrapModelForm,UserModelForm

# 一、部门管理
class DepartmentModelForm(forms.ModelForm):
    class Meta:
        model = models.Department
        fields = ['id','title']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control'}
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






# 二、用户管理
# ModelForm 与bootstrap 优化
class User1ModelForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        fields = ['name','password','age','create_time','gender','depart']
    def __init__(self,*args,**kwargs):
        # 执行父类的init方法
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():

            if field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field.label
            else:
                field.widget.attrs = {
                    'class':'form-control',
                    'placeholder':field.label
                }



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

# def user_add(request):
#     # 添加用户
#     if request.method == 'GET':
#         context = {
#             'gender_choices':models.UserInfo.gender_choices,
#             'depart_list':models.Department.objects.all()
#         }
#         return render(request,'user_add.html',context)
#
#     # 获取用户提交的数据
#     name = request.POST.get('name')
#     password = request.POST.get('password')
#     age = request.POST.get('age')
#     create_time = request.POST.get('create_time')
#     gender = request.POST.get('gender')
#     depart_id = request.POST.get('depart_id')
#
#     # 存储到数据库
#     # modes.Department.objects.create(title=title)
#     models.UserInfo.objects.create(name=name,password=password,age=age,create_time=create_time,gender=gender,depart_id=depart_id)
#     # 重定向回到部门列表
#     return redirect('/user/list')
# 表




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


