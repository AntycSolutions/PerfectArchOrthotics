from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from clients.models import Client

def index(request):
    context = RequestContext(request)

    return render_to_response('index.html', context)


