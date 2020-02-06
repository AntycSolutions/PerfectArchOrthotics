from django.views.generic.edit import DeleteView
from django.contrib.auth import mixins

from utils import views_utils

from perfect_arch_orthotics.templatetags import groups as tt_groups
from clients import models as clients_models


class DeleteDependentView(
    mixins.UserPassesTestMixin, views_utils.PermissionMixin, DeleteView
):
    template_name = 'utils/generics/delete.html'
    model = clients_models.Dependent

    def test_func(self):
        return tt_groups.check_groups(self.request.user, 'Edit')

    def get_permissions(self):
        permissions = {
            'permission': 'clients.delete_dependent',
            'redirect': self.get_object().get_absolute_url(),
        }

        return permissions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_name'] = self.model._meta.verbose_name
        context['cancel_url'] = self.object.get_absolute_url()

        return context

    def get_success_url(self):
        self.success_url = self.object.primary.get_absolute_url()

        return self.success_url
