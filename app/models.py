from datetime import datetime

from django.db import models

# Create your models here.
# 部门
class Department(models.Model):
    """部门表"""
    id = models.BigAutoField(verbose_name='id',primary_key=True)
    title = models.CharField(verbose_name='标题',max_length=32)
    # 前端渲染默认拿到对象，这样处理，可以获取对象中的title值
    def __str__(self):
        return self.title


# 员工
class UserInfo(models.Model):
    """员工表"""
    name = models.CharField(verbose_name='姓名',max_length=16)
    password = models.CharField(verbose_name='密码',max_length=64)
    age = models.IntegerField(verbose_name='年龄')
    account = models.DecimalField(verbose_name='账户余额',default=0,max_digits=10,decimal_places=2)
    # 无约束
    #create_time = models.DateTimeField(verbose_name='部门ID')
    # 有约束 to  与哪张表有关联， to_field   与对应表的哪一列有关联
    # depart 会默认生成depart_id (django内部自动做的）
    # 1.级联删除，如果没有部门id，删除用户
    depart = models.ForeignKey(verbose_name='部门ID',to='Department',to_field='id',on_delete=models.CASCADE)
    # 2.置空，如果没有部门id,不删除用户，部门id那变成空。
    #depart = models.ForeignKey(to='Department', to_fields='id',null=True,blank=True, on_delete=models.SET_NULL)
    # 入职时间
    create_time = models.DateField(verbose_name='入职时间',blank=True, null=True)
    # 性别
    gender_choices = (
        (1,'男'),
        (2,'女')
    )

    gender = models.SmallIntegerField(verbose_name='性别',choices=gender_choices)

# 手机号
class Mobel(models.Model):
    id = models.BigAutoField(verbose_name='id', primary_key=True)
    mobel = models.CharField(verbose_name='电话号码',max_length=11)
    price = models.IntegerField(verbose_name='价格')
    level_choices = (
        (1, '普通'),
        (2, '初级'),
        (3, '高级'),
        (4, '顶级'),
    )

    level = models.SmallIntegerField(verbose_name='级别', choices=level_choices,default=1,max_length=4)

    status_choices = (
        (1,'未占用'),
        (2,'已使用')
    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choices,default=2)



