# Generated by Django 5.0.4 on 2024-04-26 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='create_time',
            field=models.DateField(blank=True, null=True, verbose_name='入职时间'),
        ),
    ]
