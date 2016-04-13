import itertools
from os import path
from datetime import datetime

from django import forms
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.core import urlresolvers
from django.core.files import storage
from django.conf import settings
from django.utils.translation import ugettext as trans

from formtools.wizard import views as wizard_views, forms as wizard_forms

from utils import views_utils
from utils.forms import widgets as utils_widgets

from clients.models import Claim, Invoice, InsuranceLetter, \
    ProofOfManufacturing, Client, Coverage
from clients import models as clients_models
from clients.forms.forms import InvoiceForm, \
    InsuranceLetterForm, \
    LaboratoryInsuranceLetterFormSet, ProofOfManufacturingForm
from clients.forms import claim_forms


# class CreateClaimView(CreateView):
#     template_name = 'clients/claim/create_claim.html'
#     model = Claim
#     form_class = ClaimForm

#     def get_form(self, form_class=None):
#         if form_class is None:
#             form_class = self.get_form_class()
#         client = Client.objects.get(pk=self.kwargs['client_id'])
#         return form_class(client, **self.get_form_kwargs())

#     def get(self, request, *args, **kwargs):
#         self.object = None
#         form_class = self.get_form_class()
#         claim_form = self.get_form(form_class)

#         ClaimCoverageFormFormSet = minimum_nestedformset_factory(
#             Claim, ClaimCoverage,
#             inlineformset_factory(
#                 ClaimCoverage, ClaimItem,
#                 formset=MinimumInlineFormSet, extra=1, fields='__all__',
#             ),
#             minimum_name="Coverage", minimum_name_nested="Item",
#             extra=1, exclude=('items',),
#         )
#         nestedformset = ClaimCoverageFormFormSet()

#         insurances = claim_form.client.insurance_set.all()
#         for dependent in claim_form.client.dependent_set.all():
#             if dependent.relationship == Dependent.SPOUSE:
#                 insurances = insurances | dependent.insurance_set.all()
#         coverages = Coverage.objects.filter(insurance__in=insurances)
#         label = (
#             lambda obj:
#                 "%s - %s - %s"
#                 " [%%%s, Amount Remaining: $%s, Quantity Remaining: %s]"
#                 % (
#                     obj.insurance.provider,
#                     obj.get_coverage_type_display(),
#                     obj.claimant.full_name(),
#                     obj.coverage_percent,
#                     obj.claim_amount_remaining(),
#                     obj.quantity_remaining())
#         )
#         items_label = (
#             lambda obj:
#                 "%s - %s - %s - $%s" % (
#                     obj.get_coverage_type_display(),
#                     obj.product_code,
#                     # TODO: need to get unit_price at the time of
#                     #  submitted_datetime
#                     obj.description, obj.unit_price)
#         )
#         nestedformset.form.base_fields[
#             'coverage'].queryset = coverages
#         nestedformset.form.base_fields[
#             'coverage'].label_from_instance = label
#         nestedformset.nested_formset_class.form.base_fields[
#             'item'].label_from_instance = items_label
#         items = nestedformset.nested_formset_class.form.base_fields[
#             'item'].queryset
#         nestedformset.nested_formset_class.form.base_fields[
#             'item'].queryset = items.order_by('coverage_type', 'product_code',
#                                               'gender')
#         for form in nestedformset:
#             form.fields['coverage'].queryset = coverages
#             form.fields['coverage'].label_from_instance = label
#             form.nested.form.base_fields[
#                 'item'].label_from_instance = items_label
#             items = form.nested.form.base_fields[
#                 'item'].queryset
#             form.nested.form.base_fields[
#                 'item'].queryset = items.order_by('coverage_type',
#                                                   'product_code', 'gender')

#         return self.render_to_response(
#             self.get_context_data(claim_form=claim_form,
#                                   nestedformset=nestedformset)
#         )

#     def post(self, request, *args, **kwargs):
#         self.object = None
#         form_class = self.get_form_class()
#         claim_form = self.get_form(form_class)

#         ClaimCoverageFormFormSet = minimum_nestedformset_factory(
#             Claim, ClaimCoverage,
#             inlineformset_factory(
#                 ClaimCoverage, ClaimItem,
#                 formset=MinimumInlineFormSet, extra=1, fields='__all__',
#             ),
#             minimum_name="Coverage", minimum_name_nested="Item",
#             extra=1, exclude=('items',),
#         )
#         nestedformset = ClaimCoverageFormFormSet(request.POST)

#         insurances = claim_form.client.insurance_set.all()
#         for dependent in claim_form.client.dependent_set.all():
#             if dependent.relationship == Dependent.SPOUSE:
#                 insurances = insurances | dependent.insurance_set.all()
#         coverages = Coverage.objects.filter(insurance__in=insurances)
#         label = (
#             lambda obj:
#                 "%s - %s [%%%s, Amount Remaining: $%s, Quantity Remaining: %s]"
#                 % (
#                     obj.get_coverage_type_display(),
#                     obj.claimant.full_name(),
#                     obj.coverage_percent,
#                     obj.claim_amount_remaining(),
#                     obj.quantity_remaining())
#         )
#         items_label = (
#             lambda obj:
#                 "%s - %s - %s - $%s" % (
#                     obj.get_coverage_type_display(), obj.product_code,
#                     # TODO: need to get unit_price at the time of
#                     #  submitted_datetime
#                     obj.description, obj.unit_price)
#         )
#         nestedformset.form.base_fields[
#             'coverage'].queryset = coverages
#         nestedformset.form.base_fields[
#             'coverage'].label_from_instance = label
#         nestedformset.nested_formset_class.form.base_fields[
#             'item'].label_from_instance = items_label
#         items = nestedformset.nested_formset_class.form.base_fields[
#             'item'].queryset
#         nestedformset.nested_formset_class.form.base_fields[
#             'item'].queryset = items.order_by('coverage_type', 'product_code',
#                                               'gender')
#         for form in nestedformset:
#             form.fields['coverage'].queryset = coverages
#             form.fields['coverage'].label_from_instance = label
#             form.nested.form.base_fields[
#                 'item'].label_from_instance = items_label
#             items = form.nested.form.base_fields[
#                 'item'].queryset
#             form.nested.form.base_fields[
#                 'item'].queryset = items.order_by('coverage_type',
#                                                   'product_code', 'gender')

#         if claim_form.is_valid() and nestedformset.is_valid():
#             return self.form_valid(claim_form, nestedformset)
#         else:
#             return self.form_invalid(claim_form, nestedformset)

#     def form_valid(self, claim_form, nestedformset):
#         self.object = claim_form.save()

#         nestedformset.instance = self.object
#         nestedformset.save()

#         return HttpResponseRedirect(self.get_success_url())

#     def form_invalid(self, claim_form, nestedformset):
#         return self.render_to_response(
#             self.get_context_data(claim_form=claim_form,
#                                   nestedformset=nestedformset)
#         )

#     def get_success_url(self):
#         self.success_url = reverse_lazy('claim',
#                                         kwargs={'claim_id': self.object.id})
#         return self.success_url


class DetailClaimView(DetailView):
    template_name = 'clients/claim/detail_claim.html'
    model = Claim


# class UpdateClaimView(UpdateView):
#     template_name = 'clients/claim/update_claim.html'
#     model = Claim
#     form_class = ClaimForm
#     slug_field = "id"
#     slug_url_kwarg = "claim_id"

#     def get_form(self, form_class=None):
#         if form_class is None:
#             form_class = self.get_form_class()
#         client = self.object.patient.get_client()
#         return form_class(client, **self.get_form_kwargs())

#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         form_class = self.get_form_class()
#         claim_form = self.get_form(form_class)

#         ClaimCoverageFormFormSet = minimum_nestedformset_factory(
#             Claim, ClaimCoverage,
#             inlineformset_factory(
#                 ClaimCoverage, ClaimItem,
#                 formset=MinimumInlineFormSet, extra=1, fields='__all__',
#             ),
#             minimum_name="Coverage", minimum_name_nested="Item",
#             extra=1, exclude=('items',),
#         )
#         nestedformset = ClaimCoverageFormFormSet(instance=self.object)

#         insurances = claim_form.client.insurance_set.all()
#         for dependent in claim_form.client.dependent_set.all():
#             if dependent.relationship == Dependent.SPOUSE:
#                 insurances = insurances | dependent.insurance_set.all()
#         coverages = Coverage.objects.filter(insurance__in=insurances)
#         label = (
#             lambda obj:
#                 "%s - %s - %s"
#                 " [%%%s, Amount Remaining: $%s, Quantity Remaining: %s]"
#                 % (
#                     obj.insurance.provider,
#                     obj.get_coverage_type_display(),
#                     obj.claimant.full_name(),
#                     obj.coverage_percent,
#                     obj.claim_amount_remaining(),
#                     obj.quantity_remaining())
#         )
#         items_label = (
#             lambda obj:
#                 "%s - %s - %s - $%s" % (
#                     obj.get_coverage_type_display(),
#                     obj.product_code,
#                     # TODO: need to get unit_price at the time of
#                     #  submitted_datetime
#                     obj.description, obj.unit_price)
#         )
#         nestedformset.form.base_fields[
#             'coverage'].queryset = coverages
#         nestedformset.form.base_fields[
#             'coverage'].label_from_instance = label
#         nestedformset.nested_formset_class.form.base_fields[
#             'item'].label_from_instance = items_label
#         items = nestedformset.nested_formset_class.form.base_fields[
#             'item'].queryset
#         nestedformset.nested_formset_class.form.base_fields[
#             'item'].queryset = items.order_by('coverage_type', 'product_code',
#                                               'gender')
#         for form in nestedformset:
#             form.fields['coverage'].queryset = coverages
#             form.fields['coverage'].label_from_instance = label
#             form.nested.form.base_fields[
#                 'item'].label_from_instance = items_label
#             items = form.nested.form.base_fields[
#                 'item'].queryset
#             form.nested.form.base_fields[
#                 'item'].queryset = items.order_by('coverage_type',
#                                                   'product_code', 'gender')

#         return self.render_to_response(
#             self.get_context_data(claim_form=claim_form,
#                                   nestedformset=nestedformset)
#         )

#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         form_class = self.get_form_class()
#         claim_form = self.get_form(form_class)

#         ClaimCoverageFormFormSet = minimum_nestedformset_factory(
#             Claim, ClaimCoverage,
#             inlineformset_factory(
#                 ClaimCoverage, ClaimItem,
#                 formset=MinimumInlineFormSet, extra=1, fields='__all__',
#             ),
#             minimum_name="Coverage", minimum_name_nested="Item",
#             extra=1, exclude=('items',),
#         )
#         nestedformset = ClaimCoverageFormFormSet(
#             request.POST, instance=self.object)

#         insurances = claim_form.client.insurance_set.all()
#         for dependent in claim_form.client.dependent_set.all():
#             if dependent.relationship == Dependent.SPOUSE:
#                 insurances = insurances | dependent.insurance_set.all()
#         coverages = Coverage.objects.filter(insurance__in=insurances)
#         label = (
#             lambda obj:
#                 "%s - %s - %s"
#                 " [%%%s, Amount Remaining: $%s, Quantity Remaining: %s]"
#                 % (
#                     obj.insurance.provider,
#                     obj.get_coverage_type_display(),
#                     obj.claimant.full_name(),
#                     obj.coverage_percent,
#                     obj.claim_amount_remaining(),
#                     obj.quantity_remaining())
#         )
#         items_label = (
#             lambda obj:
#                 "%s - %s - %s - $%s" % (
#                     obj.get_coverage_type_display(), obj.product_code,
#                     # TODO: need to get unit_price at the time of
#                     #  submitted_datetime
#                     obj.description, obj.unit_price)
#         )
#         nestedformset.form.base_fields[
#             'coverage'].queryset = coverages
#         nestedformset.form.base_fields[
#             'coverage'].label_from_instance = label
#         nestedformset.nested_formset_class.form.base_fields[
#             'item'].label_from_instance = items_label
#         items = nestedformset.nested_formset_class.form.base_fields[
#             'item'].queryset
#         nestedformset.nested_formset_class.form.base_fields[
#             'item'].queryset = items.order_by('coverage_type', 'product_code',
#                                               'gender')
#         for form in nestedformset:
#             form.fields['coverage'].queryset = coverages
#             form.fields['coverage'].label_from_instance = label
#             form.nested.form.base_fields[
#                 'item'].label_from_instance = items_label
#             items = form.nested.form.base_fields[
#                 'item'].queryset
#             form.nested.form.base_fields[
#                 'item'].queryset = items.order_by('coverage_type',
#                                                   'product_code', 'gender')

#         if claim_form.is_valid() and nestedformset.is_valid():
#             return self.form_valid(claim_form, nestedformset)
#         else:
#             return self.form_invalid(claim_form, nestedformset)

#     def form_valid(self, claim_form, nestedformset):
#         self.object = claim_form.save()
#         nestedformset.save()

#         return HttpResponseRedirect(self.get_success_url())

#     def form_invalid(self, claim_form, nestedformset):
#         return self.render_to_response(
#             self.get_context_data(claim_form=claim_form,
#                                   nestedformset=nestedformset)
#         )

#     def get_success_url(self):
#         self.success_url = reverse_lazy('claim',
#                                         kwargs={'claim_id': self.object.id})
#         return self.success_url


class DeleteClaimView(views_utils.PermissionMixin, DeleteView):
    template_name = 'utils/generics/delete.html'
    model = Claim
    slug_field = "id"
    slug_url_kwarg = "claim_id"
    success_url = urlresolvers.reverse_lazy('claims')

    def get_permissions(self):
        permissions = {
            'permission': 'clients.delete_claim',
            'redirect': self.get_object().get_absolute_url(),
        }

        return permissions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_name'] = self.model._meta.verbose_name
        context['cancel_url'] = self.object.get_absolute_url()

        return context


class UpdateInvoiceView(UpdateView):
    template_name = 'clients/claim/update_invoice.html'
    model = Invoice
    form_class = InvoiceForm
    slug_field = "id"
    slug_url_kwarg = "invoice_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_name'] = self.model._meta.verbose_name
        context['cancel_url'] = self.object.get_absolute_url()

        return context

    def get_success_url(self):
        claim_id = self.object.claim.id
        self.success_url = reverse_lazy('fillOutInvoice',
                                        kwargs={'claim_id': claim_id})
        return self.success_url


class CreateInvoiceView(CreateView):
    template_name = 'clients/claim/create_invoice.html'
    model = Invoice
    form_class = InvoiceForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        claim = Claim.objects.get(id=self.kwargs['claim_id'])
        context['claim'] = claim

        context['model_name'] = self.model._meta.verbose_name
        context['cancel_url'] = urlresolvers.reverse(
            'claim', kwargs={'claim_id': self.kwargs['claim_id']}
        )

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        claim = Claim.objects.get(id=self.kwargs['claim_id'])
        self.object.claim = claim
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        claim_id = self.object.claim.id
        self.success_url = reverse_lazy('fillOutInvoice',
                                        kwargs={'claim_id': claim_id})
        return self.success_url


class UpdateInsuranceLetterView(UpdateView):
    template_name = 'clients/claim/update_insurance_letter.html'
    model = InsuranceLetter
    form_class = InsuranceLetterForm
    slug_field = "id"
    slug_url_kwarg = "insurance_letter_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_name'] = self.model._meta.verbose_name
        context['inline_model_name'] = \
            clients_models.Laboratory._meta.verbose_name
        context['inline_model_name_plural'] = \
            clients_models.Laboratory._meta.verbose_name_plural
        context['cancel_url'] = self.object.get_absolute_url()

        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        laboratory_form = LaboratoryInsuranceLetterFormSet(
            instance=self.object)
        return self.render_to_response(
            self.get_context_data(form=form, laboratory_form=laboratory_form)
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        laboratory_form = LaboratoryInsuranceLetterFormSet(
            request.POST, instance=self.object)
        if form.is_valid() and laboratory_form.is_valid():
            return self.form_valid(form, laboratory_form)
        else:
            return self.form_invalid(form, laboratory_form)

    def form_valid(self, form, laboratory_form):
        self.object = form.save()
        laboratory_form.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, laboratory_form):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  laboratory_form=laboratory_form)
        )

    def get_success_url(self):
        claim_id = self.object.claim.id
        self.success_url = reverse_lazy('fillOutInsurance',
                                        kwargs={'claim_id': claim_id})
        return self.success_url


class CreateInsuranceLetterView(CreateView):
    template_name = 'clients/claim/create_insurance_letter.html'
    model = InsuranceLetter
    form_class = InsuranceLetterForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_name'] = self.model._meta.verbose_name
        context['inline_model_name'] = \
            clients_models.Laboratory._meta.verbose_name
        context['inline_model_name_plural'] = \
            clients_models.Laboratory._meta.verbose_name_plural
        context['cancel_url'] = urlresolvers.reverse(
            'claim', kwargs={'claim_id': self.kwargs['claim_id']}
        )

        return context

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        laboratory_form = LaboratoryInsuranceLetterFormSet()
        return self.render_to_response(
            self.get_context_data(form=form, laboratory_form=laboratory_form)
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        laboratory_form = LaboratoryInsuranceLetterFormSet(request.POST)
        if form.is_valid() and laboratory_form.is_valid():
            return self.form_valid(form, laboratory_form)
        else:
            return self.form_invalid(form, laboratory_form)

    def form_valid(self, form, laboratory_form):
        self.object = form.save(commit=False)
        claim = Claim.objects.get(id=self.kwargs['claim_id'])
        self.object.claim = claim
        self.object.save()
        laboratory_form.instance = self.object
        laboratory_form.save()

        return HttpResponseRedirect(self.get_success_url(claim))

    def form_invalid(self, form, laboratory_form):
        return self.render_to_response(
            self.get_context_data(form=form, laboratory_form=laboratory_form)
        )

    def get_success_url(self, claim):
        claim_id = claim.id
        self.success_url = reverse_lazy('fillOutInsurance',
                                        kwargs={'claim_id': claim_id})
        return self.success_url


class CreateProofOfManufacturingView(CreateView):
    template_name = 'clients/claim/create_proof_of_manufacturing.html'
    model = ProofOfManufacturing
    form_class = ProofOfManufacturingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_name'] = self.model._meta.verbose_name
        context['cancel_url'] = urlresolvers.reverse(
            'claim', kwargs={'claim_id': self.kwargs['claim_id']}
        )

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        claim = Claim.objects.get(id=self.kwargs['claim_id'])
        self.object.claim = claim
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        claim_id = self.object.claim.id
        self.success_url = reverse_lazy('fillOutProof',
                                        kwargs={'claim_id': claim_id})

        return self.success_url


class CreateClaimWizard(wizard_views.NamedUrlSessionWizardView):
    file_storage = storage.FileSystemStorage(
        path.join(settings.MEDIA_ROOT, 'temp')
    )
    form_list = (
        ('info', claim_forms.ClaimForm),
        ('coverages', claim_forms.ClaimCoverageFormFormSet),
    )
    template_name = 'utils/generics/wizard.html'
    storage_name = 'utils.wizard.storage.MultiFileSessionStorage'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['save_text'] = 'create'
        context['model_name'] = Claim._meta.verbose_name
        context['form_type'] = 'multipart/form-data'
        client = Client.objects.get(id=self.kwargs['client_id'])
        context['parent'] = {
            'parent_name': Client._meta.verbose_name,
            'parent_model': client,
            'parent_text': client.full_name(),
        }
        context['cancel_url'] = (
            reverse('claim_create', kwargs={'client_id': client.id}) +
            '?reset'
        )

        return context

    def get_form_kwargs(self, step=None):
        if step == 'info' and 'client_id' in self.kwargs:
            return {'client_id': self.kwargs['client_id']}
        else:
            return super().get_form_kwargs(step)

    def get_form(self, step=None, data=None, files=None):
        if step is None:
            step = self.steps.current

        form = super().get_form(step, data, files)

        if step == 'coverages':
            info_data = self.storage.get_step_data('info')
            submitted_datetime_str = info_data.get('info-submitted_datetime')
            submitted_datetime = datetime.strptime(
                submitted_datetime_str, '%Y-%m-%d %I:%M %p'
            )
            insurance_id = info_data.get('info-insurance')

            coverages = Coverage.objects.select_related(
                'insurance', 'claimant'
            ).prefetch_related(
                'claimcoverage_set__claimitem_set'
            ).filter(
                insurance_id=insurance_id
            )
            label = (
                lambda obj:
                    "%s - %s - %s"
                    " [%%%s, Amount Remaining: $%s, Quantity Remaining: %s]"
                    % (
                        obj.insurance.provider,
                        obj.get_coverage_type_display(),
                        obj.claimant.full_name(),
                        obj.coverage_percent,
                        obj.claim_amount_remaining(),
                        obj.quantity_remaining())
            )
            items_label = (
                lambda obj:
                    "%s - %s - %s - $%s" % (
                        obj.get_coverage_type_display(),
                        obj.product_code,
                        obj.description,
                        obj.get_values(submitted_datetime)['unit_price'])
            )
            formset = form

            base_fields = formset.form.base_fields
            base_fields['coverage'].queryset = coverages
            base_fields['coverage'].label_from_instance = label

            nested_base_fields = formset.nested_formset_class.form.base_fields
            nested_base_fields['item'].label_from_instance = items_label
            items = nested_base_fields['item'].queryset.prefetch_related(
                'itemhistory_set'
            ).order_by(
                'coverage_type', 'product_code', 'gender'
            )
            nested_base_fields['item'].queryset = items
            for nested_form in formset:
                nested_form.fields['coverage'].queryset = coverages
                nested_form.fields['coverage'].label_from_instance = label

                base_fields = nested_form.nested.form.base_fields
                base_fields['item'].label_from_instance = items_label
                items = base_fields['item'].queryset
                base_fields['item'].queryset = items

        return form

    def get_step_url(self, step):
        return reverse(
            self.url_name,
            kwargs={'step': step, 'client_id': self.kwargs['client_id']}
        )

    def post(self, *args, **kwargs):
        """
        This method handles POST requests.
        The wizard will render either the current step (if form validation
        wasn't successful), the next step (if the current step was stored
        successful) or the done view (if no more steps are available)
        """
        # Look for a wizard_goto_step element in the posted data which
        # contains a valid step name. If one was found, render the requested
        # form. (This makes stepping back a lot easier).
        wizard_goto_step = self.request.POST.get('wizard_goto_step', None)
        if wizard_goto_step and wizard_goto_step in self.get_form_list():
            return self.render_goto_step(wizard_goto_step)

        # Check if form was refreshed
        management_form = wizard_forms.ManagementForm(
            self.request.POST, prefix=self.prefix
        )
        if not management_form.is_valid():
            raise forms.ValidationError(
                trans('ManagementForm data is missing or has been tampered.'),
                code='missing_management_form',
            )

        form_current_step = management_form.cleaned_data['current_step']
        if (form_current_step != self.steps.current and
                self.storage.current_step is not None):
            # form refreshed, change current step
            self.storage.current_step = form_current_step

        new_files = self.request.FILES
        old_files = self.storage.current_step_files
        files = {}
        if old_files:
            # combine new/old files as a user can be clearing old files and/or
            #  uploading new files
            for step_field_name in old_files:
                found = False
                for field_name in new_files:
                    if step_field_name in field_name:
                        files[step_field_name] = (
                            old_files[step_field_name] +
                            new_files.getlist(field_name)
                        )
                        found = True
                        break
                if not found:
                    files[step_field_name] = old_files[step_field_name]
        else:
            for field_name in new_files:
                if 'claim_package' in field_name:
                    files['claim_package'] = new_files.getlist(field_name)
                else:
                    files[field_name] = new_files.getlist(field_name)

        # get the form for the current step
        form = self.get_form(data=self.request.POST, files=files)

        # and try to validate
        if form.is_valid():
            if old_files:
                for field in form:
                    if isinstance(field.field, forms.FileField):
                        field_name = field.name

                        if field_name not in old_files:
                            continue

                        both = itertools.zip_longest(
                            form.cleaned_data[field_name],
                            old_files[field_name]
                        )
                        to_remove = []
                        for i, (_file, initial_datum) in enumerate(both):
                            if _file is None or _file == initial_datum:
                                continue
                            elif _file is False:
                                to_remove.append(initial_datum)

                                # clear checkbox data
                                field_widget_name = \
                                    field.html_name + '_{}'.format(i)
                                widget = field.field.widget.widgets[i]
                                widget_name = widget.clear_checkbox_name(
                                    field_widget_name
                                )
                                form.data[widget_name] = ''
                                # close and delete temp file
                                if not initial_datum.closed:
                                    initial_datum.close()
                                self.file_storage.delete(initial_datum.name)
                        for remove in to_remove:
                            # remove file
                            form.files[field_name].remove(remove)

            step_files = self.process_step_files(form)

            # if the form is valid, store the cleaned data and files.
            self.storage.set_step_data(self.steps.current,
                                       self.process_step(form))
            self.storage.set_step_files(self.steps.current,
                                        step_files)

            # check if the current step is the last step
            if self.steps.current == self.steps.last:
                # no more steps, render done view
                return self.render_done(form, **kwargs)
            else:
                # proceed to the next step
                return self.render_next_step(form)
        else:
            form.fields['claim_package'].widget = \
                utils_widgets.ConfirmMultiFileMultiWidget(
                    form_id="update_claim_form",  # html
                    form=self,
                    field_name='claim_package',
                    file_count=0
                )
            form.initial['claim_package'] = {}

        return self.render(form)

    def done(self, form_list, form_dict, **kwargs):
        claim_form = form_dict['info']
        claim_coverage_claim_item_form = form_dict['coverages']

        claim = claim_form.save()

        # ClaimForm save doesn't handle form wizard files
        files = claim_form.cleaned_data['claim_package']
        for _file in files:
            if _file:
                # use get_or_create in case of update
                clients_models.ClaimAttachment.objects.get_or_create(
                    attachment=_file, claim=claim
                )

        claim_coverage_claim_item_form.instance = claim
        claim_coverage_claim_item_form.save()

        return HttpResponseRedirect(reverse(
            'claim', kwargs={'claim_id': claim.id}
        ))


class UpdateClaimWizard(CreateClaimWizard):
    instance = None

    def get_context_data(self, **kwargs):
        # skip CreateClaimWizard's context
        context = super(
            wizard_views.NamedUrlSessionWizardView, self
        ).get_context_data(**kwargs)

        context['save_text'] = 'update'
        context['model_name'] = Claim._meta.verbose_name
        context['form_type'] = 'multipart/form-data'
        client = Client.objects.get(
            pk=self.instance.patient.get_client().pk
        )
        context['parent'] = {
            'parent_name': Client._meta.verbose_name,
            'parent_model': client,
            'parent_text': client.full_name(),
        }
        context['cancel_url'] = (
            reverse(
                'claim_update', kwargs={'claim_pk': self.instance.pk}
            ) +
            '?reset'
        )

        return context

    def get_form_instance(self, step):
        if not self.instance:
            claim_pk = self.kwargs['claim_pk']
            self.instance = Claim.objects.get(pk=claim_pk)

        return self.instance

    def get_step_url(self, step):
        return reverse(
            self.url_name,
            kwargs={'step': step, 'claim_pk': self.kwargs['claim_pk']}
        )
