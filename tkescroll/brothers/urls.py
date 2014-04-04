from django.conf.urls import patterns, url

from brothers import views

urlpatterns = patterns('',
    url(r'^home/$', views.index, name='index'),
    url(r'^(?P<scroll>\d+)/$', views.detail,name='detail'),
    #url(r'^search/$', views.search),
)
