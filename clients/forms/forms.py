from collections import OrderedDict

from django import forms
from django.forms import models
from django.forms import fields
from django.forms.models import inlineformset_factory

from clients.models import Client, Dependent, Insurance, CoverageType, Claim, \
    Invoice, InsuranceLetter, Laboratory, ProofOfManufacturing, Person, Item, \
    ClaimItem, ClaimCoverageType


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = '__all__'

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


class CustomListModelChoiceIterator(models.ModelChoiceIterator):

    def choice(self, obj):
        return [self.field.prepare_value(obj),
                self.field.label_from_instance(obj),
                obj
                ]


class CustomDictModelChoiceIterator(models.ModelChoiceIterator):

    def choice(self, obj):
        return {'value': self.field.prepare_value(obj),
                'label': self.field.label_from_instance(obj),
                'obj': obj}


class CustomModelMultipleChoiceField(forms.ModelMultipleChoiceField):

    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        return CustomListModelChoiceIterator(self)

    def _get_choices_dict(self):
        if hasattr(self, '_choices'):
            return self._choices
        return CustomDictModelChoiceIterator(self)

    choices = property(_get_choices,
                       fields.ChoiceField._set_choices)
    choices_dict = property(_get_choices_dict,
                            fields.ChoiceField._set_choices)


class ClaimForm(forms.ModelForm):
    items = CustomModelMultipleChoiceField(
        required=False,
        queryset=Item.objects.all(),
        widget=forms.CheckboxSelectMultiple)
    coverage_types = CustomModelMultipleChoiceField(
        queryset=CoverageType.objects.all(),
        widget=forms.CheckboxSelectMultiple)

    def __init__(self, client, *args, **kwargs):
        super(ClaimForm, self).__init__(*args, **kwargs)
        self.client = client
        fields_order = ['patient', 'insurance', 'coverage_types', 'items']
        if (len(fields_order) != len(self.fields)):
            raise forms.ValidationError("Please contact the administrator"
                                        ", ClaimForm is missing fields.")
        self.fields = OrderedDict(
            (name, self.fields[name]) for name in fields_order)
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
        insurance.queryset = client.insurance_set.all()
        insurance.label_from_instance = (
            lambda obj:
                "%s - Spouse - %s" % (obj.provider,
                                      obj.spouse.full_name()) if obj.spouse
                else "%s - Client - %s" % (obj.provider,
                                           obj.client.full_name())
        )
        insurance.widget.attrs['class'] = 'insurance_trigger'

        coverage_types = self.fields['coverage_types']
        coverage_types.queryset = CoverageType.objects.filter(
            insurance__in=insurance.queryset).order_by('insurance')

        items = self.fields['items']
        items.queryset = Item.objects.filter(
            coverage_type__in=coverage_types.queryset.values_list(
                'coverage_type', flat=True).distinct()).order_by(
                    'coverage_type', 'gender', 'product_code')

    def clean(self):
        cleaned_data = super(ClaimForm, self).clean()
        self.instance.client = self.client
        items = cleaned_data.get("items")
        coverage_types = cleaned_data.get("coverage_types")
        if not coverage_types:
            coverage_types = []

        # valid = True
        self.claim_coverage_types = []
        self.claim_items = []
        for coverage_type in coverage_types:
            estimated_amount_claimed_total = 0
            estimated_expected_back_total = 0
            actual_amount_claimed = float(
                self.data['claimed_%s' % coverage_type.id])
            actual_expected_back = float(
                self.data['expected_%s' % coverage_type.id])
            if items:
                for item in items.filter(
                        coverage_type=coverage_type.coverage_type):
                    quantity = int(
                        self.data['pairs_%s' % item.id])
                    amount = item.unit_price
                    amount_total = amount * quantity
                    # coverage_remaining = coverage_type.coverage_remaining()
                    # if quantity > coverage_type.quantity:
                    #     valid = False
                    #     self.add_error(
                    #         "items",
                    #         forms.ValidationError(
                    #             "Product Code: "
                    #             + self.data['product_code_%s' % item.id]
                    #             + " Quantity is more than "
                    #             + coverage_type.get_coverage_type_display()
                    #             + " Pair Remaining."))
                    # elif amount_total > coverage_remaining:
                    #     valid = False
                    #     self.add_error(
                    #         "items",
                    #         forms.ValidationError(
                    #             "Product Code: "
                    #             + self.data['product_code_%s' % item.id]
                    #             + " Claim Amount * Quantity is more than "
                    #             + coverage_type.get_coverage_type_display()
                    #             + " Coverage Remaining"))
                    # else:
                    # coverage_type.quantity -= quantity
                    # if coverage_type.quantity < 0:
                    #     coverage_type.quantity = 0

                    # coverage_type.total_claimed += actual_amount_claimed

                    coverage_percent = coverage_type.coverage_percent
                    estimated_amount_claimed_total += amount_total
                    estimated_expected_back_total += (
                        amount_total * (coverage_percent / 100))
                    self.claim_items.append(
                        ClaimItem(item=item, quantity=quantity)
                    )
            self.claim_coverage_types.append(
                ClaimCoverageType(
                    coverage_type=coverage_type,
                    actual_amount_claimed=actual_amount_claimed,
                    estimated_amount_claimed=estimated_amount_claimed_total,
                    actual_expected_back=actual_expected_back,
                    estimated_expected_back=estimated_expected_back_total,
                )
            )

        # if valid:
        # for coverage_type in coverage_types:
        #     coverage_type.save()

    def save(self, commit=True):
        claim = super(ClaimForm, self).save(commit=False)
        if commit:
            claim.save()
            # self.save_m2m()  # doesnt work
            for claim_coverage_type in self.claim_coverage_types:
                cct = claim_coverage_type
                try:
                    exist = ClaimCoverageType.objects.get(
                        claim=claim, coverage_type=cct.coverage_type)
                    exist.actual_amount_claimed = cct.actual_amount_claimed
                    estimated_amount_claimed = cct.estimated_amount_claimed
                    exist.estimated_amount_claimed = estimated_amount_claimed
                    exist.actual_expected_back = cct.actual_expected_back
                    exist.estimated_expected_back = cct.estimated_expected_back
                    exist.save()
                except:
                    cct.claim = claim
                    cct.save()
            for claim_item in self.claim_items:
                try:
                    exist = ClaimItem.objects.get(
                        claim=claim, item=claim_item.item)
                    exist.quantity = claim_item.quantity
                    exist.save()
                except:
                    claim_item.claim = claim
                    claim_item.save()
            # for coverage_type in self.cleaned_data['coverage_types']:
            #     coverage_type.save()
        return claim

    class Meta:
        model = Claim
        exclude = ('client',
                   'estimated_amount_claimed', 'estimated_expected_back')


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
