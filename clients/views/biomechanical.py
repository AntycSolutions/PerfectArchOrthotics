from django import http
from django import template
from django import shortcuts
from django.views import generic
from django.conf import settings
from django.core import urlresolvers

from utils import views_utils

from clients import models as clients_models
from clients.views import views as clients_views
from clients.forms import claim_forms


class BiomechanicalCreate(generic.CreateView):
    model = clients_models.Biomechanical
    template_name = 'clients/claim/biomechanical.html'
    form_class = claim_forms.BiomechanicalModelForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['save_text'] = 'create'
        context['model_name'] = self.model._meta.verbose_name
        context['cancel_url'] = urlresolvers.reverse(
            'claim', kwargs={'claim_id': self.kwargs['claim_pk']}
        )

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.claim_id = self.kwargs['claim_pk']
        self.object.save()

        return http.HttpResponseRedirect(self.get_success_url())


class BiomechanicalUpdate(generic.UpdateView):
    model = clients_models.Biomechanical
    template_name = 'clients/claim/biomechanical.html'
    form_class = claim_forms.BiomechanicalModelForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['save_text'] = 'update'
        context['model_name'] = self.model._meta.verbose_name
        context['cancel_url'] = self.object.get_absolute_url()

        return context


class BiomechanicalDelete(views_utils.PermissionMixin, generic.DeleteView):
    model = clients_models.Biomechanical
    template_name = 'utils/generics/delete.html'

    def get_permissions(self):
        permissions = {
            'permission': 'clients.delete_biomechanical',
            'redirect': self.get_object().get_absolute_url(),
        }

        return permissions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_name'] = self.model._meta.verbose_name
        context['cancel_url'] = self.object.get_absolute_url()

        return context

    def get_success_url(self):
        return urlresolvers.reverse(
            'claim', kwargs={'claim_id': self.kwargs['claim_pk']}
        )


def _biomechanical(claim_pk):
    claim = clients_models.Claim.objects.select_related(
        'patient', 'biomechanical'
    ).get(pk=claim_pk)
    try:
        biomechanical = claim.biomechanical
    except clients_models.Biomechanical.DoesNotExist:
        biomechanical = None

    return claim, biomechanical


def biomechanical_fill_out(request, claim_pk):
    context = template.RequestContext(request)

    claim, biomechanical = _biomechanical(claim_pk)

    return shortcuts.render_to_response(
        'clients/make_biomechanical.html',
        {
            'claim': claim,
            'biomechanical': biomechanical,
        },
        context
    )


def biomechanical_pdf(request, claim_pk):
    claim, biomechanical = _biomechanical(claim_pk)

    # return shortcuts.render(
    #     request,
    #     'clients/pdfs/biomechanical.html',
    #     {
    #         'title': "Bio-mechanical Examination",
    #         'claim': claim,
    #         'biomechanical': biomechanical,
    #         'address': settings.BILL_TO[0][1],
    #         'email': settings.DANNY_EMAIL,
    #     }
    # )
    return clients_views.render_to_pdf(
        request,
        'clients/pdfs/biomechanical.html',
        {
            'title': "Bio-mechanical/Gait Examination",
            'claim': claim,
            'biomechanical': biomechanical,
            'address': settings.BILL_TO[0][1],
            'email': settings.DANNY_EMAIL,
        }
    )
