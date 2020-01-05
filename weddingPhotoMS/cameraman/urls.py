from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'index/', views.index, name='index'),
    url(r'showMsg/', views.showMsg, name='showMsg'),
    url(r'updateMsg/', views.updateMsg, name='updateMsg'),
]
