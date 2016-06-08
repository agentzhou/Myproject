# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.db import models
# import hashlib
# import time
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

# Create your models here.
PLATFORM = (
	('蛙蛙', '蛙蛙'),
	('酷蛙', '酷蛙'),
	('多酷', '多酷'),
	('全民', '全民')
)


BRAND = (
	('DELL', 'DELL'),
	('HP', 'HP'),
	('IBM', 'IBM'),
	('其它', '其它')
)


STATUS = (
	('使用', '使用'),
	('故障', '故障'),
	('闲置', '闲置'),
)

POWER = (
	('是', '是'),
	('否', '否'),
)


class Servinfo(models.Model):
	sn = models.CharField('SN', max_length=10, primary_key=True, unique=True)
	wanip = models.GenericIPAddressField('外网ip', max_length=15, null=True, blank=True, unique=True)
	lanip = models.GenericIPAddressField('内网ip', max_length=15, null=True, blank=True, unique=True)
	platform = models.CharField('平台', max_length=20, choices=PLATFORM)
	brand = models.CharField('品牌', max_length=15, choices=BRAND)
	position = models.CharField('机架位', max_length=20)
	used = models.CharField('用途', max_length=50, blank=True)
	power = models.CharField('双电源', max_length=10, choices=POWER, default='否', blank=True)
	status = models.CharField('状态', max_length=20, choices=STATUS)

	class Meta:
		ordering = ['platform']

	def __str__(self):
		return '%-s-%s-%s' % (self.platform, self.used, self.sn)


class Servconf(models.Model):
	info = models.OneToOneField(Servinfo, primary_key=True)
	cpu = models.CharField('CPU', max_length=256, blank=True)
	mem = models.CharField('内存', max_length=10, blank=True)
	disk = models.CharField('磁盘', max_length=30, blank=True)

	def __str__(self):
		return self.info.sn


# class User(models.Model):
# 	username = models.CharField('用户名', max_length=15, primary_key=True, unique=True)
# 	email = models.EmailField('邮箱', max_length=254, unique=True)
# 	password = models.CharField('密码', max_length=100)
# 	class Mete:
# 		ordering = ['username']

# 	def __str__(self):
# 		return self.username

# 	def save(self, *args, **kwargs):
# 		self.password = hashlib.sha256(self.password).hexdigest()
# 		super(User, self).save(*args, **kwargs)


class MaintainRecords(models.Model):
	servinfo = models.ForeignKey(Servinfo, related_name='+')
	time = models.DateTimeField('时间', auto_now=True)
	editor = models.CharField('记录人', max_length=20)
	content = models.TextField('明细', max_length=1000)

	def __str__(self):
		return '%s-%s' % (self.servinfo_id, self.content)


class UploadFile(models.Model):
	docfile = models.FileField('位置', upload_to='uploadfile/%Y%m%d')
	uploaduser = models.CharField('上传用户', max_length=20)
	uploadtime = models.DateTimeField('上传时间', auto_now=True)

	def __str__(self):
		return '%s-%s' % (self.uploaduser, self.uploadtime)


class Wifi(models.Model):
	username = models.CharField('密码标识', max_length=50)
	passphrase = models.CharField('密码', max_length=8)
	wan = models.CharField('接入点标识', max_length=20)
	macaddr = models.CharField('物理地址', max_length=20)
	vlan = models.CharField('vlan标识', max_length=10)
	expires = models.CharField('有效期', max_length=20)
	who = models.CharField('使用人', max_length=50)
	device = models.CharField('设备名称', max_length=20)
	department = models.CharField('部门', max_length=20)

# 	class Meta:
# 		ordering = ['-username']

	def __str__(self):
		return '%s-%s-%s' % (self.username, self.wan, self.who)

# class MaintainRemarks(models.Model):
# 	info = models.OneToOneField(Servinfo, primary_key=True)
# 	time = models.DateTimeField('时间', auto_now=True)
# 	author = models.CharField('记录人', max_length=20)
# 	text = models.TextField('详细', max_length=1000)

# 	def __str__(self):
# 		return self.id
#
# 	def input(self, request, *args, **kwargs):
# 		self.time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
# 		self.author = request.session['code']
# 		super(MaintainRemarks, self).save(request, *args, **kwargs)
