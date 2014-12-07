from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect  # , HttpResponse
from django.template import RequestContext
from django.contrib.auth import logout  # , authenticate, login,
from django.contrib.auth.decorators import login_required

from clients.models import SiteStatistics


def index(request):
    context = RequestContext(request)
    statistics = SiteStatistics.objects.get_or_create(pk=0)[0]
    statistics.home_page_views += 1
    statistics.save()
    return render_to_response('index.html', context)


# def user_login(request):
#     context = RequestContext(request)
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(username=username, password=password)
#         if user:
#             if user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect('/')
#             else:
#                 return HttpResponse("Your account is inactive.")
#         else:
#             return HttpResponse("Invalid login, please try again.")
#     else:
#         return render_to_response('login.html', {}, context)


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
