"""Account URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from User_Management import views as User_Management_views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/', User_Management_views.index, name='index'),
    url(r'^$',User_Management_views.login,name='login'),
    url(r'^login/$',User_Management_views.login,name='login'),
    url(r'^changepwd/$',User_Management_views.changepwd,name='changepwd'),
    url(r'^logout/',User_Management_views.logout,name='logout'),
    url(r'^user/',User_Management_views.user,name='user'),
    url(r'^',include('Account_management.urls')),
    url(r'^',include('authority_management.urls')),
]












