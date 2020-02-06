from django.http import HttpResponseRedirect
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.core import urlresolvers
from django.contrib.staticfiles.templatetags import staticfiles
from django.contrib.auth import mixins

from utils import views_utils

from perfect_arch_orthotics.templatetags import groups as tt_groups
from clients.models import Insurance, Client, Dependent, Coverage
from clients.forms import insurance_forms


class UpdateInsuranceView(mixins.UserPassesTestMixin, UpdateView):
    template_name = 'utils/generics/update.html'
    model = Insurance
    form_class = insurance_forms.InsuranceForm
    slug_field = "id"
    slug_url_kwarg = "insurance_id"

    def test_func(self):
        return tt_groups.check_groups(self.request.user, 'Edit')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_name'] = self.model._meta.verbose_name
        context['inline_model_name'] = Coverage._meta.verbose_name
        context['inline_model_name_plural'] = \
            Coverage._meta.verbose_name_plural
        context['cancel_url'] = self.object.get_absolute_url()
        context['js_url'] = 'insurance'
        context['css_url'] = 'insurance'

        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        insurance_form = self.get_form()

        coverage_formset = insurance_forms.InsuranceCoverageFormSet(
            main_claimant_id=self.object.main_claimant_id,
            **self.get_form_kwargs()
        )

        return self.render_to_response(
            self.get_context_data(
                form=insurance_form, formset=coverage_formset
            )
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        insurance_form = self.get_form()

        coverage_formset = insurance_forms.InsuranceCoverageFormSet(
            main_claimant_id=self.object.main_claimant_id,
            **self.get_form_kwargs()
        )

        if insurance_form.is_valid() and coverage_formset.is_valid():
            return self.form_valid(insurance_form, coverage_formset)
        else:
            return self.form_invalid(insurance_form, coverage_formset)

    def form_valid(self, form, coverage_formset):
        self.object = form.save()
        coverage_formset.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, coverage_formset):
        return self.render_to_response(
            self.get_context_data(form=form, formset=coverage_formset)
        )

    def get_success_url(self):
        self.success_url = self.object.get_absolute_url()

        return self.success_url


class DeleteInsuranceView(
    mixins.UserPassesTestMixin, views_utils.PermissionMixin, DeleteView
):
    template_name = 'utils/generics/delete.html'
    model = Insurance
    slug_field = "id"
    slug_url_kwarg = "insurance_id"

    def test_func(self):
        return tt_groups.check_groups(self.request.user, 'Edit')

    def get_permissions(self):
        permissions = {
            'permission': 'clients.delete_insurance',
            'redirect': self.get_object().get_absolute_url(),
        }

        return permissions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_name'] = self.model._meta.verbose_name
        context['cancel_url'] = self.object.get_absolute_url()

        return context

    def get_success_url(self):
        self.success_url = \
            self.object.main_claimant.get_client().get_absolute_url()

        return self.success_url


class CreateInsuranceView(mixins.UserPassesTestMixin, CreateView):
    template_name = 'utils/generics/create.html'
    model = Insurance
    form_class = insurance_forms.InsuranceForm

    def test_func(self):
        return tt_groups.check_groups(self.request.user, 'Edit')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_name'] = self.model._meta.verbose_name
        context['indefinite_article'] = 'a'
        context['inline_model_name'] = Coverage._meta.verbose_name
        context['inline_model_name_plural'] = \
            Coverage._meta.verbose_name_plural
        context['cancel_url'] = urlresolvers.reverse(
            'client', kwargs={'client_id': self.kwargs['client_id']}
        )
        context['js_url'] = 'insurance'
        context['css_url'] = 'insurance'

        return context

    def get(self, request, *args, **kwargs):
        self.object = None
        insurance_form = self.get_form()

        if 'spouse_id' in self.kwargs:
            main_claimant_id = self.kwargs['spouse_id']
        else:
            main_claimant_id = self.kwargs['client_id']
        coverage_formset = insurance_forms.InsuranceCoverageFormSet(
            main_claimant_id=main_claimant_id, **self.get_form_kwargs()
        )

        return self.render_to_response(
            self.get_context_data(
                form=insurance_form, formset=coverage_formset
            )
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        insurance_form = self.get_form()

        if 'spouse_id' in self.kwargs:
            main_claimant_id = self.kwargs['spouse_id']
        else:
            main_claimant_id = self.kwargs['client_id']
        coverage_formset = insurance_forms.InsuranceCoverageFormSet(
            main_claimant_id=main_claimant_id, **self.get_form_kwargs()
        )

        if insurance_form.is_valid() and coverage_formset.is_valid():
            return self.form_valid(insurance_form, coverage_formset)
        else:
            return self.form_invalid(insurance_form, coverage_formset)

    def form_valid(self, form, coverage_formset):
        self.object = form.save(commit=False)
        if 'spouse_id' in self.kwargs:
            main_claimant = Dependent.objects.get(id=self.kwargs['spouse_id'])
        else:
            main_claimant = Client.objects.get(id=self.kwargs['client_id'])
        self.object.main_claimant = main_claimant
        self.object.save()

        coverage_formset.instance = self.object
        coverage_formset.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, coverage_formset):
        return self.render_to_response(
            self.get_context_data(form=form, formset=coverage_formset)
        )

    def get_success_url(self):
        self.success_url = self.object.get_absolute_url()

        return self.success_url
