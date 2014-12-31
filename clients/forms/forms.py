from collections import OrderedDict
from itertools import zip_longest

from django import forms
from django.forms import models, BaseInlineFormSet
from django.forms import fields
from django.forms.models import inlineformset_factory

from bootstrap3_datetime.widgets import DateTimePicker

from clients.models import Client, Dependent, Insurance, Coverage, Claim, \
    Invoice, InsuranceLetter, Laboratory, ProofOfManufacturing, Person, Item, \
    ClaimItem, ClaimCoverage


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
    # items = CustomModelMultipleChoiceField(
    #     required=False,
    #     queryset=Item.objects.all(),
    #     widget=forms.CheckboxSelectMultiple)
    # coverage_types = CustomModelMultipleChoiceField(
    #     queryset=Coverage.objects.all(),
    #     widget=forms.CheckboxSelectMultiple)

    def __init__(self, client, *args, **kwargs):
        super(ClaimForm, self).__init__(*args, **kwargs)
        self.client = client
    #     fields_order = ['patient', 'insurance', 'coverage_types', 'items']
    #     if (len(fields_order) != len(self.fields)):
    #         raise forms.ValidationError("Please contact the administrator"
    #                                     ", ClaimForm is missing fields.")
    #     self.fields = OrderedDict(
    #         (name, self.fields[name]) for name in fields_order)
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

    #     coverage_types = self.fields['coverage_types']
    #     coverage_types.queryset = Coverage.objects.filter(
    #         insurance__in=insurance.queryset).order_by('insurance')

    #     items = self.fields['items']
    #     items.queryset = Item.objects.filter(
    #         coverage_type__in=coverage_types.queryset.values_list(
    #             'coverage_type', flat=True).distinct()).order_by(
    #                 'coverage_type', 'gender', 'product_code')

    # def clean(self):
    #     cleaned_data = super(ClaimForm, self).clean()
    #     self.instance.client = self.client
    #     items = cleaned_data.get("items")
    #     coverage_types = cleaned_data.get("coverage_types")
    #     if not coverage_types:
    #         coverage_types = []

    #     # valid = True
    #     self.claim_coverage_types = []
    #     self.claim_items = []
    #     for coverage_type in coverage_types:
    #         amount_claimed_total = 0
    #         expected_back_total = 0
    #         if items:
    #             for item in items.filter(
    #                     coverage_type=coverage_type.coverage_type):
    #                 quantity = int(
    #                     self.data['pairs_%s' % item.id])
    #                 amount = item.unit_price
    #                 amount_total = amount * quantity
    #                 # coverage_remaining = coverage_type.coverage_remaining()
    #                 # if quantity > coverage_type.quantity:
    #                 #     valid = False
    #                 #     self.add_error(
    #                 #         "items",
    #                 #         forms.ValidationError(
    #                 #             "Product Code: "
    #                 #             + self.data['product_code_%s' % item.id]
    #                 #             + " Quantity is more than "
    #                 #             + coverage_type.get_coverage_type_display()
    #                 #             + " Pair Remaining."))
    #                 # elif amount_total > coverage_remaining:
    #                 #     valid = False
    #                 #     self.add_error(
    #                 #         "items",
    #                 #         forms.ValidationError(
    #                 #             "Product Code: "
    #                 #             + self.data['product_code_%s' % item.id]
    #                 #             + " Claim Amount * Quantity is more than "
    #                 #             + coverage_type.get_coverage_type_display()
    #                 #             + " Coverage Remaining"))
    #                 # else:
    #                 # coverage_type.quantity -= quantity
    #                 # if coverage_type.quantity < 0:
    #                 #     coverage_type.quantity = 0

    #                 # coverage_type.total_claimed += actual_amount_claimed

    #                 coverage_percent = coverage_type.coverage_percent
    #                 amount_claimed_total += amount_total
    #                 expected_back_total += (
    #                     amount_total * (coverage_percent / 100))
    #                 self.claim_items.append(
    #                     ClaimItem(item=item, quantity=quantity)
    #                 )
    #         self.claim_coverage_types.append(
    #             ClaimCoverage(
    #                 coverage_type=coverage_type,
    #                 amount_claimed=amount_claimed_total,
    #                 expected_back=expected_back_total,
    #             )
    #         )

    #     # if valid:
    #     # for coverage_type in coverage_types:
    #     #     coverage_type.save()

    # def save(self, commit=True):
    #     claim = super(ClaimForm, self).save(commit=False)
    #     if commit:
    #         claim.save()
    #         # self.save_m2m()  # doesnt work
    #         for claim_coverage_type in self.claim_coverage_types:
    #             try:
    #                 exist = ClaimCoverage.objects.get(
    #                     claim=claim,
    #                     coverage_type=claim_coverage_type.coverage_type)
    #                 exist.amount_claimed = claim_coverage_type.amount_claimed
    #                 exist.expected_back = claim_coverage_type.expected_back
    #                 exist.save()
    #             except:
    #                 claim_coverage_type.claim = claim
    #                 claim_coverage_type.save()
    #         for claim_item in self.claim_items:
    #             try:
    #                 exist = ClaimItem.objects.get(
    #                     claim=claim, item=claim_item.item)
    #                 exist.quantity = claim_item.quantity
    #                 exist.save()
    #             except:
    #                 claim_item.claim = claim
    #                 claim_item.save()
    #         # for coverage_type in self.cleaned_data['coverage_types']:
    #         #     coverage_type.save()
    #     return claim

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


class ProofOfManufacturingForm(forms.ModelForm):

    class Meta:
        model = ProofOfManufacturing
        exclude = ('claim',)

LaboratoryInsuranceLetterFormSet = inlineformset_factory(
    InsuranceLetter,
    Laboratory,
    exclude=('insurance_letter',)
)


# Needs to be updated for files/media
class BaseNestedFormSet(BaseInlineFormSet):

    def add_fields(self, form, index):
        super(BaseNestedFormSet, self).add_fields(form, index)

        form.nested = self.nested_formset_class(
            instance=form.instance,
            data=form.data if self.is_bound else None,
            prefix='%s-%s' % (form.prefix,
                              self.nested_formset_class.get_default_prefix())
        )

    def is_valid(self):
        result = super(BaseNestedFormSet, self).is_valid()

        if self.is_bound:
            for form in self.forms:
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


class BaseNestedModelForm(forms.ModelForm):

    def has_changed(self):
        return (super(BaseNestedModelForm, self).has_changed()
                or self.nested.has_changed())

# class CoverageFormSet(BaseNestedFormSet):

#     def __init__(self, *args, **kwargs):
#         super(CoverageFormSet, self).__init__(*args, **kwargs)


# Needs to be updated to deal with nestednested
def nestedformset_factory(parent_model, child_model, grandchild_model,
                          **kwargs):
    nested_kwargs = {}
    for key in kwargs:
        if ("nested_" in key):
            nested_kwargs[key.replace("nested_", '')] = kwargs[key]
    for key in nested_kwargs:
        kwargs.pop("nested_" + key)
    if 'formset' in kwargs:
        formset = kwargs.pop('formset')
    else:
        formset = BaseNestedFormSet
    if 'form' in kwargs:
        form = kwargs.pop('form')
    else:
        form = BaseNestedModelForm
    parent_child = inlineformset_factory(
        parent_model, child_model, form=form, formset=formset, **kwargs)
    parent_child.nested_formset_class = inlineformset_factory(
        child_model, grandchild_model, **nested_kwargs)

    return parent_child  # Is class, not instance
