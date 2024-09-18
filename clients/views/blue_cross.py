from django import http, shortcuts
from django.views import generic
from django.core import urlresolvers
from django.conf import settings
from django.contrib.auth import mixins

from utils import views_utils

from perfect_arch_orthotics.templatetags import groups as tt_groups
from clients import models as clients_models
from clients.views import views as clients_views
from clients.forms import blue_cross_forms


class BlueCrossCreate(mixins.UserPassesTestMixin, generic.CreateView):
    model = clients_models.BlueCross
    template_name = 'clients/claim/blue_cross/create.html'
    form_class = blue_cross_forms.BlueCrossModelForm

    def test_func(self):
        return tt_groups.check_groups(self.request.user, 'Edit')

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


class BlueCrossUpdate(mixins.UserPassesTestMixin, generic.UpdateView):
    model = clients_models.BlueCross
    template_name = 'clients/claim/blue_cross/update.html'
    form_class = blue_cross_forms.BlueCrossModelForm

    def test_func(self):
        return tt_groups.check_groups(self.request.user, 'Edit')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['save_text'] = 'update'
        context['model_name'] = self.model._meta.verbose_name
        context['cancel_url'] = self.object.get_absolute_url()

        return context


class BlueCrossDelete(
    mixins.UserPassesTestMixin,
    views_utils.PermissionMixin,
    generic.DeleteView,
):
    model = clients_models.BlueCross
    template_name = 'utils/generics/delete.html'

    def test_func(self):
        return tt_groups.check_groups(self.request.user, 'Edit')

    def get_permissions(self):
        permissions = {
            'permission': 'clients.delete_bluecross',
            'redirect': self.get_object().get_absolute_url(),
        }

        return permissions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_name'] = self.model._meta.verbose_name
        context['cancel_url'] = self.object.get_absolute_url()

        return context

    def get_success_url(self):
        url = urlresolvers.reverse(
            'claim', kwargs={'claim_id': self.kwargs['claim_pk']}
        )

        return url


def blue_cross_fill_out(request, claim_pk):
    try:
        claim = clients_models.Claim.objects.get(id=claim_pk)
    except clients_models.Claim.DoesNotExist:
        raise http.Http404("No Claim matches that ID")
    patient = claim.patient
    blue_cross = None
    try:
        blue_cross = claim.bluecross
    except clients_models.BlueCross.DoesNotExist:
        pass

    context = {'blue_cross': blue_cross, 'patient': patient, 'claim': claim}

    return shortcuts.render(
        request, 'clients/claim/blue_cross/fill_out.html', context
    )


def blue_cross_pdf(request, pk):
    blue_cross = clients_models.BlueCross.objects.select_related(
        'claim',
    ).get(pk=pk)
    patient = blue_cross.claim.patient
    phone = settings.BILL_TO[0][1].split('\n')[4].replace('Phone: ', '')

    context = {'blue_cross': blue_cross, 'patient': patient, 'phone': phone}

    # for debugging
    # return shortcuts.render(request, 'clients/pdfs/blue_cross.html', context)
    return clients_views.render_to_pdf(
        request, 'clients/pdfs/blue_cross.html', context
    )
