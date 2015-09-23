from django.views.generic.edit import DeleteView

from clients import models as clients_models


class DeleteDependentView(DeleteView):
    template_name = 'utils/generics/delete.html'
    model = clients_models.Dependent

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_name'] = self.model._meta.verbose_name
        context['cancel_url'] = self.object.get_absolute_url()

        return context

    def get_success_url(self):
        self.success_url = self.object.client.get_absolute_url()

        return self.success_url
