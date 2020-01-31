from django.conf.urls import url

from . import views
app_name = 'comment'
urlpatterns = [
    url(r'addComment/(?P<id>\d+)/$', views.addComment, name='addComment'),
    # url(r'addOrder/', views.addOrder, name='addOrder'),
    # url(r'showOrder/(?P<type>\w+)/$', views.showOrder, name='showOrder'),
]
