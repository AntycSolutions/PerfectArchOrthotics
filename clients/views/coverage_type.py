from django.views.generic.edit import UpdateView, DeleteView

from clients.models import CoverageType
from clients.forms import CoverageForm


class UpdateCoverageTypeView(UpdateView):
    template_name = 'clients/coverage_type/update_coverage_type.html'
    model = CoverageType
    form_class = CoverageForm
    slug_field = "id"
    slug_url_kwarg = "coverage_type_id"


class DeleteCoverageTypeView(DeleteView):
    template_name = 'clients/coverage_type/delete_coverage_type.html'
    model = CoverageType
    slug_field = "id"
    slug_url_kwarg = "coverage_type_id"
