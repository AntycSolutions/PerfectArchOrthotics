from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView

from clients.models import Claim, Invoice, InsuranceLetter, \
    ProofOfManufacturing, Client
from clients.forms.forms import ClaimForm, InvoiceForm, \
    InsuranceLetterForm, ProofOfManufacturingForm, \
    LaboratoryInsuranceLetterFormSet


class CreateClaimView(CreateView):
    template_name = 'clients/claim/create_claim.html'
    model = Claim
    form_class = ClaimForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        client = Client.objects.get(id=self.kwargs['client_id'])
        self.object.client = client
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        self.success_url = reverse_lazy('claim_detail',
                                        kwargs={'client_id': self.object.id})
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

    def get_success_url(self):
        client_id = self.object.client.id
        self.success_url = reverse_lazy('client',
                                        kwargs={'client_id': client_id})
        return self.success_url


class DeleteClaimView(DeleteView):
    template_name = 'clients/claim/delete_claim.html'
    model = Claim
    form_class = InvoiceForm
    slug_field = "id"
    slug_url_kwarg = "claim_id"
    success_url = reverse_lazy('claims')

    def get_success_url(self):
        client_id = self.object.client.id
        self.success_url = reverse_lazy('client',
                                        kwargs={'client_id': client_id})
        return self.success_url


class UpdateInvoiceView(UpdateView):
    template_name = 'clients/claim/update_invoice.html'
    model = Invoice
    form_class = InvoiceForm
    slug_field = "id"
    slug_url_kwarg = "invoice_id"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        item_form = ItemFormSet(instance=self.object)
        return self.render_to_response(
            self.get_context_data(form=form,
                                  item_form=item_form))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        item_form = ItemFormSet(request.POST, instance=self.object)
        if (form.is_valid() and item_form.is_valid()):
            return self.form_valid(form, item_form)
        else:
            return self.form_invalid(form, item_form)

    def form_valid(self, form, item_form):
        self.object = form.save()
        item_form.save()

        return HttpResponseRedirect(self.get_success_url(self.object.claim))

    def form_invalid(self, form, item_form):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  item_form=item_form))

    def get_success_url(self, claim):
        client_id = self.object.claim.client.id
        claim_id = self.object.claim.id
        self.success_url = reverse_lazy('fillOutInvoice',
                                        kwargs={'client_id': client_id,
                                                'claim_id': claim_id})
        return self.success_url


class CreateInvoiceView(CreateView):
    template_name = 'clients/claim/create_invoice.html'
    model = Invoice
    form_class = InvoiceForm

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        item_form = ItemFormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  item_form=item_form))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        item_form = ItemFormSet(request.POST)
        if (form.is_valid() and item_form.is_valid()):
            return self.form_valid(form, item_form)
        else:
            return self.form_invalid(form, item_form)

    def form_valid(self, form, item_form):
        self.object = form.save(commit=False)
        claim = Claim.objects.get(id=self.kwargs['claim_id'])
        self.object.claim = claim
        self.object.save()
        item_form.instance = self.object
        item_form.save()

        return HttpResponseRedirect(self.get_success_url(claim))

    def form_invalid(self, form, item_form):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  item_form=item_form))

    def get_success_url(self, claim):
        client_id = claim.client.id
        claim_id = claim.id
        self.success_url = reverse_lazy('fillOutInvoice',
                                        kwargs={'client_id': client_id,
                                                'claim_id': claim_id})
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
            self.get_context_data(form=form,
                                  laboratory_form=laboratory_form
                                  ))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        laboratory_form = LaboratoryInsuranceLetterFormSet(
            request.POST, instance=self.object)
        if (form.is_valid()
                and laboratory_form.is_valid()):
            return self.form_valid(form,
                                   laboratory_form
                                   )
        else:
            return self.form_invalid(form,
                                     laboratory_form
                                     )

    def form_valid(self, form,
                   laboratory_form
                   ):
        self.object = form.save()
        laboratory_form.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form,
                     laboratory_form
                     ):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  laboratory_form=laboratory_form
                                  ))

    def get_success_url(self):
        client_id = self.object.claim.client.id
        claim_id = self.object.claim.id
        self.success_url = reverse_lazy('fillOutInsurance',
                                        kwargs={'client_id': client_id,
                                                'claim_id': claim_id})
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
            self.get_context_data(form=form,
                                  laboratory_form=laboratory_form
                                  ))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        laboratory_form = LaboratoryInsuranceLetterFormSet(request.POST)
        if (form.is_valid()
                and laboratory_form.is_valid()):
            return self.form_valid(form,
                                   laboratory_form
                                   )
        else:
            return self.form_invalid(form,
                                     laboratory_form
                                     )

    def form_valid(self, form,
                   laboratory_form
                   ):
        self.object = form.save(commit=False)
        claim = Claim.objects.get(id=self.kwargs['claim_id'])
        self.object.claim = claim
        self.object.save()
        laboratory_form.instance = self.object
        laboratory_form.save()

        return HttpResponseRedirect(self.get_success_url(claim))

    def form_invalid(self, form,
                     laboratory_form
                     ):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  laboratory_form=laboratory_form
                                  ))

    def get_success_url(self, claim):
        client_id = claim.client.id
        claim_id = claim.id
        self.success_url = reverse_lazy('fillOutInsurance',
                                        kwargs={'client_id': client_id,
                                                'claim_id': claim_id})
        return self.success_url


class UpdateProofOfManufacturingView(UpdateView):
    template_name = 'clients/claim/update_proof_of_manufacturing.html'
    model = ProofOfManufacturing
    form_class = ProofOfManufacturingForm
    slug_field = "id"
    slug_url_kwarg = "proof_of_manufacturing_id"

    def get_success_url(self):
        client_id = self.object.claim.client.id
        claim_id = self.object.claim.id
        self.success_url = reverse_lazy('fillOutProof',
                                        kwargs={'client_id': client_id,
                                                'claim_id': claim_id})
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

        return HttpResponseRedirect(self.get_success_url(claim))

    def get_success_url(self, claim):
        client_id = claim.client.id
        claim_id = claim.id
        self.success_url = reverse_lazy('fillOutProof',
                                        kwargs={'client_id': client_id,
                                                'claim_id': claim_id})
        return self.success_url
