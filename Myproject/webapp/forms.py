# -*- coding: UTF-8 -*-
from django import forms
# from django.forms import ModelForm, Textarea
# from Myproject.webapp.models import MaintainRecords
reload(__import__('sys')).setdefaultencoding('utf-8')

class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=15)
    password = forms.CharField(label='密码', max_length=24, widget=forms.PasswordInput)
