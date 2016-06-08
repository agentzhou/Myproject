"""Myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from Myproject.webapp.views import login, logout, index, error, \
	manage, detail, add_info, changepassword, wifimanage, line, mobile_pc, mobile_test, private, private_test


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', login),
    url(r'^login/$', login,),
    url(r'^index/$', index,),
    url(r'^logout/$', logout),
    url(r'^error/$', error),
    url(r'^index/manage/$', manage),
    url(r'^index/manage/(?P<sn>\w{6,10})/$', detail),
    url(r'^index/manage/(?P<sn>\w{6,10})/add_info/$', add_info),
    url(r'^index/changepassword/$', changepassword),
	url(r'^index/wifimanage/$', wifimanage),
    url(r'^index/wifimanage/line/$', line),
    url(r'^index/wifimanage/mobile_pc/$', mobile_pc),
	url(r'^index/wifimanage/mobile_test/$', mobile_test),
	url(r'^index/wifimanage/private/$', private),
	url(r'^index/wifimanage/private_test/$', private_test),
]
