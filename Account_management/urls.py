from django.conf.urls import include,url
from Account_management import views

urlpatterns = [
	url(r'^list',views.inquire,name='list'),
	url(r'^file_upload/$',views.file_upload,name='file_upload'),
	url(r'^new',views.Entry_information,name='new'),
	url(r'^info',views.info_list,name='info'),
#	url(r'^del_info/(?P<list_id>\d+)$', views.del_info, name='del_info'),
#	url(r'^nwe_data/(?P<list_id>\d+)$', views.Modify_content, name='new_data'),

]