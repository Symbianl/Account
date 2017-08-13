from django.conf.urls import include,url
from authority_management import views

urlpatterns = [
	url(r'^adm_accounts',views.user_list,name='adm_accounts'),
	url(r'^adm_account_new/$',views.user_add,name='adm_account_new')
]