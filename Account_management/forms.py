# -*-coding:utf-8 -*-
from django import forms
import re
from django.core.exceptions import ValidationError

def phone(value):
	phone_re=re.compile(r'^[0-9]{11}$')
	if not phone_re.match(value):
		raise ValidationError('手机号码格式错误')

#保险表单
class insurerForm(forms.Form):
	number=forms.CharField(label='编号：', widget=forms.TextInput(attrs={"placeholder":\
    "必填", "value": "", "required": "required", }), max_length=45,\
    error_messages={"required":u"必填", "max_length":u"最大长度不超过45"})

	insurer =forms.CharField(label='保险公司：', widget=forms.TextInput(attrs={"placeholder":\
    "必填", "value": "", "required": "required", }), max_length=45,\
    error_messages={"required":u"必填", "max_length":u"最大长度不超过45"})

	ship_name = forms.CharField(label='船舶名称：', widget=forms.TextInput(attrs={"placeholder":\
    "必填", "value": "", "required": "required", }), max_length=45,\
    error_messages={"required":u"必填", "max_length":u"最大长度不超过45"})

	clerk = forms.CharField(label='业务员：', widget=forms.TextInput(attrs={"placeholder":\
    "必填", "value": "", "required": "required", }), max_length=45,\
    error_messages={"required":u"必填", "max_length":u"最大长度不超过45"})

	insured_date = forms.DateField(label='保单时间：', required=False,\
    widget=forms.DateInput(attrs={"readonly":"true"}))

	expired_date =forms.DateField(label='到期时间：', required=False,\
    widget=forms.DateInput(attrs={"readonly":"true"}))

class financingForm(forms.Form):
	unmber =forms.CharField(label='编号：', widget=forms.TextInput(attrs={"placeholder":\
    "必填", "value": "", "required": "required", }), max_length=45,\
    error_messages={"required":u"必填", "max_length":u"最大长度不超过45"})

	blank =forms.CharField(label='银行：', widget=forms.TextInput(attrs={"placeholder":\
    "必填", "value": "", "required": "required", }), max_length=45,\
    error_messages={"required":u"必填", "max_length":u"最大长度不超过45"})

	ship_name=forms.CharField(label='船舶名称：', widget=forms.TextInput(attrs={"placeholder":\
    "必填", "value": "", "required": "required", }), max_length=45,\
    error_messages={"required":u"必填", "max_length":u"最大长度不超过45"})

	clerk =forms.CharField(label='业务员：', widget=forms.TextInput(attrs={"placeholder":\
    "必填", "value": "", "required": "required", }), max_length=45,\
    error_messages={"required":u"必填", "max_length":u"最大长度不超过45"})

	sum =forms.CharField(label='金额：', widget=forms.TextInput(attrs={"placeholder":\
    "必填", "value": "", "required": "required", }), max_length=45,\
    error_messages={"required":u"必填", "max_length":u"最大长度不超过45"})

	borrower_user =forms.CharField(label='借款人：', widget=forms.TextInput(attrs={"placeholder":\
    "必填", "value": "", "required": "required", }), max_length=45,\
    error_messages={"required":u"必填", "max_length":u"最大长度不超过45"})

	borrower_tel = forms.CharField(label='借款人电话：',required=False,
		validators=[phone,],
		widget=forms.TextInput(attrs={}),
		max_length=11)

	expired_date =forms.DateField(label='保单到期时间：', required=False,\
    widget=forms.DateInput(attrs={"readonly":"true"}))






















