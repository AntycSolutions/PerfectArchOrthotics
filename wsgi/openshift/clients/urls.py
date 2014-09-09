from django.conf.urls import patterns, url
from clients import views

urlpatterns = \
    patterns('',
             url(r'^$', views.index, name='index'),
             url(r'^add_client/$', views.add_client, name='add_client'),
             url(r'^client_search/', views.clientSearchView, name='client_search'),
             url(r'^claim_search/', views.claimSearchView, name='claim_search'),
             url(r'^insurance_search/', views.insuranceSearchView, name='insurance_search'),
             url(r'^(?P<client_id>\w+)/$', views.clientView, name='client'),
             url(r'^claims', views.claimsView, name='claims'),
             url(r'^insurance', views.insuranceView, name='insurance'),
             )
