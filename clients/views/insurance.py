from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView, CreateView

from clients.models import Insurance, CoverageType, Client, Dependent
from clients.forms.forms import InsuranceForm, CoverageForm


class UpdateInsuranceView(UpdateView):
    template_name = 'clients/insurance/update_insurance.html'
    model = Insurance
    form_class = InsuranceForm
    slug_field = "id"
    slug_url_kwarg = "insurance_id"

    def get_success_url(self):
        client_id = self.object.client.id
        self.success_url = reverse_lazy('client',
                                        kwargs={'client_id': client_id})
        return self.success_url


class DeleteInsuranceView(DeleteView):
    template_name = 'clients/insurance/delete_insurance.html'
    model = Insurance
    slug_field = "id"
    slug_url_kwarg = "insurance_id"

    def get_success_url(self):
        client_id = self.object.client.id
        self.success_url = reverse_lazy('client',
                                        kwargs={'client_id': client_id})
        return self.success_url


class CreateInsuranceView(CreateView):
    template_name = 'clients/insurance/create_insurance.html'
    model = Insurance
    form_class = InsuranceForm

    def get_context_data(self, **kwargs):
        context = super(CreateInsuranceView, self).get_context_data(**kwargs)
        client = Client.objects.get(id=self.kwargs['client_id'])
        coverage_form1 = CoverageForm(
            prefix="coverage_form1",
            initial={'coverage_type': CoverageType.ORTHOTICS,
                     'coverage_percent': 0,
                     'max_claim_amount': 0,
                     'quantity': 0,
                     'period': 0})
        coverage_form2 = CoverageForm(
            prefix="coverage_form2",
            initial={'coverage_type': CoverageType.COMPRESSION_STOCKINGS,
                     'coverage_percent': 0,
                     'max_claim_amount': 0,
                     'quantity': 0,
                     'period': 0})

        coverage_form3 = CoverageForm(
            prefix="coverage_form3",
            initial={'coverage_type': CoverageType.ORTHOPEDIC_SHOES,
                     'coverage_percent': 0,
                     'max_claim_amount': 0,
                     'quantity': 0,
                     'period': 0})

        context['coverage_form1'] = coverage_form1
        context['coverage_form2'] = coverage_form2
        context['coverage_form3'] = coverage_form3
        context['client'] = client

        return context

    def form_valid(self, form):
        coverage_form1 = CoverageForm(
            self.request.POST, prefix="coverage_form1",
            initial={'coverage_type': CoverageType.ORTHOTICS,
                     'coverage_percent': 0})
        coverage_form2 = CoverageForm(
            self.request.POST, prefix="coverage_form2",
            initial={'coverage_type': CoverageType.COMPRESSION_STOCKINGS})
        coverage_form3 = CoverageForm(
            self.request.POST, prefix="coverage_form3",
            initial={'coverage_type': CoverageType.ORTHOPEDIC_SHOES})

        if (coverage_form1.is_valid()
                and coverage_form2.is_valid()
                and coverage_form3.is_valid()):
            saved = form.save(commit=False)
            client = Client.objects.get(id=self.kwargs['client_id'])
            saved.client = client
            if 'spouse_id' in self.kwargs:
                spouse = Dependent.objects.get(id=self.kwargs['spouse_id'])
                saved.spouse = spouse
            saved.save()

            coverage_1 = coverage_form1.save(commit=False)
            if coverage_1.coverage_percent == 0:
                pass
            else:
                coverage_1.insurance = saved
                coverage_1.total_claimed = 0
                coverage_1.save()

            coverage_2 = coverage_form2.save(commit=False)
            if coverage_2.coverage_percent == 0:
                pass
            else:
                coverage_2.insurance = saved
                coverage_2.total_claimed = 0
                coverage_2.save()

            coverage_3 = coverage_form3.save(commit=False)
            if coverage_3.coverage_percent == 0:
                pass
            else:
                coverage_3.insurance = saved
                coverage_3.total_claimed = 0
                coverage_3.save()

            return HttpResponseRedirect(self.get_success_url(client))
        else:
            return self.form_invalid(form)

    def get_success_url(self, client):
        self.success_url = reverse_lazy('client',
                                        kwargs={'client_id': client.id})
        return self.success_url
