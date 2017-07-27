# -*- coding:utf-8 -*-
from __future__ import division
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
from django.http import HttpResponseRedirect
from django.shortcuts import render,render_to_response
from django import forms
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logou
import MySQLdb
from myApp.models import User
from webserver.svm import SVM_Model
#定义表单模型
class UserForm(forms.Form):
    username = forms.CharField( label='用户名：',max_length=100)
    password = forms.CharField(label='密码：',widget=forms.PasswordInput())
    password2= forms.CharField(label='请确认密码',widget=forms.PasswordInput)
    def pwd_validate(self,p1,p2):
        return p1==p2

#定义登录表单模型
class LoginForm(forms.Form):
    username = forms.CharField(
            required=True,
            label=u"用户名",
            error_messages={'required':'请输入用户名'},
            widget=forms.TextInput(
                attrs={
                    'placeholder':u'用户名',
                }
            )
    )
    password = forms.CharField(
            required=True,
            label=u"密码",
            error_messages={'required':u'请输入密码'},
            widget=forms.PasswordInput(
                attrs={
                    'placeholder':u"密码",
                    }
                ),
     )
    def clear(self):
        if not self.is_valid():
            raise forms.ValidationError(u"用户名和密码为必填项")
        else:
            clear_data = super(LoginForm,self).clearn()
#主页
def index(request):
    return render(request,'index.html')


"""
def login_validate(request,username,password):
  rtvalue = False
  user = authenticate(username=username,password=password)
  if user is not None:
    if user.is_active:
      auth_login(request,user)
      return True
  return rtvalue
"""
#实现用户登录功能
def login(request):
    error=[]
    if request.method=="POST":
        uf=LoginForm(request.POST)
        if uf.is_valid():
            #获取表单用户名和密码
            username=uf.cleaned_data['username']
            password=uf.cleaned_data['password']
            #获取的表单数据与数据库数据进行比较
            user=User.objects.filter(username__exact=username,password__exact=password)
            if user:
                request.session['username']=uf.cleaned_data['username']
                #比较成功，跳转到主界面index
                response=HttpResponseRedirect('/index.html')
                return response
            else:
                error.append("用户或密码不对！")
                #比较失败，停在登录界面
                uf=LoginForm()
                return render_to_response("login.html",{'uf':uf,'error':error})


    else:
        uf=LoginForm()
    return render_to_response('login.html',{'uf':uf})


#注册页面
def register(request):
    error = []
    if request.method == "POST":
        uf= UserForm(request.POST)
        if uf.is_valid():
            #获取表单信息
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            password2 = uf.cleaned_data['password2']
            if not User.objects.all().filter(username=username):
                if uf.pwd_validate(password,password2):
                    #将表单写入数据库
                    user = User()
                    user.username = username
                    user.password = password
                    user.save()
                    response=HttpResponseRedirect('/login')
                    return response
                else:
                    error.append('请输入相同的密码!')
            else:
                error.append("该用户名已存在!")

        uf = UserForm()
        return render_to_response('register.html',{'uf':uf,'error':error})
    else:
     uf  = UserForm()
    return render_to_response('register.html',{'uf':uf})

#产品介绍页面

def introduction(request):
    login_user = request.session.get('username')
    if not login_user:
        response=HttpResponseRedirect('/login')
        return response

    return render(request,'introduction.html')

#酒店评论页面

def hotel(request):
    return render(request,'hotel.html')

#股票评论页面
def share(req):

    #正常用户分析
    scorelist=[]
    f=open('/home/demon/PycharmProjects/webserver/webserver/score.txt','r')
    while True:
        line = f.readline()
        if not line:
            break
        rel=line.replace('\n','')
        scorelist.append(float(rel))
    print scorelist
    f.close()
    #成熟用户分析
    scoreoldlist=[]
    f=open('/home/demon/PycharmProjects/webserver/webserver/scoreold.txt','r')
    while True:
        line = f.readline()
        if not line:
            break
        rel=line.replace('\n','')
        scoreoldlist.append(float(rel))
    print scoreoldlist
    f.close()
    #非成熟用户分析
    scorenewlist=[]
    f=open('/home/demon/PycharmProjects/webserver/webserver/scorenew.txt','r')
    while True:
        line = f.readline()
        if not line:
            break
        rel=line.replace('\n','')
        scorenewlist.append(float(rel))
    print scoreoldlist
    f.close()
    return render_to_response('shares.html',{'scorelist':scorelist,'scoreoldlist':scoreoldlist,'scorenewlist':scorenewlist})


