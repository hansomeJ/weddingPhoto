from django.db import models

from system.storage import ImageStorage
from DjangoUeditor.models import UEditorField
# Create your models here.
# 定义管理员表
class Admin(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='管理员主键')
    admin_Name = models.CharField(max_length=50, verbose_name='管理员账号')
    admin_nickName = models.CharField(max_length=50, verbose_name='管理员昵称')
    admin_pwd = models.CharField(max_length=50, verbose_name='管理员密码')
    admin_gender = models.CharField(max_length=20, default='男', verbose_name='性别')
    admin_regisTime = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')


# 定义婚纱表
class Bridal_Veil(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='婚纱主键')
    bv_name = models.CharField(max_length=200, verbose_name='婚纱名')
    bv_num_all = models.IntegerField(default=10, verbose_name='总数量')
    bv_num_now = models.IntegerField(default=10, verbose_name='可用数量')
    bv_image = models.ImageField(upload_to='static/img/bridalVeil/%Y%m', storage=ImageStorage(),
                                 default='default_bv.jpg', verbose_name='婚纱照片')
    bv_detail = models.TextField(verbose_name='婚纱简介')
    bv_price = models.IntegerField(default=1000, verbose_name='婚纱价格')
    bv_photoNumMax = models.IntegerField(default=50, verbose_name='拍摄照片总张数')
    bv_photoNumMin = models.IntegerField(default=10, verbose_name='可选择张数')
    bv_sale_num = models.IntegerField(default=0, verbose_name='婚纱热度')


# 定义婚纱组表
class Bridal_Veils(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='婚纱组主键')
    bvs_name = models.CharField(max_length=200, verbose_name='婚纱组名字')
    # 婚纱组与婚纱是多对多关系，一种婚纱可以属于多个婚纱组，一组婚纱里面也有多种婚纱
    # 婚纱组查询组内婚纱：BridalVeils.bvs_bv.all()
    # 婚纱查询属于那些组：BridalVeil.bvs_set.all()
    bvs_bv = models.ManyToManyField("Bridal_Veil", verbose_name='婚纱组中的婚纱')
    bvs_prices = models.IntegerField(verbose_name='婚纱组价格')
    bvs_sale_num = models.IntegerField(default=0, verbose_name='婚纱组热度')


# 定义场地表
class Space(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='场地主键')
    s_name = models.CharField(max_length=200, verbose_name='场地名字')
    s_image = models.ImageField(upload_to='static/img/space/%Y%m', storage=ImageStorage(), default='default_s.jpg',
                                verbose_name='场地图片')
    s_detail = models.TextField(verbose_name='场地简介')
    s_sale_num = models.IntegerField(default=0, verbose_name='场地热度')


# 定义通知公告表
class Notice(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='订单主键')
    notice_title = models.CharField(max_length=200, verbose_name='公告主键')
    notice_content = UEditorField(verbose_name='公告内容')
    notice_time = models.DateTimeField(auto_now_add=True, verbose_name='公告发布时间')
