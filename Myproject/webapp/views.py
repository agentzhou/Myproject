# -*- coding: UTF-8 -*-
from django.shortcuts import render, redirect, HttpResponse
from Myproject.webapp.models import Servinfo, Servconf, MaintainRecords, UploadFile, Wifi
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from datetime import datetime
# import hashlib

def login(request):
    if request.method == 'POST':
        user = request.POST.get('username', '')
        passwd = request.POST.get('password', '')
        account = auth.authenticate(username=user, password=passwd)
        if account is not None and account.is_active:
            request.session['_codename'] = user
            auth.login(request, account)
            return redirect('/index/')
    else:
        return render(request, 'login.html')


def GetUserName(request):
    userid = request.session.get('_codename', default=None)
    context = {'userid': userid}
    return context


@login_required
def index(request):
#    import json
#    cookie_content = request.session['_codename']
#    return render(request, 'base.html', {'userid': json.dumps(cookie_content)})
    return render(request, 'index.html')


@login_required
def servermanage(request):
    if request.method == 'POST':
        if request.POST.has_key('FormA'):
            platform = request.POST.get('platform', '')
            used = request.POST.get('used', '')
            listplatform = platform.split('@')
#        return HttpResponse(listplatform[:])
            result_servinfo = Servinfo.objects.filter(Q(used__icontains=used),Q(platform__in=listplatform))
            result_servinfo_count = result_servinfo.count()
            return render(request, 'servermanage.html', {'result_servinfo': result_servinfo, 'result_servinfo_count': result_servinfo_count})
        else:
            sn = request.POST.get('sn', '')
            wanip = request.POST.get('wanip', '')
            lanip = request.POST.get('lanip', '')
            result_servinfo = Servinfo.objects.filter(Q(sn__iexact=sn)|Q(wanip=wanip)|Q(lanip=lanip))
            result_servinfo_count = result_servinfo.count()
            return render(request, 'servermanage.html', {'result_servinfo': result_servinfo, 'result_servinfo_count': result_servinfo_count})
    else:
        result_default = Servinfo.objects.filter(platform__exact='蛙蛙')
        result_default_count = result_default.count()
        return render(request, 'servermanage.html', {'result_default': result_default, 'result_default_count': result_default_count})


@login_required
def add_info(request, sn):
    if request.method == 'POST':
        mr = MaintainRecords()
        mr.servinfo_id = sn
        mr.time = datetime.now().strftime('%Y-%m-%d %H:%M')
        mr.editor = request.session.get('_codename', default=None)
        mr.content = request.POST.get('content', '')
        mr.save()
        return redirect('..')
    else:
        return render(request, 'add_info.html')


@login_required
def detail(request, sn):
	result_servconf = Servconf.objects.filter(info_id__exact=sn)
	result_maintainrecords = MaintainRecords.objects.filter(servinfo_id__exact=sn)
	return render(request, 'detail.html', {'result_servconf': result_servconf, 'result_maintainrecords': result_maintainrecords})


@login_required
def changepassword(request):
	if request.method == 'POST':
	    oldpwd = request.POST.get('oldpassword', '')
	    account = auth.authenticate(username=request.session.get('_codename', default=None), password=oldpwd)
	    if account:
        	newpwd1 = request.POST.get('newpassword-1', '')
            newpwd2 = request.POST.get('newpassword-2', '')
            if len(newpwd1) < 6:
                return HttpResponse(u'密码最少需要6位')
            elif newpwd1 != newpwd2:
                return HttpResponse(u'两次输入的密码不一致')
            else:
                account.set_password(newpwd1)
                account.save()
                return redirect('/logout/')
        else:
            return render(request, 'changepassword.html')


@login_required
def uploadfile(request):
    if request.method == 'POST':
        uploadfile = request.FILES.get('uploadfile', None)
        if uploadfile == None:
            return HttpResponse('请选择需要上传的文件')
        else:
            uf = UploadFile()
            uf.docfile = uploadfile
            uf.uploaddate = datetime.now().strftime('%Y-%m-%d %H:%M')
            uf.uploaduser = request.session.get('_codename', default=None)
            uf.save()
            return redirect('/index/')
    else:
        return render(request, 'uploadfile.html')


@login_required
def wifimanage(request):
    import xlrd
    if request.method == 'POST':
        filedir = u'E:\\Myproject\\Myproject\\webapp\\uploadfile\\'
        choosefile = request.POST.get('choosefile', '')
        file = filedir + '\\' + choosefile
        ssid = request.POST.get('ssid', '')
        if choosefile:
            choosefile = xlrd.open_workbook(file)
            table = choosefile.sheets()[0]
            for irows in range(1, table.nrows):
 				wifi = Wifi(username = table.cell(irows, 0).value, passphrase = table.cell(irows, 1).value,
 				            wan = table.cell(irows, 2).value, macaddr = table.cell(irows, 3).value,
 				            vlan = table.cell(irows, 4).value, expires = table.cell(irows, 5).value,
 				            who = table.cell(irows, 6).value, device = table.cell(irows, 7).value,
 				            department = table.cell(irows, 8).value)
 				wifi.save()
            result_wifi_import = Wifi.objects.filter(wan__icontains=wifi.wan)
            return render(request, 'wifimanage.html', {'result_wifi_import': result_wifi_import})
        elif ssid:
            result_wifi_select = Wifi.objects.filter(wan__icontains=ssid)
            return render(request, 'wifimanage.html', {'result_wifi_select': result_wifi_select})
    else:
        result_wifi_default = Wifi.objects.filter(wan__icontains='line')
        return render(request, 'wifimanage.html', {'result_wifi_default': result_wifi_default})


@login_required
def logout(request):
	del request.session['_codename']
	auth.logout(request)
	return render(request, 'logout.html')


def error(request):
	return render(request, 'error.html')
