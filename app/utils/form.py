from app import models
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from app.utils.bootstrap import BootStrapModelForm,BootStrapForm
from app.utils.encrypt import md5

# 登录Form
class LoginForm(BootStrapForm):
    # 新建字段
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(render_value=True),
        required=True
    )
    def clean_password(self):
        password = self.cleaned_data.get('password')
        return md5(password)



# 登录ModelForm
class LoginModelForm(forms.ModelForm):
    # 导入字段,去orm中获取
    class Meta:
        model = models.Admin
        fields = ['username','password']


class AdminResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True)
    )
    class Meta:
        model = models.Admin
        fields = ['password','confirm_password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        md5_password = md5(password)
        # 去数据库效验当前密码和新密码是否一致
        # self.instance.pk 可以拿到当前id
        exists = models.Admin.objects.filter(id=self.instance.pk,password=md5_password).exists()
        if exists:
            raise ValidationError('密码不能与上次的密码一致！')



        return md5_password
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = md5(self.cleaned_data.get('confirm_password'))
        if confirm_password != password:
            raise ValidationError('密码不一致！')

        # 写入form.cleaned_data.confirm_password
        return confirm_password




class AdminModelForm(BootStrapModelForm):
    # 额外输入框,数据库中没有的
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True)# 报错后也会保留原来的值。
    )


    class Meta:
        model = models.Admin
        fields = ['username','password','confirm_password']
        widgets = {#render_value=True,
            'password':forms.PasswordInput(attrs={"aria-describedby":"basic-addon2"})
        }

    #
    def clean_password(self):
        password = self.cleaned_data.get('password')

        return md5(password)


    # 钩子
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = md5(self.cleaned_data.get('confirm_password'))
        if confirm_password != password:
            raise ValidationError('密码不一致！')

        # 写入form.cleaned_data.confirm_password
        return confirm_password

    def clean_username(self):
        # 获取当前的id
        # self.instance.pk

        txt_username = self.cleaned_data['username']

        exists = models.Admin.objects.filter(username=txt_username).exists()
        if exists:
            raise ValidationError('用户名已经存在！')

        return txt_username


class EditAdminModelForm(BootStrapModelForm):
    # 额外输入框,数据库中没有的
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True)  # 报错后也会保留原来的值。
    )

    class Meta:
        model = models.Admin
        fields = ['username', 'password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True)
        }

    #
    def clean_password(self):
        password = self.cleaned_data.get('password')
        md5_password = md5(password)
        # 数据库校验当前密码和新输入的密码是否一致


        return md5_password
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = md5(self.cleaned_data.get('confirm_password'))
        if confirm_password != password:
            raise ValidationError('密码不一致！')

        # 写入form.cleaned_data.confirm_password
        return confirm_password

    def clean_username(self):
            # 获取当前的id
           # self.instance.pk

        txt_username = self.cleaned_data['username']

        exists = models.Mobel.objects.exclude(id=self.instance.pk).filter(mobel=txt_username).exists()
        if exists:
            raise ValidationError('用户名已经存在！')



        return txt_username

class DepartmentModelForm(BootStrapModelForm):
    class Meta:
        model = models.Department
        fields = ['id','title']
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
