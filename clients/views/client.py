from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import DeleteView

from clients.models import Client


class DeleteClientView(DeleteView):
    template_name = 'clients/client/delete_client.html'
    model = Client
    slug_field = "id"
    slug_url_kwarg = "client_id"
    success_url = reverse_lazy('client_index')

    def get_success_url(self):
        client_id = self.object.id
        self.success_url = reverse_lazy('client',
                                        kwargs={'client_id': client_id})
        return self.success_url
