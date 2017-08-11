# -*-coding:utf-8 -*-
from django.shortcuts import render,render_to_response
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from models import Menger
from forms import *
# Create your views here.

@login_required
def index(request):
    return render(request,'index.html',{})

#登录
def login(request):
    if request.method =='POST':
        form =LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username,password=password)
            if user is not None and user.is_active:
                auth.login(request,user)
                return HttpResponseRedirect('/index/')
            else:
                return render(request,'login.html',{'form':form,'password_is_wrong':True})
        else:
            return render(request,'login.html',{'form':form,'password_is_wrong':True})
    else:
        form=LoginForm
        return render(request,'login.html',{'form':form})

#退出
@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')

#修改密码
@login_required
def changepwd(requset):
    if requset.method == 'GET':
        form = ChangpwdForm(requset.POST)
        return render(requset,'changepwd.html',{'form':form})
    else:
        form = ChangpwdForm(requset.POST)
        if form.is_valid():
            username = requset.user.username
            oldpwd = requset.POST.get('oldpwd','')
            user = auth.authenticate(username=username,password = oldpwd)
            if user is not None and user.is_active:
                newpwd = requset.POST.get('newpwd','')
                user.set_password(newpwd)
                user.save()
                return render(requset,'changepwdOK.html',{'changepwd_success':True})
            else:
                return render(requset,'changepwd.html',{'form':form,'oldpassword_is_wrong':True})
        else:
            return render(requset,'changepwd.html',{'form':form,'oldpassword_is_wrong_a':True})

#用户管理
@login_required
def user(request):
    user = request.user
    username = request.user.username
    menger = Menger.objects.get(user=user)
    list_user = User.objects.get(username=username)
    if request.method =='POST':
        form = YiheUserForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            email = form.cleaned_data['email']
            management = form.cleaned_data['management']
            insurance = form.cleaned_data['insurance']
            business = form.cleaned_data['business']
            financing = form.cleaned_data['financing']
            if insurance and business and financing or insurance and business or insurance and financing or business and financing:
                error= '只能选取一个部门'
                return render_to_response('NO.html',{'error':error})
            avalue = User.objects.get(username=username)
            menger.user =avalue
            menger.management = management
            menger.insurance = insurance
            menger.business = business
            menger.financing = financing
            menger.save()
            avalue.first_name=first_name
            avalue.email = email
            avalue.save()
            success = "修改成功"
            go_url_name="返回主页"
            go_url='/index/'
            return render_to_response('OK.html',{'success':success,'go_url_name':go_url_name,'go_url':go_url})
        else:
            error = "填写正确信息！"
            return render_to_response('NO.html',{'error':error})
    else:
        form =YiheUserForm(initial={
            'first_name':list_user.first_name,
            'email':list_user.email,
            'manager':menger.management,
            'insurance':menger.insurance,
            'business':menger.business,
            'financing':menger.financing
        })
    return render(request,'user.html',{'form':form,'list_user':list_user,'menager_manager':menger.management})














