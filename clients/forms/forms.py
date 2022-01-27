from django import forms
from django.forms.models import inlineformset_factory
from django.template import defaultfilters

from bootstrap3_datetime import widgets as bs3_widgets
from crispy_forms import helper

from clients.models import Client, Dependent, Coverage, \
    Invoice, InsuranceLetter, Laboratory, ProofOfManufacturing, Person
from clients import models as clients_models


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        referred_by = self.fields['referred_by']

        def label_from_instance(obj):
            try:
                client = clients_models.Dependent.objects.get(
                    pk=obj.pk
                ).primary
                return '{obj}, Dependent of {client}'.format(
                    obj=obj, client=client
                )
            except clients_models.Dependent.DoesNotExist:
                return obj
        referred_by.label_from_instance = label_from_instance

        queryset = referred_by.queryset.extra(
            select={
                'lower_first_name': 'lower(first_name)'
            }
        ).order_by('lower_first_name')
        referred_by.queryset = queryset


class DependentForm(forms.ModelForm):
    class Meta:
        model = Dependent
        exclude = ('primary',)


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


class InvoiceForm(forms.ModelForm):

    class Meta:
        model = Invoice
        exclude = ('claim',)
        help_texts = {
            'invoice_number':
                'Leave blank to automatically use the next number'
        }


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


class ReferralForm(forms.ModelForm):

    class EmptyClaimsQuerySet(Exception):
        pass

    class Meta:
        model = clients_models.Referral
        exclude = ('client',)
        widgets = {'claims': forms.CheckboxSelectMultiple}

    def _get_referred_claims(self, person, claims_queryset):
        referred_set = person.referred_set.all()
        for referred in referred_set:
            claims = referred.claim_set.filter(
                claimcoverage__actual_paid_date__isnull=False
            )
            claims_queryset = claims_queryset | claims

        return claims_queryset

    def _remove_credited_claims(self, claims_queryset, client):
        claims = clients_models.Referral.objects.prefetch_related(
            'claims'
        ).filter(client=client).values_list('claims', flat=True)

        clients = clients_models.Claim.objects.filter(
            id__in=claims).values_list('patient', flat=True)

        claims_queryset = claims_queryset.exclude(
            patient__in=clients)

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

        if claims_queryset:
            claims_queryset = self._remove_credited_claims(
                claims_queryset, client)

        if not claims_queryset:
            raise self.EmptyClaimsQuerySet

        self.fields['claims'].queryset = claims_queryset


class ReceiptForm(forms.ModelForm):
    datetime = forms.DateTimeField(
        input_formats=['%Y-%m-%d %I:%M %p'],
        widget=bs3_widgets.DateTimePicker(
            options={"format": "YYYY-MM-DD hh:mm a"},
            attrs={
                "class": "form-control",
                # am/pm -> AM/PM
                "style": "text-transform: uppercase; float: none;"
            },
            div_attrs={
                'class': 'input-group',
            }
        )
    )

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

        self.fields['notes'].widget.attrs['rows'] = 5

        self.helper = helper.FormHelper(self)
        self.helper.form_tag = False
