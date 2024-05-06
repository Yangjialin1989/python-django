import random,json
from django.shortcuts import render, redirect,HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django import forms

from app import models
from django.utils.safestring import mark_safe # 标记join()方法的字符串合法
# 导入分页类
from app.utils.pagination import Pagination
# 导入表单类
from app.utils.form import TaskModelForm,AdminResetModelForm,EditAdminModelForm,AdminModelForm,DepartmentModelForm,EditMobelForm,MobelForm,UserModelForm
from django.views.decorators.csrf import csrf_exempt

def task_list(request):
    queryset = models.Task.objects.all().order_by('-id')
    page_object = Pagination(request,queryset)
    if request.method == 'POST':

        data_dict = {'status': True, 'data': [12, 15, 1451]}
    # json_string = json.dumps(data_dict)
    # return HttpResponse(json_string)
    else:

        form = TaskModelForm()
        context = {
            'form':form,
            'queryset':queryset,
            'page_string':page_object.html()
        }

        return render(request, 'task_list.html', context)


# 不需要csrf
@csrf_exempt
def task_ajax(request):
    if request.method == 'POST':

        data_dict = {'status':True,'data':[12,15,1451]}
    # json_string = json.dumps(data_dict)
    # return HttpResponse(json_string)
    else:
        form = TaskModelForm()

        return render(request,'task_list1.html',{'form':form})
@csrf_exempt
def task_add(request):
    print(request.POST)
    form = TaskModelForm(data=request.POST)
    # 验证成功
    if form.is_valid():
        form.save()
        data_dict = {'status': True}
        return JsonResponse(data_dict)




    # 验证失败
    #print(form.errors)
    from django.forms.utils import ErrorDict
    #print(form.errors.get_json_data())
    data_dict = {'status':False,'error':form.errors.get_json_data()}
    #return HttpResponse(json.dumps(data_dict,ensure_ascii=False))
    #data = 'error'
    #return HttpResponse(data)
    return JsonResponse(data_dict)












