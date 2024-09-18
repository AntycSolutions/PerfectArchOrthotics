import json

from django import http
from django import shortcuts
from django.views import generic
from django.conf import settings
from django.core import urlresolvers
from django.contrib.auth import mixins

from utils import views_utils

from perfect_arch_orthotics.templatetags import groups as tt_groups
from clients import models as clients_models
from clients.views import views as clients_views
from clients.forms import claim_forms


class BiomechanicalGaitCreate(mixins.UserPassesTestMixin, generic.CreateView):
    model = clients_models.BiomechanicalGait
    template_name = 'clients/claim/biomechanical_gait.html'
    form_class = claim_forms.BiomechanicalGaitModelForm

    def test_func(self):
        return tt_groups.check_groups(self.request.user, 'Edit')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        kwargs['client_pk'] = self.kwargs['client_pk']

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['save_text'] = 'create'
        context['model_name'] = self.model._meta.verbose_name
        context['cancel_url'] = '{}?toggle=biomechanical_gaits'.format(
            urlresolvers.reverse(
                'client', kwargs={'client_id': self.kwargs['client_pk']}
            )
        )

        providers = list(
            clients_models.Insurance.objects.all().distinct(
                'provider'
            ).values_list(
                'provider', flat=True
            )
        )
        context['provider_choices'] = json.dumps(providers)

        return context


class BiomechanicalGaitUpdate(mixins.UserPassesTestMixin, generic.UpdateView):
    model = clients_models.BiomechanicalGait
    template_name = 'clients/claim/biomechanical_gait.html'
    form_class = claim_forms.BiomechanicalGaitModelForm

    def test_func(self):
        return tt_groups.check_groups(self.request.user, 'Edit')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['save_text'] = 'update'
        context['model_name'] = self.model._meta.verbose_name
        context['cancel_url'] = self.object.get_absolute_url()

        providers = list(
            clients_models.Insurance.objects.all().distinct(
                'provider'
            ).values_list(
                'provider', flat=True
            )
        )
        context['provider_choices'] = json.dumps(providers)

        return context


class BiomechanicalGaitDelete(
    mixins.UserPassesTestMixin,
    views_utils.PermissionMixin,
    generic.DeleteView,
):
    model = clients_models.BiomechanicalGait
    template_name = 'utils/generics/delete.html'

    def test_func(self):
        return tt_groups.check_groups(self.request.user, 'Edit')

    def get_permissions(self):
        permissions = {
            'permission': 'clients.delete_biomechanicalgait',
            'redirect': self.get_object().get_absolute_url(),
        }

        return permissions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_name'] = self.model._meta.verbose_name
        context['cancel_url'] = self.object.get_absolute_url()

        return context

    def get_success_url(self):
        url = '{}?toggle=biomechanical_gaits'.format(
            urlresolvers.reverse(
                'client',
                kwargs={'client_id': self.object.patient.get_client().pk}
            )
        )

        return url


def biomechanical_gait_pdf(request, pk):
    biomechanical_gait = \
        clients_models.BiomechanicalGait.objects.select_related(
            'patient',
        ).get(pk=pk)

    context = {
        'biomechanical_gait': biomechanical_gait,
        'address': settings.BILL_TO[0][1],
        'email': settings.PERFECT_ARCH_EMAIL,
    }

    # for debugging
    # return shortcuts.render(
    #     request, 'clients/pdfs/biomechanical_gait.html', context
    # )
    return clients_views.render_to_pdf(
        request, 'clients/pdfs/biomechanical_gait.html', context
    )


class BiomechanicalGait2Create(mixins.UserPassesTestMixin, generic.CreateView):
    model = clients_models.BiomechanicalGait2
    template_name = 'clients/claim/biomechanical_gait_2.html'
    form_class = claim_forms.BiomechanicalGait2ModelForm

    def test_func(self):
        return tt_groups.check_groups(self.request.user, 'Edit')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        kwargs['client_pk'] = self.kwargs['client_pk']

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['save_text'] = 'create'
        context['model_name'] = self.model._meta.verbose_name
        context['cancel_url'] = '{}?toggle=biomechanical_gaits_2'.format(
            urlresolvers.reverse(
                'client', kwargs={'client_id': self.kwargs['client_pk']}
            )
        )

        providers = list(
            clients_models.Insurance.objects.all().distinct(
                'provider'
            ).values_list(
                'provider', flat=True
            )
        )
        context['provider_choices'] = json.dumps(providers)

        return context


class BiomechanicalGait2Update(mixins.UserPassesTestMixin, generic.UpdateView):
    model = clients_models.BiomechanicalGait2
    template_name = 'clients/claim/biomechanical_gait_2.html'
    form_class = claim_forms.BiomechanicalGait2ModelForm

    def test_func(self):
        return tt_groups.check_groups(self.request.user, 'Edit')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['save_text'] = 'update'
        context['model_name'] = self.model._meta.verbose_name
        context['cancel_url'] = self.object.get_absolute_url()

        providers = list(
            clients_models.Insurance.objects.all().distinct(
                'provider'
            ).values_list(
                'provider', flat=True
            )
        )
        context['provider_choices'] = json.dumps(providers)

        return context


class BiomechanicalGait2Delete(
    mixins.UserPassesTestMixin, views_utils.PermissionMixin, generic.DeleteView
):
    model = clients_models.BiomechanicalGait2
    template_name = 'utils/generics/delete.html'

    def test_func(self):
        return tt_groups.check_groups(self.request.user, 'Edit')

    def get_permissions(self):
        permissions = {
            'permission': 'clients.delete_biomechanicalgait2',
            'redirect': self.get_object().get_absolute_url(),
        }

        return permissions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_name'] = self.model._meta.verbose_name
        context['cancel_url'] = self.object.get_absolute_url()

        return context

    def get_success_url(self):
        url = '{}?toggle=biomechanical_gaits_2'.format(
            urlresolvers.reverse(
                'client',
                kwargs={'client_id': self.object.patient.get_client().pk}
            )
        )

        return url


def biomechanical_gait_2_pdf(request, pk):
    biomechanical_gait = \
        clients_models.BiomechanicalGait2.objects.select_related(
            'patient',
        ).get(pk=pk)

    orthotics_pros_lab = settings.LABORATORIES[5][1]
    tokens = orthotics_pros_lab.split('\n')
    address = '\n'.join(tokens[1:3])
    phone = tokens[5].split(' ', 1)[1]
    context = {
        'biomechanical_gait': biomechanical_gait,
        'address': address,
        'phone': phone,
    }

    # for debugging
    # return shortcuts.render(
    #     request, 'clients/pdfs/biomechanical_gait_2.html', context
    # )
    return clients_views.render_to_pdf(
        request, 'clients/pdfs/biomechanical_gait_2.html', context
    )


class BiomechanicalFootCreate(mixins.UserPassesTestMixin, generic.CreateView):
    model = clients_models.BiomechanicalFoot
    template_name = 'clients/claim/biomechanical_foot.html'
    form_class = claim_forms.BiomechanicalFootModelForm

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


class BiomechanicalFootUpdate(mixins.UserPassesTestMixin, generic.UpdateView):
    model = clients_models.BiomechanicalFoot
    template_name = 'clients/claim/biomechanical_foot.html'
    form_class = claim_forms.BiomechanicalFootModelForm

    def test_func(self):
        return tt_groups.check_groups(self.request.user, 'Edit')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['save_text'] = 'update'
        context['model_name'] = self.model._meta.verbose_name
        context['cancel_url'] = self.object.get_absolute_url()

        return context


def _biomechanical_foot(claim_pk):
    claim = clients_models.Claim.objects.select_related(
        'patient', 'biomechanicalfoot'
    ).get(pk=claim_pk)
    try:
        biomechanical_foot = claim.biomechanicalfoot
    except clients_models.BiomechanicalFoot.DoesNotExist:
        biomechanical_foot = None

    return claim, biomechanical_foot


def biomechanical_foot_fill_out(request, claim_pk):
    claim, biomechanical_foot = _biomechanical_foot(claim_pk)

    context = {
        'claim': claim,
        'biomechanical_foot': biomechanical_foot,
    }

    return shortcuts.render(
        request, 'clients/make_biomechanical_foot.html', context
    )


def biomechanical_foot_pdf(request, claim_pk):
    claim, biomechanical_foot = _biomechanical_foot(claim_pk)

    context = {'claim': claim, 'biomechanical_foot': biomechanical_foot}

    # for debugging
    # return shortcuts.render(
    #     request, 'clients/pdfs/biomechanical_foot.html', context
    # )
    return clients_views.render_to_pdf(
        request, 'clients/pdfs/biomechanical_foot.html', context
    )
