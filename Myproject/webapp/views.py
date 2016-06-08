# -*- coding: UTF-8 -*-
from django.shortcuts import render, redirect
from Myproject.webapp.forms import LoginForm, ManageSearchForm, MaintainRecordsForm, ChangePasswordForm, UploadFileForm, SelectFileForm
from Myproject.webapp.models import Servinfo, Servconf, MaintainRecords, UploadFile, Wifi
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from datetime import datetime
import xlrd
# import hashlib


def login(request):
	if request.method == 'POST':
		lg = LoginForm(request.POST)
		if lg.is_valid():
			username = lg.cleaned_data['username']
			password = lg.cleaned_data['password']
			account = auth.authenticate(username=username, password=password)
			if account:
				request.session['code'] = username
				if account.is_active:
					auth.login(request, account)
					return redirect('/index/')
			else:
				return redirect('/error/')
	else:
		lg = LoginForm()
	return render(request, 'login.html', {'lg': lg})


@login_required
def index(request):
	return render(request, 'index.html')


@login_required
def manage(request):
	if request.method == 'POST':
		msf = ManageSearchForm(request.POST)
		if msf.is_valid():
			sn = msf.cleaned_data['sn']
			platform = msf.cleaned_data['platform']
			wanip = msf.cleaned_data['wanip']
			lanip = msf.cleaned_data['lanip']
			result_servinfo = Servinfo.objects.filter(Q(sn__iexact=sn) |
			                                          Q(platform__exact=platform) |
			                                          Q(wanip=wanip) |
			                                          Q(lanip=lanip))
			result_servinfo_count = result_servinfo.count()
			msf = ManageSearchForm(initial={'sn': None, 'platform': None, 'wanip':None, 'lanip':None})
			return render(request, 'manage.html', {'result_servinfo': result_servinfo, 'result_servinfo_count': result_servinfo_count, 'msf': msf})
		else:
			return redirect('/index/manage/')
	else:
		msf = ManageSearchForm(initial={'sn': None, 'platform': None, 'wanip':None, 'lanip':None})
	result_default = Servinfo.objects.all().filter(platform__exact='蛙蛙')
	result_default_count = result_default.count()
	return render(request, 'manage.html', {'msf': msf, 'result_default': result_default, 'result_default_count': result_default_count})


@login_required
def add_info(request, sn):
	if request.method == 'POST':
		mrf = MaintainRecordsForm(request.POST)
		mr = MaintainRecords()
		mr.servinfo_id = sn
		mr.time = datetime.now().strftime('%Y-%m-%d %H:%M')
		mr.editor = request.session.get('code', default=None)
		mr.content = mrf.__unicode__().lstrip('<tr><th><label for="id_content">明细:</label></th><td><textarea cols="120" id="id_content" maxlength="1000" name="content" rows="10">').rstrip('</textarea></td></tr>')
		mr.save()
		if mrf.is_valid():
			return redirect('..')
	else:
		mrf = MaintainRecordsForm()
	return render(request, 'add_info.html', {'mrf': mrf})


@login_required
def detail(request, sn):
	result_servconf = Servconf.objects.filter(info_id__exact=sn)
	result_maintainrecords = MaintainRecords.objects.filter(servinfo_id__exact=sn)
	return render(request, 'detail.html', {'result_servconf': result_servconf, 'result_maintainrecords': result_maintainrecords})


@login_required
def changepassword(request):
	if request.method == 'POST':
		cpf = ChangePasswordForm(request.POST)
		if cpf.is_valid():
			oldpassword = cpf.cleaned_data['oldpwd']
			account = auth.authenticate(username=request.session['code'], password=oldpassword)
			if account:
				if account.is_active:
					newpassword = cpf.cleaned_data['newpwd_2']
					account.set_password(newpassword)
					account.save()
					return redirect('/index/')
			else:
				return redirect('/index/changepassword/')
		else:
			return redirect('/index/changepassword/')
	else:
		cpf = ChangePasswordForm()
	return render(request, 'changepassword.html', {'cpf': cpf})


@login_required
def wifimanage(request):
	if request.method == 'POST':
		uff = UploadFileForm(request.POST, request.FILES)
		if uff.is_valid():
			docfile = uff.cleaned_data['docfile']
			uf = UploadFile()
			uf.docfile = docfile
			uf.uploaddate = datetime.now().strftime('%Y-%m-%d %H:%M')
			uf.uploaduser = request.session.get('code', default=None)
			uf.save()
			return redirect('/index/wifimanage/')
	else:
		uff = UploadFileForm()
	return render(request, 'wifimanage.html', {'uff': uff})


@login_required
def line(request):
	if request.method == 'POST':
		sff = SelectFileForm(request.POST)
		if sff.is_valid():
			distfile = sff.cleaned_data['distfile']
			openfile = xlrd.open_workbook(distfile)
			table = openfile.sheets()[0]
			for irows in range(1, table.nrows):
				wifi = Wifi(username = table.cell(irows, 0).value, passphrase = table.cell(irows, 1).value,
				            wan = table.cell(irows, 2).value, macaddr = table.cell(irows, 3).value,
				            vlan = table.cell(irows, 4).value, expires = table.cell(irows, 5).value,
				            who = table.cell(irows, 6).value, device = table.cell(irows, 7).value,
				            department = table.cell(irows, 8).value)
				wifi.save()
			return redirect('/index/wifimanage/line/')
		else:
			return redirect('/index/wifimanage/')
	else:
		sff = SelectFileForm()
	result_wifi = Wifi.objects.all().filter(wan__exact='GR-Line')
	return render(request, 'wifiline.html', {'reult_wifi': result_wifi, 'sff': sff})


@login_required
def mobile_pc(request):
	if request.method == 'POST':
		sff = SelectFileForm(request.POST)
		if sff.is_valid():
			distfile = sff.cleaned_data['distfile']
			openfile = xlrd.open_workbook(distfile)
			table = openfile.sheets()[0]
			for irows in range(1, table.nrows):
				wifi = Wifi(username = table.cell(irows, 0).value, passphrase = table.cell(irows, 1).value,
				            wan = table.cell(irows, 2).value, macaddr = table.cell(irows, 3).value,
				            vlan = table.cell(irows, 4).value, expires = table.cell(irows, 5).value,
				            who = table.cell(irows, 6).value, device = table.cell(irows, 7).value,
				            department = table.cell(irows, 8).value)
				wifi.save()
			return redirect('/index/wifimanage/mobile_pc/')
		else:
			return redirect('/index/wifimanage/')
	else:
		sff = SelectFileForm()
	result_wifi = Wifi.objects.all().filter(wan__exact='GR-MobilePC')
	return render(request, 'wifimobile_pc.html', {'reult_wifi': result_wifi, 'sff': sff})


@login_required
def mobile_test(request):
	if request.method == 'POST':
		sff = SelectFileForm(request.POST)
		if sff.is_valid():
			distfile = sff.cleaned_data['distfile']
			openfile = xlrd.open_workbook(distfile)
			table = openfile.sheets()[0]
			for irows in range(1, table.nrows):
				wifi = Wifi(username = table.cell(irows, 0).value, passphrase = table.cell(irows, 1).value,
				            wan = table.cell(irows, 2).value, macaddr = table.cell(irows, 3).value,
				            vlan = table.cell(irows, 4).value, expires = table.cell(irows, 5).value,
				            who = table.cell(irows, 6).value, device = table.cell(irows, 7).value,
				            department = table.cell(irows, 8).value)
				wifi.save()
			return redirect('/index/wifimanage/mobile_test/')
		else:
			return redirect('/index/wifimanage/')
	else:
		sff = SelectFileForm()
	result_wifi = Wifi.objects.all().filter(wan__exact='GR-MobileTest')
	return render(request, 'wifimobile_test.html', {'reult_wifi': result_wifi, 'sff': sff})


@login_required
def private(request):
	if request.method == 'POST':
		sff = SelectFileForm(request.POST)
		if sff.is_valid():
			distfile = sff.cleaned_data['distfile']
			openfile = xlrd.open_workbook(distfile)
			table = openfile.sheets()[0]
			for irows in range(1, table.nrows):
				wifi = Wifi(username = table.cell(irows, 0).value, passphrase = table.cell(irows, 1).value,
				            wan = table.cell(irows, 2).value, macaddr = table.cell(irows, 3).value,
				            vlan = table.cell(irows, 4).value, expires = table.cell(irows, 5).value,
				            who = table.cell(irows, 6).value, device = table.cell(irows, 7).value,
				            department = table.cell(irows, 8).value)
				wifi.save()
			return redirect('/index/wifimanage/private/')
		else:
			return redirect('/index/wifimanage/')
	else:
		sff = SelectFileForm()
	result_wifi = Wifi.objects.all().filter(wan__exact='GR-Private')
	return render(request, 'wifiprivate.html', {'reult_wifi': result_wifi, 'sff': sff})


@login_required
def private_test(request):
	if request.method == 'POST':
		sff = SelectFileForm(request.POST)
		if sff.is_valid():
			distfile = sff.cleaned_data['distfile']
			openfile = xlrd.open_workbook(distfile)
			table = openfile.sheets()[0]
			for irows in range(1, table.nrows):
				wifi = Wifi(username = table.cell(irows, 0).value, passphrase = table.cell(irows, 1).value,
				            wan = table.cell(irows, 2).value, macaddr = table.cell(irows, 3).value,
				            vlan = table.cell(irows, 4).value, expires = table.cell(irows, 5).value,
				            who = table.cell(irows, 6).value, device = table.cell(irows, 7).value,
				            department = table.cell(irows, 8).value)
				wifi.save()
			return redirect('/index/wifimanage/private_test/')
		else:
			return redirect('/index/wifimanage/')
	else:
		sff = SelectFileForm()
	result_wifi = Wifi.objects.all().filter(wan__exact='GR-PrivateTest')
	return render(request, 'wifiprivate.html', {'reult_wifi': result_wifi, 'sff': sff})


@login_required
def logout(request):
	del request.session['code']
	auth.logout(request)
	return render(request, 'logout.html')


def error(request):
	return render(request, 'error.html')
