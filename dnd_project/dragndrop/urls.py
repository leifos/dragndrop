__author__ = 'leif'
from django.conf.urls import patterns, url
from dragndrop import views, dnd_views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^help', views.help, name='help'),
        url(r'^about', views.about, name='about'),
        url(r'^goto', dnd_views.goto_url, name='goto'),
        url(r'^dnd/$', dnd_views.user_list, name='list_of_users'),
        url(r'^dnd/(?P<username>\w+)/$', dnd_views.user_folder_list, name='user_folder_list'),
        url(r'^dnd/(?P<username>\w+)/(?P<folder_page_url>\w+)/$', dnd_views.user_folder, name='user_folder_view'),

)