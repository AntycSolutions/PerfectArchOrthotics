from django import forms
from django.forms.models import inlineformset_factory

from clients.models import Client, Dependent, Insurance, CoverageType, Claim, \
    Invoice, InsuranceLetter, Laboratory, ProofOfManufacturing


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        exclude = ('dependents',)

    # def clean(self):
    #     cleaned_data = super(ClientForm, self).clean()
    #     if 'birth_date' in cleaned_data.keys():
    #         if len(cleaned_data['birth_date'].split('/')) > 1:
    #             m, d, y = cleaned_data['birth_date'].split('/')
    #             new_birth_date = "%s-%s-%s" % (y, m, d)
    #             cleaned_data['birth_date'] = new_birth_date
    #     return cleaned_data


class DependentForm(forms.ModelForm):

    class Meta:
        model = Dependent
        exclude = ('client',)

    # def clean(self):
    #     cleaned_data = super(DependentForm, self).clean()
    #     if 'birth_date' in cleaned_data.keys():
    #         if len(cleaned_data['birth_date'].split('/')) > 1:
    #             m, d, y = cleaned_data['birth_date'].split('/')
    #             new_birth_date = "%s-%s-%s" % (y, m, d)
    #             cleaned_data['birth_date'] = new_birth_date
    #     return cleaned_data


class InsuranceForm(forms.ModelForm):

    class Meta:
        model = Insurance
        exclude = ('client', 'spouse')


class CoverageForm(forms.ModelForm):

    class Meta:
        model = CoverageType
        exclude = ('insurance',)


class ClaimForm(forms.ModelForm):

    class Meta:
        model = Claim
        exclude = ('client', 'patient', 'insurance', 'coverage_types', 'items',
                   'amount_claimed', 'estimated_expected_back')


class InvoiceForm(forms.ModelForm):

    class Meta:
        model = Invoice
        exclude = ('claim',)


class InsuranceLetterForm(forms.ModelForm):

    class Meta:
        model = InsuranceLetter
        exclude = ('claim',)


class ProofOfManufacturingForm(forms.ModelForm):

    class Meta:
        model = ProofOfManufacturing
        exclude = ('claim',)


LaboratoryInsuranceLetterFormSet = inlineformset_factory(
    InsuranceLetter,
    Laboratory,
    exclude=('insurance_letter', 'proof_of_manufacturing')
)
