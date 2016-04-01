from itertools import zip_longest
import itertools

from django import forms
from django.forms import BaseInlineFormSet
from django.forms.models import inlineformset_factory
from django.template import defaultfilters

from crispy_forms import helper, layout, bootstrap

from bootstrap3_datetime.widgets import DateTimePicker

from utils.forms import fields as utils_fields, widgets as utils_widgets

from clients.models import Client, Dependent, Insurance, Coverage, Claim, \
    Invoice, InsuranceLetter, Laboratory, ProofOfManufacturing, Person, Item, \
    ClaimItem, ClaimCoverage, ClaimAttachment
from clients import models as clients_models


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = '__all__'


class DependentForm(forms.ModelForm):

    class Meta:
        model = Dependent
        exclude = ('client',)


class InsuranceForm(forms.ModelForm):

    class Meta:
        model = Insurance
        exclude = ('main_claimant', 'claimants')


class CoverageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        main_claimant = kwargs.pop('main_claimant', None)
        super(CoverageForm, self).__init__(*args, **kwargs)
        if main_claimant:
            dependents = main_claimant.get_client().dependent_set.all()
            dependents_pks = list(dependents.values_list('pk', flat=True))
            pks = dependents_pks + [main_claimant.pk]
            self.fields['claimant'].queryset = Person.objects.filter(
                pk__in=pks)

    class Meta:
        model = Coverage
        exclude = ('insurance',)


class ClaimForm(forms.ModelForm):
    submitted_datetime = forms.DateTimeField(
        label="Submitted Datetime",
        input_formats=['%Y-%m-%d %I:%M %p'],
        widget=DateTimePicker(
            options={"format": "YYYY-MM-DD hh:mm a"},
            attrs={"class": "form-control",
                   # am/pm -> AM/PM
                   "style": "text-transform: uppercase; float: none;"},
        )
    )
    claim_package = utils_fields.MultiFileField(
        label="Claim Package",
        required=False,
        max_file_size=3.0*1024*1024  # mb*kb*b,
    )

    def __init__(self, client, *args, **kwargs):
        super().__init__(*args, **kwargs)

        file_list = [
            claim_attachment.attachment
            for claim_attachment in self.instance.claimattachment_set.all()
        ]
        claim_package = self.fields['claim_package']
        claim_package.widget = \
            utils_widgets.ConfirmMultiFileMultiWidget(
                form_id="update_claim_form",  # html
                form=self,
                field_name='claim_package',
                file_count=len(file_list)
            )
        self.initial['claim_package'] = file_list

        self.client = client

        patients = []
        spouse = None
        for dependent in client.dependent_set.all():
            if dependent.relationship == Dependent.SPOUSE:
                spouse = dependent.id
            patients.append(dependent.id)
        patients.append(client.id)
        patient = self.fields['patient']
        patient.queryset = Person.objects.filter(id__in=patients)
        patient.label_from_instance = (
            lambda obj:
                "Client - %s" % obj.full_name() if obj.id == client.id
                else "Spouse - %s" % obj.full_name() if obj.id == spouse
                else "Child - %s" % obj.full_name()
        )

        insurance = self.fields['insurance']
        insurance.queryset = Insurance.objects.filter(
            main_claimant__pk__in=patients)
        insurance.label_from_instance = (
            lambda obj:
                "%s - Spouse - %s" % (
                    obj.provider,
                    obj.main_claimant.full_name()
                ) if obj.main_claimant.pk == spouse
                else "%s - Client - %s" % (
                    obj.provider, obj.main_claimant.full_name())
        )
        insurance.widget.attrs['class'] = 'insurance_trigger'

    def save(self, commit=True):
        instance = super().save(commit)

        LAST_INITIAL = object()
        both = itertools.zip_longest(self.cleaned_data['claim_package'],
                                     self.initial['claim_package'],
                                     fillvalue=LAST_INITIAL)
        for _file, initial_datum in both:
            if _file is None or _file == initial_datum:
                continue
            elif _file is False:
                ClaimAttachment.objects.get(
                    attachment=initial_datum, claim=instance
                ).delete()
            elif initial_datum is LAST_INITIAL:
                for _new_file in _file:
                    ClaimAttachment.objects.create(attachment=_new_file,
                                                   claim=instance)
            else:
                raise Exception("Unknown Exception during MultiFile save.")

        return instance

    class Meta:
        model = Claim
        exclude = ('coverages',)


class InvoiceForm(forms.ModelForm):

    class Meta:
        model = Invoice
        exclude = ('claim',)


class InsuranceLetterForm(forms.ModelForm):

    class Meta:
        model = InsuranceLetter
        exclude = ('claim',)


LaboratoryInsuranceLetterFormSet = inlineformset_factory(
    InsuranceLetter,
    Laboratory,
    exclude=('insurance_letter',)
)


class ProofOfManufacturingForm(forms.ModelForm):

    class Meta:
        model = ProofOfManufacturing
        exclude = ('claim',)


class BaseNestedFormSet(BaseInlineFormSet):

    def add_fields(self, form, index):
        super(BaseNestedFormSet, self).add_fields(form, index)

        form.nested = self.nested_formset_class(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            files=form.files if form.is_bound else None,
            prefix='%s-%s' % (
                form.prefix,
                self.nested_formset_class.get_default_prefix()
            ),
        )

    def is_valid(self):
        result = super(BaseNestedFormSet, self).is_valid()

        if self.is_bound:
            for form in self.forms:
                if not self._should_delete_form(form):
                    result = result and form.nested.is_valid()

        return result

    def save(self, commit=True):
        result = super(BaseNestedFormSet, self).save(commit=commit)

        nested_result_list = []
        for form in self.forms:
            if not self._should_delete_form(form):
                nested_result = form.nested.save(commit=commit)
                if nested_result:
                    nested_result_list.append(nested_result)

        result_tuples = []
        for r, nr in zip_longest(result, nested_result_list):
            result_tuples.append((r, nr))

        return result_tuples

    @property
    def media(self):
        return self.empty_form.media + self.empty_form.nested.media


class BaseNestedModelForm(forms.ModelForm):

    def has_changed(self):
        return (super(BaseNestedModelForm, self).has_changed()
                or self.nested.has_changed())


class MinimumInlineFormSet(BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        super(MinimumInlineFormSet, self).__init__(*args, **kwargs)

        if not hasattr(self, 'minimum'):
            self.minimum = 1
        if not hasattr(self, 'minimum_name'):
            self.minimum_name = self.model.__name__

    def clean(self):
        super(MinimumInlineFormSet, self).clean()

        count = 0
        for form in self.forms:
            try:
                if (form.cleaned_data
                        and not form.cleaned_data.get('DELETE', False)):
                    count += 1
            except AttributeError:
                # Invalid subform raises AttributeError for cleaned_data
                pass

        if (count < self.minimum) and self.validate_minimum:
            raise forms.ValidationError(
                'Please add at least %s %s%s.' % (
                    self.minimum, self.minimum_name,
                    '' if self.minimum == 1 else 's'
                )
            )


class MinimumNestedFormSet(BaseNestedFormSet):

    def __init__(self, *args, **kwargs):
        super(MinimumNestedFormSet, self).__init__(*args, **kwargs)

        if not hasattr(self, 'minimum'):
            self.minimum = 1
        if not hasattr(self, 'minimum_name'):
            self.minimum_name = self.model.__name__

    def clean(self):
        count = 0
        for form in self.forms:
            try:
                form.nested.validate_minimum = False
                if (form.cleaned_data
                        and not form.cleaned_data.get('DELETE', False)):
                    count += 1
                    if form.cleaned_data['id'] or form.has_changed():
                        form.nested.validate_minimum = True
            except AttributeError:
                # Invalid subform raises AttributeError for cleaned_data
                pass

        if count < self.minimum:
            raise forms.ValidationError(
                'Please add at least %s %s%s.' % (
                    self.minimum, self.minimum_name,
                    '' if self.minimum == 1 else 's'
                )
            )

        super(MinimumNestedFormSet, self).clean()


def nestedformset_factory(parent_model, child_model, nested_formset, **kwargs):
    if 'formset' not in kwargs:
        kwargs['formset'] = BaseNestedFormSet
    if 'form' not in kwargs:
        kwargs['form'] = BaseNestedModelForm

    NestedFormSet = inlineformset_factory(
        parent_model,
        child_model,
        **kwargs
    )
    NestedFormSet.nested_formset_class = nested_formset

    return NestedFormSet  # Is class, not instance


def minimum_nestedformset_factory(
        parent_model, model, nested_formset,
        minimum=1, minimum_name=None,
        minimum_nested=1, minimum_name_nested=None,
        **kwargs):
    if 'formset' not in kwargs:
        kwargs['formset'] = MinimumNestedFormSet
    if 'form' not in kwargs:
        kwargs['form'] = BaseNestedModelForm

    NestedFormSet = inlineformset_factory(
        parent_model,
        model,
        **kwargs
    )
    NestedFormSet.nested_formset_class = nested_formset

    if not hasattr(NestedFormSet, 'minimum'):
        NestedFormSet.minimum = minimum
    if not hasattr(NestedFormSet, 'minimum_name'):
        NestedFormSet.minimum_name = minimum_name
    if not hasattr(NestedFormSet.nested_formset_class, 'minimum'):
        NestedFormSet.nested_formset_class.minimum = (
            minimum_nested or model.__name__
        )
    if not hasattr(NestedFormSet.nested_formset_class, 'minimum_name'):
        NestedFormSet.nested_formset_class.minimum_name = (
            minimum_name_nested or nested_formset.model.__name__
        )

    return NestedFormSet  # Is class, not instance


class ReferralForm(forms.ModelForm):

    class EmptyClaimsQuerySet(Exception):
        pass

    class Meta:
        model = clients_models.Referral
        exclude = ('client',)
        widgets = {'claims': forms.CheckboxSelectMultiple}

    def _get_referred_claims(self, person, claims_queryset):
        referred_set = person.referred_by.select_related(
            'person_ptr', 'referred_by',
        ).all()
        for referred in referred_set:
            claims = referred.claim_set.filter(
                claimcoverage__actual_paid_date__isnull=False
            )
            claims_queryset = claims_queryset | claims

        return claims_queryset

    def __init__(self, client, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['claims'].label_from_instance = (
            lambda obj:
                "{} - {}".format(
                    obj.patient,
                    defaultfilters.date(obj.submitted_datetime,
                                        "N j, Y, P")
                )
        )

        claims_queryset = clients_models.Claim.objects.none()
        claims_queryset = self._get_referred_claims(
            client.person_ptr, claims_queryset
        )

        for dependent in client.dependent_set.all():
            claims_queryset = self._get_referred_claims(
                dependent.person_ptr, claims_queryset
            )

        claims = clients_models.Referral.objects.prefetch_related(
            'claims'
        ).filter(client=client).values_list('claims', flat=True)
        if claims_queryset:
            claims_queryset = claims_queryset.exclude(id__in=claims)

        if not claims_queryset:
            raise self.EmptyClaimsQuerySet

        self.fields['claims'].queryset = claims_queryset


class ReceiptForm(forms.ModelForm):

    class Meta:
        model = clients_models.Receipt
        exclude = ['claim']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['MID'].help_text = \
            'Ex. 8027813602'
        self.fields['TID'].help_text = \
            'Ex. 0089250008027813602107'
        self.fields['REF'].help_text = \
            'Ex. 00000001'
        self.fields['batch'].help_text = \
            'Ex. 138'
        self.fields['RRN'].help_text = \
            'Ex. 00046752128 (for DEBIT)'
        self.fields['APPR'].help_text = \
            'Ex. 035787'
        self.fields['trace'].help_text = \
            'Ex. 1'
        self.fields['card_number'].help_text = \
            'Ex. 1234'

        self.fields['AID'].help_text = \
            'Ex. A0000000031010 (for CHIP)'
        self.fields['TVR'].help_text = \
            'Ex. 00 80 00 80 00 (for CHIP)'
        self.fields['TSI'].help_text = \
            'Ex. F8 00 (for CHIP)'


class NoteForm(forms.ModelForm):
    class Meta:
        model = clients_models.Note
        exclude = ['client']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = helper.FormHelper(self)
        self.helper.form_tag = False
