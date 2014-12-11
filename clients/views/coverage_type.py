from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView, CreateView

from clients.models import CoverageType, Insurance
from clients.forms.forms import CoverageForm


class UpdateCoverageTypeView(UpdateView):
    template_name = 'clients/coverage_type/update_coverage_type.html'
    model = CoverageType
    form_class = CoverageForm
    slug_field = "id"
    slug_url_kwarg = "coverage_type_id"

    def get_success_url(self):
        client_id = self.object.insurance.client.id
        self.success_url = reverse_lazy('client',
                                        kwargs={'client_id': client_id})
        return self.success_url


class DeleteCoverageTypeView(DeleteView):
    template_name = 'clients/coverage_type/delete_coverage_type.html'
    model = CoverageType
    slug_field = "id"
    slug_url_kwarg = "coverage_type_id"

    def get_success_url(self):
        client_id = self.object.insurance.client.id
        self.success_url = reverse_lazy('client',
                                        kwargs={'client_id': client_id})
        return self.success_url


class CreateCoverageTypeView(CreateView):
    template_name = 'clients/coverage_type/create_coverage_type.html'
    model = CoverageType
    form_class = CoverageForm

    def form_valid(self, form):
        saved = form.save(commit=False)
        insurance = Insurance.objects.get(id=self.kwargs['insurance_id'])
        saved.insurance = insurance
        saved.save()

        return HttpResponseRedirect(self.get_success_url(insurance))

    def get_success_url(self, insurance):
        self.success_url = reverse_lazy('insurance_update',
                                        kwargs={'insurance_id': insurance.id})
        return self.success_url
