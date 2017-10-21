import itertools
from os import path
from datetime import datetime

from django import forms, shortcuts
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.core import urlresolvers
from django.core.files import storage, uploadedfile
from django.conf import settings
from django.utils.translation import ugettext as trans
from django.utils import safestring
from django.db import utils as db_utils
from django.contrib import messages

from formtools.wizard import views as wizard_views, forms as wizard_forms

from utils import views_utils
from utils.wizard import views as utils_wizard_views

from clients.models import Claim, Invoice, InsuranceLetter, \
    ProofOfManufacturing, Client, Coverage
from clients import models as clients_models
from clients.forms.forms import InvoiceForm, \
    InsuranceLetterForm, \
    LaboratoryInsuranceLetterFormSet, ProofOfManufacturingForm
from clients.forms import claim_forms


class DetailClaimView(DetailView):
    template_name = 'clients/claim/detail_claim.html'
    model = Claim


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

    def get(self, request, *args, **kwargs):
        # Ensure Invoice does not already exist
        claim = Claim.objects.get(id=self.kwargs['claim_id'])
        try:
            claim.invoice
            return HttpResponseRedirect(
                claim.invoice.get_absolute_url()
            )
        except clients_models.Invoice.DoesNotExist:
            pass

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        claim_id = self.kwargs['claim_id']
        self.object.claim_id = claim_id
        try:
            self.object.save()
        except db_utils.IntegrityError:
            claim = Claim.objects.get(id=claim_id)
            # Was receiving errors that a user was trying to create a
            #  second invoice for this claim, so redirect to
            #  existing invoice since one already exists
            #  for this OneToOne
            return HttpResponseRedirect(
                claim.invoice.get_absolute_url()
            )

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        claim_id = self.object.claim_id

        self.success_url = reverse_lazy(
            'fillOutInvoice', kwargs={'claim_id': claim_id}
        )

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
        # Ensure InsuranceLetter does not already exist
        claim = Claim.objects.get(id=self.kwargs['claim_id'])
        try:
            claim.insuranceletter
            return HttpResponseRedirect(
                claim.insuranceletter.get_absolute_url()
            )
        except clients_models.InsuranceLetter.DoesNotExist:
            pass

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
        claim_id = self.kwargs['claim_id']
        self.object.claim_id = claim_id
        try:
            self.object.save()
        except db_utils.IntegrityError:
            claim = Claim.objects.get(id=claim_id)
            # Was receiving errors that a user was trying to create a
            #  second insurance letter for this claim, so redirect to
            #  existing insurance letter since one already exists
            #  for this OneToOne
            return HttpResponseRedirect(
                claim.insuranceletter.get_absolute_url()
            )

        laboratory_form.instance = self.object
        laboratory_form.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, laboratory_form):
        return self.render_to_response(
            self.get_context_data(form=form, laboratory_form=laboratory_form)
        )

    def get_success_url(self):
        claim_id = self.object.claim_id

        self.success_url = reverse_lazy(
            'fillOutInsurance', kwargs={'claim_id': claim_id}
        )

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

    def get(self, request, *args, **kwargs):
        # Ensure ProofOfManufacturing does not already exist
        claim = Claim.objects.get(id=self.kwargs['claim_id'])
        try:
            claim.proofofmanufacturing
            return HttpResponseRedirect(
                claim.proofofmanufacturing.get_absolute_url()
            )
        except clients_models.ProofOfManufacturing.DoesNotExist:
            pass

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        claim_id = self.kwargs['claim_id']
        self.object.claim_id = claim_id
        try:
            self.object.save()
        except db_utils.IntegrityError:
            claim = Claim.objects.get(id=claim_id)
            # Was receiving errors that a user was trying to create a
            #  second proof of manufacturing for this claim, so redirect to
            #  existing proof of manufacturing since one already exists
            #  for this OneToOne
            return HttpResponseRedirect(
                claim.proofofmanufacturing.get_absolute_url()
            )

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        claim_id = self.object.claim.id

        self.success_url = reverse_lazy(
            'fillOutProof', kwargs={'claim_id': claim_id}
        )

        return self.success_url


class CreateClaimWizard(
    utils_wizard_views.FileStorageNamedUrlSessionWizardView
):
    INFO = 'info'
    COVERAGES = 'coverages'
    form_list = (
        (INFO, claim_forms.ClaimForm),
        (COVERAGES, claim_forms.ClaimCoverageFormFormSet),
    )
    template_name = 'utils/generics/wizard.html'

    class SkippedStepException(BaseException):
        pass

    class MissingPeriodDateException(BaseException):
        pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['save_text'] = 'create'
        context['model_name'] = Claim._meta.verbose_name
        context['form_id'] = 'claim_form'
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
        if step == self.INFO and 'client_id' in self.kwargs:
            return {'client_id': self.kwargs['client_id']}
        else:
            return super().get_form_kwargs(step)

    def get_form(self, step=None, data=None, files=None):
        if step is None:
            step = self.steps.current

        form = super().get_form(step, data, files)

        if step == self.COVERAGES:
            info_data = self.storage.get_step_data(self.INFO)
            if not info_data:
                raise self.SkippedStepException
            submitted_datetime_str = info_data.get('info-submitted_datetime')
            submitted_datetime = datetime.strptime(
                submitted_datetime_str, '%Y-%m-%d %I:%M %p'
            )
            insurance_id = info_data.get('info-insurance')
            patient_id = info_data.get('info-patient')

            coverages = Coverage.objects.select_related(
                'insurance', 'claimant'
            ).prefetch_related(
                'claimcoverage_set__claimitem_set'
            ).filter(
                insurance_id=insurance_id, claimant_id=patient_id
            )
            for coverage in coverages:
                requires_period_date = (
                    coverage.period == Coverage.BENEFIT_YEAR and
                    coverage.period_date is None
                )
                if requires_period_date:
                    exception = self.MissingPeriodDateException
                    exception.coverage = coverage
                    raise exception
            label = (
                lambda obj:
                    "%s - %s - %s"
                    " [%%%s, Amount Remaining: $%s, Quantity Remaining: %s]"
                    % (
                        obj.insurance.provider,
                        obj.get_coverage_type_display(),
                        obj.claimant.full_name(),
                        obj.coverage_percent,
                        obj.claim_amount_remaining_period(),
                        obj.quantity_remaining_period())
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

    def get(self, *args, **kwargs):
        try:
            return super().get(*args, **kwargs)
        except self.SkippedStepException:
            self.storage.current_step = self.steps.first

            return shortcuts.redirect(self.get_step_url(self.steps.first))
        except self.MissingPeriodDateException as e:
            self.storage.current_step = self.steps.first

            coverage = e.coverage
            messages.add_message(
                self.request, messages.ERROR,
                safestring.mark_safe(
                    "One of {}'s Coverages is set to Benefit Year "
                    "but does not have a Period Date set. Please "
                    "<a href='{}'>Click here to edit it</a> "
                    "before continuing".format(
                        coverage.claimant,
                        urlresolvers.reverse(
                            'insurance_update',
                            kwargs={'insurance_id': coverage.insurance.pk}
                        )
                    )
                )
            )

            return shortcuts.redirect(self.get_step_url(self.steps.first))

    def post(self, *args, **kwargs):
        try:
            return super().post(*args, **kwargs)
        except self.SkippedStepException:
            self.storage.current_step = self.steps.first

            return shortcuts.redirect(self.get_step_url(self.steps.first))

    def done(self, form_list, form_dict, **kwargs):
        claim_form = form_dict[self.INFO]
        claim_coverage_claim_item_form = form_dict[self.COVERAGES]

        claim = claim_form.save()

        claim_coverage_claim_item_form.instance = claim
        claim_coverage_claim_item_form.save()

        # has to be here just in case we need to clear new files
        LAST_INITIAL = object()
        both = itertools.zip_longest(
            claim_form.cleaned_data['claim_package'],
            claim_form.initial['claim_package'],
            fillvalue=LAST_INITIAL
        )
        for _file, initial_datum in both:
            if _file is None:
                raise Exception(
                    'MultiFile: _file is None, '
                    'initial_datum: {}'.format(initial_datum)
                )
            elif _file == initial_datum:
                if isinstance(_file, uploadedfile.UploadedFile):
                    # form wizard files are temporarily uploaded
                    clients_models.ClaimAttachment.objects.create(
                        attachment=_file, claim=claim
                    )
                else:
                    # no change
                    continue
            elif _file is False:
                if isinstance(initial_datum, uploadedfile.UploadedFile):
                    # form wizard files are temporarily uploaded
                    if not initial_datum.closed:
                        initial_datum.close()
                    self.file_storage.delete(initial_datum.name)
                else:
                    clients_models.ClaimAttachment.objects.get(
                        attachment=initial_datum, claim=claim
                    ).delete()
            elif initial_datum is LAST_INITIAL:
                raise Exception(
                    'MultiFile: initial_datum is LAST_INITIAL, '
                    'cleaned_data len does not match initial len, '
                    '_file: {}'.format(_file)
                )
            else:
                raise Exception(
                    'MultiFile: Exception, ',
                    '_file: {}, initial_datum: {}'.format(_file, initial_datum)
                )

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
        context['form_id'] = 'claim_form'
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
