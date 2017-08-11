from django.conf.urls import include,url
from Account_management import views

urlpatterns = [
	url(r'^list',views.inquire,name='list'),
	url(r'^file_upload/$',views.file_upload,name='file_upload')
]