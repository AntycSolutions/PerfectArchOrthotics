from django import forms
from django.forms.models import inlineformset_factory

from clients.models import Client, Dependent, Insurance, CoverageType, Claim, \
    Invoice, Item, InsuranceLetter, Laboratory, ProofOfManufacturing


class ClientForm(forms.ModelForm):
    # required
    # first_name = forms.CharField(
    #     max_length=128, help_text="Client first name")
    # last_name = forms.CharField(
    #     max_length=128, help_text="Client last name")
    # birth_date = forms.CharField(
    #     help_text="Client birthdate")

    # not required
    # address = forms.CharField(
    #     max_length=128, help_text="Client address", required=False)
    # city = forms.CharField(
    #     max_length=128, help_text="Client city", required=False)
    # postal_code = forms.CharField(
    #     max_length=6, help_text="Client postal code (no spaces)",
    #     required=False)
    # phone_number = forms.CharField(
    #     max_length=14, help_text="Client home phone", required=False)
    # cell_number = forms.CharField(
    #     max_length=14, help_text="Client cell phone", required=False)
    # email = forms.CharField(
    #     max_length=254, help_text="Client email", required=False)
    # gender = forms.ChoiceField(
    #     choices=Person.GENDER_CHOICES, help_text="Gender", required=False)
    # employer = forms.CharField(
    #     max_length=128, help_text="Client employer", required=False)
    # referred_by = forms.CharField(
    #     max_length=128, required=False)
    # health_care_number = forms.CharField(
    #     max_length=20, required=False)

    class Meta:
        model = Client

        # fields = ('firstName', 'lastName', 'birthdate', 'address', 'city',
        #           'postalCode', 'phoneNumber', 'cellNumber', 'email',
        #           'healthcareNumber', 'gender', 'employer', 'referredBy')
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
    # first_name = forms.CharField(
    #     max_length=128, help_text="Dependent first name")
    # last_name = forms.CharField(
    #     max_length=128, help_text="Dependent last name")
    # birth_date = forms.CharField(
    #     help_text="Dependent birthdate")
    # gender = forms.ChoiceField(
    #     choices=Dependent.GENDER_CHOICES, help_text="Gender", required=False)
    # relationship = forms.ChoiceField(
    #     choices=Dependent.RELATIONSHIP_CHOICES, help_text="Relationship",
    #     required=False)

    class Meta:
        model = Dependent

        # fields = ('firstName', 'lastName', 'birthdate', 'gender',
        #           'relationship')
        fields = ('__all__')

    # def clean(self):
    #     cleaned_data = super(DependentForm, self).clean()
    #     if 'birth_date' in cleaned_data.keys():
    #         if len(cleaned_data['birth_date'].split('/')) > 1:
    #             m, d, y = cleaned_data['birth_date'].split('/')
    #             new_birth_date = "%s-%s-%s" % (y, m, d)
    #             cleaned_data['birth_date'] = new_birth_date
    #     return cleaned_data


class InsuranceForm(forms.ModelForm):
    # provider = forms.CharField(
    #     max_length=128)
    # policy_number = forms.CharField(
    #     max_length=128, required=False)
    # contract_number = forms.CharField(
    #     max_length=128, required=False)
    # billing = forms.ChoiceField(
    #     choices=Insurance.BILLING_CHOICES, required=False)
    # gait_scan = forms.BooleanField(
    #     required=False)
    # insurance_card = forms.BooleanField(
    #     required=False)

    class Meta:
        model = Insurance

        # fields = ('provider', 'policyNumber', 'contractNumber', 'billing',
        #           'gaitScan', 'insuranceCard')
        exclude = ('client', 'spouse')


class CoverageForm(forms.ModelForm):
    # coverage_type = forms.ChoiceField(
    #     choices=CoverageType.COVERAGE_TYPE, required=False)
    # coverage_percent = forms.IntegerField()
    # max_claim_amount = forms.IntegerField()
    # quantity = forms.IntegerField()
    # period = forms.IntegerField()

    class Meta:
        model = CoverageType

        # fields = ('coverageType', 'coveragePercent', 'maxClaimAmount',
        #           'quantity', 'period')
        exclude = ('insurance',)


class ClaimForm(forms.ModelForm):
    # payment_type = forms.ChoiceField(
    #     choices=Claim.PAYMENT_CHOICES, required=True)

    class Meta:
        model = Claim

        # fields = ('claimType', 'paymentType',)
        exclude = ('client', 'patient', 'coverage_types', 'amount_claimed',
                   'expected_back')


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


ItemFormSet = inlineformset_factory(
    Invoice, Item,
    exclude=('invoice',)
)

LaboratoryInsuranceLetterFormSet = inlineformset_factory(
    InsuranceLetter,
    Laboratory,
    exclude=('insurance_letter', 'proof_of_manufacturing')
)

LaboratoryProofOfManufacturingFormSet = inlineformset_factory(
    ProofOfManufacturing,
    Laboratory,
    exclude=('insurance_letter', 'proof_of_manufacturing'),
    extra=1
)
