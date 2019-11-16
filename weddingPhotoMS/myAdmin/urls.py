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
    url(r'showBv/(\d+)/', views.showBv, name='showBv'),
    # 修改婚纱路由
    url(r'updateBv/(\d+)/', views.updateBv, name='updateBv'),
    url(r'deleteBv/(\d+)/', views.deleteBv, name='deleteBv'),
    # 添加婚纱组路由
    url(r'addBvs/', views.addBvs, name='addBvs'),
]
