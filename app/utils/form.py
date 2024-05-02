from app import models
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from app.utils.bootstrap import BootStrapModelForm
class UserModelForm(BootStrapModelForm):
    # 自定义错误信息
    name = forms.CharField(min_length=3,label='用户名')
    password = forms.CharField(min_length=6,label='密码')
    class Meta:
        model = models.UserInfo
        fields = ['name','password','age','create_time','gender','depart']
        # css 重新定义init方法。
        # widgets = {
        #     'create_time':forms.DateInput(attrs=={'type':'date'})
        # }

    # def __init__(self,*args,**kwargs):
    #     # 执行父类的init方法
    #     super().__init__(*args,**kwargs)
    #     for name,field in self.fields.items():
    #          #print(name,field)
    #         # if name == 'create_time':
    #         #    #field.widget.attrs = {'class':'from-control'}
    #         #    field.widget = forms.DateInput(attrs={'tpye':'date','class':'form-control'})
    #         #     #print(field)
    #         #    continue
    #         field.widget.attrs = {'class':'form-control'}

class MobelForm(BootStrapModelForm):
    # 效验方法一、
    # mobel = forms.CharField(
    #     label='手机号',
    #     validators=[RegexValidator(r'^[0-9]+$', '请输入数字'), RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')],
    # )



    class Meta:
        model = models.Mobel
        # fields = "__all__"  所有字段
        # exclude = ["level"] 除了level，其他所有字段
        fields = "__all__"

    # 效验方法二   勾子方法
    def clean_mobel(self):
        # 获取当前的id
        #self.instance.pk

        txt_mobel = self.cleaned_data['mobel']

        exists = models.Mobel.objects.filter(mobel=txt_mobel).exists()
        if exists:
            raise ValidationError('手机号已经存在！')


        if len(txt_mobel) != 11:
            raise ValidationError("格式错误")

        return txt_mobel

class EditMobelForm(BootStrapModelForm):
    # mobel = forms.CharField(disabled=True,label='手机号')
    mobel = forms.CharField(
        label='手机号',
        validators=[RegexValidator(r'^1[3-9]\d{9}$','手机号格式错误！')]
    )

    class Meta:
        model = models.Mobel
        # fields = "__all__"  所有字段
        # exclude = ["level"] 除了level，其他所有字段
        fields = ['mobel','price','level','status']


        # 效验方法二   勾子方法
    def clean_mobel(self):
            # 获取当前的id
           # self.instance.pk

        txt_mobel = self.cleaned_data['mobel']

        exists = models.Mobel.objects.exclude(id=self.instance.pk).filter(mobel=txt_mobel).exists()
        if exists:
            raise ValidationError('手机号已经存在！')



        return txt_mobel
