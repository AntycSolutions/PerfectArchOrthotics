from collections import OrderedDict
from itertools import zip_longest
import itertools

from django import forms
from django.forms import models, BaseInlineFormSet
from django.forms import fields
from django.forms.models import inlineformset_factory

from bootstrap3_datetime.widgets import DateTimePicker

from utils.forms import fields as utils_fields, widgets as utils_widgets

from clients.models import Client, Dependent, Insurance, Coverage, Claim, \
    Invoice, InsuranceLetter, Laboratory, ProofOfManufacturing, Person, Item, \
    ClaimItem, ClaimCoverage, ClaimAttachment


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
