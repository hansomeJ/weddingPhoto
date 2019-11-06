from django.db import models
from system.storage import ImageStorage


# Create your models here.
# 创建摄影师表
class Cameraman(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='摄影师主键')
    ca_name = models.CharField(max_length=200, verbose_name='账号')
    ca_nickName = models.CharField(max_length=200, verbose_name='昵称')
    ca_pwd = models.CharField(max_length=50, verbose_name='密码')
    ca_detail = models.TextField(verbose_name='简介')
    ca_image = models.ImageField(upload_to='static/img/cameraman/%Y%m', storage=ImageStorage(),
                                 default='default_ca.jpg', verbose_name='摄影师照片')
    ca_lv = models.CharField(max_length=200, default='初级', verbose_name='摄影师等级')
    ca_gender = models.CharField(max_length=20, default='男', verbose_name='性别')
    ca_regisTime = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')
