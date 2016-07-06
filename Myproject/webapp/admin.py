# -*- coding: UTF-8 -*-
# Register your models here.
# admin.site.register(user)
reload(__import__('sys')).setdefaultencoding('utf-8')
from django.contrib import admin
from Myproject.webapp.models import Servinfo, Servconf, MaintainRecords, Wifi, UploadFile

admin.site.register(Servinfo)
admin.site.register(Servconf)
admin.site.register(MaintainRecords)
admin.site.register(Wifi)
admin.site.register(UploadFile)
