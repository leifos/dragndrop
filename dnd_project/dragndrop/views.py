from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect

def index(request):
    context = RequestContext(request)
    return render_to_response('dragndrop/index.html', {}, context)
