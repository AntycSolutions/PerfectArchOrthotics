from django.conf.urls import patterns, url
from clients import views

urlpatterns = \
    patterns('',
             url(r'^$', views.index, name='index'),
             url(r'^add_client/$', views.add_client, name='add_client'),
             url(r'^(?P<client_id>\w+)/$', views.clientView, name='client'),
             )
