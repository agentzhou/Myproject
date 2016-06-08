# -*- coding: UTF-8 -*-
from django import forms
from django.forms import ModelForm, Textarea
from Myproject.webapp.models import MaintainRecords

reload(__import__('sys')).setdefaultencoding('utf-8')

NAME = {
	('None', 'None'),
	('蛙蛙', '蛙蛙'),
	('酷蛙', '酷蛙'),
	('全民', '全民'),
}


class LoginForm(forms.Form):
	username = forms.CharField(label='用户名', max_length=15)
	password = forms.CharField(label='密码', max_length=24, widget=forms.PasswordInput)


class ManageSearchForm(forms.Form):
	sn = forms.CharField(label='SN号', widget=forms.TextInput(attrs={'size': 10}), max_length=10, required=False)
	platform = forms.ChoiceField(label='平台', widget=forms.Select, choices=NAME, initial='None', required=False)
	wanip = forms.GenericIPAddressField(label='外网IP', widget=forms.TextInput(attrs={'size': 10}), required=False)
	lanip = forms.GenericIPAddressField(label='内网IP', widget=forms.TextInput(attrs={'size': 10}), required=False)


class MaintainRecordsForm(ModelForm):
	class Meta:
		model = MaintainRecords
		fields = ['content']
		widgets = {'content': Textarea(attrs={'cols': 120, 'rows': 10})}


class ChangePasswordForm(forms.Form):
	oldpwd = forms.CharField(label='原始密码', max_length=30, widget=forms.PasswordInput(attrs={'size': 20, 'placeholder': '原始密码'}))
	newpwd_1 = forms.CharField(label='新密码', max_length=30, widget=forms.PasswordInput(attrs={'size': 20, 'placeholder': '新密码'}))
	newpwd_2 = forms.CharField(label='新密码确认', max_length=30, widget=forms.PasswordInput(attrs={'size': 20, 'placeholder': '新密码确认'}))

	def clean(self):
		if not self.is_valid():
			raise forms.ValidationError('所有项为必填项')
		elif len(self.cleaned_data['newpwd_1']) < 6:
			raise forms.ValidationError('密码长度不少于6位')
		elif self.cleaned_data['newpwd_1'] != self.cleaned_data['newpwd_2']:
			raise forms.ValidationError('两次输入的密码不一致')
		else:
			return super(ChangePasswordForm, self).clean()

class UploadFileForm(forms.Form):
	docfile = forms.FileField(required=True, allow_empty_file=False, widget=forms.FileInput)

class SelectFileForm(forms.Form):
	distfile = forms.FilePathField(label='目标文件',path='F:\\Myproject\\Myproject\\webapp\\uploadfile', recursive=True, match='.*\.xl(s|sx)$')
