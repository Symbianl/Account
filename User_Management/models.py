# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Menger(models.Model):
    user = models.OneToOneField(User)
    management = models.IntegerField(blank=True,null=True)#管理
    insurance = models.IntegerField(blank=True,null=True)#保险
    business = models.IntegerField(blank=True,null=True)#业务
    financing = models.IntegerField(blank=True,null=True)#融资

    def __unicode__(self):
        return self.user.first_name
