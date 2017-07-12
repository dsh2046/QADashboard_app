from django.conf.urls import url
from django.contrib import admin
from home.views import *

urlpatterns = [
    # url(r'^index/', IndexView.as_view(), name='index'),
    # url(r'^table/', table, name='table'),
    url(r'^detail/', detail, name='detail'),
    # url(r'^histogram/', home_views.histogram, name='histogram'),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^login/', login, name='login'),
    url(r'^logout/', logout, name='logout'),
    url(r'^login_validate/', login_validate, name='login_validate'),
    #url(r'^home/(\d+)/(\d+)', home_views.add, name='add'),
    url(r'^admin/', admin.site.urls),
    url(r'^getfile/', getfile, name='getfile'),

    url(r'^compare/', CompareView.as_view(), name='compare'),
]
