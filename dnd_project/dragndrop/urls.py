__author__ = 'leif'
from django.conf.urls import patterns, url
from dragndrop import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r''),
        url(r'^help', views.help, name='help'),
        url(r'^about', views.about, name='about'),
        url(r'^goto', user_views.goto_url, name='goto'),
        url(r'^users/$', user_views.list_of_users, name='list_of_users'),
        url(r'^users/(?P<username>\w+)/$', user_views.user_folder_list, name='user_folder_list'),
        url(r'^users/(?P<username>\w+)/(?P<folder_page_url>\w+)/$', user_views.user_folder_view, name='user_folder_view'),
        url(r'^(?P<folder_page_url>\w+)/$', views.folder, name='folderpage'),



)