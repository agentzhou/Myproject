# -*- coding: UTF-8 -*-
# Register your models here.
# admin.site.register(user)
from django.contrib import admin
from Myproject.webapp.models import Servinfo, Servconf, MaintainRecords, Wifi, UploadFile

admin.site.register(Servinfo)
admin.site.register(Servconf)
admin.site.register(MaintainRecords)
admin.site.register(Wifi)
admin.site.register(UploadFile)
# admin.site.register(MaintainRecords)