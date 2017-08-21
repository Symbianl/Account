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
		return render(request,'user_list.html',{'users':users})
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
			go_url = '/user_list/'
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
			return render(request,'user_add.html',{'form':form,'error':error})
	else:
		form = AccountForm()
	return render(request,'user_add.html',{'form':form})


@login_required
def user_change(request,user_id):
	user = User.objects.get(id = user_id)
	member = Menger.objects.get(user=user)
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
			avalue = User.objects.get(username=username)
			avalue.username = username
			avalue.password = password
			avalue.email = email
			avalue.first_name = first_name
			avalue.save()
			member.management = management
			member.insurance = insurance
			member.business = business
			member.financing = financing
			member.save()
			success = "修改成功"
			go_url_name = "返回主页"
			go_url = '/user_list/'
			return render_to_response('OK.html',{'success':success,'go_url_name':go_url_name,'go_url':go_url})
		else:
			form = AccountForm(initial={'username':username,
				'password':password,
				'email':email,
				'first_name':first_name,
				'management':management,
				'insurance':insurance,
				'business':business,
				'financing':financing})
			error = form.errors
			return render(request,'user_add.html',{'form':form,'error':error,'user_id':user_id})
	else:
		form = AccountForm(initial={'username':user.username,
				'password':user.password,
				'email':user.email,
				'first_name':user.first_name,
				'management':member.management,
				'insurance':member.insurance,
				'business':member.business,
				'financing':member.financing})
	return render(request,'user_add.html',{'form':form,'user_id':user_id})

def user_del(request,user_id):
	user = User.objects.get(id = user_id).delete()
	member = Menger.objects.get(user=user)
	if member.all_authority != 1:
		error = "你没有权限哦！"
		return render_to_response('NO.html', {'error':error})
	success = "删除成功"
	go_url_name ='返回'
	go_url = "/user_list/"
	return render_to_response('OK.html', {'success':success, 'go_url_name':go_url_name, 'go_url':go_url})