from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import DeleteView

from clients.models import Client


class DeleteClientView(DeleteView):
    template_name = 'clients/client/delete_client.html'
    model = Client
    slug_field = "id"
    slug_url_kwarg = "client_id"
    success_url = reverse_lazy('clients')
