# Generated by Django 5.0.4 on 2024-04-22 00:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('title', models.CharField(max_length=32, verbose_name='标题')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, verbose_name='姓名')),
                ('password', models.CharField(max_length=64, verbose_name='密码')),
                ('age', models.IntegerField(verbose_name='年龄')),
                ('account', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='账户余额')),
                ('gender', models.SmallIntegerField(choices=[(1, '男'), (2, '女')], verbose_name='性别')),
                ('depart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.department', verbose_name='部门ID')),
            ],
        ),
    ]