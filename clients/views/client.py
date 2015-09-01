from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView

from clients.models import Client
from clients.forms.forms import ClientForm


class CreateClientView(CreateView):
    template_name = 'clients/client/create_client.html'
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        client_id = self.object.id
        self.success_url = reverse_lazy('client',
                                        kwargs={'client_id': client_id})
        return self.success_url


class DeleteClientView(DeleteView):
    template_name = 'utils/generics/delete.html'
    model = Client
    slug_field = "id"
    slug_url_kwarg = "client_id"
    success_url = reverse_lazy('client_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_name'] = self.model._meta.verbose_name
        context['cancel_url'] = self.object.get_absolute_url()

        return context
