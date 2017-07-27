# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models
#用户信息表
class User(models.Model):
    #设置的用户登录名
    username=models.CharField(max_length=50,null=True)
    #设置用户名密码
    password=models.CharField(max_length=50,null=True)
    def __unicode__(self):
        return self.username
