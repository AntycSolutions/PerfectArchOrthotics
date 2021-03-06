from django.core import urlresolvers
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth import mixins

from utils import views_utils

from perfect_arch_orthotics.templatetags import groups as tt_groups
from clients.models import Client
from clients.forms.forms import ClientForm


class CreateClientView(mixins.UserPassesTestMixin, CreateView):
    template_name = 'clients/client/create_client.html'
    model = Client
    form_class = ClientForm

    def test_func(self):
        return tt_groups.check_groups(self.request.user, 'Edit')

    def get_success_url(self):
        client_id = self.object.id
        self.success_url = urlresolvers.reverse_lazy(
            'client', kwargs={'client_id': client_id}
        )
        return self.success_url


class DeleteClientView(
    mixins.UserPassesTestMixin, views_utils.PermissionMixin, DeleteView
):
    template_name = 'utils/generics/delete.html'
    model = Client
    slug_field = "id"
    slug_url_kwarg = "client_id"
    success_url = urlresolvers.reverse_lazy('client_list')

    def test_func(self):
        return tt_groups.check_groups(self.request.user, 'Edit')

    def get_permissions(self):
        permissions = {
            'permission': 'inventory.delete_shoeorder',
            'redirect': self.get_object().get_absolute_url(),
        }

        return permissions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_name'] = self.model._meta.verbose_name
        context['cancel_url'] = self.object.get_absolute_url()

        return context
