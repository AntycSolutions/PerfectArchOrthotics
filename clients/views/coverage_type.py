from django.http import HttpResponseRedirect
from django.core import urlresolvers
from django.views.generic.edit import UpdateView, DeleteView, CreateView

from utils import views_utils

from clients.models import Coverage, Insurance
from clients.forms.forms import CoverageForm


class UpdateCoverageView(UpdateView):
    template_name = 'clients/coverage_type/update_coverage.html'
    model = Coverage
    form_class = CoverageForm
    slug_field = "id"
    slug_url_kwarg = "coverage_type_id"

    def get_success_url(self):
        if 'client_id' in self.kwargs:
            self.success_url = urlresolvers.reverse_lazy(
                'claim_create',
                kwargs={'client_id': self.kwargs['client_id']})

            return self.success_url

        client_id = self.object.insurance.client.id
        self.success_url = urlresolvers.reverse_lazy(
            'client', kwargs={'client_id': client_id}
        )

        return self.success_url


# TODO: delete? it is unused, need to check permissions when updating insurance
#  as you can delete coverage there
class DeleteCoverageView(views_utils.PermissionMixin, DeleteView):
    template_name = 'clients/coverage_type/delete_coverage.html'
    model = Coverage
    slug_field = "id"
    slug_url_kwarg = "coverage_type_id"

    def get_permissions(self):
        permissions = {
            'permission': 'clients.delete_coverage',
            'redirect': self.get_object().insurance.get_absolute_url(),
        }

        return permissions

    def get_success_url(self):
        client_id = self.object.insurance.client.id
        self.success_url = urlresolvers.reverse_lazy(
            'client', kwargs={'client_id': client_id}
        )

        return self.success_url


class CreateCoverageView(CreateView):
    template_name = 'clients/coverage_type/create_coverage.html'
    model = Coverage
    form_class = CoverageForm

    def form_valid(self, form):
        saved = form.save(commit=False)
        insurance = Insurance.objects.get(id=self.kwargs['insurance_id'])
        saved.insurance = insurance
        saved.save()

        return HttpResponseRedirect(self.get_success_url(insurance))

    def get_success_url(self, insurance):
        self.success_url = urlresolvers.reverse_lazy(
            'insurance_update', kwargs={'insurance_id': insurance.id}
        )

        return self.success_url
