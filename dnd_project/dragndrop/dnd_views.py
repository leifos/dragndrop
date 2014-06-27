__author__ = 'leif'
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect



def goto_url(request):
    return HttpResponse('goto url')

def user_list(request, username):
    return HttpResponse('user list')

def user_folder_list(request,username):
    return HttpResponse('user folder list')

def user_folder(request,username,folder_page_url):
    return HttpResponse('user folder')
