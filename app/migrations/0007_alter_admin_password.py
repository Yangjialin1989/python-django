# Generated by Django 5.0.4 on 2024-05-02 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='password',
            field=models.CharField(max_length=64, verbose_name='密码'),
        ),
    ]
