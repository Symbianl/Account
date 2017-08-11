# -*-coding:utf-8 -*-
from django import forms
from django.contrib.admin import widgets

TITLE_AUTHORITY_CHOICES = (
    ('0','关闭'),
    ('1','开启'),
)

#用户表单
class AccountForm(forms.Form):
    password = forms.CharField(label='用户密码：',
                               widget=forms.PasswordInput(attrs={"placeholder":"必填","value":"","required":"required"}),
                               max_length=45,error_messages={"required":u"必填","max_length":u"最大长度不超过45"})

    username = forms.CharField(label='用户账号：',
                               widget=forms.TextInput(attrs={"placeholder":'必填','value':"","required":"required"}),
                               max_length=45,error_messages={"required":u'必填',"max_length":u"最大长度不超过45"})

    email = forms.EmailField(label='电子邮箱:',
                             widget=forms.TextInput(attrs={"placeholder":'必填','value':'',"required":"required"}),
                             max_length=45,error_messages={"required":u"必填","max_length":u"最大长度不超过45"})

#登录表单
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':u"用户名"}),
        error_messages={'required':u'请输入用户名'},
        required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':u"密码"}),
        error_messages={'required':u'请输入密码'},
        required=True
    )
    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u'账号和密码必须填写')
        else:
            cleaned_data = super(LoginForm, self).clean()
            return cleaned_data

class ChangpwdForm(forms.Form):
    oldpwd = forms.CharField(
        label=u"原密码",
        error_messages={'required':u'请输入原密码'},
        widget=forms.PasswordInput(attrs={'placeholder':u'原密码','value':"","required":"required",}),
        required=True
    )
    newpwd = forms.CharField(
        required=True,
        label=u"新密码",
        error_messages={'required':u'请输入新密码'},
        widget=forms.PasswordInput(attrs={'placeholder':u"新密码","value":"","required":"required",}),
    )
    newpwd2 = forms.CharField(
        required=True,
        label=u"确认密码",
        error_messages={'required':u'请再次输入新密码'},
        widget=forms.PasswordInput(attrs={'placeholder':u'确认密码',"value":"","required":"required",}),
    )
    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"所有选项都为必填项")
        elif self.cleaned_data['newpwd']<>self.cleaned_data['newpwd2']:
            raise forms.ValidationError(u"两次输入的新密码不一样")
        else:
            cleaned_data = super(ChangpwdForm,self).clean()
            return cleaned_data
#权限表单
class YiheUserForm(forms.Form):
    first_name = forms.CharField(label="用户姓名：",required=False,
                                 widget=forms.TextInput(attrs={'placeholder':""}),max_length=45,error_messages={"required":u"必填","max_length":u"最大长度不超过45"})
    email = forms.EmailField(label='电子邮箱:',required=False)

    management = forms.IntegerField(label='全部权限',
                                    widget=forms.Select(choices=TITLE_AUTHORITY_CHOICES))

    insurance = forms.IntegerField(label='保险部权限:',
                                   widget=forms.Select(choices=TITLE_AUTHORITY_CHOICES))

    business = forms.IntegerField(label='业务部权限:',
                                  widget=forms.Select(choices=TITLE_AUTHORITY_CHOICES))

    financing = forms.IntegerField(label='融资部权限:',
                                   widget=forms.Select(choices=TITLE_AUTHORITY_CHOICES))