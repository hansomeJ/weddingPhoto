from django.conf.urls import url

from . import views

urlpatterns = [
    # 注册路由
    url(r'register/', views.register, name='register'),
    # 生成验证码路由
    url(r'code/', views.code, name='code'),
    # 登录路由
    url(r'login/', views.login, name='login'),
    # 主页路由
    url(r'index/', views.index, name='index'),
    url(r'test/', views.test, name='test'),
    # 添加婚纱路由
    url(r'addBv/', views.addBv, name='addBv'),
    # 查看婚纱路由
    url(r'showBv/(?P<id>\d+)/', views.showBv, name='addBv'),
]
