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
from Myproject.webapp.views import login, logout, index, error, servermanage, detail, add_info, changepassword, uploadfile, wifimanage


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', login),
    url(r'^login/$', login),
    url(r'^index/$', index),
    url(r'^logout/$', logout),
    url(r'^error/$', error),
    url(r'^index/servermanage/$', servermanage),
    url(r'^index/servermanage/(?P<sn>\w{6,10})/$', detail),
    url(r'^index/servermanage/(?P<sn>\w{6,10})/add_info/$', add_info),
    url(r'^index/changepassword/$', changepassword),
    url(r'^index/uploadfile/$', uploadfile),
    url(r'^index/wifimanage/$', wifimanage),
]
