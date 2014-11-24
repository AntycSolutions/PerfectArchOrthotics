from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required

from clients.views import views
from clients.views.insurance import UpdateInsuranceView, DeleteInsuranceView, \
    CreateInsuranceView
from clients.views.client import DeleteClientView
from clients.views.coverage_type import UpdateCoverageTypeView, \
    DeleteCoverageTypeView


insurance_patterns = patterns(
    '',
    url(r'^$', views.insuranceView, name='insurance'),
    url(r'^edit/(?P<insurance_id>\w+)/$',
        login_required(UpdateInsuranceView.as_view()),
        name='insurance_edit'),
    url(r'^delete/(?P<insurance_id>\w+)/$',
        login_required(DeleteInsuranceView.as_view()),
        name='insurance_delete'),
    url(r'^create/(?P<client_id>\w+)/$',
        login_required(CreateInsuranceView.as_view()),
        name='insurance_create'),
    url(r'^create/(?P<client_id>\w+)/(?P<spouse_id>\w+)/$',
        login_required(CreateInsuranceView.as_view()),
        name='insurance_create_spouse'),
)

coverage_type_patterns = patterns(
    '',
    url(r'^edit/(?P<coverage_type_id>\w+)/$',
        login_required(UpdateCoverageTypeView.as_view()),
        name='coverage_type_edit'),
    url(r'^delete/(?P<coverage_type_id>\w+)/$',
        login_required(DeleteCoverageTypeView.as_view()),
        name='coverage_type_delete'),
)

#TODO: make this not gross
urlpatterns = patterns(
    '',  # Tells django to view the rest as str
    url(r'^$', views.index, name='client_index'),
    url(r'^add_insurance/(?P<client_id>\w+)/$', views.add_insurance,
        name='add_insurance'),
    url(r'^add_dependent/(?P<client_id>\w+)/$', views.add_dependent,
        name='add_dependent'),
    url(r'^add_client/$', views.add_client, name='add_client'),
    url(r'^client_search/$', views.clientSearchView, name='client_search'),
    url(r'^claim_search/$', views.claimSearchView, name='claim_search'),
    url(r'^insurance_search/$', views.insuranceSearchView,
        name='insurance_search'),
    url(r'^(?P<client_id>\d+)/$', views.clientView, name='client'),
    url(r'^claims/$', views.claimsView, name='claims'),
    url(r'^(?P<client_id>\d+)/claim/(?P<claim_id>\w+)/$', views.claimView,
        name='claim'),
    url(r'^(?P<client_id>\d+)/claim/(?P<claim_id>\w+)/invoice/$',
        views.invoice_view, name='invoice'),
    url(r'^(?P<client_id>\d+)/claim/(?P<claim_id>\w+)/insurance_letter/$',
        views.insurance_letter, name='insurance_letter'),
    url(r'^(?P<client_id>\d+)/claim/(?P<claim_id>\w+)/proof_of_manufacturing/$',
        views.proof_of_manufacturing, name='proof'),
    url(r'^(?P<client_id>\d+)/claim/(?P<claim_id>\w+)/fill_out_invoice/$',
        views.fillOutInvoiceView, name='fillOutInvoice'),
    url(r'^(?P<client_id>\d+)/claim/(?P<claim_id>\w+)/fill_out_insurance_letter/$',
        views.fillOutInsuranceLetterView, name='fillOutInsurance'),
    url(r'^(?P<client_id>\d+)/claim/(?P<claim_id>\w+)/fill_out_proof_of_manufacturing/$',
        views.fillOutProofOfManufacturingView, name='fillOutProof'),
    url(r'^insurance/', include(insurance_patterns)),
    url(r'^coverage_type/', include(coverage_type_patterns)),
    url(r'^pdftest.pdf$', views.HelloPDFView.as_view(), name='pdf'),
    url(r'^pdftest2.pdf$', views.invoice_view, name='invoice'),
    url(r'^pdftest3.pdf$', views.insurance_letter,
        name='insurance_letter'),
    url(r'^pdftest4.pdf$', views.proof_of_manufacturing, name='proof'),
    url(r'^edit_client/(?P<client_id>\w+)/$', views.editClientView,
        name='client_edit'),
    url(r'^delete_client/(?P<client_id>\w+)/$',
        login_required(DeleteClientView.as_view()),
        name='client_delete'),
    url(r'^make_claim/(?P<client_id>\w+)/$', views.makeClaimView,
        name='make_claim'),
    url(r'^edit_dependent/(?P<client_id>\w+)/(?P<dependent_id>\w+)/$',
        views.editDependentsView, name='dependent_edit'),
    url(r'^delete_dependent/(?P<client_id>\w+)/(?P<dependent_id>\w+)/$',
        views.deleteDependentsView, name='dependent_delete'),
    url(r'^add_new_dependent/(?P<client_id>\w+)/$', views.add_new_dependent,
        name='add_new_dependent'),
)
