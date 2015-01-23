from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required

from inventory.views import views
from inventory.views.shoe import CreateShoeView, ListShoeView, \
    DetailShoeView, UpdateShoeView, DeleteShoeView


shoe_patterns = patterns(
    '',
    url(r'^$',
        login_required(ListShoeView.as_view()),
        name='shoe_list'),
    url(r'^(?P<pk>\d+)/$',
        login_required(DetailShoeView.as_view()),
        name='shoe_detail'),
    url(r'^update/(?P<pk>\d+)/$',
        login_required(UpdateShoeView.as_view()),
        name='shoe_update'),
    url(r'^delete/(?P<pk>\d+)/$',
        login_required(DeleteShoeView.as_view()),
        name='shoe_delete'),
    url(r'^create/$',
        login_required(CreateShoeView.as_view()),
        name='shoe_create'),
)

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='inventory_index'),
    url(r'^shoe/', include(shoe_patterns)),
)
