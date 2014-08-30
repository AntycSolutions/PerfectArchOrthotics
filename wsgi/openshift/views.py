from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from clients.models import Client
from django.contrib.auth import authenticate, login

def index(request):
    context = RequestContext(request)

    return render_to_response('index.html', context)


def user_login(request):
    context = RequestContext(request)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Your account is deactivated")
        else:
            return HttpResponse("Invalid login details supplied")
    else:
        return render_to_response('login.html', {}, context)
