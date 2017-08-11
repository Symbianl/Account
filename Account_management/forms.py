# -*-coding:utf-8 -*-
from django import forms
from models import ImportFile

class ImportFileForm(forms.Form):
	file= forms.FileField()