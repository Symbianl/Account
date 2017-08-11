# -*- coding:utf-8 -*-
from django.db import models
# Create your models here.

class Account_insurer(models.Model):
    number = models.CharField(max_length=45, blank=True, null=True)  # 编号
    insurer = models.CharField(max_length=45, blank=True, null=True)  # 保险公司
    ship_name = models.CharField(max_length=45)#船舶名称
    Clerk =models.CharField(max_length=45,blank=True,null=True)#业务员
    Insured_date =models.DateTimeField(blank=True,null=True)#投保时间
    Expired_date =models.DateTimeField(blank=True,null=True)#投保过期时间

    class Meta:
        db_table = 'account_insurer'


class Account_financing(models.Model):
    number = models.CharField(max_length=45,blank=True,null=True)#编号
    Blank = models.CharField(max_length=45,blank=True,null=True)#银行
    ship_name = models.CharField(max_length=45)#船舶名称
    Clerk = models.CharField(max_length=45,blank=True,null=True)#业务员
    sum = models.CharField(max_length=45,blank=True,null=True)#金额
    Borrower_user = models.CharField(max_length=45,blank=True,null=True)#借款人
    Borrower_Tel =models.BigIntegerField(blank=True,null=True) #联系方式
    Expired_date =models.DateTimeField(blank=True,null=True)#保单到期时间

    class Meta:
        db_table = 'account_financing'



class ImportFile(models.Model):#文件上传
    file = models.FileField(upload_to = './upload/')

    class Meta:
        ordering=['file']

    def __unicode__(self):
        return self.file







