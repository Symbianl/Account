#coding:utf-8
from __future__ import absolute_import

import logging
from celery import task
from celery.utils.log import get_task_logger
from celery.schedules import crontab
from django.core.mail import send_mail

from .models import Account_insurer,Account_financing
from datetime import datetime
from User_Management.models import Menger

@task
def check_insurance_list_expiration_time():
	message = ''
	insurance_list = Account_insurer.objects.all()
	members = Menger.objects.all()
	principal =[]
	for member in members:
		if member.all_authority and member.insurance:
			principal.append(member.user.email)
	for lists in insurance_list:
		Expired_date = lists.Expired_date
		now_time = datetime.now().date()
		if (Expired_date - now_time).total_seconds() <= 2592000 and (Expired_date - now_time).total_seconds() >0 and lists.due_notice :
			message += u'编号为：'
			message += str(lists.number)
			message += u' 保单到期时间：'
			message += lists.expire_time.strftime("%Y-%m-%d")
			message +='\n'
	if message.strip():
		message += u'以上保单还有将近一个月过期，请及时处理！！！'
		message += u'\n 关闭提醒功能请点击链接进行处理 http://192.168.1.189:8000/list/list_due_notice/'
		send_mail(u'保单到期提示', message, '313904661@qq.com',
		    principal)

@task
def check_finance_list_expiration_time():
	finance_list = Account_financing.objects.all()
	members = Menger.objects.all()
	message = ''
	principal =[]
	for member in members:
		if member.all_authority and member.finance:
			principal.append(member.user.email)
	for lists in finance_list:
		Expired_date = lists.Expired_date
		now_time = datetime.now().date()
		if (Expired_date - now_time).total_seconds() <= 2592000 and (Expired_date - now_time).total_seconds() >0 and lists.due_notice :
			message += u'编号为：'
			message += lists.number
			message += u' 保单到期时间：'
			message += lists.expire_time.strftime("%Y-%m-%d")
			message +='\n'
	if message.strip():
		message += u'以上保单还有将近一个月过期，请及时处理！！！'
		message += u'\n 关闭提醒功能请点击进行处理 http://192.168.1.189:8000/list/list_due_notice/'
		send_mail(u'保单到期提示', message, '313904661@qq.com',
		    principal)
