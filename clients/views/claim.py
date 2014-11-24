from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView

from clients.models import Claim
from clients.forms.forms import ClaimForm


class UpdateClaimView(UpdateView):
    template_name = 'clients/claim/update_claim.html'
    model = Claim
    form_class = ClaimForm
    slug_field = "id"
    slug_url_kwarg = "claim_id"

    def get_success_url(self):
        client_id = self.object.claim.client.id
        self.success_url = reverse_lazy('client',
                                        kwargs={'client_id': client_id})
        return self.success_url


class DeleteClaimView(DeleteView):
    template_name = 'clients/claim/delete_claim.html'
    model = Claim
    slug_field = "id"
    slug_url_kwarg = "claim_id"
    success_url = reverse_lazy('claims')

    def get_success_url(self):
        client_id = self.object.client.id
        self.success_url = reverse_lazy('client',
                                        kwargs={'client_id': client_id})
        return self.success_url
