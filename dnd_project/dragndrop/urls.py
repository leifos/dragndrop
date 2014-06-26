__author__ = 'leif'
from django.conf.urls import patterns, url
from dragndrop import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'))