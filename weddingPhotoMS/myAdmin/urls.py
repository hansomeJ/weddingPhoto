from django.conf.urls import url

from . import views

urlpatterns = [
    # 注册路由
    url(r'register/', views.register, name='register'),
    # 生成验证码路由
    url(r'code/', views.code, name='code'),
    url(r'login/', views.login, name='login'),
    url(r'index/', views.index, name='index'),
]
