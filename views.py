from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import logout


def index(request):
    context = RequestContext(request)
    return render_to_response('index.html', context)


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
