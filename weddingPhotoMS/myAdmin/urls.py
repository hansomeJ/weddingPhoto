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
    # 删除婚纱路由
    url(r'deleteBv/(\d+)/', views.deleteBv, name='deleteBv'),
    # 添加婚纱组路由
    url(r'addBvs/', views.addBvs, name='addBvs'),
    # 查看婚纱组路由
    url(r'showBvs/', views.showBvs, name='showBvs'),
    # 删除婚纱组路由
    url(r'deleteBvs/(\d+)/', views.deleteBvs, name='deleteBvs'),
    # 添加场地路由
    url(r'addSpace/', views.addSpace, name='addSpace'),
    # 查看场地路由
    url(r'showSpace/', views.showSpace, name='showSpace'),
    # 删除场地路由
    url(r'deleteSpace/(\d+)/', views.deleteSpace, name='deleteSpace'),
    # 更新场地路由
    url(r'updateSpace/(\d+)/', views.updateSpace, name='updateSpace'),
    # 更新场地路由
    url(r'notice/', views.notice, name='notice'),

]
