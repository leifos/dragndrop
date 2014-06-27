from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from find.search.engine import EngineFactory
from find.search.query import Query
e = EngineFactory('dummy')




def index(request):
    context = RequestContext(request)
    q = Query('one')
    r = e.search(q)
    print r

    return render_to_response('dragndrop/index.html', {}, context)
