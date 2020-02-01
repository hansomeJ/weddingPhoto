from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'index/', views.index, name='index'),
    url(r'showMsg/', views.showMsg, name='showMsg'),
    url(r'updateMsg/', views.updateMsg, name='updateMsg'),
    url(r'showComment/', views.showComment, name='showComment'),
    url(r'showOrder/(?P<id>\d+)/(?P<type>\w+)/$', views.showOrder, name='showOrder'),
    url(r'updateOrder/(?P<id>\d+)/', views.updateOrder, name='updateOrder'),
]
