#-*- coding:utf-8 -*-
from django.shortcuts import render,render_to_response
from User_Management.models import Menger
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import (is_password_usable, make_password,)
from User_Management.forms import AccountForm
from django.conf import settings

# Create your views here.
@login_required
def user_list(request):
	user = request.user
	menger = Menger.objects.get(user=user)
	if menger.management == 1 :
		menger.insurance==1
		users = User.objects.all()
		return render(request,'adm_accounts.html',{'users':users})
	else:
		error = "你没有权限！"
		return render_to_response('NO.html', {'error':error})

@login_required
def user_add(request):
	user = request.user
	menger = Menger.objects.get(user=user)
	if menger.management != 1:
		error = "你没有权限！"
		return render_to_response('NO.html', {'error':error})
	if request.method == 'POST':
		form = AccountForm(request.POST)
		if form.is_valid():
			first_name = form.cleaned_data['first_name']
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			email = form.cleaned_data['email']
			management = form.cleaned_data['management']
			insurance = form.cleaned_data['insurance']
			business = form.cleaned_data['business']
			financing = form.cleaned_data['financing']
			is_active = True
			if insurance and business and financing or insurance and business or insurance and financing or business and financing:
				error = '只能选取一个部门权限'
				return render_to_response('No.html',{'error':error})
			salt = settings.SALT if hasattr(settings, 'SALT') else "asosfr"
			salted_password = make_password(password, salt)
			User.objects.create(username=username,password=salted_password,first_name=first_name,email=email,is_active=is_active)
			new_user = User.objects.get(username=username)
			Menger.objects.create(user=new_user,management=management,insurance=insurance,business=business,financing=financing)
			success = "创建成功"
			go_url_name = "返回主页"
			go_url = '/adm_accounts/'
			return render_to_response('OK.html',{'success':success,'go_url_name':go_url_name,'go_url':go_url})
		else:
			form = AccountForm(initial={
				'first_name': first_name,
				'username':username,
				'password':password,
				'email':email,
				'management':management,
				'insurance':insurance,
				'business':business,
				'financing':financing})
			error = form.errors
			return render(request,'adm_account_new.html',{'form':form,'error':error})
	else:
		form = AccountForm()
	return render(request,'adm_account_new.html',{'form':form})