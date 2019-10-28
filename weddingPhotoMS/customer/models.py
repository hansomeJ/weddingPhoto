from django.db import models

# 创建顾客表
class Customer(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='顾客主键')
    cs_name = models.CharField(max_length=200,verbose_name='顾客账号')
    cs_nickName = models.CharField(max_length=200,verbose_name='顾客昵称')
    cs_pwd = models.CharField(max_length=20,verbose_name='顾客密码')
    cd_address = models.CharField(max_length=200,verbose_name='顾客地址')
    cs_phoneNum = models.CharField(max_length=11,verbose_name='顾客电话')
    cs_gender = models.CharField(max_length=20, default='男', verbose_name='性别')
    cs_regisTime = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')