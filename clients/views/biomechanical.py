import json

from django import http
from django import shortcuts
from django.views import generic
from django.conf import settings
from django.core import urlresolvers

from utils import views_utils

from clients import models as clients_models
from clients.views import views as clients_views
from clients.forms import claim_forms


class BiomechanicalGaitCreate(generic.CreateView):
    model = clients_models.BiomechanicalGait
    template_name = 'clients/claim/biomechanical_gait.html'
    form_class = claim_forms.BiomechanicalGaitModelForm

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

        try:
            # PostgreSQL
            providers = list(
                clients_models.Insurance.objects.all().distinct(
                    'provider'
                ).values_list(
                    'provider', flat=True
                )
            )
        except NotImplementedError:
            # SQLite
            providers = list(set(
                clients_models.Insurance.objects.all().values_list(
                    'provider', flat=True
                )
            ))
        context['provider_choices'] = json.dumps(providers)

        return context


class BiomechanicalGaitUpdate(generic.UpdateView):
    model = clients_models.BiomechanicalGait
    template_name = 'clients/claim/biomechanical_gait.html'
    form_class = claim_forms.BiomechanicalGaitModelForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['save_text'] = 'update'
        context['model_name'] = self.model._meta.verbose_name
        context['cancel_url'] = self.object.get_absolute_url()

        try:
            # PostgreSQL
            providers = list(
                clients_models.Insurance.objects.all().distinct(
                    'provider'
                ).values_list(
                    'provider', flat=True
                )
            )
        except NotImplementedError:
            # SQLite
            providers = list(set(
                clients_models.Insurance.objects.all().values_list(
                    'provider', flat=True
                )
            ))
        context['provider_choices'] = json.dumps(providers)

        return context


class BiomechanicalGaitDelete(views_utils.PermissionMixin, generic.DeleteView):
    model = clients_models.BiomechanicalGait
    template_name = 'utils/generics/delete.html'

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

    # return shortcuts.render(
    #     request,
    #     'clients/pdfs/biomechanical_gait.html',
    #     {
    #         'title': "Bio-mechanical/Gait Examination",
    #         'biomechanical_gait': biomechanical_gait,
    #         'address': settings.BILL_TO[0][1],
    #         'email': settings.DANNY_EMAIL,
    #     }
    # )
    return clients_views.render_to_pdf(
        request,
        'clients/pdfs/biomechanical_gait.html',
        {
            'title': "Bio-mechanical/Gait Examination",
            'biomechanical_gait': biomechanical_gait,
            'address': settings.BILL_TO[0][1],
            'email': settings.DANNY_EMAIL,
        }
    )


class BiomechanicalGait2Create(generic.CreateView):
    model = clients_models.BiomechanicalGait2
    template_name = 'clients/claim/biomechanical_gait_2.html'
    form_class = claim_forms.BiomechanicalGait2ModelForm

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

        try:
            # PostgreSQL
            providers = list(
                clients_models.Insurance.objects.all().distinct(
                    'provider'
                ).values_list(
                    'provider', flat=True
                )
            )
        except NotImplementedError:
            # SQLite
            providers = list(set(
                clients_models.Insurance.objects.all().values_list(
                    'provider', flat=True
                )
            ))
        context['provider_choices'] = json.dumps(providers)

        return context


class BiomechanicalGait2Update(generic.UpdateView):
    model = clients_models.BiomechanicalGait2
    template_name = 'clients/claim/biomechanical_gait_2.html'
    form_class = claim_forms.BiomechanicalGait2ModelForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['save_text'] = 'update'
        context['model_name'] = self.model._meta.verbose_name
        context['cancel_url'] = self.object.get_absolute_url()

        try:
            # PostgreSQL
            providers = list(
                clients_models.Insurance.objects.all().distinct(
                    'provider'
                ).values_list(
                    'provider', flat=True
                )
            )
        except NotImplementedError:
            # SQLite
            providers = list(set(
                clients_models.Insurance.objects.all().values_list(
                    'provider', flat=True
                )
            ))
        context['provider_choices'] = json.dumps(providers)

        return context


class BiomechanicalGait2Delete(
    views_utils.PermissionMixin, generic.DeleteView
):
    model = clients_models.BiomechanicalGait2
    template_name = 'utils/generics/delete.html'

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

    context = {
        'title':
            "Biomechanical Evaluation, Gait Analysis, & Casting Method",
        'biomechanical_gait': biomechanical_gait,
    }
    # return shortcuts.render(
    #     request,
    #     'clients/pdfs/biomechanical_gait_2.html',
    #     context
    # )
    return clients_views.render_to_pdf(
        request,
        'clients/pdfs/biomechanical_gait_2.html',
        context
    )


class BiomechanicalFootCreate(generic.CreateView):
    model = clients_models.BiomechanicalFoot
    template_name = 'clients/claim/biomechanical_foot.html'
    form_class = claim_forms.BiomechanicalFootModelForm

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


class BiomechanicalFootUpdate(generic.UpdateView):
    model = clients_models.BiomechanicalFoot
    template_name = 'clients/claim/biomechanical_foot.html'
    form_class = claim_forms.BiomechanicalFootModelForm

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

    # return shortcuts.render(
    #     request,
    #     'clients/pdfs/biomechanical_foot.html',
    #     {
    #         'title': "Biomechanical Foot Examination",
    #         'claim': claim,
    #         'biomechanical_foot': biomechanical_foot,
    #     }
    # )
    return clients_views.render_to_pdf(
        request,
        'clients/pdfs/biomechanical_foot.html',
        {
            'title': "Biomechanical Foot Examination",
            'claim': claim,
            'biomechanical_foot': biomechanical_foot,
        }
    )
