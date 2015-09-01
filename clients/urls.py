from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required

from clients.views import views
from clients.views.insurance import UpdateInsuranceView, DeleteInsuranceView, \
    CreateInsuranceView
from clients.views.client import CreateClientView, DeleteClientView
from clients.views.coverage_type import UpdateCoverageView, \
    DeleteCoverageView, CreateCoverageView
from clients.views.claim import UpdateClaimView, DeleteClaimView, \
    UpdateInvoiceView, CreateInvoiceView, UpdateInsuranceLetterView, \
    CreateInsuranceLetterView, UpdateProofOfManufacturingView, \
    CreateProofOfManufacturingView, CreateClaimView
from .views.item import CreateItemView, ListItemView, DetailItemView, \
    UpdateItemView, DeleteItemView
from clients.views import statistics


item_patterns = patterns(
    '',
    url(r'^$',
        login_required(ListItemView.as_view()),
        name='item_list'),
    url(r'^(?P<pk>\d+)/$',
        login_required(DetailItemView.as_view()),
        name='item_detail'),
    url(r'^update/(?P<pk>\d+)/$',
        login_required(UpdateItemView.as_view()),
        name='item_update'),
    url(r'^delete/(?P<pk>\d+)/$',
        login_required(DeleteItemView.as_view()),
        name='item_delete'),
    url(r'^create/$',
        login_required(CreateItemView.as_view()),
        name='item_create'),
)

insurance_patterns = patterns(
    '',
    url(r'^$',
        login_required(views.insuranceSearchView),
        name='insurance'),
    url(r'^update/(?P<insurance_id>\w+)/$',
        login_required(UpdateInsuranceView.as_view()),
        name='insurance_update'),
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
    url(r'^update/(?P<coverage_type_id>\w+)/$',
        login_required(UpdateCoverageView.as_view()),
        name='coverage_type_update'),
    url(r'^update/(?P<coverage_type_id>\w+)/(?P<client_id>\w+)/$',
        login_required(UpdateCoverageView.as_view()),
        name='coverage_type_update_from_claim'),
    url(r'^delete/(?P<coverage_type_id>\w+)/$',
        login_required(DeleteCoverageView.as_view()),
        name='coverage_type_delete'),
    url(r'^create/(?P<insurance_id>\w+)/$',
        login_required(CreateCoverageView.as_view()),
        name='coverage_type_create'),
)

claim_patterns = patterns(
    '',
    url(r'^$',
        login_required(views.claimSearchView),
        name='claims'),
    url(r'^create/(?P<client_id>\w+)/$',
        login_required(CreateClaimView.as_view()),
        name='claim_create'),
    url(r'^update/(?P<claim_id>\w+)/$',
        login_required(UpdateClaimView.as_view()),
        name='claim_update'),
    url(r'^delete/(?P<claim_id>\w+)/$',
        login_required(DeleteClaimView.as_view()),
        name='claim_delete'),
    url(r'^invoice/update/(?P<invoice_id>\w+)/$',
        login_required(UpdateInvoiceView.as_view()),
        name='invoice_update'),
    url(r'^invoice/create/(?P<claim_id>\w+)/$',
        login_required(CreateInvoiceView.as_view()),
        name='invoice_create'),
    url(r'^insurance_letter/update/(?P<insurance_letter_id>\w+)/$',
        login_required(UpdateInsuranceLetterView.as_view()),
        name='insurance_letter_update'),
    url(r'^insurance_letter/create/(?P<claim_id>\w+)/$',
        login_required(CreateInsuranceLetterView.as_view()),
        name='insurance_letter_create'),
    url(r'^proof_of_manufacturing/update/(?P<proof_of_manufacturing_id>\w+)/$',
        login_required(UpdateProofOfManufacturingView.as_view()),
        name='proof_of_manufacturing_update'),
    url(r'^proof_of_manufacturing/create/(?P<claim_id>\w+)/$',
        login_required(CreateProofOfManufacturingView.as_view()),
        name='proof_of_manufacturing_create'),
)

# TODO: make this not gross
urlpatterns = patterns(
    '',  # Tells django to view the rest as str
    url(r'^$',
        login_required(views.clientSearchView),
        name='client_list'),
    url(r'^add_dependent/(?P<client_id>\w+)/$',
        login_required(views.add_dependent),
        name='add_dependent'),
    url(r'^add_client/$',
        login_required(views.add_client),
        name='add_client'),
    url(r'^add_client_test/$',
        login_required(CreateClientView.as_view()),
        name='add_client_test'),
    url(r'^(?P<client_id>\d+)/$',
        login_required(views.clientView),
        name='client'),
    url(r'^claim/', include(claim_patterns)),
    url(r'^claim/(?P<claim_id>\w+)/$',
        login_required(views.claimView),
        name='claim'),
    url(r'^claim/(?P<claim_id>\w+)/invoice/$',
        login_required(views.invoice_view),
        name='invoice'),
    url(r'^claim/(?P<claim_id>\w+)/insurance_letter/$',
        login_required(views.insurance_letter_view),
        name='insurance_letter'),
    url(r'^claim/(?P<claim_id>\w+)/proof_of_manufacturing/$',
        login_required(views.proof_of_manufacturing_view),
        name='proof'),
    url(r'^claim/(?P<claim_id>\w+)/fill_out_invoice/$',
        login_required(views.fillOutInvoiceView),
        name='fillOutInvoice'),
    url(r'^claim/(?P<claim_id>\w+)/fill_out_insurance_letter/$',
        login_required(views.fillOutInsuranceLetterView),
        name='fillOutInsurance'),
    url(r'^claim/(?P<claim_id>\w+)/fill_out_proof_of_manufacturing/$',
        login_required(views.fillOutProofOfManufacturingView),
        name='fillOutProof'),
    url(r'^insurance/', include(insurance_patterns)),
    url(r'^coverage_type/', include(coverage_type_patterns)),
    url(r'^item/', include(item_patterns)),
    url(r'^edit_client/(?P<client_id>\w+)/$',
        login_required(views.editClientView),
        name='client_edit'),
    url(r'^delete_client/(?P<client_id>\w+)/$',
        login_required(DeleteClientView.as_view()),
        name='client_delete'),
    # url(r'^make_claim/(?P<client_id>\w+)/$',
    #     login_required(views.makeClaimView),
    #     name='make_claim'),
    url(r'^edit_dependent/(?P<client_id>\w+)/(?P<dependent_id>\w+)/$',
        login_required(views.editDependentsView),
        name='dependent_edit'),
    url(r'^delete_dependent/(?P<client_id>\w+)/(?P<dependent_id>\w+)/$',
        login_required(views.deleteDependentsView),
        name='dependent_delete'),
    url(r'^add_new_dependent/(?P<client_id>\w+)/$',
        login_required(views.add_new_dependent),
        name='add_new_dependent'),
    url(r'^statistics/claims/$',
        login_required(statistics.ClaimsStatistics.as_view()),
        name='claims_statistics'),
    url(r'^statistics/inventory_orders/$',
        login_required(statistics.InventoryOrdersStatistics.as_view()),
        name='inventory_orders_statistics'),
)
