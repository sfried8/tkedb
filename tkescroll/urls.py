from django.conf.urls import patterns, include, url
from brothers import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tkescroll.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$',views.home,name="home"),
    url(r'^brothers/', include('brothers.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^PC/(?P<pc>\d+)/$', views.PC),
    url(r'^PC/ZT(?P<pc>\d+)/$', views.PC),
    url(r'^scroll/$',views.scroll),
    url(r'^actives/$',views.actives),
    url(r'^actives/edit$',views.editActives),
    url(r'^actives/update_active$',views.update_active),
    url(r'^eboard/$',views.eboard),
    url(r'^search/$', views.search),
    url(r'^fullSearch/$',views.searchPage),
    url(r'^facts/$', views.facts),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^register/$', views.register),
    url(r'^message/$', views.message),
    url(r'^forgot/$', views.forgot),
    url(r'^newPass/(?P<username>\w+)/$', views.newPass),
    url(r'^newPass/$', views.goHome),
)
