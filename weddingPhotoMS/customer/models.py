from django.db import models
from myAdmin.models import Bridal_Veil as bv
from myAdmin.models import Bridal_Veils as bvs
from cameraman.models import Cameraman
from myAdmin.models import Space


# 创建顾客表
class Customer(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='顾客主键')
    cs_name = models.CharField(max_length=200, verbose_name='顾客账号')
    cs_nickName = models.CharField(max_length=200, verbose_name='顾客昵称')
    cs_pwd = models.CharField(max_length=50, verbose_name='顾客密码')
    cs_address = models.CharField(max_length=200, verbose_name='顾客地址')
    cs_phoneNum = models.CharField(max_length=11, verbose_name='顾客电话')
    cs_gender = models.CharField(max_length=20, default='男', verbose_name='性别')
    cs_regisTime = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')


# 创建订单表
class Order(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='订单主键')
    order_bv = models.ManyToManyField(to=bv, verbose_name='订单中的婚纱')
    order_bvs = models.ForeignKey(to=bvs, to_field='id', verbose_name='婚纱组')
    order_photographTime = models.DateTimeField(verbose_name='拍照时间')
    order_selectTime = models.DateTimeField(verbose_name='选片时间')
    order_getTime = models.DateTimeField(verbose_name='取片时间')
    order_space = models.ForeignKey(to=Space, to_field='id', verbose_name='场地')
    order_cameraman = models.ForeignKey(to=Cameraman, to_field='id', verbose_name='摄影师')
    order_moneyNum = models.IntegerField(verbose_name='订单总价')
    order_starTime = models.DateTimeField(auto_now_add=True, verbose_name='订单开始时间')
    order_endTime = models.DateTimeField(verbose_name='订单结束时间')
    order_status = models.CharField(max_length=200, default='待拍摄', verbose_name='订单状态')
