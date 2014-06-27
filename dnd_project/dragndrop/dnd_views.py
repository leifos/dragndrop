__author__ = 'leif'
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
import json

from folders import get_user_folders

def get_user(username):
    try:
        u = User.objects.get(username=username)
    except:
        u = None
    return u

def return_json(request):
    json_response = False
    if request.method == 'GET':
        if request.GET['type'] == 'json':
            json_response = True
    return json_response


def goto_url(request):
    return HttpResponse('goto url')

def user_list(request):
    context = RequestContext(request)
    ulist = User.objects.all()

    if return_json(request):
        nul = []
        for u in ulist:
            nul.append(u.username)
        return HttpResponse(json.dumps(nul))
    else:
        return render_to_response('dragndrop/user_list.html', { 'all_users': ulist }, context)

def user_folder_list(request,username):
    context = RequestContext(request)
    u = get_user(username)
    flist = []
    if u:
        flist = get_user_folders(u)


    if return_json(request):
        ufl = []
        for f in flist:
            ufl.append(f.name)
        return HttpResponse(json.dumps({'owner':u.username, 'folders': ufl } ))

    else:
        return render_to_response('dragndrop/user_folder_list.html', { 'owner': u, 'folders': flist }, context )


def user_folder(request,username,folder_page_url):

    return HttpResponse('user folder')
