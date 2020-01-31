from django.db import models
from myAdmin.models import Bridal_Veil as bv
from myAdmin.models import Bridal_Veils as bvs
from myAdmin.models import Space
from cameraman.models import Cameraman
from customer.models import Customer


# Create your models here.

# 婚纱评论
class Comment_Bv(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='评论主键')
    c_content = models.TextField(verbose_name='婚纱评价')
    c_bvId = models.ForeignKey(to=bv, to_field='id', on_delete=models.CASCADE, verbose_name='外键，指向婚纱id')
    c_customerId = models.ForeignKey(to=Customer, to_field='id', on_delete=models.CASCADE,verbose_name='外键，指向顾客')
    c_time = models.DateTimeField(auto_now_add=True,verbose_name='评论时间')

# 场地评论
class Comment_Space(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='评论主键')
    c_content = models.TextField(verbose_name='场地评价')
    c_spaceId = models.ForeignKey(to=Space, to_field='id', on_delete=models.CASCADE, verbose_name='外键，指向场地')
    c_customerId = models.ForeignKey(to=Customer, to_field='id',on_delete=models.CASCADE, verbose_name='外键，指向顾客')
    c_time = models.DateTimeField(auto_now_add=True,verbose_name='评论时间')


# 摄影师评论
class Comment_Camerman(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='评论主键')
    c_content = models.TextField(verbose_name='场地评价')
    c_cameraman = models.ForeignKey(to=Cameraman, to_field='id', on_delete=models.CASCADE, verbose_name='外键，指向摄影师')
    c_customer = models.ForeignKey(to=Customer, to_field='id', verbose_name='外键，指向顾客')
    c_time = models.DateTimeField(auto_now_add=True,verbose_name='评论时间')


# 婚纱组评论
class Comment_Bvs(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='评论主键')
    c_content = models.TextField(verbose_name='婚纱组评价')
    c_bvs = models.ForeignKey(to=bvs, to_field='id', on_delete=models.CASCADE, verbose_name='外键，指向婚纱组id')
    c_customer = models.ForeignKey(to=Customer, to_field='id', verbose_name='外键，指向顾客')
    c_time = models.DateTimeField(auto_now_add=True,verbose_name='评论时间')
