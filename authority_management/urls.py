from django.conf.urls import include,url
from authority_management import views

urlpatterns = [
	url(r'^user_list',views.user_list,name='user_list'),
	url(r'^user_add/$',views.user_add,name='user_add'),
	url(r'^user_change/(?P<user_id>\d+)$', views.user_change, name='user_change'),
	url(r'^user_del/(?P<user_id>\d+)$',views.user_del,name='user_del'),
]