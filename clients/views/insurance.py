from django.views.generic.edit import UpdateView, DeleteView

from clients.models import Insurance
from clients.forms import InsuranceForm


class UpdateInsuranceView(UpdateView):
    template_name = 'clients/insurance/update_insurance.html'
    model = Insurance
    form_class = InsuranceForm
    slug_field = "id"
    slug_url_kwarg = "insurance_id"


class DeleteInsuranceView(DeleteView):
    template_name = 'clients/insurance/delete_insurance.html'
    model = Insurance
    slug_field = "id"
    slug_url_kwarg = "insurance_id"
