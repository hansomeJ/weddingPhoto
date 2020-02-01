from django.conf.urls import url

from . import views
app_name = 'comment'
urlpatterns = [
    url(r'addComment/(?P<id>\d+)/$', views.addComment, name='addComment'),
    url(r'showComment/', views.showComment, name='showComment'),
    # url(r'showOrder/(?P<type>\w+)/$', views.showOrder, name='showOrder'),
]
