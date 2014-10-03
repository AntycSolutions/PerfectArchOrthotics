from django.conf.urls import patterns, url
from clients import views

urlpatterns = \
    patterns('',
             url(r'^$', views.index, name='client_index'),
             url(r'^add_insurance/(?P<client_id>\w+)', views.add_insurance, name='add_insurance'),
             url(r'^add_dependent/(?P<client_id>\w+)', views.add_dependent, name='add_dependent'),
             url(r'^add_client/', views.add_client, name='add_client'),
             url(r'^client_search/', views.clientSearchView, name='client_search'),
             url(r'^claim_search/', views.claimSearchView, name='claim_search'),
             url(r'^insurance_search/', views.insuranceSearchView, name='insurance_search'),
             url(r'^(?P<client_id>\w+)/$', views.clientView, name='client'),
             url(r'^claims', views.claimsView, name='claims'),
             url(r'^(?P<client_id>\w+)/claim/(?P<claim_id>\w+)', views.claimView, name='claim'),
             url(r'^insurance', views.insuranceView, name='insurance'),
             url(r'^pdftest.pdf$', views.HelloPDFView.as_view(), name='pdf'),
             url(r'^pdftest2.pdf$', views.myview, name='pdf2'),
             url(r'^pdftest3.pdf$', views.insurance_letter, name='insurance_letter'),
             url(r'^pdftest4.pdf$', views.proof_of_manufacturing, name='proof'),
             url(r'^edit_client/(?P<client_id>\w+)', views.editClientView, name='client_edit'),
             url(r'^make_claim/(?P<client_id>\w+)', views.makeClaimView, name='make_claim'),
             url(r'^edit_dependant/(?P<client_id>\w+)/(?P<dependent_id>\w+)',
                 views.editDependantsView, name='dependant_edit'),
             url(r'^delete_dependant/(?P<client_id>\w+)/(?P<dependent_id>\w+)',
                 views.deleteDependantsView, name='dependant_delete'),
             url(r'^add_new_dependent/(?P<client_id>\w+)', views.add_new_dependent, name='add_new_dependent'),
             )
