from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.forms.models import inlineformset_factory

from clients.models import Claim, Invoice, InsuranceLetter, \
    ProofOfManufacturing, Client, Coverage, ClaimCoverage, ClaimItem, Dependent
from clients.forms.forms import ClaimForm, InvoiceForm, \
    InsuranceLetterForm, ProofOfManufacturingForm, \
    LaboratoryInsuranceLetterFormSet, \
    MinimumInlineFormSet, minimum_nestedformset_factory


class CreateClaimView(CreateView):
    template_name = 'clients/claim/create_claim.html'
    model = Claim
    form_class = ClaimForm

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        client = Client.objects.get(pk=self.kwargs['client_id'])
        return form_class(client, **self.get_form_kwargs())

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        claim_form = self.get_form(form_class)

        ClaimCoverageFormFormSet = minimum_nestedformset_factory(
            Claim, ClaimCoverage,
            inlineformset_factory(
                ClaimCoverage, ClaimItem,
                formset=MinimumInlineFormSet, extra=1, fields='__all__',
            ),
            minimum_name="Coverage", minimum_name_nested="Item",
            extra=1, exclude=('items',),
        )
        nestedformset = ClaimCoverageFormFormSet()

        insurances = claim_form.client.insurance_set.all()
        for dependent in claim_form.client.dependent_set.all():
            if dependent.relationship == Dependent.SPOUSE:
                insurances = insurances | dependent.insurance_set.all()
        coverages = Coverage.objects.filter(insurance__in=insurances)
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
                    obj.description, obj.unit_price)
        )
        nestedformset.form.base_fields[
            'coverage'].queryset = coverages
        nestedformset.form.base_fields[
            'coverage'].label_from_instance = label
        nestedformset.nested_formset_class.form.base_fields[
            'item'].label_from_instance = items_label
        items = nestedformset.nested_formset_class.form.base_fields[
            'item'].queryset
        nestedformset.nested_formset_class.form.base_fields[
            'item'].queryset = items.order_by('coverage_type', 'product_code',
                                              'gender')
        for form in nestedformset:
            form.fields['coverage'].queryset = coverages
            form.fields['coverage'].label_from_instance = label
            form.nested.form.base_fields[
                'item'].label_from_instance = items_label
            items = form.nested.form.base_fields[
                'item'].queryset
            form.nested.form.base_fields[
                'item'].queryset = items.order_by('coverage_type',
                                                  'product_code', 'gender')

        return self.render_to_response(
            self.get_context_data(claim_form=claim_form,
                                  nestedformset=nestedformset)
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        claim_form = self.get_form(form_class)

        ClaimCoverageFormFormSet = minimum_nestedformset_factory(
            Claim, ClaimCoverage,
            inlineformset_factory(
                ClaimCoverage, ClaimItem,
                formset=MinimumInlineFormSet, extra=1, fields='__all__',
            ),
            minimum_name="Coverage", minimum_name_nested="Item",
            extra=1, exclude=('items',),
        )
        nestedformset = ClaimCoverageFormFormSet(request.POST)

        insurances = claim_form.client.insurance_set.all()
        for dependent in claim_form.client.dependent_set.all():
            if dependent.relationship == Dependent.SPOUSE:
                insurances = insurances | dependent.insurance_set.all()
        coverages = Coverage.objects.filter(insurance__in=insurances)
        label = (
            lambda obj:
                "%s - %s [%%%s, Amount Remaining: $%s, Quantity Remaining: %s]"
                % (
                    obj.get_coverage_type_display(),
                    obj.claimant.full_name(),
                    obj.coverage_percent,
                    obj.claim_amount_remaining(),
                    obj.quantity_remaining())
        )
        items_label = (
            lambda obj:
                "%s - %s - %s - $%s" % (
                    obj.get_coverage_type_display(), obj.product_code,
                    obj.description, obj.unit_price)
        )
        nestedformset.form.base_fields[
            'coverage'].queryset = coverages
        nestedformset.form.base_fields[
            'coverage'].label_from_instance = label
        nestedformset.nested_formset_class.form.base_fields[
            'item'].label_from_instance = items_label
        items = nestedformset.nested_formset_class.form.base_fields[
            'item'].queryset
        nestedformset.nested_formset_class.form.base_fields[
            'item'].queryset = items.order_by('coverage_type', 'product_code',
                                              'gender')
        for form in nestedformset:
            form.fields['coverage'].queryset = coverages
            form.fields['coverage'].label_from_instance = label
            form.nested.form.base_fields[
                'item'].label_from_instance = items_label
            items = form.nested.form.base_fields[
                'item'].queryset
            form.nested.form.base_fields[
                'item'].queryset = items.order_by('coverage_type',
                                                  'product_code', 'gender')

        if claim_form.is_valid() and nestedformset.is_valid():
            return self.form_valid(claim_form, nestedformset)
        else:
            return self.form_invalid(claim_form, nestedformset)

    def form_valid(self, claim_form, nestedformset):
        self.object = claim_form.save()

        nestedformset.instance = self.object
        nestedformset.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, claim_form, nestedformset):
        return self.render_to_response(
            self.get_context_data(claim_form=claim_form,
                                  nestedformset=nestedformset)
        )

    def get_success_url(self):
        self.success_url = reverse_lazy('claim',
                                        kwargs={'claim_id': self.object.id})
        return self.success_url


class DetailClaimView(DetailView):
    template_name = 'clients/claim/detail_claim.html'
    model = Claim


class UpdateClaimView(UpdateView):
    template_name = 'clients/claim/update_claim.html'
    model = Claim
    form_class = ClaimForm
    slug_field = "id"
    slug_url_kwarg = "claim_id"

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        client = self.object.patient.get_client()
        return form_class(client, **self.get_form_kwargs())

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        claim_form = self.get_form(form_class)

        ClaimCoverageFormFormSet = minimum_nestedformset_factory(
            Claim, ClaimCoverage,
            inlineformset_factory(
                ClaimCoverage, ClaimItem,
                formset=MinimumInlineFormSet, extra=1, fields='__all__',
            ),
            minimum_name="Coverage", minimum_name_nested="Item",
            extra=1, exclude=('items',),
        )
        nestedformset = ClaimCoverageFormFormSet(instance=self.object)

        insurances = claim_form.client.insurance_set.all()
        for dependent in claim_form.client.dependent_set.all():
            if dependent.relationship == Dependent.SPOUSE:
                insurances = insurances | dependent.insurance_set.all()
        coverages = Coverage.objects.filter(insurance__in=insurances)
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
                    obj.description, obj.unit_price)
        )
        nestedformset.form.base_fields[
            'coverage'].queryset = coverages
        nestedformset.form.base_fields[
            'coverage'].label_from_instance = label
        nestedformset.nested_formset_class.form.base_fields[
            'item'].label_from_instance = items_label
        items = nestedformset.nested_formset_class.form.base_fields[
            'item'].queryset
        nestedformset.nested_formset_class.form.base_fields[
            'item'].queryset = items.order_by('coverage_type', 'product_code',
                                              'gender')
        for form in nestedformset:
            form.fields['coverage'].queryset = coverages
            form.fields['coverage'].label_from_instance = label
            form.nested.form.base_fields[
                'item'].label_from_instance = items_label
            items = form.nested.form.base_fields[
                'item'].queryset
            form.nested.form.base_fields[
                'item'].queryset = items.order_by('coverage_type',
                                                  'product_code', 'gender')

        return self.render_to_response(
            self.get_context_data(claim_form=claim_form,
                                  nestedformset=nestedformset)
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        claim_form = self.get_form(form_class)

        ClaimCoverageFormFormSet = minimum_nestedformset_factory(
            Claim, ClaimCoverage,
            inlineformset_factory(
                ClaimCoverage, ClaimItem,
                formset=MinimumInlineFormSet, extra=1, fields='__all__',
            ),
            minimum_name="Coverage", minimum_name_nested="Item",
            extra=1, exclude=('items',),
        )
        nestedformset = ClaimCoverageFormFormSet(
            request.POST, instance=self.object)

        insurances = claim_form.client.insurance_set.all()
        for dependent in claim_form.client.dependent_set.all():
            if dependent.relationship == Dependent.SPOUSE:
                insurances = insurances | dependent.insurance_set.all()
        coverages = Coverage.objects.filter(insurance__in=insurances)
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
                    obj.get_coverage_type_display(), obj.product_code,
                    obj.description, obj.unit_price)
        )
        nestedformset.form.base_fields[
            'coverage'].queryset = coverages
        nestedformset.form.base_fields[
            'coverage'].label_from_instance = label
        nestedformset.nested_formset_class.form.base_fields[
            'item'].label_from_instance = items_label
        items = nestedformset.nested_formset_class.form.base_fields[
            'item'].queryset
        nestedformset.nested_formset_class.form.base_fields[
            'item'].queryset = items.order_by('coverage_type', 'product_code',
                                              'gender')
        for form in nestedformset:
            form.fields['coverage'].queryset = coverages
            form.fields['coverage'].label_from_instance = label
            form.nested.form.base_fields[
                'item'].label_from_instance = items_label
            items = form.nested.form.base_fields[
                'item'].queryset
            form.nested.form.base_fields[
                'item'].queryset = items.order_by('coverage_type',
                                                  'product_code', 'gender')

        if claim_form.is_valid() and nestedformset.is_valid():
            return self.form_valid(claim_form, nestedformset)
        else:
            return self.form_invalid(claim_form, nestedformset)

    def form_valid(self, claim_form, nestedformset):
        self.object = claim_form.save()
        nestedformset.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, claim_form, nestedformset):
        return self.render_to_response(
            self.get_context_data(claim_form=claim_form,
                                  nestedformset=nestedformset)
        )

    def get_success_url(self):
        self.success_url = reverse_lazy('claim',
                                        kwargs={'claim_id': self.object.id})
        return self.success_url


class DeleteClaimView(DeleteView):
    template_name = 'utils/generics/delete.html'
    model = Claim
    slug_field = "id"
    slug_url_kwarg = "claim_id"
    success_url = reverse_lazy('claims')

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
        context = super(CreateInvoiceView, self).get_context_data(**kwargs)
        claim = Claim.objects.get(id=self.kwargs['claim_id'])
        context['claim'] = claim

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


class UpdateProofOfManufacturingView(UpdateView):
    template_name = 'clients/claim/update_proof_of_manufacturing.html'
    model = ProofOfManufacturing
    form_class = ProofOfManufacturingForm
    slug_field = "id"
    slug_url_kwarg = "proof_of_manufacturing_id"

    def get_success_url(self):
        claim_id = self.object.claim.id
        self.success_url = reverse_lazy('fillOutProof',
                                        kwargs={'claim_id': claim_id})
        return self.success_url


class CreateProofOfManufacturingView(CreateView):
    template_name = 'clients/claim/create_proof_of_manufacturing.html'
    model = ProofOfManufacturing
    form_class = ProofOfManufacturingForm

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
